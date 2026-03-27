from database import Database
from models import User, Task
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.db = Database()
        self.current_user = None
    
    def login(self, username, password):
        """Inicia sesión de usuario"""
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        user_data = self.db.fetch_one(query, (username, password))
        
        if user_data:
            self.current_user = User(**user_data)
            print(f"✅ Bienvenido, {self.current_user.username}!")
            return True
        else:
            print("❌ Usuario o contraseña incorrectos")
            return False
    
    def register(self, username, email, password):
        """Registra un nuevo usuario"""
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        if self.db.execute_query(query, (username, email, password)):
            print("✅ Usuario registrado exitosamente")
            return True
        return False
    
    def create_task(self, title, description, priority='medium', due_date=None):
        """Crea una nueva tarea para el usuario actual"""
        if not self.current_user:
            print("❌ Debes iniciar sesión primero")
            return False
        
        query = """
            INSERT INTO tasks (user_id, title, description, priority, due_date) 
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (self.current_user.id, title, description, priority, due_date)
        
        if self.db.execute_query(query, params):
            print("✅ Tarea creada exitosamente")
            return True
        return False
    
    def get_tasks(self, status=None):
        """Obtiene las tareas del usuario actual"""
        if not self.current_user:
            print("❌ Debes iniciar sesión primero")
            return []
        
        query = "SELECT * FROM tasks WHERE user_id = %s"
        params = [self.current_user.id]
        
        if status:
            query += " AND status = %s"
            params.append(status)
        
        query += " ORDER BY priority DESC, due_date ASC"
        
        tasks_data = self.db.fetch_all(query, tuple(params))
        return [Task(**task) for task in tasks_data]
    
    def update_task_status(self, task_id, new_status):
        """Actualiza el estado de una tarea"""
        if not self.current_user:
            print("❌ Debes iniciar sesión primero")
            return False
        
        query = """
            UPDATE tasks 
            SET status = %s 
            WHERE id = %s AND user_id = %s
        """
        if self.db.execute_query(query, (new_status, task_id, self.current_user.id)):
            print("✅ Estado de tarea actualizado")
            return True
        return False
    
    def delete_task(self, task_id):
        """Elimina una tarea"""
        if not self.current_user:
            print("❌ Debes iniciar sesión primero")
            return False
        
        query = "DELETE FROM tasks WHERE id = %s AND user_id = %s"
        if self.db.execute_query(query, (task_id, self.current_user.id)):
            print("✅ Tarea eliminada")
            return True
        return False
    
    def get_statistics(self):
        """Obtiene estadísticas de tareas del usuario"""
        if not self.current_user:
            return None
        
        stats = {}
        
        # Total de tareas
        query = "SELECT COUNT(*) as total FROM tasks WHERE user_id = %s"
        result = self.db.fetch_one(query, (self.current_user.id,))
        stats['total'] = result['total'] if result else 0
        
        # Tareas por estado
        for status in ['pending', 'in_progress', 'completed']:
            query = "SELECT COUNT(*) as count FROM tasks WHERE user_id = %s AND status = %s"
            result = self.db.fetch_one(query, (self.current_user.id, status))
            stats[status] = result['count'] if result else 0
        
        # Tareas por prioridad
        for priority in ['low', 'medium', 'high']:
            query = "SELECT COUNT(*) as count FROM tasks WHERE user_id = %s AND priority = %s"
            result = self.db.fetch_one(query, (self.current_user.id, priority))
            stats[priority] = result['count'] if result else 0
        
        return stats
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        self.db.disconnect()