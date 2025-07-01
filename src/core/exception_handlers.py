from starlette.websockets import WebSocket
from starlette.exceptions import WebSocketException
from logger import logger

async def WebSocketExceptionHandler(
    websocket: WebSocket,
    exc: WebSocketException
) -> None:
    logger.error(exc.reason)
    
    await websocket.close(code=exc.code, reason=exc.reason)
    

exception_handlers: dict[Exception, callable] = {
    WebSocketException: WebSocketExceptionHandler,
}