import pydantic

from . import model


class EntrypointCLIDocumentation(pydantic.BaseModel):
    description: str
    usage: str


class EntrypointCLI(model.EntrypointModel):
    name: str
    group: str
    
    documentation: EntrypointCLIDocumentation
    
    def __init__(
        self, 
        name: str, 
        group: str, 
        documentation: EntrypointCLIDocumentation, 
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.name = name
        self.group = group
        self.documentation = documentation