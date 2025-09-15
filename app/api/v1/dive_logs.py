from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.dive_log import DiveLog
from app.schemas.dive_log import DiveLogCreate, DiveLogResponse, DiveLogSummary, DiveLogUpdate

router = APIRouter()

@router.post("/", response_model=DiveLogResponse)
async def create_dive_log(
    dive_data: DiveLogCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Crear nuevo registro de buceo
    """
    # Calcular el siguiente dive_number para el usuario
    last_dive = db.query(DiveLog).filter(
        DiveLog.user_id == current_user.id
    ).order_by(desc(DiveLog.dive_number)).first()
    
    next_dive_number = 1 if not last_dive else last_dive.dive_number + 1
    
    # Crear nuevo dive log
    new_dive_log = DiveLog(
        user_id=current_user.id,
        dive_number=next_dive_number,
        dive_site_name=dive_data.dive_site_name,
        dive_date=dive_data.dive_date,
        max_depth=dive_data.max_depth,
        dive_duration=dive_data.dive_duration,
        avg_depth=dive_data.avg_depth,
        water_temperature=dive_data.water_temperature,
        air_temperature=dive_data.air_temperature,
        visibility=dive_data.visibility,
        country=dive_data.country,
        region=dive_data.region,
        suit_type=dive_data.suit_type,
        suit_thickness=dive_data.suit_thickness,
        weight_used=dive_data.weight_used,
        tank_volume=dive_data.tank_volume,
        gas_mix=dive_data.gas_mix,
        start_pressure=dive_data.start_pressure,
        end_pressure=dive_data.end_pressure,
        current=dive_data.current,
        surge=dive_data.surge,
        weather=dive_data.weather,
        sea_state=dive_data.sea_state,
        buddy_name=dive_data.buddy_name,
        dive_guide=dive_data.dive_guide,
        safety_stop=dive_data.safety_stop,
        safety_stop_time=dive_data.safety_stop_time,
        marine_life=dive_data.marine_life,
        notes=dive_data.notes,
        rating=dive_data.rating
    )
    
    db.add(new_dive_log)
    db.commit()
    db.refresh(new_dive_log)
    
    # Actualizar total_dives del usuario
    current_user.total_dives = next_dive_number
    if dive_data.max_depth and (not current_user.max_depth_achieved or dive_data.max_depth > current_user.max_depth_achieved):
        current_user.max_depth_achieved = dive_data.max_depth
    
    db.commit()
    
    return DiveLogResponse.from_orm(new_dive_log)

@router.get("/", response_model=List[DiveLogSummary])
async def get_user_dive_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener dive logs del usuario actual
    """
    dive_logs = db.query(DiveLog).filter(
        DiveLog.user_id == current_user.id
    ).order_by(desc(DiveLog.dive_date)).offset(skip).limit(limit).all()
    
    return [DiveLogSummary.from_orm(dive_log) for dive_log in dive_logs]

@router.get("/{dive_id}", response_model=DiveLogResponse)
async def get_dive_log_detail(
    dive_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener detalle de un dive log específico
    """
    dive_log = db.query(DiveLog).filter(
        DiveLog.id == dive_id,
        DiveLog.user_id == current_user.id
    ).first()
    
    if not dive_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dive log not found"
        )
    
    return DiveLogResponse.from_orm(dive_log)

@router.put("/{dive_id}", response_model=DiveLogResponse)
async def update_dive_log(
    dive_id: int,
    dive_update: DiveLogUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar dive log existente
    """
    dive_log = db.query(DiveLog).filter(
        DiveLog.id == dive_id,
        DiveLog.user_id == current_user.id
    ).first()
    
    if not dive_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dive log not found"
        )
    
    # Actualizar campos que no son None
    update_data = dive_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dive_log, field, value)
    
    db.commit()
    db.refresh(dive_log)
    
    return DiveLogResponse.from_orm(dive_log)

@router.delete("/{dive_id}")
async def delete_dive_log(
    dive_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar dive log
    """
    dive_log = db.query(DiveLog).filter(
        DiveLog.id == dive_id,
        DiveLog.user_id == current_user.id
    ).first()
    
    if not dive_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dive log not found"
        )
    
    db.delete(dive_log)
    db.commit()
    
    return {"message": "Dive log deleted successfully"}

@router.get("/stats/summary")
async def get_dive_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Estadísticas de buceo del usuario
    """
    dive_logs = db.query(DiveLog).filter(DiveLog.user_id == current_user.id).all()
    
    if not dive_logs:
        return {
            "total_dives": 0,
            "max_depth": 0,
            "total_time": 0,
            "average_depth": 0,
            "favorite_locations": []
        }
    
    total_dives = len(dive_logs)
    max_depth = max([dive.max_depth for dive in dive_logs])
    total_time = sum([dive.dive_duration for dive in dive_logs if dive.dive_duration])
    avg_depth = sum([dive.avg_depth for dive in dive_logs if dive.avg_depth]) / len([dive for dive in dive_logs if dive.avg_depth])
    
    # Ubicaciones más visitadas
    locations = {}
    for dive in dive_logs:
        country = dive.country or "Unknown"
        locations[country] = locations.get(country, 0) + 1
    
    favorite_locations = sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "total_dives": total_dives,
        "max_depth": max_depth,
        "total_time_minutes": total_time,
        "average_depth": round(avg_depth, 1) if avg_depth else 0,
        "favorite_locations": [{"country": loc[0], "dives": loc[1]} for loc in favorite_locations]
    }