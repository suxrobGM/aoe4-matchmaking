import {Routes} from "@angular/router";

export const matchmakingRoutes: Routes = [
  {
    path: "",
    loadComponent: () =>
      import("./matchmaking.component").then((m) => m.MatchmakingComponent),
  },
];
