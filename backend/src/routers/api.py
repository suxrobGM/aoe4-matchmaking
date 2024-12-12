from fastapi import APIRouter
from .matchmaking_router import matchmaking_router
from .players_router import players_router

api_router = APIRouter(prefix="/api")
api_router.include_router(matchmaking_router)
api_router.include_router(players_router)
