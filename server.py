import asyncio
import websockets
import json

games = {}

async def server_handler(websocket):
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")
            match_id = data.get("match_id")
            username = data.get("username")
            
            if action == "create_game":
                games[match_id] = {"players": [username]}
            elif action == "join_game":
                if match_id in games:
                    games[match_id]["players"].append(username)
                else:
                    await websocket.send(json.dumps({"error": "Game not found"}))
                    continue

            # Broadcast updated lobby state
            await websocket.send(json.dumps({
                "action": "update_lobby",
                "match_id": match_id,
                "players": games[match_id]["players"]
            }))
    except Exception as e:
        print(f"Error: {e}")

async def run_server():
    async with websockets.serve(server_handler, "localhost", 8765):
        print("Server running on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(run_server())
