import asyncio
import platform
import websockets
import json

games = {}
active_connections = set()  # Track all active WebSocket connections

async def server_handler(websocket):
    print("A player has connected.")
    active_connections.add(websocket)  # Add the connection to the set
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")

            if action == "create_game":
                match_id = data.get("match_id")
                username = data.get("username")
                if match_id not in games:
                    games[match_id] = {"players": [username]}
                else:
                    games[match_id]["players"].append(username)
                await broadcast_lobby_state(match_id)
            
            elif action == "join_game":
                match_id = data.get("match_id")
                username = data.get("username")
                if match_id in games:
                    games[match_id]["players"].append(username)
                    await broadcast_lobby_state(match_id)
                else:
                    await websocket.send(json.dumps({"error": "Game not found"}))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        active_connections.remove(websocket)  # Remove the connection when it closes
        await websocket.close()

async def broadcast_lobby_state(match_id):
    if match_id in games:
        state = {"action": "update_lobby", "match_id": match_id, "players": games[match_id]["players"]}
        message = json.dumps(state)
        disconnected = []
        for websocket in active_connections:
            try:
                await websocket.send(message)
            except websockets.ConnectionClosed:
                print("A")
                disconnected.append(websocket)
        for websocket in disconnected:
            active_connections.remove(websocket)

async def run_server():
    server = await websockets.serve(server_handler, "localhost", 8765)
    print("Server started on ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    if platform.system() == 'Darwin':
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(run_server())
