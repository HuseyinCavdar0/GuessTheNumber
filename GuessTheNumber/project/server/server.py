# server.py
# =========
# Güncelleme: Admin Şifresi ile Leaderboard Sıfırlama Özelliği

import asyncio
import json
import time
import os

import websockets

from game_logic import (
    NUM_DIGITS,
    ATTEMPTS_PER_ROUND,
    generate_secret,
    plus_minus,
    calculate_turn_score,
    calculate_win_bonus,
    validate_guess,
)

HOST = "0.0.0.0"
PORT = 8765
LEADERBOARD_FILE = "leaderboard.json"
ADMIN_PASSWORD = "666"  # <-- Admin şifresi burada tanımlı

# Global Durumlar
players = {}       
global_leaderboard = {} 
secret_number = None

# --- DOSYA İŞLEMLERİ ---
def load_leaderboard():
    global global_leaderboard
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                global_leaderboard = json.load(f)
            print("[SERVER] Leaderboard yüklendi.")
        except Exception as e:
            print(f"[SERVER] Leaderboard yüklenirken hata: {e}")
            global_leaderboard = {}
    else:
        print("[SERVER] Kayıtlı leaderboard bulunamadı, yeni oluşturuluyor.")
        global_leaderboard = {}

def save_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(global_leaderboard, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[SERVER] Leaderboard kaydedilemedi: {e}")

# --- SERVER MANTIĞI ---

async def broadcast(message_dict: dict):
    if not players: return
    data = json.dumps(message_dict)
    await asyncio.gather(*[ws.send(data) for ws in list(players.keys())], return_exceptions=True)

def scores_payload() -> dict:
    active_list = [
        {"name": info["name"], "total": info["total"]}
        for info in players.values()
    ]
    active_list.sort(key=lambda x: x["total"], reverse=True)

    global_list = [
        {"name": name, "total": score}
        for name, score in global_leaderboard.items()
    ]
    global_list.sort(key=lambda x: x["total"], reverse=True)
    
    return {
        "type": "scores",
        "active": active_list,
        "global": global_list[:10] 
    }

async def handle_player(ws):
    global secret_number, global_leaderboard

    # --- BAĞLANTI ---
    try:
        raw = await ws.recv()
        msg = json.loads(raw)
        if msg.get("type") != "join": raise ValueError("Not join")
    except:
        return

    name = str(msg.get("name", "Anon"))[:20]
    
    existing_names = [info["name"] for info in players.values()]
    original_name = name
    suffix = 2
    while name in existing_names:
        name = f"{original_name}{suffix}"
        suffix += 1

    players[ws] = {
        "name": name,
        "total": 0,
        "round": 0,
        "round_start_time": time.time(), 
        "last_guess_time": time.time(),
        "attempts": ATTEMPTS_PER_ROUND,
    }

    if name not in global_leaderboard:
        global_leaderboard[name] = 0

    if secret_number is None:
        secret_number = generate_secret(NUM_DIGITS)
        print(f"[SERVER] Yeni sayı: {secret_number}")

    print(f"[SERVER] Bağlandı: {name}")
    await ws.send(json.dumps({"type": "welcome", "msg": f"Hoş geldin {name}!"}))
    await ws.send(json.dumps(scores_payload()))
    await broadcast(scores_payload())

    # --- OYUN DÖNGÜSÜ ---
    try:
        async for raw in ws:
            try:
                msg = json.loads(raw)
            except: continue
            
            mtype = msg.get("type")

            # 1) TAHMİN İŞLEMİ
            if mtype == "guess":
                guess = str(msg.get("guess", "")).strip()
                info = players.get(ws)
                if not info: break

                ok, err = validate_guess(guess, NUM_DIGITS)
                if not ok:
                    await ws.send(json.dumps({"type": "error", "msg": err}))
                    continue
                if info["attempts"] <= 0:
                    await ws.send(json.dumps({"type": "error", "msg": "Hakkın bitti"}))
                    continue

                now = time.time()
                dt_turn = now - info["last_guess_time"]
                info["last_guess_time"] = now

                plus, minus = plus_minus(secret_number, guess)
                turn_points = calculate_turn_score(plus, minus)
                
                info["round"] += turn_points
                info["total"] += turn_points
                info["attempts"] -= 1

                win_bonus = 0
                is_winner = False
                
                if plus == NUM_DIGITS:
                    is_winner = True
                    total_duration = time.time() - info["round_start_time"]
                    attempts_used = ATTEMPTS_PER_ROUND - info["attempts"]
                    win_bonus = calculate_win_bonus(attempts_used, total_duration)
                    info["total"] += win_bonus
                    
                    if info["total"] > global_leaderboard[info["name"]]:
                        global_leaderboard[info["name"]] = info["total"]
                        save_leaderboard()

                await ws.send(json.dumps({
                    "type": "result",
                    "guess": guess,
                    "plus": plus,
                    "minus": minus,
                    "gained": turn_points + win_bonus,
                    "remaining": info["attempts"],
                    "time": round(dt_turn, 2),
                }))

                await broadcast(scores_payload())

                if is_winner:
                    winner_name = info["name"]
                    await broadcast({
                        "type": "winner",
                        "winner": winner_name,
                        "secret": secret_number,
                    })

                    secret_number = generate_secret(NUM_DIGITS)
                    print(f"[SERVER] Yeni sayı: {secret_number}")
                    
                    for p in players.values():
                        p["round"] = 0
                        p["attempts"] = ATTEMPTS_PER_ROUND
                        p["round_start_time"] = time.time()
                        p["last_guess_time"] = time.time()
                    
                    await broadcast({"type": "newround"})

            # 2) LEADERBOARD SIFIRLAMA (YENİ)
            elif mtype == "reset_leaderboard":
                password = str(msg.get("key", ""))
                if password == ADMIN_PASSWORD:
                    # Sıfırla
                    global_leaderboard.clear()
                    # Anlık oyuncuları da global listeye 0 puanla geri ekle (isimleri kaybolmasın diye)
                    for p_info in players.values():
                        global_leaderboard[p_info["name"]] = 0 # Veya p_info["total"] korunabilir, tercih meselesi. 
                                                               # "Her şeyi sil" dendiği için 0 mantıklı.
                    save_leaderboard()
                    await broadcast(scores_payload())
                    await ws.send(json.dumps({"type": "info", "msg": "✅ Leaderboard başarıyla sıfırlandı."}))
                    print(f"[ADMIN] {players[ws]['name']} leaderboard'ı sıfırladı.")
                else:
                    await ws.send(json.dumps({"type": "error", "msg": "⛔ Yanlış Şifre! Erişim Reddedildi."}))

    except websockets.ConnectionClosed:
        pass
    finally:
        info = players.pop(ws, None)
        if info:
            print(f"[SERVER] Ayrıldı: {info['name']}")
            if info["total"] > global_leaderboard.get(info["name"], 0):
                global_leaderboard[info["name"]] = info["total"]
                save_leaderboard()
            await broadcast(scores_payload())

async def main():
    load_leaderboard()
    print(f"[SERVER] {HOST}:{PORT} çalışıyor...")
    async with websockets.serve(handle_player, HOST, PORT):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SERVER] Kapatıldı.")