from fastapi import APIRouter, HTTPException # type: ignore
from dataclasses import dataclass
from typing import Dict, Any, Optional
import asyncio
import websockets # type: ignore
import json
from datetime import datetime, timezone
from typing import Any, Dict
from src.services.redis_service import publish_to_redis
from src.utils.logging_setup import logger

router = APIRouter()

SOLANA_WEBSOCKET_URL = "wss://pumpportal.fun/api/data"
SUBSCRIPTION_METHOD = "subscribeNewToken"
REDIS_CHANNEL = "new_tokens"

@dataclass
class TokenEvent:
    """Represents a structured token event."""
    signature: str
    mint: str
    trader_public_key: str
    transaction_type: str
    initial_buy: float
    sol_amount: float
    bonding_curve_key: str
    v_tokens_in_curve: float
    v_sol_in_curve: float
    market_cap_sol: float
    name: str
    symbol: str
    uri: str
    pool: str
    timestamp: float

    @staticmethod
    def from_message(data: Dict[str, Any]) -> Optional["TokenEvent"]:
        """Parses raw message data into a TokenEvent."""
        try:
            return TokenEvent(
                signature=data["signature"],
                mint=data["mint"],
                trader_public_key=data["traderPublicKey"],
                transaction_type=data["txType"],
                initial_buy=data["initialBuy"],
                sol_amount=data["solAmount"],
                bonding_curve_key=data["bondingCurveKey"],
                v_tokens_in_curve=data["vTokensInBondingCurve"],
                v_sol_in_curve=data["vSolInBondingCurve"],
                market_cap_sol=data["marketCapSol"],
                name=data["name"],
                symbol=data["symbol"],
                uri=data["uri"],
                pool=data["pool"],
                timestamp=datetime.now(timezone.utc).isoformat(),  # Add a timestamp (UTC, iso format)
            )
        except KeyError as e:
            logger.error(f"Missing required field in message: {e}")
            return None

async def connect_and_listen():
    """Connects to the Solana WebSocket and listens for new token creation events."""
    while True:
        try:
            logger.info("Connecting to Solana WebSocket...")
            async with websockets.connect(SOLANA_WEBSOCKET_URL) as websocket:
                logger.info("Connection established. Subscribing to new token events...")

                # Send subscription message
                subscription_message = {
                    "method": SUBSCRIPTION_METHOD
                }
                await websocket.send(json.dumps(subscription_message))

                # Wait for subscription confirmation
                response = await websocket.recv()
                response_data = json.loads(response)

                if response_data.get("message") == "Successfully subscribed to token creation events.":
                    logger.info("Subscription successful. Listening for new tokens...")
                else:
                    raise HTTPException(status_code=500, detail="Subscription failed.")

                # Listen for incoming token creation messages
                async for message in websocket:
                    await process_message(message)

        except websockets.ConnectionClosed as e:
            logger.error(f"WebSocket connection closed: {e.code} - {e.reason}")
            logger.info("Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.info("Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

async def process_message(message: str):
    """Processes a raw message, parses it, and publishes it to Redis."""
    try:
        # Parse the incoming JSON message
        data = json.loads(message)
        token_event = TokenEvent.from_message(data)

        if not token_event:
            logger.error("Failed to parse token event.")
            return

        # Log the parsed token event
        logger.info(f"New Token : {token_event.symbol} ({token_event.name}) | {token_event.mint}")

        # Publish the token event to Redis
        await publish_to_redis(REDIS_CHANNEL, token_event.__dict__)

    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON message: {message}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

@router.on_event("startup")
async def start_listener():
    """Starts the WebSocket listener when the FastAPI application starts."""
    asyncio.create_task(connect_and_listen())
