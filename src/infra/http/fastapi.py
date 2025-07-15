import itertools
from typing import Any, Callable, Dict, Optional, TypeVar, cast

import fastapi

from src.domain.entrypoint import http as domain_http
from src.domain.entrypoint import model as model_http
from src.domain.services import command
from src.infra.jwt import model as jwt_model

from . import model

T = TypeVar("T", bound=command.Command)
V = TypeVar("V", bound=command.CommandRequest)
X = Optional[str]
oauth2_scheme = fastapi.security.APIKeyHeader(name="Authorization")


call_function_str = """
async def endpoint_function_handler({str_parameters}):
    return await endpoint_base({return_str_parameters})
"""


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

    def _generate_documentation(
        self, route: domain_http.EntrypointHttp
    ) -> Dict[int, Any]:
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
        return response_documentation

    def _create_dynamic_endpoint(self, route: domain_http.EntrypointHttp) -> Callable:
        is_get = route.method == model_http.HttpStatusType.GET
        with_token = route.security.require_security

        async def endpoint_base(**kwargs: Any) -> command.CommandResponse:
            if with_token:
                token = fastapi.Depends(oauth2_scheme)
                status_authentication = self.check_authentication(
                    token=cast(str, token), route=route
                )
                if status_authentication.status is not model_http.StatusType.OK:
                    self._status_error_response(status_authentication)

            cmd = cast(command.Command, route.cmd)

            cmd.inject_parameters(
                {
                    parameter: kwargs.get(parameter, "")
                    for parameter in route.path_parameters
                }
            )
            if is_get:
                request_data = command.CommandRequest()
                cmd.inject_request(request_data)
            else:
                cmd.inject_request(kwargs.get("payload", ...))

            return await cmd.execute()

        namespace = locals()
        parameters = {parameter: "str" for parameter in route.path_parameters}
        if with_token:
            parameters.update({"token": "fastapi.Depends(oauth2_scheme)"})
        if is_get:
            parameters.update({"q": "command.CommandRequest | None"})
            namespace["command"] = command
        else:
            parameters.update({"payload": route.cmd.request_type.__name__})

        def create_dynamic_function() -> str:
            str_parameters = ",".join(
                f"{name}: {type_}" for name, type_ in parameters.items()
            )
            return_str_parameters = ",".join(
                f"{name}={name}" for name, _ in parameters.items()
            )
            return call_function_str.format(
                str_parameters=str_parameters,
                return_str_parameters=return_str_parameters,
            )

        namespace[route.cmd.request_type.__name__] = route.cmd.request_type
        exec(create_dynamic_function(), namespace)
        return namespace["endpoint_function_handler"]

    def _inject_route(self, route: domain_http.EntrypointHttp) -> None:
        endpoint = self._create_dynamic_endpoint(route)

        decorator = self._get_decorator(route)(
            path=route.route,
            name=route.name,
            status_code=route.status_code,
            tags=route.documentation.tags,
            summary=route.documentation.summary,
            responses=self._generate_documentation(route),
            description=route.documentation.description,
        )

        decorated_endpoint = decorator(endpoint)

        setattr(self.app, f"endpoint_{route.name}", decorated_endpoint)

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
