import re


def validate_password_strength(value: str) -> str:
    if not re.search(r'[A-Z]', value):
        raise ValueError('La contraseña debe contener al menos una letra mayúscula.')
    
    if not re.search(r'[!@#$%^&*(),.?\':{}|<>]', value):
        raise ValueError('La contraseña debe contener al menos un carácter especial.')
        
    return value