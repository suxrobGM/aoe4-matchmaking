from core import PydanticBaseModel

class PredictMatchOutcomeDto(PydanticBaseModel):
    player_1: int
    player_2: int
