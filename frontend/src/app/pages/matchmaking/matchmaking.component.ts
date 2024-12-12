import {Component} from "@angular/core";
import {
  FindMatchFormComponent,
  PlayersGridComponent,
  PredictMatchFormComponent,
} from "./components";

@Component({
  selector: "app-matchmaking",
  imports: [
    FindMatchFormComponent,
    PredictMatchFormComponent,
    PlayersGridComponent,
  ],
  templateUrl: "./matchmaking.component.html",
})
export class MatchmakingComponent {}
