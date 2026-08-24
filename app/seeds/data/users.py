from app.models.users import Role

USERS = [
    {
        'email': 'carlos@example.com',
        'full_name': 'Carlos',       
        'role': Role.CLIENT.value,
        'password': 'carlos123!'
    },
    {
        'email': 'maria@example.com',
        'full_name': 'María',         
        'role': Role.CLIENT.value,
        'password': 'maria123!'
    },
    {
        'email': 'pedro@example.com',
        'full_name': 'Pedro',         
        'role': Role.CLIENT.value,
        'password': 'pedro123!'
    },
    {
        'email': 'marcelo@example.com',
        'full_name': 'Marcelo',       
        'role': Role.CLIENT.value,
        'password': 'marcelo123!'
    },
    {
        'email': 'ricardo@example.com',
        'full_name': 'Ricardo Cuéllar',        
        'role': Role.ECOMMERCE_ASSISTANT.value,
        'password': 'pruebas123!'
    },
    {
        'email': 'fernando@example.com',
        'full_name': 'Fernando Herrera',        
        'role': Role.ECOMMERCE_ASSISTANT.value,
        'password': 'pruebas123!'
    },
    {
        'email': 'juanperez@example.com',
        'full_name': 'Juan Pérez',        
        'role': Role.MANAGER.value,
        'password': 'pruebas123!'
    },
]