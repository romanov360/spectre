# Code review, round 2: `paper-prepub-review-squashed` at 469f9db

This round covers two things:
- the fix commit 469f9db, which addresses round 1 (`CODE_REVIEW.md`);
- the parts of the code that round 1 only skimmed:
  - the Theorem 1 certificate;
  - the (H) and (R) certificates and the Lemma 2 orbit certificate;
  - `chair44_hull.py`, `chair44_twoadic.py` and `spectrelean.py`;
  - the remaining test suites, and every `except` clause in scope.

Every finding below was verified, either by running code or by tracing a concrete path through it. Line numbers refer
to 469f9db.

## Summary

| # | Severity | Where | One line |
|---|---|---|---|
| 1 | Minor | `spectrelean.py:746-767, 784-826` | the "measured, not asserted" axiom audit asserts "Classical.choice appears nowhere … constructive" unconditionally, and never checks that the audit run succeeded or covered every theorem |
| 2 | Minor | `spectrepaper.py` (lines 603-661, 1346-1448, 1861-1904) | numbers taken from the certificates (135, 33/18/15, 93, 1192, 1193, 142, 162, 67, 15,214) are typed into the text, and nothing ties them to the certificate outputs |
| 3 | Minor | `chair44_lines.py:277-278` (introduced in 469f9db) | the new stack-length test builds its expected dict from the keys it is testing, so it never checks that the seven differences are the set T |
| 4 | Nit | `chair44_hull.py:166-172` | the periodic-point search stops at period 63 |
| 5 | Nit | `chair44facts.py:360` | `spectral_radius=2` is a literal; the computed characteristic polynomial is never compared with it |
| 6 | Nit | `spectrefacts.py:1297-1316` | `except ImportError: pass` covers the whole atlas cross-check, including the analysis call |
| 7 | Nit | `hierarchy_certificate/chair44_atlas.py:126-147, 150-156` | contact legality checks only the root's pyramids, and the contact search box has no border guard |

---

## Findings

### 1. Minor: the Lean axiom audit claims constructivity without checking it, and does not check that it ran

**Where:** `spectrelean.audit_block` (`spectrelean.py:746-767`) and `spectrelean.check` (`:784-826`).

**What is wrong:**
- `audit_block` parses the `#print axioms` output. Whenever some theorem uses any axiom, it appends the fixed text
  "Classical.choice appears nowhere, so every proof here is constructive", even when the list it has just printed
  contains `Classical.choice`. Reproduction:
  ```
  >>> import spectrelean as L
  >>> print(L.audit_block("'Spectre.foo' does not depend on any axioms\n"
  ...                     "'Spectre.bar' depends on axioms: [propext, Classical.choice, Quot.sound]\n"))
      1 depend on Classical.choice, Quot.sound, propext -- the standard Lean foundation.
      They are the induction proofs; `simp` and `omega`
      bring these in. Classical.choice appears nowhere, so
      every proof here is constructive.
  ```
  The header contradicts itself. The module's own docstring says the audit is "measured, not asserted", but this
  sentence is asserted.
- `check()` never looks at `audited.returncode`. It does not check that every theorem in `names` appears in the audit
  output. It does not handle a `#print axioms` line that Lean wraps across several lines; a wrapped line would make
  `split('axioms: ')[1]` drop the axioms after the break. If the probe fails to elaborate, the output has no
  "depends" lines. `audit_block` then writes "0 theorems depend on no axioms … sorryAx appears nowhere: nothing is
  admitted", and the check passes, because the only guard is `'sorryAx' in audited.stdout`.
- `AUDIT_SENTENCE` (`:738`, "nothing depends on Classical.choice, so every proof in the file is constructive") is
  defined and never used.
- `spectre_supplement.preface` prints "%d theorems, kernel-accepted, no admitted proofs" with
  `nt = len(L.theorem_names(L.document()))`. That number is a count of theorem names in generated text, produced
  without running Lean. Nothing in the paper build re-checks kernel acceptance.

**Not verified:** whether the real Lean file uses `Classical.choice`. Lean is not installed here, and the paper's own
`make lean` was not rerun, as instructed.

