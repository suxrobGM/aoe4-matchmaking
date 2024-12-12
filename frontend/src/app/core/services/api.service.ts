import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {catchError, Observable, of} from "rxjs";
import {
  PagedQuery,
  PagedResult,
  PairPlayersDto,
  PlayerDto,
  PlayerIdDto,
  PredictMatchOutcomeDto,
  Result,
} from "@/core/models";
import {ToastService} from "./toast.service";

@Injectable({
  providedIn: "root",
})
export class ApiService {
  private readonly baseUrl = "http://localhost:8000/api";

  constructor(
    private readonly http: HttpClient,
    private readonly toastService: ToastService
  ) {}

  addPlayerToQueue(playerId: number): Observable<Result> {
    return this.post<Result, PlayerIdDto>("/matchmaking/queue", {
      playerId,
    });
  }

  removePlayerFromQueue(playerId: number): Observable<Result> {
    return this.post<Result, PlayerIdDto>("/matchmaking/queue/remove", {
      playerId,
    });
  }

  predictMatchOutcome(
    payload: PredictMatchOutcomeDto
  ): Observable<Result<number>> {
    return this.post<Result<number>, PredictMatchOutcomeDto>(
      "/matchmaking/predict",
      payload
    );
  }

  findMatch(playerId: number): Observable<Result<PairPlayersDto>> {
    return this.post<Result<PairPlayersDto>, PlayerIdDto>(`/matchmaking/pair`, {
      playerId,
    });
  }

  getPlayerById(playerId: number): Observable<Result<PlayerDto>> {
    return this.get<Result<PlayerDto>>(`/players/${playerId}`);
  }

  getPlayers(query: PagedQuery): Observable<PagedResult<PlayerDto>> {
    return this.get<PagedResult<PlayerDto>>(
      `/players?${this.stringfyQuery(query)}`
    );
  }

  parseSortProperty(
    sortField?: string | null,
    sortOrder?: number | null
  ): string {
    if (!sortOrder) {
      sortOrder = 1;
    }

    if (!sortField) {
      sortField = "";
    }

    return sortOrder <= -1 ? `-${sortField}` : sortField;
  }

  private get<TResponse>(endpoint: string): Observable<TResponse> {
    return this.http
      .get<TResponse>(this.baseUrl + endpoint)
      .pipe(catchError((err) => this.handleError(err)));
  }

  private post<TResponse, TBody>(
    endpoint: string,
    body: TBody
  ): Observable<TResponse> {
    return this.http
      .post<TResponse>(this.baseUrl + endpoint, body)
      .pipe(catchError((err) => this.handleError(err)));
  }

  private put<TResponse, TBody>(
    endpoint: string,
    body: TBody
  ): Observable<TResponse> {
    return this.http
      .put<TResponse>(this.baseUrl + endpoint, body)
      .pipe(catchError((err) => this.handleError(err)));
  }

  private delete<TResponse>(endpoint: string): Observable<TResponse> {
    return this.http
      .delete<TResponse>(this.baseUrl + endpoint)
      .pipe(catchError((err) => this.handleError(err)));
  }

  private stringfyQuery(query: PagedQuery): string {
    const searchParams = new URLSearchParams();
    searchParams.set("page", query.page.toString());
    searchParams.set("pageSize", query.pageSize.toString());

    if (query.orderBy) {
      searchParams.set("orderBy", query.orderBy);
    }

    if (query.filter) {
      searchParams.set("filter", query.filter);
    }

    return searchParams.toString();
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private handleError(responseData: any): Observable<any> {
    const errorMessage = responseData.error?.error ?? responseData.error;

    this.toastService.showError(errorMessage);
    console.error(errorMessage ?? responseData);
    return of({error: errorMessage, success: false});
  }
}
