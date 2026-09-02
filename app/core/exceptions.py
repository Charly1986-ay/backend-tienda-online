from fastapi import HTTPException, status

class CredentialsException(HTTPException):
    '''Excepción que se produce cuando el usuario no logra autenticarse.'''
    def __init__(self, detail: str = 'No se pudieron validar las credenciales'):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=detail,
            headers={'WWW-Authenticate': 'Bearer'},
    )


class ExpiredTokenException(HTTPException):
    '''Excepción específica para token expirado.'''
    def __init__(self, detail: str = 'Token expirado, inicia sesión nuevamente'):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


class ForbiddenException(HTTPException):
    '''Excepción lanzada cuando un usuario itenta acceder a un recurso que no tiene permiso.'''
    def __init__(self, detail: str = 'No tienes permisos para acceder a este recurso'):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=detail
    )


class UserInactiveException(HTTPException):
    '''Excepción que ocurre cuando un usuario está inactivo.'''
    def __init__(self, detail: str = 'Usuario inactivo'):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=detail
    )
        

class UserExistsException (HTTPException):
    '''Excepción se produce cuando el email existe en la base de datos.'''
    def __init__(self, detail: str = 'Email ya existe en la base de datos'):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, 
            detail=detail
    )


class UserNotFound(HTTPException):
    '''Excepción lanzada cuando un usuario no es encontrado en base de datos.'''
    def __init__(self, detail: str = 'Usuario no encontrado'):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail
    )


class CategoryExistsException (HTTPException):
    '''Excepción se produce cuando la categoría existe en la base de datos.'''
    def __init__(self, detail: str = 'La categoría ya existe'):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, 
            detail=detail
    )


class BrandExistsException (HTTPException):
    '''Excepción se produce cuando la marca existe en la base de datos.'''
    def __init__(self, detail: str = 'La marca ya existe'):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, 
            detail=detail
    )


class ArticleNotFound(HTTPException):
    '''Excepción lanzada cuando un articulo no es encontrado en base de datos.'''
    def __init__(self, detail: str = 'Articulo no encontrado'):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail
    )


class InvoiceNotFound(HTTPException):
    '''Excepción lanzada cuando una factura no es encontrado en base de datos.'''
    def __init__(self, detail: str = 'Factura no encontrado'):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail
    )


class InsufficientInventory(HTTPException):
    '''Excepción lanzada cuando un articulo no tiene suficiente stock en base de datos.'''
    def __init__(self, detail: str = 'Stock insuficiente'):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=detail
    )


class PriceMismatch(HTTPException):
    '''Excepción lanzada cuando el precio enviado no coincide o es más bajo que el de la base de datos.'''
    def __init__(self, detail: str = 'El precio del artículo ha cambiado o no es válido'):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=detail
        )


class CategoryNotFound(HTTPException):
    '''Excepción lanzada cuando una categoría no es encontrada en base de datos.'''
    def __init__(self, detail: str = 'Categoría no es encontrada'):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail
    )


class BrandNotFound(HTTPException):
    '''Excepción lanzada cuando una marca no es encontrada en base de datos.'''
    def __init__(self, detail: str = 'Marca no es encontrada'):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail
    )


class PaymentException(HTTPException):
    """Excepción lanzada cuando el pago no pudo ser realizado."""
    def __init__(self, detail: str = "El pago no pudo ser realizado. Verifique los datos"):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED, 
            detail=detail
    )