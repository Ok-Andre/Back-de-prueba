class contacto:
    def __init__(self, id=None, nombre=None, telefono=None, email=None):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
    
    def to_dict(self):
        return {
            'id': self.id,        # ← DOS PUNTOS : no igual =
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email
        }