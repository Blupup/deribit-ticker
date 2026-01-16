import aiohttp
from typing import Optional
from app.config import get_settings


class DeribitClient:
    """Клиент для работы с Deribit API"""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.deribit_api_url
        
    async def get_index_price(self, currency: str) -> Optional[float]:
        """
        Получить index price для валюты
        
        Args:
            currency: Валюта (BTC или ETH)
            
        Returns:
            Index price или None в случае ошибки
        """
        url = f"{self.base_url}/public/get_index_price"
        params = {"index_name": f"{currency.lower()}_usd"}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("result", {}).get("index_price")
                    else:
                        print(f"Error fetching {currency} price: {response.status}")
                        return None
        except aiohttp.ClientError as e:
            print(f"Client error fetching {currency} price: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching {currency} price: {e}")
            return None
    
    async def get_btc_price(self) -> Optional[float]:
        """Получить BTC index price"""
        return await self.get_index_price("BTC")
    
    async def get_eth_price(self) -> Optional[float]:
        """Получить ETH index price"""
        return await self.get_index_price("ETH")
