import random
from pathlib import Path

# Fixed seed: same selection of calculations (and same training / trial order in mist.py)
# for every participant. Change the value to get a different set.
SEED = 256745

LEVELS_FOLDER = Path(__file__).resolve().parent / "niveaux"
MAX_MULT_BY_ZERO = 10   # max number of multiplications/divisions involving 0 (levels 4 and 5)


def read_calculations_from_file(filename):
    """Return the non-empty lines of a file, or an empty list if it cannot be read."""
    if not filename.exists():
        print(f"Fichier introuvable : {filename}")
        return []
    with filename.open("r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def multiplication_by_zero(calculation_line):
    """Detect a multiplication or division involving 0 in a 4-number calculation."""
    tokens = calculation_line.split()
    if len(tokens) < 7:
        return False
    nums = [int(t) for t in tokens[0::2]]
    operations = tokens[1::2]
    return any(op in ("*", "/") and (a == 0 or b == 0)
               for op, a, b in zip(operations, nums, nums[1:]))


def repeat_to_length(calculations, n):
    """Repeat a list (reshuffled each time) until it contains n items."""
    result = []
    while calculations and len(result) < n:
        batch = calculations[:]
        random.shuffle(batch)
        result.extend(batch)
    return result[:n]


def create_selected_calculations_by_level(n_per_level=305):
    """Select n_per_level calculations per level (default: 5 training + 300 test)."""
    random.seed(SEED)
    selected_calculations_by_level = {}

    for level in range(1, 6):
        calculations = read_calculations_from_file(LEVELS_FOLDER / f"niveau{level}_all_solution.txt")

        if level == 1:
            # Level 1 only has 85 possible calculations: they are repeated to reach n_per_level
            selected = repeat_to_length(calculations, n_per_level)
        else:
            random.shuffle(calculations)
            selected = []
            mult_by_zero_count = 0
            for calculation in calculations:
                if level in (4, 5) and multiplication_by_zero(calculation):
                    if mult_by_zero_count >= MAX_MULT_BY_ZERO:
                        continue
                    mult_by_zero_count += 1
                selected.append(calculation)
                if len(selected) >= n_per_level:
                    break

        if len(selected) < n_per_level:
            print(f"Attention : niveau {level}, seulement {len(selected)} calculs "
                  f"au lieu de {n_per_level}")
        selected_calculations_by_level[level] = selected

    return selected_calculations_by_level