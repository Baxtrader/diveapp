from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from app.core.database import Base

class DiveLog(Base):
    __tablename__ = "dive_logs"

    id = Column(Integer, primary_key=True, index=True)
    dive_number = Column(Integer, nullable=False)  # Sequential dive number for user
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=True)
    
    # Basic dive info
    dive_date = Column(DateTime, nullable=False)
    dive_time_start = Column(DateTime, nullable=True)
    dive_time_end = Column(DateTime, nullable=True)
    dive_duration = Column(Integer, nullable=True)  # in minutes
    
    # Location
    location = Geography(geometry_type='POINT', srid=4326, nullable=True)
    dive_site_name = Column(String, nullable=False)
    country = Column(String, nullable=True)
    region = Column(String, nullable=True)
    
    # Technical data
    max_depth = Column(Float, nullable=False)  # in meters
    avg_depth = Column(Float, nullable=True)  # in meters
    water_temperature = Column(Float, nullable=True)  # in Celsius
    air_temperature = Column(Float, nullable=True)  # in Celsius
    visibility = Column(Float, nullable=True)  # in meters
    
    # Equipment and gas
    suit_type = Column(String, nullable=True)  # wetsuit, drysuit, etc.
    suit_thickness = Column(String, nullable=True)  # 3mm, 5mm, etc.
    weight_used = Column(Float, nullable=True)  # in kg
    tank_volume = Column(Float, nullable=True)  # in liters
    gas_mix = Column(String, default="Air")  # Air, Nitrox 32%, etc.
    start_pressure = Column(Integer, nullable=True)  # in bar
    end_pressure = Column(Integer, nullable=True)  # in bar
    
    # Conditions
    current = Column(String, nullable=True)  # None, Light, Medium, Strong
    surge = Column(String, nullable=True)  # None, Light, Medium, Strong
    weather = Column(String, nullable=True)  # Sunny, Cloudy, Rainy, etc.
    sea_state = Column(String, nullable=True)  # Calm, Light, Moderate, Rough
    
    # Safety and companions
    buddy_name = Column(String, nullable=True)
    dive_guide = Column(String, nullable=True)
    safety_stop = Column(Boolean, default=False)
    safety_stop_time = Column(Integer, nullable=True)  # in minutes
    
    # Notes and observations
    marine_life = Column(Text, nullable=True)  # JSON array of species seen
    notes = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 stars
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="dive_logs")
    operator = relationship("Operator", back_populates="dive_logs")
    
    def __repr__(self):
        return f"<DiveLog(id={self.id}, site='{self.dive_site_name}', depth={self.max_depth}m)>"