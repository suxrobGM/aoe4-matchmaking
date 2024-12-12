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

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            profile_id=data["profile_id"],
            name=data["name"],
            rank=data["rank"],
            rating=data["rating"],
            games_count=data["games_count"],
            wins_count=data["wins_count"],
            last_game_at=data["last_game_at"],
            rank_level=data["rank_level"],
            country=data["country"],
            avg_mmr=data["avg_mmr"],
            avg_opp_mmr=data["avg_opp_mmr"],
            avg_game_length=data["avg_game_length"],
            common_civ=data["common_civ"],
            win_rate=data["win_rate"],
            input_type=data["input_type"]
        )
