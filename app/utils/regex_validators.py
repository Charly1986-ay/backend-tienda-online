import re


def validate_password_strength(value: str) -> str:
    if not re.search(r'[A-Z]', value):
        raise ValueError('La contraseña debe contener al menos una letra mayúscula.')
    
    if not re.search(r'[!@#$%^&*(),.?\':{}|<>]', value):
        raise ValueError('La contraseña debe contener al menos un carácter especial.')
        
    return value


def clean_string_spaces(value):
    """Limpia los espacios en blanco al inicio y al final si es un string."""
    if isinstance(value, str):
        return value.strip()
    return value