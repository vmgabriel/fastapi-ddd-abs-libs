from typing import Any, Dict, Generic, List, Type, TypeVar, cast

from src import settings

T = TypeVar("T")

# All Infra Configuration


class InfraOption(Generic[T]):
    title: str
    priority: int
    type: T

    def __init__(self, title: str, priority: int, type_adapter: T):
        self.title = title
        self.priority = priority
        self.type = type_adapter


class InfraRequest(Generic[T]):
    title: str
    requirements: List[str]
    options: List[InfraOption]
    with_fallback: bool = (
        False  # If you want could you include a fallback method from here
    )

    def __init__(
        self,
        title: str,
        requirements: List[str],
        options: List[InfraOption],
    ):
        self.title = title
        self.requirements = requirements
        self.options = options
        self.with_fallback = False


class InfraBase(Generic[T]):
    request: InfraRequest
    configurations: settings.BaseSettings
    logger_adapter: Any

    _dict_options: Dict[str, T]

    def __init__(
        self,
        request: InfraRequest,
        logger_adapter,
        configurations: settings.BaseSettings,
    ) -> None:
        self.request = request
        self.configurations = configurations
        self.logger_adapter = logger_adapter
        self._dict_options = {
            option.title: cast(T, option.type) for option in request.options
        }

    @property
    def title(self) -> str:
        return self.request.title

    def select(self, option: str) -> Type[T]:
        if option not in self._dict_options:
            raise ValueError(f"Invalid option: {option}")
        self.logger_adapter.info(f"Selected option: {self._dict_options[option]}")
        return cast(Type[T], self._dict_options[option])

    def all(self) -> List[Type[T]]:
        return cast(List[Type[T]], list(self._dict_options.values()))

    def select_and_inject(self, option: str, dependencies: Dict[str, Any]) -> T:
        infra: Type[T] = self.select(option)
        required_dependencies = {
            dependency_name: value
            for dependency_name, value in dependencies.items()
            if dependency_name in self.request.requirements
        }
        return cast(T, infra(**required_dependencies))

    def selected_with_configuration(self, dependencies: Dict[str, Any]) -> T:
        option = getattr(self.configurations, self.title + "_provider")
        if not option:
            raise ValueError(f"Not Configured provider: {self.title + '_provider'}")
        return cast(T, self.select_and_inject(option, dependencies))
