# Current manuscript: focused content revision (2026-09-16)

[Current PDF](paper/latex/facepot/main.pdf): 21 total pages, 9 main-text pages. [Revision details](reviews/current/focused_curation_20260916/REVISION_ZH.md). Six main sections and four scientific appendices; Fig1 unchanged and Fig2 presents the two independent matched studies. Original results and adverse findings remain intact. No new training. Entries below describe historical revisions.

# Completed research: long-budget and partition robustness (2026-09-16)

**Campaign closed after its final failed development gate.** [Chinese report and recommendation](experiments/threshold_longrun/research/AUTO_RESEARCH_REPORT_ZH.md). No strong BCE advantage or new confirmed improvement was established. All 1,152 scientific optimizer trajectories are complete; cumulative occupation is 6,720.884 / 14,400 seconds. The simple-intervention stopping rule was reached before the time cap. No training is active.

The three-objective long-budget study has completed 648 development and 120 confirmation fits of 6,000 updates. [Results and failed strong-BCE gate](experiments/threshold_longrun/research/ROUND0_RESULTS.md), [independent claim review](experiments/threshold_longrun/research/ROUND0_CLAIM_REVIEW.md), and [research contract](experiments/threshold_longrun/research/CAMPAIGN.md). Brier beats Mean-MSE on both synthetic tasks after correction and beats BCE on ReLU; no Digits comparison passes correction. The paper now reports these ranking changes prominently. The historical frozen studies remain unchanged.

All five development screens fail their gates ([schedule](experiments/threshold_schedule_screen/work/SCREEN_REPORT.md), [SPO](experiments/threshold_longrun/research/SPO_SCREEN_RESULTS.md), [smoothing](experiments/threshold_longrun/research/SMOOTHING_SCREEN_RESULTS.md), [EMA](experiments/threshold_longrun/research/EMA_SCREEN_RESULTS.md), [mean blend](experiments/threshold_longrun/research/MEANBLEND_SCREEN_RESULTS.md)). Their saved models and exact decisions replay successfully; none proceeds to confirmation. Mean blending improves only .119358 pp and harms Digits BCE by1.757813 pp. The predeclared stopping rule ends this sequence of small adjustments. These exploratory studies have no evaluation access or significance claims. See the [independent campaign assessment](experiments/threshold_longrun/research/CAMPAIGN_REASSESSMENT_REVIEW.md). No strong advantage or ICLR acceptance is promised.

- [Current paper](paper/latex/facepot/main.pdf): 9 main-text pages, 24 total (long-budget revision).
- [Long-budget raw summary](experiments/threshold_longrun/round0/summary.json) and [complete analysis](experiments/threshold_longrun/round0/analysis.json).
- The prior 12.8 MB Warcraft ZIP below is an archived snapshot; it does not contain this new revision.

# Earlier manuscript snapshot: completed Warcraft evidence (2026-09-16)

Active paper: **Learning Costs for Decisions: Matching Targets Before Comparing Losses**. The completed Warcraft extension adds 27 development and 30 confirmation runs, with longer training and independent saved-path verification. Its exact error ordering is significant, but nearly all errors are nominal-cost ties and regret is tiny. This is a bounded result, not a benchmark-record or convergence claim.

- [Current paper](paper/latex/facepot/main.pdf): main text 9 pages, 21 total.
- [Revision and evidence interpretation](reviews/current/warcraft_results_revision_20260916/REVISION_ZH.md).
- [Independent result-to-claim review](reviews/current/warcraft_results_revision_20260916/CLAIM_GATE.md).
- [Study status](experiments/warcraft_matched/work_full/status.json).
- [Compact private review ZIP](artifacts/packages/ICLR_Warcraft_Results_Revision_20260916/ICLR_Warcraft_Results_Revision_20260916.zip): 12.8 MB, including saved predictions and portable audit; checkpoints and map images omitted.

Earlier entries below are archived descriptions, not the current paper status.

# Archived visual revision: Figure1 (2026-09-14)

[Editable Figure1 and updated paper](artifacts/packages/Figure1_20260914/Figure1_Editable_and_Paper.zip). The current paper has17 total pages, with conclusion still on8; the first figure is on2. Original storyline deliverables below remain archived snapshots.

# Current entry: matched-threshold storyline revision (2026-09-14)

The active paper is **Learning Costs for Decisions: Separating Target Granularity from Scoring Rules**. The completed 540-development/180-confirmation Brier/BCE/mean-MSE study is central; old15-method/24-test evidence remains separately labeled. No training was added during this revision.

- [Current paper](paper/latex/facepot/main.pdf)
- [Narrative and submission scope](reviews/current/storyline_revision_20260914/STORYLINE_ZH.md)
- [Review dispositions](reviews/current/storyline_revision_20260914/REVIEW_LEDGER.md)
- [Anonymous compact paper/code supplement](artifacts/packages/ICLR_Storyline_Revision_20260914/ICLR_Anonymous_Paper_and_Supplement_20260914.zip)

Validation:16 total pages, conclusion on8, statements through9; all fonts embedded, no undefined citations or overfull boxes. Anonymous selected sources compile separately, and all9 registered tests reproduce from packaged integer seed counts. This is a bounded analytical-study CONDITIONAL GO, not guaranteed acceptance. Original archives remain unchanged; compact supplement omits raw models/per-context arrays and discloses that scope.

## Prior entry (2026-09-12)

# Current entry: independently audited decision-learning extension

See [current team review](DECISION_EXTENSION_TEAM_REVIEW_20260912.md), [revised paper](paper/latex/facepot/main.pdf), and [extension audit](reviews/r049/decision_extension_audit_20260912/START_HERE.md).

The extension's supplied primary statistics reproduce. The revision distinguishes matched-head objectives from encoding, fixes the reproduction entry in a separate wrapper, and retains adverse prior results. No new scientific training was launched in this review.

## Previous team review

See [latest review entry](reviews/current/team_optimization_20260912/START_HERE.md), [protocol](experiments/allocation_regularization_v2/protocol.json), and [status](experiments/allocation_regularization_v2/STATUS.json).

The earlier scientific studies remain sealed. The new fixed-alpha study has 375 completed runs; CE outperformed both predeclared alternatives. Computational acceleration and numerical/I/O fixes were separately verified. Historical intermediate manuscript material was removed from compilation. The unrelated ZIP remains excluded.
