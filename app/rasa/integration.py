import httpx
import json
from typing import Optional, Dict, Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class RasaIntegration:
    """Integration with Rasa server for natural language processing"""
    
    def __init__(self, server_url: str = None):
        self.server_url = server_url or settings.rasa_server_url
        self.session = httpx.AsyncClient(timeout=10.0)
    
    async def process_message(self, message: str, sender_id: str) -> Optional[Dict[Any, Any]]:
        """Process message through Rasa and get response"""
        try:
            payload = {
                "sender": sender_id,
                "message": message
            }
            
            response = await self.session.post(
                f"{self.server_url}/webhooks/rest/webhook",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                if result:
                    return result[0]  # Return first response
                
        except Exception as e:
            logger.error(f"Rasa integration error: {e}")
        
        return None
    
    async def get_intent(self, message: str) -> Optional[str]:
        """Get intent classification from Rasa"""
        try:
            payload = {"text": message}
            
            response = await self.session.post(
                f"{self.server_url}/model/parse",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                intent = result.get("intent", {})
                if intent.get("confidence", 0) > 0.5:  # Threshold for intent confidence
                    return intent.get("name")
                
        except Exception as e:
            logger.error(f"Intent recognition error: {e}")
        
        return None
    
    async def is_rasa_available(self) -> bool:
        """Check if Rasa server is available"""
        try:
            response = await self.session.get(f"{self.server_url}/status")
            return response.status_code == 200
        except:
            return False
    
    async def close(self):
        """Close HTTP session"""
        await self.session.aclose()


# Global instance
rasa_integration = RasaIntegration()


# Helper functions for bot handlers
async def should_use_rasa(message_text: str) -> bool:
    """Determine if message should be processed by Rasa"""
    # Use Rasa for conversational messages, not for menu commands
    menu_commands = [
        "👤 Мой профиль",
        "💬 Общение",
        "🎉 Мероприятия",
        "❓ Помощь",
        "⚙️ Админ панель",
        "🔙 Назад"
    ]
    
    # Don't use Rasa for menu commands
    if message_text in menu_commands:
        return False
    
    # Don't use Rasa for commands starting with /
    if message_text.startswith("/"):
        return False
    
    # Use Rasa for conversational text
    return True


async def process_with_rasa(message_text: str, user_id: str) -> Optional[str]:
    """Process message with Rasa and return response text"""
    if not await rasa_integration.is_rasa_available():
        return None
    
    response = await rasa_integration.process_message(message_text, str(user_id))
    if response and "text" in response:
        return response["text"]
    
    return None
