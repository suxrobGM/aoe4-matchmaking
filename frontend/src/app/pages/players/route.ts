import {Routes} from "@angular/router";

export const playersRoute: Routes = [
  {
    path: "players",
    loadComponent: () =>
      import("./players.component").then((m) => m.PlayersComponent),
  },
];
