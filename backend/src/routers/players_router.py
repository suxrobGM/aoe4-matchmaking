
from typing import Annotated
from fastapi import APIRouter, Depends
from core import PagedQuery, PagedResult, ResultWithData
from models import PlayerDto
from services import PlayerService

players_router = APIRouter(prefix="/players", tags=["player"])
router = players_router

player_service = PlayerService()
    
@router.get("/{player_id}")
def get_player_by_id(player_id: int) -> ResultWithData[PlayerDto]:
    """
    Get a player by ID.
    """
    player = player_service.get_player(player_id)

    if player is None:
        return ResultWithData.fail("Player not found")
    
    return ResultWithData.succeed(player)

@router.get("/")
def get_players_paged(paged_query: Annotated[PagedQuery, Depends()]) -> PagedResult[PlayerDto]:
    """
    Get a list of players with pagination.
    """
    paged_result = player_service.get_players(paged_query)
    return paged_result
