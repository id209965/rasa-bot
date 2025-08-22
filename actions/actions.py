import re
from typing import Text, Dict, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, ActiveLoop
import sqlite3

# ... (ваш код init_db и другие классы без изменений) ...

# --- ДОБАВЬТЕ ЭТОТ КЛАСС ---
class ActionCheckAdmin(Action):
    def name(self) -> Text:
        return "action_check_admin"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        phone_number = tracker.get_slot("phone_number")
        
        # Список номеров администраторов (можно вынести в конфиг)
        admin_phones = ["+70000000000", "80000000000"] # Замените на реальные номера
        
        is_admin = phone_number in admin_phones
        
        return [SlotSet("is_admin", is_admin)]

# --- ДОБАВЬТЕ ЭТИ ЗАГЛУШКИ ---
class ActionCreateEvent(Action):
    def name(self) -> Text:
        return "action_create_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Это действие просто запускает форму, логика не нужна
        return []

class ActionSaveEvent(Action):
    def name(self) -> Text:
        return "action_save_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Мероприятие сохранено!")
        # Здесь будет логика сохранения в БД
        return []

class ActionCancelEvent(Action):
    def name(self) -> Text:
        return "action_cancel_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Создание мероприятия отменено.")
        return []

class ActionAdminUploadLists(Action):
    def name(self) -> Text:
        return "action_admin_upload_lists"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Функция загрузки списков в разработке.")
        return []

class ActionAdminGenerateUsersReport(Action):
    def name(self) -> Text:
        return "action_admin_generate_users_report"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Генерирую отчет по пользователям...")
        return []

class ActionAdminGenerateEventsReport(Action):
    def name(self) -> Text:
        return "action_admin_generate_events_report"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Генерирую отчет по мероприятиям...")
        return []

