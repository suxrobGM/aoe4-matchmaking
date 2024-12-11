from core import PydanticBaseModel
from .player import PlayerDto

class PairPlayersDto(PydanticBaseModel):
    player_1: PlayerDto
    player_2: PlayerDto
    player_1_win_prob: float
