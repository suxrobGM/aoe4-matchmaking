import {PlayerDto} from "./player.dto";

export interface PairPlayersDto {
  player1: PlayerDto;
  player2: PlayerDto;
  player1WinProb: number;
}
