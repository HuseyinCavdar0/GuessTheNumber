import asyncio
import json
import websockets

async def listen_server(ws):
    try:
        async for raw in ws:
            try:
                msg = json.loads(raw)
            except:
                continue

            mtype = msg.get("type")

            if mtype == "welcome":
                print(f"\n[SERVER] {msg.get('msg')}")

            elif mtype == "scores":
                print("\n" + "="*30)
                print("       SKOR TABLOSU")
                print("="*30)
                
                print("--- [ 🟢 AKTİF OYUNCULAR ] ---")
                active = msg.get("active", [])
                if not active: print("  (Kimse yok)")
                for s in active:
                    print(f"  • {s['name']}: {s['total']} puan")
                
                print("\n--- [ 🏆 TÜM ZAMANLAR ] ---")
                glob = msg.get("global", [])
                if not glob: print("  (Boş)")
                for i, s in enumerate(glob, 1):
                    print(f"  {i}. {s['name']}: {s['total']}")
                
                print("="*30 + "\n")

            elif mtype == "result":
                print(f"[SONUÇ] {msg['guess']} -> +{msg['plus']} -{msg['minus']} ({msg['gained']} puan)")

            elif mtype == "winner":
                print(f"\n*** KAZANAN: {msg['winner']} (Sayı: {msg['secret']}) ***\n")

            elif mtype == "newround":
                print("\n--- YENİ TUR ---\n")

            elif mtype == "error":
                print(f"[HATA] {msg['msg']}")

    except websockets.ConnectionClosed:
        print("Bağlantı kapandı.")


async def send_guesses(ws):
    loop = asyncio.get_event_loop()
    while True:
        guess = await loop.run_in_executor(None, input)
        if not guess: continue
        await ws.send(json.dumps({"type": "guess", "guess": guess}))


async def main():
    ip = input("IP (Enter=localhost): ").strip() or "localhost"
    name = input("Adın: ").strip() or "TerminalUser"
    uri = f"ws://{ip}:8765"
    
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"type": "join", "name": name}))
        await asyncio.gather(listen_server(ws), send_guesses(ws))

if __name__ == "__main__":
    try: asyncio.run(main())
    except: pass