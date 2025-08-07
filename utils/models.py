
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import date

class EmailData(BaseModel):
    id: str
    subject: str
    body: str
    from_email: EmailStr = Field(..., alias="from")
    stage: Optional[str] = None
    intent: Optional[str] = None

class CustomerInfo(BaseModel):
    name: str
    company: str
    country: Optional[str] = None
    stage: Literal["New", "Qualified", "Customer", "Negotiation", "Closed Won", "Closed Lost"]
    role: Optional[str] = None
    email: Optional[EmailStr] = None

class Opportunity(BaseModel):
    id: Optional[str]
    name: str
    accountName: str
    description: str
    stage: str
    source: str = "Email"
    amount: Optional[float] = 0
    closeDate: Optional[date] = None
