# MIST_Code_Project

*RDG README File Template — General — Version 0.1 (2022-10-04)*

This README file was generated on 2026-11-02 by Amélie Puech.
Last updated: 2026-11-02.

---

## General information

**Dataset title:** MIST_Code_Project – Implementation of the Montreal Imaging Stress Task (MIST)

**DOI:** [To be completed]

**Contact email:** amelie.puech@univ-lyon1.fr

---

## Methodological information

### Environmental/experimental conditions

The task runs full screen on a computer with a keyboard and speakers or headphones (an error sound is played after each incorrect response or timeout). By default it is displayed on a second screen (`SCREEN = 1` in `main_code_MIST.py`; set it to `0` to use the main screen).

Stimulus positions are defined in pixels: for optimal positioning, the screen should be at least about 1280 × 900 pixels.

Participants answer with the keyboard:

| Key | Action |
|---|---|
| ← / → | Move the selection around the response dial (digits 0 to 9) |
| ↓ | Confirm the answer |
| Escape | Quit the task |

### Description of sources and methods used to collect and generate data

The task is a mental arithmetic task under time pressure, adapted from the MIST (Dedovic et al., 2005). It induces psychosocial stress through an adaptive time limit, negative feedback and an unfavourable comparison with a fictitious "group" performance.

#### Procedure

1. **Instructions and demonstration**: one demonstration trial (2 + 4), not recorded.
2. **Training**: 5 calculations per level (5 levels), with no time limit and no feedback.
3. **Test**: 3 blocks of 5 minutes. Each trial has a time limit shown by a countdown, followed by 1 s of feedback (correct, incorrect or time expired). A gauge shows the participant's percentage of correct answers in the current block, with a second, fixed arrow showing the fictitious group score of that block.
4. **After each block**: the participant's score is displayed next to a fictitious "group" score (81.1 %, 74.3 % and 78.2 % for blocks 1, 2 and 3).

#### Calculation levels

All results are integers between 0 and 9.

| Level | Numbers | Operators |
|---|---|---|
| 1 | 2 numbers from 0 to 9 (first ≥ second) | + − |
| 2 | 3 numbers from 0 to 9 | + − |
| 3 | 1 number from 0 to 9, then 2 numbers from 0 to 99 | + − × |
| 4 | 2 numbers from 0 to 9, then 2 numbers from 0 to 99 | + − × |
| 5 | 4 numbers from 0 to 99 | + − × ÷ |

#### Stimulus generation and selection

- A generation script lists the calculations of each level whose result is an integer between 0 and 9 and writes them to the `niveau<N>_all_solution.txt` files. For levels 1 to [X], the files contain every possible calculation. For level 5, only a subset was kept, because the complete list would have made the files too large.
- At each session, `niveaux_all_possible_stims.py` draws 305 calculations per level from these files (5 for training and 300 for the test, i.e. 100 per level and per block). Level 1 contains only 85 possible calculations, which are repeated (and reshuffled) to reach 305. At levels 4 and 5, at most 10 calculations containing a multiplication or division involving 0 are kept.
- A fixed random seed (`SEED = 256745`) is used, so every participant receives the same calculations, the same training and the same trial order. To obtain a different set of calculations, change the value of `SEED` in `niveaux_all_possible_stims.py`.

#### Adaptive time limit

- The initial time limit of each level is 10 % shorter than the mean training response time for that level, excluding the first 2 trials (5 s by default if no data is available).
- **3 correct answers in a row**: the time limit becomes 10 % shorter than the mean response time of these 3 answers (minimum 1 s), as in Dedovic et al. (2005).
- **3 errors or timeouts in a row**: the time limit increases by 10 %.

Block duration is measured in real time, feedback included. A new trial starts only if less than 5 minutes have elapsed, so the last trial of a block may exceed this limit by a few seconds.

### Methods for processing the data

The results files contain raw trial-by-trial data. No processing is applied after collection. The only value computed during the task is the percentage of correct answers per block (correct answers / trials in the block × 100, timeouts counted as errors), which is displayed to the participant but not saved.

### Quality-assurance procedures performed on the data

