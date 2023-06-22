import random
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
import uvicorn
from collections import Counter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TransactionModel(BaseModel):
    name: str
    amount: float

SQLALCHEMY_DATABASE_URL = "sqlite:///./transactions.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    type = Column(String)


Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/transaction")
def create_transaction():
    # Обработка создания транзакции
    return {"message": "Transaction created successfully"}


@app.get("/balance")
def get_balance(db: Session = Depends(get_db)):
    total_value = db.query(func.sum(Transaction.value)).scalar()
    return {"balance": total_value or 0.0}


PAIR_COEFF = 2
FULL_HOUSE_COEFF = 3
BALUT_COEFF = 4
STRAIGHT_COEFF = 5

def has_pair(arr):
    counter = Counter(arr)
    if max(counter.values()) >= 2:
        return True
    return False

def has_full_house(arr):
    counter = Counter(arr)
    if len(counter) == 2 and 3 in counter.values():
        return True
    return False

def has_balut(arr):
    counter = Counter(arr)
    if len(counter) == 1 and max(counter.values()) == 5:
        return True
    return False

def has_straight(arr):
    sorted_arr = sorted(arr)
    for i in range(len(sorted_arr) - 1):
        if sorted_arr[i + 1] != sorted_arr[i] + 1:
            return False
    return True

def check_combinations(dice_values):
    if has_pair(dice_values):
        return "PAIR"
    elif has_full_house(dice_values):
        return "FULL HOUSE"
    elif has_balut(dice_values):
        return "BALUT"
    elif has_straight(dice_values):
        return "STRAIGHT"
    return None


def calculate_prize(combination, bet, adjusted_odds):
    if combination == "STRAIGHT":
        return bet * (STRAIGHT_COEFF / adjusted_odds)
    elif combination == "BALUT":
        return bet * (BALUT_COEFF / adjusted_odds)
    elif combination == "FULL HOUSE":
        return bet * (FULL_HOUSE_COEFF / adjusted_odds)
    elif combination == "PAIR":
        return bet * (PAIR_COEFF / adjusted_odds)
    else:
        return 0


def simulate_game(iterations, adjusted_odds):
    total_wins = 0
    total_bets = 0

    for _ in range(iterations):
        dice_values = [random.randint(1, 6) for _ in range(5)]
        combination = check_combinations(dice_values)

        total_bets += bet

        if combination:
            prize = calculate_prize(combination, bet, adjusted_odds)
            total_wins += prize

    return total_wins, total_bets


def calculate_rtp(wins, bets):
    return (wins / bets) * 100


iterations = 1000000
bet = 5

target_rtp = 95
adjusted_odds = (target_rtp / 100) * (bet / (iterations * bet / STRAIGHT_COEFF))

wins, bets = simulate_game(iterations, adjusted_odds)
rtp = calculate_rtp(wins, bets)

bet = 5
combination = "FULL HOUSE"
prize = calculate_prize(combination, bet, adjusted_odds)
print(f"Prize for {combination} with a bet of {bet}: {prize}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)