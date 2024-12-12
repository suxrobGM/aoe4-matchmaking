
import pandas as pd
from core import get_model_path, PagedResult, PagedQuery
from models import PlayerDto

class PlayerService:
    players_df: pd.DataFrame
    is_data_loaded = False

    def load_players(self):
        if self.is_data_loaded:
            return

        self.players_df = pd.read_csv(get_model_path("clustered_players.csv"))
        self.is_data_loaded = True

    def get_player(self, player_id: int) -> PlayerDto | None:
        self.load_players() # Ensure data is loaded
        player = self.players_df[self.players_df["profile_id"] == player_id].iloc[0]

        if player is None:
            return None

        return PlayerDto(
            profile_id=player["profile_id"],
            name=player["name"],
            rank=player["rank"],
            rating=player["rating"],
            games_count=player["games_count"],
            wins_count=player["wins_count"],
            last_game_at=player["last_game_at"],
            rank_level=player["rank_level"],
            country=player["country"],
            avg_mmr=player["avg_mmr"],
            avg_opp_mmr=player["avg_opp_mmr"],
            avg_game_length=player["avg_game_length"],
            common_civ=player["common_civ"],
            win_rate=player["win_rate"]
        )
    
    def get_players(self, paged_query: PagedQuery) -> PagedResult[PlayerDto]:
        self.load_players() # Ensure data is loaded
        filtered_df = self.players_df

        if paged_query.filter:
            filtered_df = filtered_df.fillna({"name": ""})
            filter_condition = f"name.str.contains('{paged_query.filter}')"
            filtered_df = filtered_df.query(filter_condition)

        items_count = len(filtered_df)
        page_index = paged_query.page - 1

        if paged_query.order_by:
            filtered_df = filtered_df.sort_values(by=paged_query.order_by)

        start = page_index * paged_query.page_size
        end = start + paged_query.page_size
        page_data = filtered_df.iloc[start:end]

        players = [
            PlayerDto(
                profile_id=player["profile_id"],
                name=player["name"],
                rank=player["rank"],
                rating=player["rating"],
                games_count=player["games_count"],
                wins_count=player["wins_count"],
                last_game_at=player["last_game_at"],
                rank_level=player["rank_level"],
                country=player["country"],
                avg_mmr=player["avg_mmr"],
                avg_opp_mmr=player["avg_opp_mmr"],
                avg_game_length=player["avg_game_length"],
                common_civ=player["common_civ"],
                win_rate=player["win_rate"]
            )
            for _, player in page_data.iterrows()
        ]

        return PagedResult.succeed(
            data=players,
            page_index=page_index,
            page_size=paged_query.page_size,
            items_count=items_count
        )
