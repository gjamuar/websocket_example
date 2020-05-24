# WS server example

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets
from RecognizerService import RecognizerService
from config import DatabasePath, mode, FingerprintDirectory, RecordingTime
import json

recognizer = RecognizerService(DatabasePath)

# async def time(websocket, path):
#     while True:
#         now = datetime.datetime.utcnow().isoformat() + "Z"
#         match_list = recognizer.stream_recognize_file_path("mp3/Brad-Sucks--Total-Breakdown.mp3")
#         await websocket.send(now)
#         # await asyncio.sleep(random.random() * 3)
#         for match in match_list:
#             y = json.dumps(match)
#             print(y)
#             await websocket.send(y)

async def recognize(websocket, path):
    match_list = recognizer.stream_recognize_file_path("mp3/Brad-Sucks--Total-Breakdown.mp3")
    for match in match_list:
        y = json.dumps(match)
        # print(y)
        await websocket.send(y)




if __name__ == "__main__":
    start_server = websockets.serve(recognize, "127.0.0.1", 5678)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
