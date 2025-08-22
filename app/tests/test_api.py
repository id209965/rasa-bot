import pytest
from httpx import AsyncClient
from app.api.main import app
from app.database.connection import init_database


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def setup_database():
    await init_database()


class TestAPI:
    """Test API endpoints"""
    
    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint"""
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint"""
        response = await client.get("/")
        assert response.status_code == 200
        assert "Test Bot API is running" in response.json()["message"]
    
    async def test_geocode_without_key(self, client: AsyncClient):
        """Test geocode endpoint without API key"""
        response = await client.get("/api/maps/geocode?address=Moscow")
        assert response.status_code == 500
        assert "API key not configured" in response.json()["detail"]
    
    async def test_upload_data_without_admin(self, client: AsyncClient):
        """Test admin upload without admin rights"""
        files = {"file": ("test.xlsx", b"fake excel content", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        data = {"admin_phone": "+1234567890"}
        
        response = await client.post("/api/admin/upload-data", files=files, data=data)
        assert response.status_code == 403
        assert "прав" in response.json()["detail"]
