import logging
import numpy as np
import pandas as pd
from joblib import load
from xgboost import XGBClassifier
from core import get_model_path

class Matchmaker:
    classifier_model: XGBClassifier
    players_df: pd.DataFrame
    is_model_loaded = False
    players_queue: list[int]
    logger = logging.getLogger()

    def load_models(self) -> None:
        """
        Load the classifier model and the players DataFrame from disk.
        """
        if self.is_model_loaded:
            return

        self.classifier_model = load(get_model_path("classifier_model.joblib"))
        self.players_df = pd.read_csv(get_model_path("clustered_players.csv"))
        self.players_queue = self.players_df["profile_id"].tolist() # TODO: Initialize queue with all players, for real scenario this should be empty
        self.is_model_loaded = True
        self.logger.info("Models loaded successfully")
        self.logger.info(f"Players data shape: {self.players_df.shape}")

    def add_player_to_queue(self, player_id: int) -> bool:
        """
        Add a player to the queue.
        Args:
            player_id: The profile ID of the player to add to the queue.
        Returns:
            True if the player was successfully added to the queue, False otherwise.
        """
        # Check if player exists
        player_exists = (self.players_df["profile_id"] == player_id).any()

        if not player_exists:
            self.logger.error(f"Player {player_id} not found in the database")
            return False
        
        # Add player to queue
        self.players_queue.append(player_id)
        self.logger.info(f"Player {player_id} added to queue")
        return True
    
    def remove_player_from_queue(self, player_id: int) -> bool:
        """
        Remove a player from the queue.
        Args:
            player_id: The profile ID of the player to remove from the queue.
        Returns:
            True if the player was successfully removed from the queue, False otherwise.
        """
        try:
            self.players_queue.remove(player_id)
            self.logger.info(f"Player {player_id} removed from queue")
            return True
        except ValueError:
            self.logger.error(f"Player {player_id} not found in the queue")
            return False

    def predict_match_outcome(self, player_id_A: int, player_id_B: int) -> float:
        """
        Predict the probability that player A wins against player B.
        Args:
            player_id_A: The profile ID of player A.
            player_id_B: The profile ID of player B.
        Returns:
            The probability that player A wins against player B.
        """
        if not self.is_model_loaded:
            raise ValueError("Models are not loaded. Call load_models() first.")
        
        self.logger.info(f"Predicting match outcome between {player_id_A} and {player_id_B}")

        # Retrieve players info
        pA: pd.Series = self.players_df.loc[self.players_df["profile_id"] == player_id_A].squeeze()
        pB: pd.Series = self.players_df.loc[self.players_df["profile_id"] == player_id_B].squeeze()
        
        # Extract features
        X_match = self._get_match_features(pA, pB)
        
        # Predict probability that A wins
        prob = self.classifier_model.predict_proba(X_match)[:,1]
        self.logger.info(f"Predicted probability that {pA["name"]} (ID: {player_id_A}) wins against {pB["name"]} (ID: {player_id_B}): {prob}")
        return prob
    
    def find_match_for_player(self, profile_id: int, target=0.5, tolerance=0.1) -> dict:
        """
        Find a match for a player in the queue.
        Args:
            profile_id: The profile ID of the player for whom to find a match.
            target: The target probability that the opponent will win.
            tolerance: The maximum difference between the target probability and the predicted probability.
        Returns:
            The opponent player data if a match is found, None otherwise.
        """
        if not self.is_model_loaded:
            raise ValueError("Models are not loaded. Call load_models() first.")

        # Find player's cluster
        player: pd.Series = self.players_df.loc[self.players_df["profile_id"] == profile_id].squeeze()
        player_cluster: int = player["cluster"]
        self.logger.info(f"Trying to match player '{player["name"]}' (ID: {profile_id}) from cluster {player_cluster}")
        
        # Collect candidates from the queue in the same cluster (excluding the player itself)
        candidates = [pid for pid in self.players_queue if pid != profile_id]
        cluster_candidates = self.players_df.loc[self.players_df["profile_id"].isin(candidates) & (self.players_df["cluster"] == player_cluster)]
        
        # If no candidates in same cluster, we can relax and consider all candidates
        if cluster_candidates.empty:
            cluster_candidates = self.players_df.loc[self.players_df["profile_id"].isin(candidates)]
        
        # Shuffle the candidates to avoid always picking the same one
        cluster_candidates = cluster_candidates.sample(frac=1)

        # Attempt to find the best partner
        best_partner: dict | None = None
        best_diff = float("inf")
        last_prob: float | None = None # Store the last probability for logging

        for _, opponent in cluster_candidates.iterrows():
            self.logger.info(f"Trying to match '{player["name"]}' (ID: {profile_id}) with '{opponent["name"]}' (ID: {opponent["profile_id"]})")
            prob = self.predict_match_outcome(profile_id, opponent["profile_id"])
            diff = abs(prob - target)

            if diff < best_diff and diff <= tolerance:
                best_diff = diff
                best_partner = opponent.to_dict()
                last_prob = prob
        
        if best_partner is not None:
            self.logger.info(f"Matched '{player["name"]}' (ID: {profile_id}) with '{best_partner["name"]}' (ID: {best_partner["profile_id"]}) using cluster")
            self.logger.info(f"The probability that {player["name"]} wins against {best_partner["name"]} is {last_prob}")
        else:
            # If no perfect match found, use ELO rating to find an opponent
            self.logger.info(f"No perfect match found for '{player["name"]}' (ID: {profile_id}). Trying to find an opponent using ELO rating")
            best_partner = self._find_opponent_using_elo(profile_id)

        # Remove matched players from the queue
        self.remove_player_from_queue(profile_id)
        self.remove_player_from_queue(best_partner["profile_id"])
        return {
            "player_1": player.to_dict(),
            "player_2": best_partner,
            "player_1_win_prob": last_prob
        }
            
    def queue_length(self) -> int:
        """
        Get the number of players in the queue waiting for a match.
        """
        return len(self.players_queue)
    
    def _find_opponent_using_elo(self, player_id: int) -> dict:
        """
        Find an opponent for a player with the closest ELO rating.
        Args:
            player_id: The profile ID of the player for whom to find an opponent.
        Returns:
            The profile ID of the player to match with.
        """
        # Retrieve player's ELO rating
        player: pd.Series = self.players_df.loc[self.players_df["profile_id"] == player_id].squeeze()
        player_elo: float = player["rating_A"]

        # Find the closest ELO rating to the player's ELO rating
        opponents = self.players_df.loc[self.players_df["profile_id"] != player_id]
        closest_opponent = opponents.iloc[(opponents["rating_A"] - player_elo).abs().argsort()[:1]]
        self.logger.info(f"Matched '{player["name"]}' (ID: {player_id}) with '{closest_opponent["name"].values[0]}' (ID: {closest_opponent["profile_id"].values[0]}) using ELO rating")
        return closest_opponent.to_dict()

    def _get_match_features(self, pA: pd.Series, pB: pd.Series) -> np.ndarray:
        """
        Extract features for the match prediction model.
        Args:
            pA: The row (Series) from players_df representing player A.
            pB: The row (Series) from players_df representing player B.
        Returns:
            The feature vector for the match prediction model.
        """
        # pA and pB are rows (Series) from players_df representing each player.
        # Extract relevant features as done during training:
        rating_A = pA["rating"]
        rating_B = pB["rating"]
        win_rate_A = pA["win_rate"]
        win_rate_B = pB["win_rate"]
        games_count_A = pA["games_count"]
        games_count_B = pB["games_count"]
        wins_count_A = pA["wins_count"]
        wins_count_B = pB["wins_count"]
        rank_level_encoded_A = pA["rank_level_encoded"]
        rank_level_encoded_B = pB["rank_level_encoded"]
        avg_mmr_diff_10_A = pA["avg_mmr_diff_10"]
        avg_mmr_diff_10_B = pB["avg_mmr_diff_10"]
        avg_mmr_diff_50_A = pA["avg_mmr_diff_50"]
        avg_mmr_diff_50_B = pB["avg_mmr_diff_50"]
        avg_mmr_A = pA["avg_mmr"]
        avg_mmr_B = pB["avg_mmr"]
        avg_opp_mmr_A = pA["avg_opp_mmr"]
        avg_opp_mmr_B = pB["avg_opp_mmr"]
        avg_game_length_A = pA["avg_game_length"]
        avg_game_length_B = pB["avg_game_length"]
        
        # Return feature vector in the same order as training
        features = np.array([[
            rating_A, win_rate_A, games_count_A, wins_count_A, 
            rank_level_encoded_A, avg_mmr_diff_10_A, avg_mmr_diff_50_A, avg_mmr_A, 
            avg_opp_mmr_A, avg_game_length_A, rating_B, win_rate_B,
            games_count_B, wins_count_B, rank_level_encoded_B, avg_mmr_diff_10_B, 
            avg_mmr_diff_50_B, avg_mmr_B, avg_opp_mmr_B, avg_game_length_B
        ]])
        return features
