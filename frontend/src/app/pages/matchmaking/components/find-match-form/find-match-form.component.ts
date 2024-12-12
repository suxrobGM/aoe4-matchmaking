import {Component, signal} from "@angular/core";
import {Card} from "primeng/card";
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from "@angular/forms";
import {CommonModule} from "@angular/common";
import {FloatLabel} from "primeng/floatlabel";
import {InputTextModule} from "primeng/inputtext";
import {ButtonModule} from "primeng/button";
import {ApiService, ToastService} from "@/core/services";
import {PairPlayersDto} from "@/core/models";

@Component({
  selector: "app-find-match-form",
  imports: [
    CommonModule,
    ButtonModule,
    Card,
    ReactiveFormsModule,
    FloatLabel,
    InputTextModule,
  ],
  templateUrl: "./find-match-form.component.html",
})
export class FindMatchFormComponent {
  public readonly isLoading = signal(false);
  public readonly pairPlayerData = signal<PairPlayersDto | null>(null);
  public readonly form: FormGroup<FindMatchForm>;

  constructor(
    private readonly apiService: ApiService,
    private readonly toastService: ToastService
  ) {
    this.form = new FormGroup({
      playerId: new FormControl(0, {validators: Validators.required}),
    });
  }

  findMatch() {
    const {playerId} = this.form.value;

    if (!playerId) {
      return;
    }

    this.isLoading.set(true);
    this.pairPlayerData.set(null);

    this.apiService.findMatch(playerId).subscribe((result) => {
      if (result.success && result.data) {
        this.pairPlayerData.set(result.data);
      } else {
        this.toastService.showError(`Failed to find match: ${result.error}`);
      }

      this.isLoading.set(false);
    });
  }
}

interface FindMatchForm {
  playerId: FormControl<number | null>;
}
