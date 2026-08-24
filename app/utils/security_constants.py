FORBIDDEN_WORDS = [
    # SQL Injection / Comandos
    'select', 'union', 'drop', 'truncate', 'insert', 'update', 
    'delete', 'exec',
    # XSS / Scripts
    '<script', '</script', 'javascript:', 'vbscript:','data:text/html',
    'onerror=', 'onload=', 'onclick=', 'onmouseover=', 'onfocus=',
    'onmouseenter=', 'eval(', 'settimeout(', 'setinterval(',
    # Secretos / Tokens
    'access_token', 'refresh_token', 'password', 'api_key', 'secret'
]

def validate_no_forbidden_words(value: str) -> str:
    """Función reutilizable para validar cualquier texto"""
    val_lower = value.lower()
    for word in FORBIDDEN_WORDS:
        if word in val_lower:
            raise ValueError(f'El texto contiene contenido o patrones no permitidos')
    return value