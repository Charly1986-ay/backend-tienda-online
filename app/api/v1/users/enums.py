from enum import Enum


class UserStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class Role(str, Enum):
    CLIENT = 'client'                                # Cliente
    ECOMMERCE_ASSISTANT = 'ecommerce_assistant'     # Asistente operativo y administrativo
    MANAGER = 'manager'                              # Gerente
    IT_SUPPORT_ESPECIALIST = 'it_support_specialist' # Soporte técnico IT