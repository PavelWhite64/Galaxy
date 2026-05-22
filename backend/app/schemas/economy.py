"""
Economy schemas for wallets and transactions.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class WalletBase(BaseModel):
    pass


class WalletResponse(WalletBase):
    id: int
    user_id: int
    credits_balance: float
    stars_balance: float
    daily_credit_limit: float
    daily_star_limit: float
    is_frozen: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    transaction_type: str
    currency_type: str  # "credits" or "stars"
    amount: float
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    wallet_id: int
    balance_before: float
    balance_after: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
