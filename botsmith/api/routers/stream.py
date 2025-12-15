import json
import asyncio
from typing import AsyncGenerator
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from botsmith.app import BotSmithApp
from botsmith.api.deps import get_botsmith_app
import concurrent.futures

router = APIRouter()

@router.get("/stream")
async def stream_bot_creation(prompt: str, project_name: str = "stream_bot", app: BotSmithApp = Depends(get_botsmith_app)):
    """
    Server-Sent Events (SSE) endpoint for real-time bot creation.
    """
    
    # Capture the main event loop
    main_loop = asyncio.get_running_loop()
    
    # We use a queue to bridge the sync executor callback to the async generator
    queue = asyncio.Queue()
    
    def on_event(event_type: str, data: dict):
        # This runs in the thread pool, so we use the captured main_loop to schedule updates
        main_loop.call_soon_threadsafe(queue.put_nowait, {"type": event_type, "data": data})

    def run_bot():
        try:
            app.create_bot(prompt, project_name, on_event)
            # Signal done
            on_event("done", {"status": "success"})
        except Exception as e:
            on_event("error", {"message": str(e)})
            on_event("done", {"status": "failed"})

    async def event_generator() -> AsyncGenerator[str, None]:
        # Start bot creation in a separate thread
        # Fire and forget (in thread pool)
        main_loop.run_in_executor(None, run_bot)
        
        while True:
            # Wait for next event
            event = await queue.get()
            
            # SSE Format: "data: <json>\n\n"
            yield f"data: {json.dumps(event)}\n\n"
            
            if event["type"] == "done":
                break

    return StreamingResponse(event_generator(), media_type="text/event-stream")
