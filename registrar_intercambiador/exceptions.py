class edadInvalida(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje