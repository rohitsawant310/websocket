#!/usr/bin/env python

# WS listner example
import asyncio
import websockets
import time 

async def reciever():
    uri = "ws://localhost:8765/listner"
    async with websockets.connect(uri) as websocket:
            while True:
                greeting = await websocket.recv()
                print(f"{greeting}")
                await asyncio.sleep(1)      

asyncio.get_event_loop().run_until_complete(reciever())