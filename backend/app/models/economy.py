"""
Economy models: Wallets, Transactions, and Currency.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SQLEnum, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class CurrencyType(enum.Enum):
    """Currency types in the economy."""
    CREDITS = "credits"  # Soft currency - earned through activities
    STARS = "stars"      # Hard currency - purchased or rare rewards


class Wallet(Base):
    """User wallet for holding currencies."""
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="wallets")
    
    # Balances
    credits_balance = Column(Float, default=0.0)
    stars_balance = Column(Float, default=0.0)
    
    # Limits (for anti-fraud and economy balance)
    daily_credit_limit = Column(Float, default=10000.0)
    daily_star_limit = Column(Float, default=1000.0)
    
    # Status
    is_frozen = Column(Boolean, default=False)
    freeze_reason = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="wallet", foreign_keys="Transaction.wallet_id")


class Transaction(Base):
    """Transaction record for audit trail."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    wallet = relationship("Wallet", foreign_keys=[wallet_id], back_populates="transactions")
    
    # Transaction details
    transaction_type = Column(String(50), nullable=False)  # deposit, withdrawal, transfer, purchase, reward, tax
    currency_type = Column(SQLEnum(CurrencyType), nullable=False)
    amount = Column(Float, nullable=False)
    
    # Balance snapshot (for audit)
    balance_before = Column(Float, nullable=False)
    balance_after = Column(Float, nullable=False)
    
    # Metadata
    description = Column(Text, nullable=True)
    reference_id = Column(String(100), nullable=True)  # External reference (e.g., Stripe payment ID)
    metadata_json = Column(JSON, default=dict)
    
    # Counterparty (for transfers)
    counterparty_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=True)
    
    # Status
    status = Column(String(20), default="completed")  # pending, completed, failed, reversed
    failure_reason = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
