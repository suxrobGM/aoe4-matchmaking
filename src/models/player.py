from core import PydanticBaseModel

class PlayerDto(PydanticBaseModel):
    profile_id: int
    name: str
    rank: int
    rating: float
    games_count: int
    wins_count: int
    last_game_at: str
    rank_level: str
    country: str
    avg_mmr: float
    avg_opp_mmr: float
    avg_game_length: float
    common_civ: str
    win_rate: float
    input_type: str
