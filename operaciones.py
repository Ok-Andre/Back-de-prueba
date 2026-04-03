from modelos import contacto
from database import database

class operaciones:

    def __init__(self):
        self.db = database()
    
    def conectar(self):
        return self.db.connect()
    
    def cerrar(self):
        return self.db.disconnect()
    
    def lista_contactos(self):
        consulta = "SELECT * FROM contactos ORDER BY nombre"  # ← Espacio después de *
        datos_consulta = self.db.obtener_todo(consulta)
        contactos = [contacto(**data) for data in datos_consulta]
        return contactos
    
    def buscar_contacto(self, termino):
        consulta = "SELECT * FROM contactos WHERE nombre LIKE %s OR telefono LIKE %s ORDER BY nombre"  # ← nombre minúscula
        parametros = (f"%{termino}%", f"%{termino}%")
        contactos_datos = self.db.obtener_todo(consulta, parametros)
        return [contacto(**data) for data in contactos_datos]
    
    def agregar_contacto(self, nombre, telefono, email):
        if not nombre:
            print("OPERACION NO VALIDA: NOMBRE NECESARIO")
            return False
        consulta = "INSERT INTO contactos (nombre, telefono, email) VALUES (%s, %s, %s)"  # ← INSERT correcto
        return self.db.ejecutar_consulta(consulta, (nombre, telefono, email))
    
    def editar_contacto(self, id, nombre, telefono, email):
        consulta = "UPDATE contactos SET nombre = %s, telefono = %s, email = %s WHERE id = %s"  # ← telefono no numero
        return self.db.ejecutar_consulta(consulta, (nombre, telefono, email, id))
    
    def eliminar_contacto(self, id):
        consulta = "DELETE FROM contactos WHERE id = %s"  # ← DELETE FROM sin *
        return self.db.ejecutar_consulta(consulta, (id,))
    
    def buscar_por_id(self, id):
        consulta = "SELECT * FROM contactos WHERE id = %s"  # ← Espacio después de *
        datos = self.db.obtener_uno(consulta, (id,))
        if datos:
            return contacto(**datos)
        return None