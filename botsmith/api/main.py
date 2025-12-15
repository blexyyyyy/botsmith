from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from botsmith.api.routers import health, bot, stream

app = FastAPI(
    title="BotSmith API",
    description="REST API for BotSmith - AI-powered bot generator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(bot.router, prefix="/bot", tags=["Bot"])
app.include_router(stream.router, prefix="/bot", tags=["Stream"])

@app.get("/")
async def root():
    return {"message": "BotSmith API is running!", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
