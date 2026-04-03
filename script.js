// Configuración
const API_URL = 'http://localhost:5000/api/contactos';

// Elementos del DOM
let contactsList = document.getElementById('contactsList');
let searchInput = document.getElementById('searchInput');
let searchBtn = document.getElementById('searchBtn');
let clearSearchBtn = document.getElementById('clearSearchBtn');
let contactForm = document.getElementById('contactForm');
let contactId = document.getElementById('contactId');
let nombre = document.getElementById('nombre');
let telefono = document.getElementById('telefono');
let email = document.getElementById('email');
let formTitle = document.getElementById('formTitle');
let cancelBtn = document.getElementById('cancelBtn');

// Variable para saber si estamos editando
let isEditing = false;

// ============== FUNCIONES PRINCIPALES ==============

// Cargar todos los contactos
async function cargarContactos() {
    try {
        mostrarLoading();
        const response = await fetch(API_URL);
        const result = await response.json();
        
        if (result.success) {
            mostrarContactos(result.data);
        } else {
            mostrarError(result.error);
        }
    } catch (error) {
        mostrarError('Error al conectar con el servidor: ' + error.message);
    }
}

// Buscar contactos
async function buscarContactos(termino) {
    if (!termino.trim()) {
        cargarContactos();
        return;
    }
    
    try {
        mostrarLoading();
        const response = await fetch(`${API_URL}/buscar?q=${encodeURIComponent(termino)}`);
        const result = await response.json();
        
        if (result.success) {
            mostrarContactos(result.data);
            if (result.data.length === 0) {
                mostrarMensaje('No se encontraron contactos con: "' + termino + '"');
            }
        } else {
            mostrarError(result.error);
        }
    } catch (error) {
        mostrarError('Error en la búsqueda: ' + error.message);
    }
}

// Crear nuevo contacto
async function crearContacto(contacto) {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(contacto)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('✅ ' + result.message);
            cargarContactos();
            resetForm();
        } else {
            alert('❌ Error: ' + result.error);
        }
    } catch (error) {
        alert('❌ Error al crear contacto: ' + error.message);
    }
}

// Actualizar contacto
async function actualizarContacto(id, contacto) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(contacto)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('✅ ' + result.message);
            cargarContactos();
            resetForm();
        } else {
            alert('❌ Error: ' + result.error);
        }
    } catch (error) {
        alert('❌ Error al actualizar contacto: ' + error.message);
    }
}

// Eliminar contacto
async function eliminarContacto(id, nombre) {
    const confirmar = confirm(`¿Estás seguro de eliminar a "${nombre}"?`);
    
    if (!confirmar) return;
    
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('✅ ' + result.message);
            cargarContactos();
        } else {
            alert('❌ Error: ' + result.error);
        }
    } catch (error) {
        alert('❌ Error al eliminar contacto: ' + error.message);
    }
}

// Editar contacto (cargar datos en el formulario)
function editarContacto(contacto) {
    contactId.value = contacto.id;
    nombre.value = contacto.nombre;
    telefono.value = contacto.telefono || '';
    email.value = contacto.email || '';
    formTitle.textContent = 'Editar Contacto';
    isEditing = true;
    
    // Scroll al formulario
    document.getElementById('formCard').scrollIntoView({ behavior: 'smooth' });
}

// ============== FUNCIONES DE UI ==============

// Mostrar contactos en el DOM
function mostrarContactos(contactos) {
    if (!contactsList) return;
    
    if (contactos.length === 0) {
        contactsList.innerHTML = '<div class="empty">📭 No hay contactos para mostrar</div>';
        return;
    }
    
    contactsList.innerHTML = contactos.map(contacto => `
        <div class="contact-card">
            <h3>👤 ${escapeHTML(contacto.nombre)}</h3>
            ${contacto.telefono ? `<p class="phone">📞 ${escapeHTML(contacto.telefono)}</p>` : ''}
            ${contacto.email ? `<p class="email">✉️ ${escapeHTML(contacto.email)}</p>` : ''}
            <div class="card-buttons">
                <button class="btn btn-warning" onclick="editarContacto(${JSON.stringify(contacto).replace(/"/g, '&quot;')})">
                    ✏️ Editar
                </button>
                <button class="btn btn-danger" onclick="eliminarContacto(${contacto.id}, '${escapeHTML(contacto.nombre)}')">
                    🗑️ Eliminar
                </button>
            </div>
        </div>
    `).join('');
}

// Mostrar loading
function mostrarLoading() {
    if (contactsList) {
        contactsList.innerHTML = '<div class="loading">⏳ Cargando contactos...</div>';
    }
}

// Mostrar error
function mostrarError(mensaje) {
    if (contactsList) {
        contactsList.innerHTML = `<div class="empty">❌ Error: ${mensaje}</div>`;
    }
}

// Mostrar mensaje temporal
function mostrarMensaje(mensaje) {
    const mensajeDiv = document.createElement('div');
    mensajeDiv.className = 'empty';
    mensajeDiv.textContent = mensaje;
    
    if (contactsList) {
        contactsList.innerHTML = '';
        contactsList.appendChild(mensajeDiv);
        
        setTimeout(() => {
            cargarContactos();
        }, 2000);
    }
}

// Resetear formulario
function resetForm() {
    contactId.value = '';
    nombre.value = '';
    telefono.value = '';
    email.value = '';
    formTitle.textContent = '➕ Nuevo Contacto';
    isEditing = false;
}

// Escapar HTML para prevenir XSS
function escapeHTML(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// ============== EVENT LISTENERS ==============

// Manejar envío del formulario
contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const contacto = {
        nombre: nombre.value.trim(),
        telefono: telefono.value.trim(),
        email: email.value.trim()
    };
    
    if (!contacto.nombre) {
        alert('❌ El nombre es obligatorio');
        return;
    }
    
    if (isEditing && contactId.value) {
        actualizarContacto(contactId.value, contacto);
    } else {
        crearContacto(contacto);
    }
});

// Cancelar edición
cancelBtn.addEventListener('click', () => {
    resetForm();
});

// Búsqueda
searchBtn.addEventListener('click', () => {
    buscarContactos(searchInput.value);
});

// Limpiar búsqueda
clearSearchBtn.addEventListener('click', () => {
    searchInput.value = '';
    cargarContactos();
});

// Búsqueda al presionar Enter
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        buscarContactos(searchInput.value);
    }
});

// ============== INICIALIZACIÓN ==============

// Cargar contactos al iniciar
cargarContactos();