from sqlalchemy import Column, String, Float, Integer, Index
from app.database import Base

class CryptoPrice(Base):
    __tablename__ = "crypto_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), nullable=False, index=True)
    price = Column(Float, nullable=False)
    timestamp = Column(Integer, nullable=False, index=True)
    
    __table_args__ = (
        Index('idx_ticker_timestamp', 'ticker', 'timestamp'),
    )
