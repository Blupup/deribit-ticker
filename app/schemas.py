from pydantic import BaseModel, Field

class CryptoPriceResponse(BaseModel):
    id: int
    ticker: str
    price: float
    timestamp: int
    
    class Config:
        from_attributes = True

class PriceFilterParams(BaseModel):
    ticker: str = Field(..., description="Ticker symbol (btc_usd or eth_usd)")
    start_date: int | None = Field(None, description="Start timestamp (UNIX)")
    end_date: int | None = Field(None, description="End timestamp (UNIX)")
