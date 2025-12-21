"""
game_logic.py
-------------
Güncelleme:
- Puanlar eski görseldeki gibi yüksek hissedilecek şekilde ayarlandı.
- "Spam" engellemek için final bonusu devasa hale getirildi.
- Az denemede bilen, çok deneyip puan toplayanı ezer geçer.
"""

import random
from typing import Tuple, Optional

# ======================
# AYARLAR
# ======================
NUM_DIGITS = 4
ATTEMPTS_PER_ROUND = 15

# ======================
# SAYI ÜRETİMİ
# ======================
def generate_secret(num_digits: int = NUM_DIGITS) -> str:
    """Rakamları birbirinden farklı sayı üretir."""
    digits = random.sample(range(10), num_digits)
    return "".join(map(str, digits))

# ======================
# TAHMİN DOĞRULAMA
# ======================
def validate_guess(guess: str, num_digits: int = NUM_DIGITS) -> Tuple[bool, Optional[str]]:
    guess = guess.strip()
    if not guess.isdigit():
        return False, "Sadece rakam girmelisin."
    if len(guess) != num_digits:
        return False, f"{num_digits} haneli olmalı."
    if len(set(guess)) != len(guess):
        return False, "Rakamlar birbirinden farklı olmalı."
    return True, None

# ======================
# + / - HESAPLAMA (Fixlendi)
# ======================
def plus_minus(target: str, guess: str) -> Tuple[int, int]:
    """
    Standard Mastermind mantığı.
    """
    plus = 0
    minus = 0
    length = len(target)

    for i in range(length):
        if guess[i] == target[i]:
            plus += 1
        elif guess[i] in target:
            minus += 1
            
    return plus, minus

# ======================
# DENGELİ PUANLAMA SİSTEMİ
# ======================

def calculate_turn_score(plus: int, minus: int) -> int:
    """
    Ara tahminlerde verilen puan.
    Eski fotoğraftaki gibi yüksek hissettirmesi için arttırıldı.
    """
    # Önceki hali: plus*5 + minus*2 (Çok düşüktü)
    # Yeni hali: plus*20 + minus*10 (Tatmin edici)
    return (plus * 20) + (minus * 10)

def calculate_win_bonus(attempts_used: int, total_time_seconds: float) -> int:
    """
    Oyun kazanıldığında verilen BÜYÜK ödül.
    Adaleti burası sağlar.
    """
    # Taban ödül çok yüksek, böylece ara puanlardan çok daha değerli olur.
    BASE_SCORE = 3000
    
    # Her deneme bu büyük ödülden ciddi puan siler (Hakkını idareli kullanma)
    # 1. denemede bilen: ~2900 puan alır.
    # 10. denemede bilen: ~1500 puan alır.
    attempt_penalty = attempts_used * 150
    
    # Süre cezası (Çok bekleme)
    time_penalty = int(total_time_seconds * 3)
    
    final_score = BASE_SCORE - attempt_penalty - time_penalty
    
    # Puan asla 500'ün altına düşmesin (Teselli)
    return max(500, int(final_score))