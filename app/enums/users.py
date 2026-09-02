from enum import Enum


class UserStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class Role(str, Enum):
    CLIENT = 'client'                                # Cliente
    ECOMMERCE_ASSISTANT = 'E-commerce Assistant'     # Asistente operativo y administrativo
    MANAGER = 'manager'                              # Gerente
    IT_SUPPORT_ESPECIALIST = 'IT Support Specialist' # Soporte técnico IT