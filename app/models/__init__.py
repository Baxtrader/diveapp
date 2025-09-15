# Importar todos los modelos para que SQLAlchemy los reconozca
from .user import User
from .dive_log import DiveLog

# Esto asegura que los modelos estén disponibles cuando se importe este módulo
__all__ = ["User", "DiveLog"]