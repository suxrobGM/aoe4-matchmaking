export interface PlayerDto {
  profileId: number;
  name: string;
  rank: number;
  rating: number;
  gamesCount: number;
  winsCount: number;
  lastGameAt: string;
  rankLevel: string;
  country: string;
  avgMmr: number;
  avgOppMmr: number;
  avgGameLength: number;
  commonCiv: string;
  winRate: number;
  inputType: string;
}
