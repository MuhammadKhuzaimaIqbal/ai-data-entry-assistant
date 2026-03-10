from pydantic import BaseModel
from typing import Optional

#Bussiness card schema

class BusinessCard(BaseModel):
    name: Optional[str]
    title: Optional[str]
    company: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]

#Invoice schema

class LineItem(BaseModel):
    description: str
    quantity: int
    price: float

class Invoice(BaseModel):
    vendor: Optional[str]
    invoice_number: Optional[str]
    date: Optional[str]
    line_items: list[LineItem]
    total: Optional[float]
    tax: Optional[float]

#Resume schema

class Resume(BaseModel):
    name: Optional[str]
    education: list[str]
    experience: list[str]
    skills: list[str]