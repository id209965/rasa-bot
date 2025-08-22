from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import pandas as pd
import io
import os
from datetime import datetime

from app.config import settings
from app.database.connection import get_session
from app.database.models import User, Event, Interest, Region, AdminAction, AdminActionType, UserInterest, EventInterest, EventParticipant

router = APIRouter()


async def verify_admin_phone(phone_number: str) -> bool:
    """Verify if phone number belongs to admin"""
    return phone_number in settings.admin_phone_list


@router.post("/upload-data")
async def upload_data(
    file: UploadFile = File(...),
    admin_phone: str = None,
    session: AsyncSession = Depends(get_session)
):
    """Upload Excel file with regions and interests data"""
    
    if not admin_phone or not await verify_admin_phone(admin_phone):
        raise HTTPException(status_code=403, detail="Нет прав администратора")
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Файл должен быть в формате Excel")
    
    try:
        # Read Excel file
        content = await file.read()
        df = pd.read_excel(io.BytesIO(content))
        
        # Expected columns: 'regions', 'interests'
        if 'regions' not in df.columns and 'interests' not in df.columns:
            raise HTTPException(
                status_code=400, 
                detail="Файл должен содержать колонки 'regions' и/или 'interests'"
            )
        
        regions_added = 0
        interests_added = 0
        
        # Process regions
        if 'regions' in df.columns:
            for region_name in df['regions'].dropna().unique():
                if region_name.strip():
                    # Check if region already exists
                    result = await session.execute(
                        select(Region).where(Region.name == region_name.strip())
                    )
                    if not result.scalar_one_or_none():
                        region = Region(name=region_name.strip())
                        session.add(region)
                        regions_added += 1
        
        # Process interests
        if 'interests' in df.columns:
            for interest_name in df['interests'].dropna().unique():
                if interest_name.strip():
                    # Check if interest already exists
                    result = await session.execute(
                        select(Interest).where(Interest.name == interest_name.strip())
                    )
                    if not result.scalar_one_or_none():
                        interest = Interest(name=interest_name.strip())
                        session.add(interest)
                        interests_added += 1
        
        # Get admin user
        admin_result = await session.execute(
            select(User).where(User.phone_number == admin_phone)
        )
        admin_user = admin_result.scalar_one_or_none()
        
        if admin_user:
            # Log admin action
            action = AdminAction(
                admin_user_id=admin_user.id,
                action_type=AdminActionType.UPLOAD_DATA,
                description=f"Добавлено регионов: {regions_added}, интересов: {interests_added}",
                created_at=datetime.utcnow()
            )
            session.add(action)
        
        await session.commit()
        
        return {
            "message": "Данные успешно загружены",
            "regions_added": regions_added,
            "interests_added": interests_added
        }
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Ошибка обработки файла: {str(e)}")


@router.get("/export-users")
async def export_users(
    admin_phone: str,
    session: AsyncSession = Depends(get_session)
):
    """Export users data to Excel"""
    
    if not admin_phone or not await verify_admin_phone(admin_phone):
        raise HTTPException(status_code=403, detail="Нет прав администратора")
    
    try:
        # Get all users with their data
        result = await session.execute(
            select(User, Region.name.label('region_name'))
            .join(Region, User.region_id == Region.id)
        )
        users_data = result.all()
        
        # Prepare data for export
        export_data = []
        for user, region_name in users_data:
            # Get user interests
            interests_result = await session.execute(
                select(Interest.name)
                .join(UserInterest, Interest.id == UserInterest.interest_id)
                .where(UserInterest.user_id == user.id)
            )
            interests = [interest[0] for interest in interests_result.all()]
            
            export_data.append({
                'Номер телефона': user.phone_number,
                'Имя': user.first_name,
                'Фамилия': user.last_name,
                'Возраст': user.age,
                'Пол': user.gender.value if user.gender else '',
                'Регион': region_name,
                'Интересы': ', '.join(interests),
                'Ссылка на фото': user.photo_url or ''
            })
        
        # Create Excel file
        df = pd.DataFrame(export_data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Пользователи', index=False)
        output.seek(0)
        
        # Log admin action
        admin_result = await session.execute(
            select(User).where(User.phone_number == admin_phone)
        )
        admin_user = admin_result.scalar_one_or_none()
        
        if admin_user:
            action = AdminAction(
                admin_user_id=admin_user.id,
                action_type=AdminActionType.EXPORT_USERS,
                description=f"Экспорт {len(export_data)} пользователей",
                created_at=datetime.utcnow()
            )
            session.add(action)
            await session.commit()
        
        return StreamingResponse(
            io.BytesIO(output.read()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=users_export.xlsx"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка экспорта: {str(e)}")


@router.get("/export-events")
async def export_events(
    admin_phone: str,
    session: AsyncSession = Depends(get_session)
):
    """Export events data to Excel"""
    
    if not admin_phone or not await verify_admin_phone(admin_phone):
        raise HTTPException(status_code=403, detail="Нет прав администратора")
    
    try:
        # Get all events with creator info
        result = await session.execute(
            select(Event, User.first_name, User.last_name, User.phone_number)
            .join(User, Event.creator_id == User.id)
        )
        events_data = result.all()
        
        # Prepare data for export
        export_data = []
        for event, creator_first_name, creator_last_name, creator_phone in events_data:
            # Get event interests
            interests_result = await session.execute(
                select(Interest.name)
                .join(EventInterest, Interest.id == EventInterest.interest_id)
                .where(EventInterest.event_id == event.id)
            )
            interests = [interest[0] for interest in interests_result.all()]
            
            # Get participants
            participants_result = await session.execute(
                select(User.first_name, User.last_name)
                .join(EventParticipant, User.id == EventParticipant.user_id)
                .where(EventParticipant.event_id == event.id)
            )
            participants = [f"{p[0]} {p[1]}" for p in participants_result.all()]
            
            export_data.append({
                'Название': event.title,
                'Дата': event.event_date.strftime('%Y-%m-%d'),
                'Время': event.event_time,
                'Интересы': ', '.join(interests),
                'Адрес': event.address,
                'Описание': event.description or '',
                'Ссылка на изображение': event.image_url or '',
                'Организатор': f"{creator_first_name} {creator_last_name} ({creator_phone})",
                'Участники': '; '.join(participants)
            })
        
        # Create Excel file
        df = pd.DataFrame(export_data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Мероприятия', index=False)
        output.seek(0)
        
        # Log admin action
        admin_result = await session.execute(
            select(User).where(User.phone_number == admin_phone)
        )
        admin_user = admin_result.scalar_one_or_none()
        
        if admin_user:
            action = AdminAction(
                admin_user_id=admin_user.id,
                action_type=AdminActionType.EXPORT_EVENTS,
                description=f"Экспорт {len(export_data)} мероприятий",
                created_at=datetime.utcnow()
            )
            session.add(action)
            await session.commit()
        
        return StreamingResponse(
            io.BytesIO(output.read()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=events_export.xlsx"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка экспорта: {str(e)}")
