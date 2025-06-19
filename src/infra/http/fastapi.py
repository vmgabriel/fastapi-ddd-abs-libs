import itertools
from typing import Any, Callable, Dict, Optional, TypeVar, cast

import fastapi

from src.domain.entrypoint import http as domain_http
from src.domain.entrypoint import model as model_http
from src.domain.services import command
from src.infra.jwt import model as jwt_model

from . import model

T = TypeVar("T", bound=command.Command)
oauth2_scheme = fastapi.security.APIKeyHeader(name="Authorization")


class FastApiAdapter(model.HttpModel):
    app: fastapi.FastAPI
    responses_type: Dict[model_http.ResponseType, str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app = fastapi.FastAPI(
            debug=self.configuration.has_debug,
            title=self.configuration.title,
            summary=self.configuration.summary,
            contact=self.configuration.contact_info,
            docs_url=self.configuration.docs_url,
            root_path=self.configuration.prefix_api_url,
        )

        self.responses_type = {
            model_http.ResponseType.JSON: "application/json",
            model_http.ResponseType.WS: "application/ws",
        }

    def _get_decorator(self, route: domain_http.EntrypointHttp) -> Callable:
        status_callable: Dict[model_http.HttpStatusType, Callable] = {
            model_http.HttpStatusType.GET: self.app.get,
            model_http.HttpStatusType.POST: self.app.post,
            model_http.HttpStatusType.PUT: self.app.put,
            model_http.HttpStatusType.PATCH: self.app.patch,
            model_http.HttpStatusType.DELETE: self.app.delete,
        }
        return status_callable[route.method]

    def _generate_documentation(self, route: domain_http.EntrypointHttp):
        response_documentation = {}
        router_documentation = route.documentation
        for status_code, responses_group in itertools.groupby(
            router_documentation.responses, key=lambda x: x.status_code
        ):
            resp: Any = ...
            examples_responses = {}
            for x in responses_group:
                examples_responses[x.example_name] = {"value": x.content}
                resp = x
            response_documentation[resp.status_code] = {
                "description": resp.description,
                "content": {
                    self.responses_type[resp.type]: {"examples": examples_responses}
                },
            }

    def _inject_route(self, route: domain_http.EntrypointHttp) -> None:
        built_entrypoint_decorator = self._get_decorator(route)(
            path=route.route,
            name=route.name,
            status_code=route.status_code,
            tags=route.documentation.tags,
            summary=route.documentation.summary,
            responses=self._generate_documentation(route),
            description=route.documentation.description,
        )

        if route.method == model_http.HttpStatusType.GET:

            @built_entrypoint_decorator
            async def callable_context_get(
                token: Optional[str] = (
                    fastapi.Depends(oauth2_scheme)
                    if route.security.require_security
                    else None
                ),
            ) -> command.CommandResponse:
                if route.security.require_security:
                    status_authentication = self.check_authentication(
                        token=cast(str, token), route=route
                    )
                    if status_authentication.status is not model_http.StatusType.OK:
                        self._status_error_response(status_authentication)
                cmd = cast(command.Command, route.cmd)
                return await cmd.execute()

            return

        @built_entrypoint_decorator
        async def callable_context_post(
            payload: T,
            token: Optional[str] = (
                fastapi.Depends(oauth2_scheme)
                if route.security.require_security
                else None
            ),
        ) -> command.CommandResponse:
            if route.security.require_security:
                status_authentication = self.check_authentication(
                    token=cast(str, token), route=route
                )
                if status_authentication.status is not model_http.StatusType.OK:
                    self._status_error_response(status_authentication)

            cmd = cast(command.Command, route.cmd)
            cmd.inject_request(payload)
            return await cmd.execute()

    def _inject_routes(self) -> None:
        for route in self.routes:
            self._inject_route(route)

    def _status_error_response(
        self, status_response: jwt_model.StatusCheckJWT
    ) -> fastapi.responses.JSONResponse:
        status = {
            model_http.StatusType.OK: 200,
            model_http.StatusType.NOT_AUTHORIZED: 401,
            model_http.StatusType.EXPIRED: 401,
            model_http.StatusType.NOT_COMPLETE: 422,
            model_http.StatusType.NOT_PERMISSIONS: 403,
        }

        if status[status_response.type] != 200:
            raise fastapi.HTTPException(
                status_code=status[status_response.type],
                detail=status.get(status_response.type),
            )

        return fastapi.responses.JSONResponse(
            content={"payload": {}, "errors": [{"message": status_response.message}]},
            status_code=status[status_response.type],
        )

    def check_authentication(
        self,
        token: str,
        route: domain_http.EntrypointHttp,
    ) -> jwt_model.StatusCheckJWT:
        if not token.startswith(self.configuration.auth_type + " "):
            return jwt_model.StatusCheckJWT(
                message="Not authenticated",
                status=False,
                type=model_http.StatusType.NOT_AUTHORIZED,
            )
        response = self.jwt.check_and_decode(
            token=token.split(" ")[1], allowed_aud=route.security.audiences
        )
        if not response.status:
            return jwt_model.StatusCheckJWT(
                message=response.message,
                status=False,
                type=response.type,
            )
        return jwt_model.StatusCheckJWT(
            message="ok",
            status=True,
            type=model_http.StatusType.OK,
            data=response.data,
        )

    def execute(self) -> model.AppHttp:
        self._inject_routes()
        return model.AppHttp(instance=self.app)
