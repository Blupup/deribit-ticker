from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.price_service import PriceService
from app.schemas import CryptoPriceResponse

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/", response_model=List[CryptoPriceResponse])
def get_all_prices(
    ticker: str = Query(..., description="Ticker symbol (btc_usd or eth_usd)"),
    db: Session = Depends(get_db)
):
    """Получить все сохраненные данные по указанной валюте"""
    service = PriceService(db)
    prices = service.get_all_prices(ticker)
    
    if not prices:
        raise HTTPException(status_code=404, detail=f"No prices found for ticker: {ticker}")
    
    return prices


@router.get("/latest", response_model=CryptoPriceResponse)
def get_latest_price(
    ticker: str = Query(..., description="Ticker symbol (btc_usd or eth_usd)"),
    db: Session = Depends(get_db)
):
    """Получить последнюю цену валюты"""
    service = PriceService(db)
    price = service.get_latest_price(ticker)
    
    if not price:
        raise HTTPException(status_code=404, detail=f"No price found for ticker: {ticker}")
    
    return price


@router.get("/filter", response_model=List[CryptoPriceResponse])
def get_prices_by_date(
    ticker: str = Query(..., description="Ticker symbol (btc_usd or eth_usd)"),
    start_date: Optional[int] = Query(None, description="Start timestamp (UNIX)"),
    end_date: Optional[int] = Query(None, description="End timestamp (UNIX)"),
    db: Session = Depends(get_db)
):
    """Получить цены валюты с фильтром по дате"""
    service = PriceService(db)
    prices = service.get_prices_by_date(ticker, start_date, end_date)
    
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for specified criteria")
    
    return prices
