import random
from collections import Counter

# PAIR_COEFF = 1
# FULL_HOUSE_COEFF = 1
# BALUT_COEFF = 5
# STRAIGHT_COEFF = 1 kf for 95% rtp

PAIR_COEFF = 2
FULL_HOUSE_COEFF = 3
BALUT_COEFF = 4
STRAIGHT_COEFF = 5
ITERATIONS = 1_000_000

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

def simulate_game(iterations):
    total_wins = 0
    total_bets = 0

    for _ in range(iterations):
        bet = 1
        arr = [random.randint(1, 6) for _ in range(5)]

        if has_straight(arr):
            target_coeff = STRAIGHT_COEFF
        elif has_balut(arr):
            target_coeff = BALUT_COEFF
        elif has_full_house(arr):
            target_coeff = FULL_HOUSE_COEFF
        elif has_pair(arr):
            target_coeff = PAIR_COEFF
        else:
            target_coeff = 0

        if target_coeff != 0:
            total_wins += bet * target_coeff

        total_bets += bet

    return abs(total_wins), total_bets

def calculate_rtp(wins, bets):
    return (wins / bets) * 100

wins, bets = simulate_game(ITERATIONS)
rtp = calculate_rtp(wins, bets)

print(f"Total wins: {wins}")
print(f"Total bets: {bets}")
print(f"RTP: {rtp}%")

print("PAIR, Should be True:", has_pair([2, 2, 5, 1, 3]))
print("PAIR, Should be True:", has_pair([2, 2, 5, 3, 3]))

print("FULL HOUSE, Should be True:", has_full_house([2, 2, 2, 3, 3]))
print("FULL HOUSE, Should be False:", has_full_house([1, 2, 3, 3, 3]))

print("BALUT, Should be True:", has_balut([2, 2, 2, 2, 2]))
print("Should be False:", has_balut([1, 1, 1, 1, 2]))
print("Should be True:", has_balut([1, 1, 1, 1, 1]))

print("STRAIGHT, Should be True:", has_straight([2, 3, 4, 5, 6]))





