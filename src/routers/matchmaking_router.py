
from fastapi import APIRouter
from core import PydanticBaseModel
from core.result import Result, ResultWithData
from matchmaking import Matchmaker

matchmaking_router = APIRouter(prefix="/matchmaking", tags=["matchmaking"])
router = matchmaking_router

matchmaker = Matchmaker()
matchmaker.load_models()

class AddPlayerToQueueDto(PydanticBaseModel):
    player_id: int

class PredictMatchOutcomeDto(PydanticBaseModel):
    player_1: int
    player_2: int

class FindMatchDto(PydanticBaseModel):
    player_id: int

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
        return Result.fail(str(e))
    
@router.post("/queue")
def add_player_to_queue(payload: AddPlayerToQueueDto) -> Result:
    """
    Add a player to the matchmaking queue.
    """
    success = matchmaker.add_player_to_queue(payload.player_id)
    return Result.succeed() if success else Result.fail("Player not found")

@router.post("/pair")
def find_match(payload: FindMatchDto) -> ResultWithData[str]:
    """
    Pair a player with an opponent and form a match. 
    Return the opponent's ID.
    """
    opponent = matchmaker.find_match_for_player(payload.player_id)
    return Result.succeed(opponent) if opponent else Result.fail("No match found")

