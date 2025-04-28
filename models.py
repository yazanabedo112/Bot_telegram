from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    phone_number: str

@dataclass
class Offer:
    offer_id: int
    description: str
    price: float

@dataclass
class Transaction:
    tx_id: int
    user_id: int
    offer_id: int
    status: str
    created_at: str
