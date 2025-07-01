from starlette.applications import Starlette
from starlette.websockets import WebSocket
from starlette.endpoints import WebSocketEndpoint
from starlette.exceptions import WebSocketException
from starlette.routing import WebSocketRoute

from configs import debug
from core import exception_handlers, lifespan

from orm import async_session, Message
from logger import logger

from sqlalchemy.exc import OperationalError

from time import perf_counter
from asyncio import gather

connected_clients: set[WebSocket] = set()

class WSChatEndpoint(WebSocketEndpoint):
    encoding: str = "text"
    
    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
            
        connected_clients.add(websocket)
        
        logger.info("WebSocket connection opened. Ready to receive data.")
        logger.info("Connected clients [\x1b[1;36m%d\x1b[0m]", len(connected_clients))
        
    async def on_receive(self, websocket: WebSocket, data: str) -> None:
        start: float = perf_counter()
        logger.info("Received message data. Processing ...")
        
        data: str = data.strip()
        
        if not data:
            await websocket.send_json({
                "success": False,
                "error": "Message can't be empty." 
            })
            
            return
        
        
        async with async_session() as session:
            try:
                message: Message = Message(content=data)
                
                session.add(message)
                await session.commit()
                
                logger.debug("Message data has been commited to database.")
            
            except OperationalError:
                raise WebSocketException(
                    code=1011,
                    reason="Couldn't connect to database."
                )
                
        json_response: dict = {
            "success": True,
            "data": f"[{message.date.strftime('%Y-%m-%d %H:%M:%S')}] {message.content}"
        }
                
        responses: None | Exception = await gather(*[
            client.send_json(json_response) for client in connected_clients
        ], return_exceptions=True)
        
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                logger.error("Client [\x1b[1;36m%d\x1b[0m] raised an exception: %s", i, response)
        
        logger.debug("Message data was sent to connected clients.")
        logger.info("Successfully processing message data.")
        
        response_time: int = round((perf_counter() - start) * 1000)
        if response_time > 50:
            logger.warning("Response time is extremely slow [\x1b[1;91m%dms\x1b[0m]", response_time)
            
        elif response_time > 18:
            logger.warning("Response time is slower than excepted  [\x1b[1;33m%dms\x1b[0m]", response_time)
            
        else:
            logger.info("Response time [\x1b[1;32m%dms\x1b[0m]", response_time)
        
    async def on_disconnect(self, websocket: WebSocket, close_code: int):
        try:
            connected_clients.remove(websocket)
            logger.info("WebSocket connection closed [\x1b[1;36m%d\x1b[0m]", close_code)
            
            logger.info("Connected clients [\x1b[1;36m%d\x1b[0m]", len(connected_clients))
            
        except KeyError:
            logger.warning("No WebSocket element found in the connected clients.")
            
            
app: Starlette = Starlette(
    debug=debug,
    routes=[WebSocketRoute("/ws/chat", WSChatEndpoint)],
    lifespan=lifespan,
    exception_handlers=exception_handlers
)