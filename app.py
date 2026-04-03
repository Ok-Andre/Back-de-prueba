from flask import Flask, request, jsonify
from flask_cors import CORS
from operaciones import operaciones

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app)

# Instanciar el gestor de contactos
manager = operaciones()

# Conectar a la base de datos al iniciar
manager.conectar()

# ============== RUTAS DE LA API ==============

@app.route('/')
def home():
    """Ruta principal (información de la API)"""
    return jsonify({
        'nombre': 'API de Contactos',
        'version': '1.0',
        'endpoints': [
            {'GET': '/api/contactos', 'descripcion': 'Listar todos los contactos'},
            {'GET': '/api/contactos/buscar?q=texto', 'descripcion': 'Buscar contactos'},
            {'GET': '/api/contactos/<id>', 'descripcion': 'Obtener un contacto'},
            {'POST': '/api/contactos', 'descripcion': 'Crear nuevo contacto'},
            {'PUT': '/api/contactos/<id>', 'descripcion': 'Actualizar contacto'},
            {'DELETE': '/api/contactos/<id>', 'descripcion': 'Eliminar contacto'}
        ]
    })

@app.route('/api/contactos', methods=['GET'])
def listar_contactos():
    """Lista todos los contactos"""
    try:
        contactos = manager.lista_contactos()
        # Convertir cada objeto contacto a diccionario usando to_dict()
        contactos_dict = [c.to_dict() for c in contactos]
        
        return jsonify({
            'success': True,
            'data': contactos_dict,
            'total': len(contactos_dict)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/contactos/buscar', methods=['GET'])
def buscar_contactos():
    """Busca contactos por término"""
    termino = request.args.get('q', '')
    if not termino:
        return jsonify({
            'success': False,
            'error': 'Se requiere término de búsqueda'
        }), 400
    
    try:
        contactos = manager.buscar_contacto(termino)
        contactos_dict = [c.to_dict() for c in contactos]
        return jsonify({
            'success': True,
            'data': contactos_dict,
            'total': len(contactos_dict)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/contactos/<int:id_contacto>', methods=['GET'])
def obtener_contacto(id_contacto):
    """Obtiene un contacto específico"""
    try:
        contacto = manager.buscar_por_id(id_contacto)
        if contacto:
            return jsonify({
                'success': True,
                'data': contacto.to_dict()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Contacto no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/contactos', methods=['POST'])
def crear_contacto():
    """Crea un nuevo contacto"""
    data = request.get_json()
    
    nombre = data.get('nombre', '').strip()
    telefono = data.get('telefono', '').strip()
    email = data.get('email', '').strip()
    
    if not nombre:
        return jsonify({
            'success': False,
            'error': 'El nombre es obligatorio'
        }), 400
    
    try:
        if manager.agregar_contacto(nombre, telefono, email):
            return jsonify({
                'success': True,
                'message': 'Contacto creado exitosamente'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Error al crear contacto'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/contactos/<int:id_contacto>', methods=['PUT'])
def actualizar_contacto(id_contacto):
    """Actualiza un contacto existente"""
    data = request.get_json()
    
    nombre = data.get('nombre', '').strip()
    telefono = data.get('telefono', '').strip()
    email = data.get('email', '').strip()
    
    if not nombre:
        return jsonify({
            'success': False,
            'error': 'El nombre es obligatorio'
        }), 400
    
    try:
        if manager.editar_contacto(id_contacto, nombre, telefono, email):
            return jsonify({
                'success': True,
                'message': 'Contacto actualizado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error al actualizar contacto'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/contactos/<int:id_contacto>', methods=['DELETE'])
def eliminar_contacto(id_contacto):
    """Elimina un contacto"""
    try:
        if manager.eliminar_contacto(id_contacto):
            return jsonify({
                'success': True,
                'message': 'Contacto eliminado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error al eliminar contacto'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============== INICIAR EL SERVIDOR ==============

if __name__ == '__main__':
    print("🚀 Servidor iniciando en http://localhost:5000")
    app.run(debug=True, port=5000)