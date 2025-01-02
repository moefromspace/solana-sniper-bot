from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import token_listener, aggregator, trade_executor, portfolio_tracker
from src.utils.logging_setup import setup_logging
from src.services.redis_service import connect_redis
from src.config import REDIS_HOST, REDIS_PORT

# Initialize the app
app = FastAPI(
    title="Solana Token Sniper Bot API",
    description="Backend for the Solana Token Sniper Bot.",
    version="1.0.0",
)

# Set up logging
setup_logging()

# CORS Middleware (customize based on frontend's origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin (adjust in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(token_listener.router, prefix="/tokens", tags=["Token Listener"])
#app.include_router(aggregator.router, prefix="/aggregator", tags=["Aggregator"])
#app.include_router(trade_executor.router, prefix="/trades", tags=["Trade Executor"])
#app.include_router(portfolio_tracker.router, prefix="/portfolio", tags=["Portfolio Tracker"])

# Event handlers
@app.on_event("startup")
async def on_startup():
    """
    Code to run when the application starts.
    """
    # Placeholder: Add startup logic like initializing Redis connections or database connections
    redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}"
    await connect_redis(redis_url)
    pass

@app.on_event("shutdown")
async def on_shutdown():
    """
    Code to run when the application shuts down.
    """
    # Placeholder: Add cleanup logic like closing database or Redis connections
    pass

# Root endpoint (for testing purposes)
@app.get("/")
def root():
    return {"message": "Solana Token Sniper Bot API is running!"}
