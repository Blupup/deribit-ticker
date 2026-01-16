from fastapi import FastAPI
from app.api import routes
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Deribit Price Tracker API",
    description="API for tracking BTC and ETH prices from Deribit",
    version="1.0.0"
)

app.include_router(routes.router)

@app.get("/")
def root():
    return {
        "message": "Deribit Price Tracker API",
        "docs": "/docs",
        "endpoints": {
            "all_prices": "/Получение всех сохраненных данных по указанной валюте?ticker=btc_usd",
            "latest_price": "/Получение последней цены валюты?ticker=btc_usd",
            "filter_by_date": "/Получение цены валюты с фильтром по датеfilter?ticker=btc_usd&start_date=1234567890"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
