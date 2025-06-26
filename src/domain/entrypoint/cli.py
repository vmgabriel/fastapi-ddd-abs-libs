from . import model


class EntrypointCLI(model.EntrypointModel):
    name: str
    
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name