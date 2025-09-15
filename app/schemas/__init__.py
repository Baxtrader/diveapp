# Importar todos los schemas
from .user import UserCreate, UserLogin, UserResponse, UserUpdate, Token
from .dive_log import DiveLogCreate, DiveLogResponse, DiveLogSummary, DiveLogUpdate

__all__ = [
    "UserCreate", 
    "UserLogin", 
    "UserResponse", 
    "UserUpdate", 
    "Token",
    "DiveLogCreate", 
    "DiveLogResponse", 
    "DiveLogSummary", 
    "DiveLogUpdate"
]