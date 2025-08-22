import asyncio
import uvicorn
from multiprocessing import Process

from app.config import settings
from app.bot.main import main as bot_main
from app.api.main import app as api_app


def run_api():
    """Run FastAPI server"""
    uvicorn.run(
        api_app,
        host=settings.api_host,
        port=settings.api_port,
        log_level="info" if settings.debug else "warning"
    )


async def run_bot():
    """Run Telegram bot"""
    await bot_main()


def main():
    """Main function to run both API and Bot"""
    print(f"Starting Test Bot...")
    print(f"API will be available at http://{settings.api_host}:{settings.api_port}")
    
    # Start API server in separate process
    api_process = Process(target=run_api)
    api_process.start()
    
    try:
        # Run bot in main process
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        api_process.terminate()
        api_process.join()
        print("Test Bot stopped.")


if __name__ == "__main__":
    main()
