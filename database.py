import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
            print("✅ CONECTADO A LA BASE DE DATOS")
            return True
        except Error as e:
            print(f"❌ SIN CONEXION: {e}")
            return False   
         
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("🔌 CONEXION CERRADA")

    def ejecutar_consulta(self, consulta, params=None):
        try:
            if params:
                self.cursor.execute(consulta, params)   
            else:
                self.cursor.execute(consulta)      
            self.connection.commit()   
            return True 
        except Error as e:
            print(f"❌ ERROR AL EJECUTAR CONSULTA: {e}")
            self.connection.rollback()                  
            return False
            
    def obtener_todo(self, consulta, params=None):     
        try:
            if params:
                self.cursor.execute(consulta, params)
            else: 
                self.cursor.execute(consulta)
            return self.cursor.fetchall()          
        except Error as e:
            print(f"❌ ERROR EN REGISTROS: {e}")
            return []
           
    def obtener_uno(self, consulta, params=None):
        try:          
            if params:
                self.cursor.execute(consulta, params)
            else:
                self.cursor.execute(consulta)    
            return self.cursor.fetchone()
        except Error as e:
            print(f"❌ ERROR EN REGISTRO: {e}")
            return None