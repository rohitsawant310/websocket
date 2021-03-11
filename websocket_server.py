#!/usr/bin/env python
import asyncio
import time
import websockets
import subprocess as sp
import logging

ws_clients = set()
async def broadcast(message = "default broadcast MSG", push = True):
    """
        Here we can broadcast data to connecting websocket client .
    """
    try:
        if push:
            while True:
                await asyncio.gather(
                    *[ws.send(message) for ws in ws_clients],
                    return_exceptions=True,
                )
                await asyncio.sleep(2)
        else:
            await asyncio.gather(
                        *[ws.send(message) for ws in ws_clients],
                        return_exceptions=True,
                    )
    except Exception as Error:
        print(Error)

async def register(websocket,path):
    """
        This function Register new client 
    """
    ws_clients.add(websocket)


async def unregister(websocket,path):
    """
        Unregister websocket client on client connection close.
    """
    try:
        ws_clients.remove(websocket)
        await asyncio.sleep(0.01)
        print("client closed ")
    except Exception as Error:
        print(Error)
    
    
async def consumer_handler(websocket, path):
    """
        This function broadcast client message to other ws clients
    """
    async for message in websocket:
        await broadcast(message,False)

            
async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))
    print(path)
    try:
        await register(websocket,path)
        await websocket.wait_closed()
        try:
            async for msg in websocket:
                print("on main")
                if msg == "close":
                  print("inside close")
                break
                
        except websockets.exceptions.ConnectionClosedError:
                    print("ABNORMAL CLOSE")
            
                
    except Exception as Error:
        print(Error)

    finally:

            await unregister(websocket,path)
            

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.create_task(broadcast())
    
    start_server = websockets.serve(handler, "localhost", 8765,ping_interval=None,ping_timeout=1)
    loop.run_until_complete(start_server)
    try:
        loop.run_forever()
        
    except KeyboardInterrupt:
        print("Exiting")
        
    except :
        pass