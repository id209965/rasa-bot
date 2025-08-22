import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, User, Region, Interest
from app.database.models.user import GenderEnum


@pytest.fixture
async def async_session():
    """Create async session for testing"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with AsyncSessionLocal() as session:
        yield session
    
    await engine.dispose()


class TestModels:
    """Test database models"""
    
    async def test_create_region(self, async_session: AsyncSession):
        """Test creating region"""
        region = Region(name="Москва")
        async_session.add(region)
        await async_session.commit()
        
        assert region.id is not None
        assert region.name == "Москва"
        assert region.is_active is True
    
    async def test_create_interest(self, async_session: AsyncSession):
        """Test creating interest"""
        interest = Interest(name="Спорт")
        async_session.add(interest)
        await async_session.commit()
        
        assert interest.id is not None
        assert interest.name == "Спорт"
        assert interest.is_active is True
    
    async def test_create_user(self, async_session: AsyncSession):
        """Test creating user"""
        # Create region first
        region = Region(name="Москва")
        async_session.add(region)
        await async_session.flush()  # Get ID without committing
        
        user = User(
            telegram_id=123456789,
            phone_number="+1234567890",
            first_name="Иван",
            last_name="Иванов",
            gender=GenderEnum.MALE,
            age=25,
            region_id=region.id
        )
        async_session.add(user)
        await async_session.commit()
        
        assert user.id is not None
        assert user.telegram_id == 123456789
        assert user.phone_number == "+1234567890"
        assert user.first_name == "Иван"
        assert user.last_name == "Иванов"
        assert user.gender == GenderEnum.MALE
        assert user.age == 25
        assert user.is_admin is False
        assert user.is_active is True
