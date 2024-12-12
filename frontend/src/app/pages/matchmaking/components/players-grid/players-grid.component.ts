import {CommonModule} from "@angular/common";
import {Component, signal} from "@angular/core";
import {Card} from "primeng/card";
import {TableLazyLoadEvent, TableModule} from "primeng/table";
import {InputTextModule} from "primeng/inputtext";
import {PagedQuery, PlayerDto} from "@/core/models";
import {ApiService, ToastService} from "@/core/services";

@Component({
  selector: "app-players-grid",
  imports: [CommonModule, TableModule, Card, InputTextModule],
  templateUrl: "./players-grid.component.html",
})
export class PlayersGridComponent {
  public readonly players = signal<PlayerDto[]>([]);
  public readonly isLoading = signal(false);
  public readonly isPredictingMatch = signal(false);
  public readonly isFindingMatch = signal(false);
  public readonly totalRecords = signal(0);
  public readonly first = signal(0);

  constructor(
    private readonly apiService: ApiService,
    private readonly toastService: ToastService
  ) {}

  searchPlayer(event: Event) {
    const searchValue = (event.target as HTMLInputElement).value;
    this.handlePlayerSearch({filter: searchValue, page: 1, pageSize: 10});
  }

  load(event: TableLazyLoadEvent) {
    const first = event.first ?? 1;
    const rows = event.rows ?? 10;
    const page = first / rows + 1;
    const sortField = this.apiService.parseSortProperty(
      event.sortField as string,
      event.sortOrder
    );

    this.handlePlayerSearch({
      page: page,
      pageSize: rows,
      orderBy: sortField,
    });
  }

  formatDate(dateStr: string) {
    return new Date(dateStr);
  }

  private handlePlayerSearch(params: PagedQuery) {
    this.isLoading.set(true);

    this.apiService.getPlayers(params).subscribe((result) => {
      if (result.success && result.data) {
        this.players.set(result.data);
        this.totalRecords.set(result.pageSize * result.pagesCount);
      } else {
        this.toastService.showError(`Failed to fetch players: ${result.error}`);
      }

      this.isLoading.set(false);
    });
  }
}
