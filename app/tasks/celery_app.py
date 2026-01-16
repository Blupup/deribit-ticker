from celery import Celery
from celery.schedules import crontab
import asyncio
from app.config import get_settings
from app.database import SessionLocal
from app.services.deribit_client import DeribitClient
from app.services.price_service import PriceService

settings = get_settings()

# Создаем Celery app
celery_app = Celery(
    "deribit_tracker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend
)

# Конфигурация Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Настройка периодических задач
celery_app.conf.beat_schedule = {
    'fetch-crypto-prices-every-minute': {
        'task': 'app.tasks.celery_app.fetch_and_save_prices',
        'schedule': crontab(minute='*'),  # Каждую минуту
    },
}


@celery_app.task(name='app.tasks.celery_app.fetch_and_save_prices')
def fetch_and_save_prices():
    """Периодическая задача для получения и сохранения цен"""
    print("Starting price fetch task...")
    
    # Создаем сессию БД
    db = SessionLocal()
    
    try:
        # Получаем цены асинхронно
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        client = DeribitClient()
        btc_price = loop.run_until_complete(client.get_btc_price())
        eth_price = loop.run_until_complete(client.get_eth_price())
        
        # Сохраняем в БД
        service = PriceService(db)
        
        if btc_price:
            service.save_price("btc_usd", btc_price)
            print(f"Saved BTC price: {btc_price}")
        else:
            print("Failed to fetch BTC price")
        
        if eth_price:
            service.save_price("eth_usd", eth_price)
            print(f"Saved ETH price: {eth_price}")
        else:
            print("Failed to fetch ETH price")
        
        return {
            "btc_price": btc_price,
            "eth_price": eth_price,
            "status": "success"
        }
    
    except Exception as e:
        print(f"Error in fetch_and_save_prices: {e}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()
