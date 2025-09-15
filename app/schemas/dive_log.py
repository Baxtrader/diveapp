from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema para crear dive log
class DiveLogCreate(BaseModel):
    dive_site_name: str
    dive_date: datetime
    max_depth: float  # en metros
    
    # Datos opcionales pero comunes
    dive_duration: Optional[int] = None  # en minutos
    avg_depth: Optional[float] = None
    water_temperature: Optional[float] = None
    air_temperature: Optional[float] = None
    visibility: Optional[float] = None
    
    # Ubicación
    country: Optional[str] = None
    region: Optional[str] = None
    # location_lat: Optional[float] = None  # Por ahora sin GPS
    # location_lng: Optional[float] = None
    
    # Equipo
    suit_type: Optional[str] = None
    suit_thickness: Optional[str] = None
    weight_used: Optional[float] = None
    tank_volume: Optional[float] = None
    gas_mix: Optional[str] = "Air"
    start_pressure: Optional[int] = None
    end_pressure: Optional[int] = None
    
    # Condiciones
    current: Optional[str] = None
    surge: Optional[str] = None
    weather: Optional[str] = None
    sea_state: Optional[str] = None
    
    # Compañeros y seguridad
    buddy_name: Optional[str] = None
    dive_guide: Optional[str] = None
    safety_stop: Optional[bool] = False
    safety_stop_time: Optional[int] = None
    
    # Observaciones
    marine_life: Optional[str] = None
    notes: Optional[str] = None
    rating: Optional[int] = None  # 1-5 estrellas

# Schema para respuesta de dive log
class DiveLogResponse(BaseModel):
    id: int
    dive_number: int
    user_id: int
    dive_site_name: str
    dive_date: datetime
    max_depth: float
    dive_duration: Optional[int] = None
    avg_depth: Optional[float] = None
    water_temperature: Optional[float] = None
    air_temperature: Optional[float] = None
    visibility: Optional[float] = None
    
    country: Optional[str] = None
    region: Optional[str] = None
    
    suit_type: Optional[str] = None
    gas_mix: Optional[str] = None
    buddy_name: Optional[str] = None
    rating: Optional[int] = None
    notes: Optional[str] = None
    marine_life: Optional[str] = None
    
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schema para listar dive logs (versión resumida)
class DiveLogSummary(BaseModel):
    id: int
    dive_number: int
    dive_site_name: str
    dive_date: datetime
    max_depth: float
    dive_duration: Optional[int] = None
    country: Optional[str] = None
    rating: Optional[int] = None
    
    class Config:
        from_attributes = True

# Schema para actualizar dive log
class DiveLogUpdate(BaseModel):
    dive_site_name: Optional[str] = None
    dive_date: Optional[datetime] = None
    max_depth: Optional[float] = None
    dive_duration: Optional[int] = None
    notes: Optional[str] = None
    rating: Optional[int] = None
    marine_life: Optional[str] = None