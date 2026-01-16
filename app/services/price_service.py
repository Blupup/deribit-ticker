from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import CryptoPrice
import time


class PriceService:
    """Сервис для работы с ценами криптовалют"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save_price(self, ticker: str, price: float) -> CryptoPrice:
        """Сохранить цену в базу данных"""
        crypto_price = CryptoPrice(
            ticker=ticker,
            price=price,
            timestamp=int(time.time())
        )
        self.db.add(crypto_price)
        self.db.commit()
        self.db.refresh(crypto_price)
        return crypto_price
    
    def get_all_prices(self, ticker: str) -> List[CryptoPrice]:
        """Получить все цены для указанного ticker"""
        return self.db.query(CryptoPrice).filter(
            CryptoPrice.ticker == ticker
        ).order_by(CryptoPrice.timestamp.desc()).all()
    
    def get_latest_price(self, ticker: str) -> Optional[CryptoPrice]:
        """Получить последнюю цену для ticker"""
        return self.db.query(CryptoPrice).filter(
            CryptoPrice.ticker == ticker
        ).order_by(CryptoPrice.timestamp.desc()).first()
    
    def get_prices_by_date(
        self, 
        ticker: str, 
        start_date: Optional[int] = None, 
        end_date: Optional[int] = None
    ) -> List[CryptoPrice]:
        """Получить цены с фильтром по дате"""
        query = self.db.query(CryptoPrice).filter(CryptoPrice.ticker == ticker)
        
        if start_date:
            query = query.filter(CryptoPrice.timestamp >= start_date)
        if end_date:
            query = query.filter(CryptoPrice.timestamp <= end_date)
        
        return query.order_by(CryptoPrice.timestamp.desc()).all()