**Fix:**
- In `audit_block`, state constructivity only when `'Classical.choice' not in every`; otherwise say which theorems use
  it.
- In `check`, require `audited.returncode == 0` and require that the set of names in the audit output equals `names`.
  Parse the output with a multi-line-safe regex.
- Delete `AUDIT_SENTENCE`.
- Have the supplement say "named in the Lean file (kernel-checked by `make lean`)" rather than assert acceptance.

### 2. Minor: numbers taken from the certificates are typed into the paper

**Where:** `spectrepaper.py`:
- 603, 605: 162 reports and 67 files, from the Lean rebuild;
- 631-638: 135 facet triples, and 33 enclosures, of which 18 are dead and 15 live, from (H);
- 650, 661: 15,214 orbits;
- 1346-1448: 93 live types, from Theorem 1;
- 1861-1904: 1192 types, at most 1193 pieces and 142 intersecting types, from Theorem 3.

**What is wrong:** each of these is the output of a certificate script that the paper build does not run. That is
reasonable, since several scripts take minutes. But no check compares the typed number with the committed output
file. If a certificate changes, the paper silently drifts. Round 1 (#2) raised this for 360,189; the same applies
here.

**Verification:** every number currently agrees. I re-ran:
- `check_chair44_hierarchy.py`: output identical to `out_chair44_hierarchy.txt`, with 135, 33, 18/15, (U) 15/15 and
  (Pr) 1 + 14;
- `spectre_window.py`: 1192 / 142 / 14 / 16;
- `registration_audit.py`: STATUS: PASS.

The 93 is in `out_spectre_boundary_proof.txt`, and 162/67 are in `lean_rebuild/`.

**Fix:** add a selftest check that parses the committed `out_*.txt` files (the format is stable) and asserts each of
these numbers. Better still, fill them into the text from those files with `@markers@`.

### 3. Minor: the new stack-length test cannot see a wrong set of differences (469f9db)

**Where:** `chair44_lines.py:277-278`:
```python
chk(all(s['lengths'] == {e: 2 ** 6 if e == (0, 0) else 2 ** 6 - 1 for e in s['lengths']} for s in sc), ...)
```
**What is wrong:** the expected dict is built over `s['lengths']`'s own keys, so the test only checks the values.
Suppose a line were found at e = (1, −1) instead of (1, 1). Its length would also be 2⁶ − 1, and the test would pass.
`lines_distinct` (7 keys) and `one_line_per_cell` do not pin the keys down either. The paper states
T = {(0,0), ±(1,0), ±(0,1), ±(1,1)} explicitly. The current data is right: the keys are exactly T, as checked in round
1.

**Fix:** compare with a fixed dict built from the paper's T:
`T = [(0,0),(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1)]`, then `{e: 2**6 if e == (0,0) else 2**6-1 for e in T}`. In the
ledger, record the keys as well as the sorted values.

### 4. Nit: `chair44_hull` searches for periodic points only up to period 63

`report()` iterates Φ at most 63 times from each block (`for per in range(1, 64)`). Φ acts on 1410 blocks, so a cycle
of period ≥ 64 would not be found, and the claim "27 periodic points, all fixed" would still pass. `chair44_blocks_indep.py`
finds the periodic set exhaustively (it iterates 1411 times and then traces the cycle) and also gets 27, so the result
is right. Fix: iterate `len(blocks)` times, or detect cycles directly.

### 5. Nit: the transfer matrix's spectral radius is a literal

`chair44facts.py:360` stores `spectral_radius=2` in the `chair_coincidence` value. `chair44_twoadic.report()` computes
`charpoly` but nothing compares the two. I checked: the characteristic polynomial is x⁵(x−2)⁴(x−1)³², and the
largest |eigenvalue| of the 41×41 matrix is 2.0. Fix: derive the radius from `tw['charpoly']` and assert it in the
selftest.

### 6. Nit: a broad `except ImportError: pass` in the ledger selftest

`spectrefacts.py:1297-1316` wraps `import spectreatlas` **and** `A.analyse(3)` and the comparisons in one
`try … except ImportError: pass`. An `ImportError` raised lazily inside `analyse` (for example, a missing optional
dependency) would silently skip the X-charge cross-check, with no message. Today `spectreatlas` imports and the check
runs. Fix: put only the import inside the `try`, and print a line when the check is skipped.

### 7. Nit: `chair44_atlas` relies on assumptions it does not assert

- `contact_type` treats a shared face as legal when every pyramid of the root on that face has a complementary pyramid
  of B at the same foot. It does not check that B has no extra pyramids there. This is sound only because every panel
  carries all eight allowed foot positions. That holds: 24 panels × 8 here, and `registration_audit.py` asserts the
  positions are distinct. But `chair44_atlas.py` itself does not assert it.
- `all_contacts` searches translations in [−4, 4]³ with no check that no contact touches the border.
  `chair44_blocks_indep.py` searches ±5 and asserts that the maximum is 4, so nothing is missed.

Fix: add both asserts.

---

## What I checked and found sound

- **`boundary_certificate/check_spectre_boundary_proof.py` (Theorem 1), read in full:**
  - Cayley–Hamilton: `seq` has n + 6 = 99 terms, and the recurrence is checked for k < dim B = 95.
  - The Mystic recurrence check stays in range at the order it finds (4).
  - Radius bounds: `r[X]` has K + 1 entries, so `separated` never indexes past it.
  - The tail bound covers the |μ| ≤ 1 eigen-components for k ≥ K.
  - Pruned children contribute 0; live children are closed under `children`.
  - Level-0 overlap and length use the exact patch geometry, and the margins are printed.
- **`hierarchy_certificate/check_chair44_hierarchy.py`:**
  - Re-run output is identical to the committed file.
  - Dead/live classification is exhaustive, with a node-limit assert rather than silent truncation.
  - (U) asserts uniqueness. (Pr) fails loudly, not silently, if a child does not touch the central child.
  - Note: it fails with `python3 -I` (ModuleNotFoundError for `chair44_atlas`), because `-I` drops the script
    directory from the path. The README does not use `-I`. I ran it under `-I` with an explicit `sys.path`.
- **`chair44_independent/registration_audit.py`** (with the solid, the atlas and the 5273-witness certificate):
  STATUS: PASS in 282 s.
- **`chair44_independent/c44lemma_cert.py` and `c44adm.py`:** the orbit-certificate logic is sound:
  - every representative is checked to be the least element of its orbit, with the right orbit size;
  - the union of the orbits is checked to equal the admissible set;
  - σ is checked to commute with O, and L to be O-invariant;
  - in `build_compat`, `comp[E8[i]-E8[j]][blk[j]][l]` indexes compatibility in the right direction.
- **`chair44_hull.act`:** for a frame `(p, s)`, `g[1][i]` is the sign of output axis i, so the corner shift is
  correct. Its stabiliser counts (1:1296, 2:96, 4:12, 8:6, summing to 1410) are consistent with the independent
  `act` in `chair44_blocks_indep.py`.
- **`chair44_twoadic`:** the address convention puts the most significant digit first, matching the fix in 469f9db.
  The counts satisfy c(M) = 28·2ᴹ − 48, consistent with the characteristic polynomial (a simple eigenvalue 2 and a
  constant term from (x−1)).
- **Test suites:** `symchair44_tests.py` passes 10/10, and `chair44_tests.py` (full, not `--quick`) passes 11/11.
  `spectre_tests.py` exits 0, but it has only three asserts, and the paper does not cite it.
- **The `run_tests` helpers** in `chair44_diffraction`, `chair44_slice` and `chair44_unfold` catch every exception
  but count it as a failure and return False, so nothing is swallowed. `spectre_boundary.find_recurrence`'s
  `except Exception: continue` only skips a singular least-squares order.
- **The 469f9db fixes**, in addition to the passing selftests reported with that commit:
  - `fine_decomposition` asserts the four growing types and their pairing;
  - `exact_boundary_recount` removes its `sys.path` entry in a `finally`;
  - the supplement's new count checks read the numbers back from the rendered text and compare them with the table
    rows, the checkmarks and the fact environments, so each can now fail independently;
  - the `QUOTED_FITS` link between the paper and `spectre_boundary` is checked at both ends.
