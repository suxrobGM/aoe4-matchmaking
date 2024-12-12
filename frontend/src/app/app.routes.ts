import {Routes} from "@angular/router";
import {uploadRoutes} from "@/pages/upload";
import {playersRoute} from "@/pages/players";

export const routes: Routes = [...uploadRoutes, ...playersRoute];
