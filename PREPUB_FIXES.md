# Fixes from the prepublication review

This branch (`paper-prepub-fixes`) starts from `989ef7f` (`paper-review-fixes`). It applies the fixes proposed in
`research/prepub_review/REPORT.md`, which is on branch `paper-prepub-review` of this repository. The `.tex` files are
regenerated from the generators and ledgers; none was edited by hand.

## Build status (run on this branch)

| step | result |
|---|---|
| `python3 spectrepaper.py --selftest` | all checks pass |
| `python3 spectre_supplement.py --selftest` | all checks pass (one new check: the count of numbered Facts) |
| `make facts` | passes: spectrefacts 62 facts, monotilefacts 8 checks, chair44facts 43 checks, chair44_hull and chair44_lines tests (pyCICY not installed, so its optional cross-check was skipped) |
| `make lean` | `SpectreFacts.lean`: 67 theorems, kernel accepted (Lean 4.33.1) |
| `boundary_certificate/check_spectre_fractal.py` | passes; output in `out_spectre_fractal.txt` |
| `boundary_certificate/spectre_window.py` | passes; output in `out_spectre_window.txt` |
| `pdflatex` ×3 | `spectre_substrate.pdf` 31 pages, `spectre_supplement.pdf` 4 pages; no undefined references, no "may have changed", no overfull boxes in either |

## Major

**M1. Theorem 3 (window).** Fixed with option (b) of the report, restating the theorem as what is proved. The proof is
now self-contained and no longer cites BGMS for regularity.
- **Positive area and measure-disjointness, now proved.**
  - The certificate now asserts that no contact type is the identity. The nearest candidate is at distance 4.11.
  - Pieces of depth m within δλ⁻ᵐ of each other have a live type. So a disc of radius δλ⁻ᵐ/2 meets at most 1193
    pieces.
  - The mass distribution principle then gives positive area.
  - Measure-disjointness follows from the Perron argument.
- **The theorem now states:**
  - the seams have box dimension exactly log(√2+√3)/log λ = 1.110977…;
  - the lower box dimension of ∂Z_p(S) is at least that value for all four window types. The certificate now checks
    that the lower bound reaches all four.
- **A new paragraph after the proof says what is missing for ∂W itself:**
  - an upper bound needs the neighbouring windows of a covering of internal space;
  - BGMS's lattice tiling for CASPr would supply this once W is identified with their window;
  - this is not done here.
- The abstract and the conclusion are reworded to match.

**M2. The supplement.**
- The "beyond k=6 the recurrence is a conjecture" paragraph is replaced. It now says that `charpoly` is the one input
  and that `boundary_recurrence` is proved by Theorem 1.
- "Every Fact of the paper — all 71" now reads "ledger entries", with the count of numbered Facts (25) given
  separately.
- `internal_plane` now says the 1.2 is a box count and points to the exact seam value. Its docstring and method say
  the same.
- `chair_hull_theorem` now reads C₂^diag.

**M3. Stale statements.**
- Introduction: "one quoted input and two finite computations".
- Conclusion: one unrefereed input, (R), plus Lemmas 1–2.
- Sec. 5: "for every order (Theorem 1)".
- The box count's patch level: "a level-5 patch; Figure 3 shows level 4".
- Scope paragraph: Lee–Moody [LeeMoody] with [LMS] for the hull.
- Look-back paragraph: the count is c_O G_O(ℓ) + c_G G_G(ℓ), with both glue formulas given, and the Mystic
  convention is stated (with the other convention, the first ratio is 0.368).
- Abstract: "with ratio tending exactly to ν/λ²".

