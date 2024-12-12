import {Component, signal} from "@angular/core";
import {CommonModule} from "@angular/common";
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from "@angular/forms";
import {ButtonModule} from "primeng/button";
import {Card} from "primeng/card";
import {FloatLabel} from "primeng/floatlabel";
import {InputTextModule} from "primeng/inputtext";
import {ApiService, ToastService} from "@/core/services";

@Component({
  selector: "app-predict-match-form",
  imports: [
    CommonModule,
    ButtonModule,
    Card,
    ReactiveFormsModule,
    FloatLabel,
    InputTextModule,
  ],
  templateUrl: "./predict-match-form.component.html",
})
export class PredictMatchFormComponent {
  public readonly isLoading = signal(false);
  public readonly predictedMatchProb = signal<number | null>(null);
  public readonly form: FormGroup<PredictMatchOutcomeForm>;

  constructor(
    private readonly apiService: ApiService,
    private readonly toastService: ToastService
  ) {
    this.form = new FormGroup({
      player1: new FormControl(0, {validators: Validators.required}),
      player2: new FormControl(0, {validators: Validators.required}),
    });
  }

  predictMatchOutcome() {
    const {player1, player2} = this.form.value;

    if (!player1 || !player2) {
      return;
    }

    this.isLoading.set(true);
    this.predictedMatchProb.set(null);

    this.apiService
      .predictMatchOutcome({player1, player2})
      .subscribe((result) => {
        if (result.success && result.data) {
          this.predictedMatchProb.set(result.data);
        } else {
          this.toastService.showError(
            `Failed to predict match outcome: ${result.error}`
          );
        }

        this.isLoading.set(false);
      });
  }
}

interface PredictMatchOutcomeForm {
  player1: FormControl<number | null>;
  player2: FormControl<number | null>;
}
