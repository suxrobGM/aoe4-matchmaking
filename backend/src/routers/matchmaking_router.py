
from fastapi import APIRouter
from core.result import Result, ResultWithData
from matchmaking import Matchmaker
from models import PlayerIdDto, PredictMatchOutcomeDto, PairPlayersDto
from models.player import PlayerDto

matchmaking_router = APIRouter(prefix="/matchmaking", tags=["matchmaking"])
router = matchmaking_router

matchmaker = Matchmaker()
matchmaker.load_models()
    
@router.post("/queue")
def add_player_to_queue(payload: PlayerIdDto) -> Result:
    """
    Add a player to the matchmaking queue.
    """
    success = matchmaker.add_player_to_queue(payload.player_id)
    return Result.succeed() if success else Result.fail("Player not found")

@router.post("/queue/remove")
def remove_player_from_queue(payload: PlayerIdDto) -> Result:
    """
    Remove a player from the matchmaking queue.
    """
    success = matchmaker.remove_player_from_queue(payload.player_id)
    return Result.succeed() if success else Result.fail("Player not found")

@router.post("/predict")
def predict_match_outcome(payload: PredictMatchOutcomeDto) -> ResultWithData[float]:
    """
    Predict the outcome of a match between two players. 
    Return the probability that player 1 wins against player 2.
    """
    try:
        probability = matchmaker.predict_match_outcome(payload.player_1, payload.player_2)
        return ResultWithData.succeed(probability)
    except ValueError as e:
        return ResultWithData.fail(str(e))

@router.post("/pair")
def find_match(payload: PlayerIdDto) -> ResultWithData[PairPlayersDto]:
    """
    Pair a player with an opponent and form a match. 
    Return the opponent's data.
    """
    match_data = matchmaker.find_match_for_player(payload.player_id)
    
    if match_data:
        dto = PairPlayersDto(
            player_1=PlayerDto.from_dict(match_data["player_1"]),
            player_2=PlayerDto.from_dict(match_data["player_2"]),
            player_1_win_prob=match_data["player_1_win_prob"]
        )
        return ResultWithData.succeed(dto)

    return ResultWithData.fail("No match found")