- The results file is saved after every trial, so data are kept if the task is interrupted.
- Every calculation in the stimulus files is checked to give an integer result between 0 and 9.
- The number of calculations selected per level is checked, and a warning is printed if a level contains fewer than requested.
- The fixed random seed makes the stimulus selection and order reproducible across sessions.

### Other contextual information

- **Software**: Python 3, PsychoPy, openpyxl (tqdm is only needed to generate the stimulus files). See `requirements.txt` for versions.
- **Stimulus files**: generating level 5 requires evaluating several billion combinations and takes a very long time: the existing stimulus files should be kept rather than regenerated.
- **Debriefing**: the "group" scores are fictitious and part of the stress manipulation; they must be explained to participants during debriefing.
- **Language**: on-screen texts and the results file headers are in French.

#### Reference

Dedovic, K., Renwick, R., Mahani, N. K., Engert, V., Lupien, S. J., & Pruessner, J. C. (2005). The Montreal Imaging Stress Task: using functional imaging to investigate the effects of perceiving and processing psychosocial stress in the human brain. *Journal of Psychiatry & Neuroscience, 30*(5), 319–325.

---

## Data & file overview

### File naming convention

- `niveau<N>_all_solution.txt`: all possible calculations for level N (N = 1 to 5)
- `resultats_<participant ID>.xlsx`: results of one participant (`participant_inconnu` if no ID was entered)

### File hierarchy convention

```
.
├── main_code_MIST.py                         main task script
├── consignes.py                              instruction screens and performance display
├── niveaux_all_possible_stims.py             selection of the calculations presented
├── generate_all_possible_stims_by_levels.py  generation of the stimulus files
│                                             (not needed if the provided .txt files are used)
├── requirements.txt                          Python dependencies
├── niveaux/                                  pre-generated stimulus files, provided in the repository:
│                                             niveau1_all_solution.txt … niveau5_all_solution.txt
├── medias/                                   error.wav, entrainement.png, test2.png, test3.png
└── data/                                     results files (created automatically)
```

---

## Data-specific information for: `niveau<N>_all_solution.txt`

### Variable/Column list

Plain text file, UTF-8, one calculation per line, with numbers and operators separated by spaces (e.g. `3 + 4 * 2`). Calculations are written without parentheses and follow standard operator precedence; parentheses around × and ÷ are added only for on-screen display.

### Missing data codes

None.

### Additional information

None.

---

## Data-specific information for: `resultats_<participant ID>.xlsx`

### Variable/Column list

One sheet (`Résultats`), one row per trial (training and test). The demonstration trial is not recorded. Numeric values are stored as numbers, so the decimal separator depends on the display settings of the spreadsheet software.

| Column | Description | Unit / format | Allowed values |
|---|---|---|---|
| Phase | Phase of the task | text | `Entraînement` (training), `Test` |
| Bloc | Block number | integer | 0 (training), 1 to 3 (test blocks) |
| Numéro d'essai | Trial number; starts at 1 at the beginning of training, restarts at 1 at the beginning of the test phase and continues across the 3 test blocks | integer | positive integers |
| Level | Difficulty level of the calculation | text | `level1` to `level5` |
| Calcul | Calculation as displayed to the participant (with parentheses around × and ÷) | text | — |
| Solution | Correct answer | integer | 0 to 9 |
| Réponse choisie | Answer given by the participant | integer or text | 0 to 9, or `Timeout` |
| Correct | Whether the answer is correct | text | `Oui` (yes), or empty |
| Incorrect | Whether the answer is incorrect (timeouts included) | text | `Oui` (yes), or empty |
| Temps de réponse (s) | Time between the display of the calculation and the confirmation of the answer; equal to the allocated time for a timeout | seconds, rounded to 2 decimals | — |
| Temps alloué (s) | Time limit for the trial | seconds, not rounded | 0 during training (no time limit) |

### Missing data codes

- `Timeout` in *Réponse choisie*: no answer given within the time limit.
- Empty cell in *Correct* or *Incorrect*: means "no".
- `0` in *Temps alloué (s)*: no time limit (training).

### Additional information

The file is created at the start of the session and saved after every trial. The percentage of correct answers per block can be recomputed from the *Correct* column of the test rows.
