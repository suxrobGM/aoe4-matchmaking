import {Injectable, OnDestroy} from "@angular/core";
import {Observable} from "rxjs";
import {Result} from "@/core/models";

@Injectable({
  providedIn: "root",
})
export class ApiService {
  private apiUrl = "http://localhost:8000/api";
}