**M4. The 4D paragraph.**
- 1566 is now called Kamenetsky's random-start plateau, and 273 is said to be above his structured-family value of 158.
- The 400-pose cap of the test is stated, and so is the ≤300 cap in Kamenetsky's Theorem B.
- The paper now says that the search records are not part of its build.
- The search code and logs are now in `nd_search/` (copied unchanged from the authors' working repository), with a
  README. The counts are checked against the logs: 4288+4212+4284 = 12,784 assignments in the search and
  2399+3208+3424+3101 = 12,132 evaluations in the annealing. The paper now says 12,132 rather than "about 12,100".
- The claim that the 3D score is minimised exactly by the closed assignments was not verifiable without running the
  external code, so it is removed.

**M5. Lean rebuild.**
- The paper now says that the 162 regenerated reports agree with the published log theorem by theorem, up to the
  namespace prefix, and that the post-build log equals the published one byte for byte.
  - I checked this by fetching `lean/R44/build_axioms.log` at `d53d224` from GitHub. It is identical to
    `committed_axioms_log` in `r44_build_result.json` (53,556 bytes).
- A sentence on statement fidelity is added, and so is one on trusting the compiler.
- `lean_rebuild/README.md`: the old diff-audit row now says that its output was not saved.
- The statement-fidelity claim is now checked by `lean_rebuild/discharge_audit_indep.py`, written for this review
  without importing the project's audit script. Output: `lean_rebuild/out_discharge_audit_indep.txt`.
  - All 67 Proved files differ from the newest delivery containing them only in marked compile-fix hunks.
  - 76 declaration texts differ. All are notation (parentheses, `|x|` to `abs`, `section` to `«section»`, spacing),
    five structure-valued `theorem`s that became `def`s, one delivered `sorry` placeholder replaced by a call to the
    proved theorem of the same statement, or added helper lemmas.
  - The paper now says this, citing the script.
- The misleading comment in `r44_build.py` is corrected.

## Minor

- **m1.** In the proof of Theorem 2:
  - It says which tiling is used: a limit of supertiles re-centred at deep tiles. Their neighbour placements are
    live types.
  - It cites the Spectre paper [SmithEtAl2, Thms 2.2, 5.1] instead of the Hat paper.
  - The lower bound names the boundaries involved.
  - `check_spectre_fractal.py` now asserts that O–O sibling pairs reach the block, so the bound applies to K and not
    only to the Mystic limit.
- **m2.** Lemma 1 uses Kamenetsky's labels (C1)–(C3), with (C2) (tightness of the face rules) stated separately.
- **m3.** `spectre_window.py` now asserts key separation (at least 1.909) in place of the dead `ds` line.
- **m4.** The BGMS paraphrase is corrected. Their value is a Hausdorff dimension, and their remark is about uniformity
  along the boundary.
- **m5.** Fact 24: the ±2 and ±3 sums are bounded, and the ±4 sums grow linearly, so h = 0 there.
- **m6.** Build fixes:
  - `make paper` and `paperfast` run pdflatex three times;
  - `make paper` also builds the supplement;
  - the supplement's 11 overfull boxes are fixed in `facts_appendix`: top-level `\text{}` is set as running text, and
    long filenames may break after underscores;
  - the page count in `REVIEW_FIXES.md` is corrected.
- **m7.** The `boundary_exact` method now cites `boundary_certificate/spectre_exact.py`, the exact recount for k ≤ 6.
  pyCICY is described as optional, and the selftest message is updated to match.
- **m8.** The `SpectreFacts.lean` comment now says that only the two inequalities are proved, not fractality.
  - A first wording of it began a comment line with "theorem", which made the theorem count read 68. The comment is
    rewrapped and the count is back to 67.
- **m9.** The conclusion now says "One further problem remains open".
- **m10.** The supplement's author name now matches the paper: "Brent Hartshorn".
- **m11.** `chair44_data/ATTRIBUTION.md` no longer lists Flicker's paper as a source of the data.
- **m12.** The third implementation of Lemma 2 is now in the repository: `hierarchy_certificate/chair44_blocks_indep.py`,
  with its output and a README section. The paper cites it there instead of the private repository.
- **m13.** The Figure 2 caption now reads "by Theorem 1 they equal the recurrence".
- **Bibliography.** BaakeHat now carries its journal reference: J. Math. Phys. 66 (2025) 092707.

## Not changed

- The upper bound for ∂W (option (a) of the report) is not proved.
  - The internal coordinates of `spectre_window.py` are a projection along the expanding planes E_p. That projection is
    not a Galois star map: no Galois embedding of Z[ζ12] (σ = 5, 7, 11) vanishes on E_0 or E_1, and neither does the
    physical one (|σ(e)| ≥ 1.48 on the basis vectors).
  - BGMS show that the CASPr tilings are mutually locally derivable from model sets; they do not use this projection.
    A covering of internal space by translates of W would follow from their work only once W is identified with their
    window, which the paper already says is missing.
  - Their window-boundary value is a Hausdorff dimension, which does not bound the upper box dimension of ∂Z_p(S), so
    even with the identification it would not give option (a) by itself.
  - Option (b), stating only what is proved, stands.

## Second and third review rounds

A fresh adversarial pass over the fixed paper found the following. All are fixed on this branch.

- **R2-1 to R2-7** (round 2):
  - the exact interface law, with its Mystic term, replaces the approximate one in `spectre_boundary.py`, and the selftest
    checks it at depths 3 and 4 (depth 5 was checked separately);
  - the paragraph after Proposition `sstar` gives the measured drift (2.66 at depth 4, 2.41 at depth 5, against μ ≈ 1.859)
    and says that the exact closed form reproduces it;
  - three places that called Tsiokos's result proved now say it rests on his claimed proof, which is quoted and not
    checked here;
  - the remaining round-2 items were wording fixes; R2-5 needed no change.
- **Corner lines.** The bounded/linear behaviour of the d_z sums on the (0,0,1) and (1,0,0) corner lines is now argued in
  the text (the d_z values on the closed class run +1,+1,−1,−1,…, so the sums stay in {0,1,2}; on (1,0,0) every letter has
  d_z = 1, so the sums equal L). `chair44_lines.py --tests` now checks both and that τ_(0,0,1) sends its closed class onto
  two words.
- **Centre diffraction (round 3).** Fact `centrediff` now defines the amplitude a(k) = lim 8⁻ⁿ Σ_{x∈X_n} e^{ik·x}, so
  a(0) = 1, and the Bragg intensity is |a(k)|² times the squared density 1/49. Before, the normalisation was left implicit
  and Σ I = 1/7 did not follow from the text.
- **References.** Every arXiv entry was checked against its arXiv record (authors, titles, journal references for
  BaakeSpectre, BGS and BaakeHat). The numbers the paper quotes from Kamenetsky (Problem 9.1, 2187, 3 closed at cap 300,
  30→44→44, plateau 1566, structured family 158) match the arXiv text. The Chéritat–Ma web page could not be fetched from
  this environment (the proxy returns 403), so that entry is unverified.
- **Supplement.** Its counts (25 numbered Facts, 71 ledger entries, 24 Lean-marked, 67 theorems) match the paper, the
  ledgers and `SpectreFacts.lean`. Its rows for `chair_lines`, `centre_diffraction` and `internal_plane` agree with the
  paper.
