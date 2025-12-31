import random
from typing import Tuple, Optional

NUM_DIGITS = 4
ATTEMPTS_PER_ROUND = 20

# SAYI ÜRETİMİ
def generate_secret(num_digits: int = NUM_DIGITS) -> str:
    digits = random.sample(range(10), num_digits)
    return "".join(map(str, digits))

# TAHMİN DOĞRULAMA
def validate_guess(guess: str, num_digits: int = NUM_DIGITS) -> Tuple[bool, Optional[str]]:
    guess = guess.strip()
    if not guess.isdigit():
        return False, "Sadece rakam girmelisin."
    if len(guess) != num_digits:
        return False, f"{num_digits} haneli olmalı."
    if len(set(guess)) != len(guess):
        return False, "Rakamlar birbirinden farklı olmalı."
    return True, None

# + / - HESAPLAMA 
def plus_minus(target: str, guess: str) -> Tuple[int, int]:
    plus = 0
    minus = 0
    length = len(target)

    for i in range(length):
        if guess[i] == target[i]:
            plus += 1
        elif guess[i] in target:
            minus += 1
            
    return plus, minus


# PUANLAMA SİSTEMİ

# Sayıyı bulana kadar herkes (Ara Puanlar)
def calculate_turn_score(plus: int, minus: int) -> int:
    # Yeri doğruysa 20 puan, yeri yanlışsa 10 puan (sayı başınsa) 
    return (plus * 20) + (minus * 10)

# Sayıyı Bulan (Final Bonusu)
def calculate_win_bonus(attempts_used: int, total_time_seconds: float) -> int:
    # Ödül taban puanı
    BASE_SCORE = 3000
    
    # Kaçıncı denemende 
    attempt_penalty = attempts_used * 50
    
    # Süre cezası
    time_penalty = int(total_time_seconds * 2)
    
    # 3000 (Taban Puan) - (Harcanan Hak Cezası) - (Süre Cezası)
    final_score = BASE_SCORE - attempt_penalty - time_penalty
    
    return max(1000, int(final_score))