#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MIST (Montreal Imaging Stress Task) - PsychoPy version.

Procedure: instructions, demonstration trial, training (no time limit),
then N_BLOCKS test blocks with an adaptive time limit, a performance gauge
and a comparison with a "group" performance.
"""
import math
import random
from pathlib import Path

import openpyxl
from psychopy import core, event, gui, visual
from psychopy.sound import Sound

from consignes import (afficher_consignes_entrainement1, afficher_consignes_entrainement2,
                       afficher_consignes_test_2, afficher_consignes_test_3,
                       afficher_perf_moyenne)

try:
    from niveaux_all_possible_stims import create_selected_calculations_by_level
except ImportError:
    print("Le fichier niveaux_all_possible_stims.py est introuvable. "
          "Assurez-vous qu'il est dans le même répertoire.")
    core.quit()


# ============================================================
# Configuration
# ============================================================
SCRIPT_FOLDER = Path(__file__).parent
MEDIA_FOLDER = SCRIPT_FOLDER / "medias"
RESULTS_FOLDER = SCRIPT_FOLDER / "data"

SCREEN = 1                      # 0 = main screen, 1 = second screen
BLOCK_DURATION = 300.0          # duration of a test block (s)
N_BLOCKS = 3
TRAINING_PER_LEVEL = 5          # training calculations per level
TEST_PER_LEVEL_PER_BLOCK = 100  # test calculations drawn per level and per block
FEEDBACK_DURATION = 1.0         # feedback duration during the test phase (s)
TRAINING_PAUSE = 0.5            # pause after each training response (s)
DEFAULT_TIME = 5.0              # allocated time if no training data is available (s)
TIME_FACTOR = 0.9               # time limit = 10 % less than the reference response time

# "Group" success rates displayed after each block.
# Fictitious values:
GROUP_SUCCESS = {1: 81.1, 2: 74.3, 3: 78.2}


# ============================================================
# Formatting the calculations
# ============================================================
def format_expression(nums, ops):
    """Put parentheses around runs of * and / in a mixed expression."""
    if all(op in ("*", "/") for op in ops):   # no parentheses, every operator kept
        return str(nums[0]) + "".join(f" {op} {n}" for op, n in zip(ops, nums[1:]))
    parts = [str(nums[0])]
    i = 0
    while i < len(ops):
        if ops[i] in ("*", "/"):
            j = i
            while j < len(ops) and ops[j] in ("*", "/"):
                j += 1
            group = str(nums[i]) + "".join(f" {ops[k]} {nums[k + 1]}" for k in range(i, j))
            parts[-1] = f"({group})"   # replace the preceding number with the group
            i = j
        else:
            parts += [f" {ops[i]} ", str(nums[i + 1])]
            i += 1
    return "".join(parts)


def format_problem(expr):
    if "*" not in expr and "/" not in expr:
        return expr
    parts = expr.split()
    return format_expression(list(map(int, parts[::2])), parts[1::2])


# ============================================================
# Task
# ============================================================
class Mist:

    def __init__(self):
        self.subject_id = self.ask_subject_id()
        self.error_sound = Sound(str(MEDIA_FOLDER / "error.wav"))
        self.win = visual.Window(fullscr=True, monitor="testMonitor", color="gainsboro",
                                 units="pix", screen=SCREEN)
        self.create_results_file()
        self.create_stimuli()
        self.prepare_problems()

        self.is_training = True
        self.trial_number = 0
        self.errors = []                 # current block: 0 = correct, 1 = error or timeout
        self.trial_clock = core.Clock()
        self.training_times = {level: [] for level in self.levels}
        self.allocated_time = {}
        self.correct_rts = {level: [] for level in self.levels}   # RTs of consecutive correct responses
        self.n_incorrect = dict.fromkeys(self.levels, 0)          # consecutive incorrect responses

    # ---------- Initialization ----------

    @staticmethod
    def ask_subject_id():
        dlg = gui.DlgFromDict({"ID du participant": ""}, title="Identification du participant")
        if not dlg.OK:
            core.quit()
        return dlg.data[0].strip() or "participant_inconnu"

    def create_results_file(self):
        RESULTS_FOLDER.mkdir(parents=True, exist_ok=True)
        self.results_file = RESULTS_FOLDER / f"resultats_{self.subject_id}.xlsx"
        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = "Résultats"
        self.sheet.append(["Phase", "Bloc", "Numéro d'essai", "Level", "Calcul", "Solution",
                           "Réponse choisie", "Correct", "Incorrect",
                           "Temps de réponse (s)", "Temps alloué (s)"])

    def create_stimuli(self):
        win = self.win
        self.calc_text = visual.TextStim(win, text="", height=60, color="black",
                                         pos=(0, 200), wrapWidth=10000)
        self.feedback_text = visual.TextStim(win, text="", height=60, pos=(-250, -200))
        self.timer_text = visual.TextStim(win, text="", height=40, pos=(0, 50), wrapWidth=200)
        self.message_bg = visual.Rect(win, width=2000, height=1500,
                                      fillColor="gainsboro", lineColor=None)
        self.message_text = visual.TextStim(win, text="", height=50, color="black", wrapWidth=800)

        # Gauge: 800 px wide, from x = -400 (0 %) to x = 400 (100 %)
        # The target arrow (group score) is positioned at the start of each block
        self.target_arrow = visual.ShapeStim(win, vertices=self.target_vertices(-400),
                                             fillColor="black", lineColor=None)
        self.progress_arrow = visual.ShapeStim(win, vertices=self.arrow_vertices(-400),
                                               fillColor="black", lineColor=None)
        self.gauge = [
            visual.Rect(win, width=800, height=20, fillColor=None, lineColor="black", pos=(0, 360)),
            visual.Rect(win, width=480, height=20, fillColor="red", lineColor=None, pos=(-160, 360)),   # 0-60 %
            visual.Rect(win, width=160, height=20, fillColor="white", lineColor=None, pos=(160, 360)),  # 60-80 %
            visual.Rect(win, width=160, height=20, fillColor="green", lineColor=None, pos=(320, 360)),  # 80-100 %
            self.target_arrow,
            self.progress_arrow,
        ]

        # Response dial (0 at the top left, digits arranged clockwise)
        self.dial = []
        self.dial_stims = []
        for i, digit in enumerate([0, 9, 8, 7, 6, 5, 4, 3, 2, 1]):
            angle = math.radians(i * 36 - 245)
            pos = (400 + 200 * math.cos(angle), -200 + 200 * math.sin(angle))
            circle = visual.Circle(win, radius=40, fillColor="blue", lineColor="white", pos=pos)
            label = visual.TextStim(win, text=str(digit), color="white", height=30, pos=pos)
            self.dial.append((digit, circle))
            self.dial_stims += [circle, label]

        self.all_stims = ([self.calc_text, self.feedback_text, self.timer_text,
                           self.message_bg, self.message_text] + self.dial_stims + self.gauge)

    def prepare_problems(self):
        n_per_level = TRAINING_PER_LEVEL + TEST_PER_LEVEL_PER_BLOCK * N_BLOCKS
        problems_by_level = {f"level{i}": [format_problem(e) for e in calculs]
                             for i, calculs in create_selected_calculations_by_level(n_per_level).items()}
        self.levels = list(problems_by_level)

        # Training: 5 calculations per level, presented level by level.
        # Test: up to 100 x N_BLOCKS other calculations per level, shuffled then dealt out to the blocks in turn.
        n_test = TEST_PER_LEVEL_PER_BLOCK * N_BLOCKS
        self.training_problems, test_problems = [], []
        for level, problems in problems_by_level.items():
            random.shuffle(problems)
            self.training_problems += [(p, level) for p in problems[:TRAINING_PER_LEVEL]]
            test_problems += [(p, level) for p in problems[TRAINING_PER_LEVEL:TRAINING_PER_LEVEL + n_test]]
        random.shuffle(test_problems)
        self.block_problems = {b: test_problems[b - 1::N_BLOCKS] for b in range(1, N_BLOCKS + 1)}

    # ---------- Display ----------

    @staticmethod
    def arrow_vertices(x):
        return [(x, 340), (x - 10, 310), (x + 10, 310)]

    @staticmethod
    def target_vertices(x):
        return [(x, 380), (x - 10, 410), (x + 10, 410)]

    @staticmethod
    def set_visible(stims, visible):
        for stim in stims:
            stim.setAutoDraw(visible)

    def clean_screen(self):
        self.set_visible(self.all_stims, False)
        event.clearEvents()
        self.win.flip()

    def show_message(self, message, duration, hide=True):
        self.clean_screen()
        self.message_text.text = message
        self.set_visible([self.message_bg, self.message_text], True)
        self.win.flip()
        core.wait(duration)
        if hide:
            self.set_visible([self.message_bg, self.message_text], False)
            self.win.flip()
            core.wait(0.1)

    def highlight(self, selected):
        for digit, circle in self.dial:
            circle.fillColor = "orange" if digit == selected else "blue"

    def percent_correct(self):
        if not self.errors:
            return 0
        return 100 * (1 - sum(self.errors) / len(self.errors))

    def update_arrow(self):
        self.progress_arrow.vertices = self.arrow_vertices(-400 + self.percent_correct() * 8)

    # ---------- Response ----------

    def collect_response(self, timeout=None):
        """Move around the dial (left/right) and confirm (down).
        Return (chosen digit, response time), or (None, timeout) if time runs out."""
        selected = 0
        self.highlight(selected)
        self.trial_clock.reset()
        while True:
            if timeout is not None:
                elapsed = self.trial_clock.getTime()
                remaining = max(0, timeout - elapsed)
                self.timer_text.text = f"{remaining:.2f}"
                self.timer_text.color = "red" if remaining <= 2.0 else "black"
                if elapsed >= timeout:
                    return None, timeout

            keys = event.getKeys(["left", "right", "down", "escape"])
            if "escape" in keys:
                self.quit()
            if "right" in keys:
                selected = (selected + 1) % 10
                self.highlight(selected)
            if "left" in keys:
                selected = (selected - 1) % 10
                self.highlight(selected)
            if "down" in keys:
                return selected, self.trial_clock.getTime()

            self.win.flip()
            core.wait(0.01)

    # ---------- Allocated time ----------

    def initial_time(self, level):
        """10 % less than the mean training time for the level, ignoring the first 2 trials."""
        times = self.training_times[level]
        if len(times) >= 3:
            times = times[2:]
        if not times:   # no times for this level: use the mean of the other levels
            times = [t for ts in self.training_times.values() if len(ts) >= 3 for t in ts[2:]]
        return TIME_FACTOR * sum(times) / len(times) if times else DEFAULT_TIME

    def update_time_allocation(self, level, correct, rt):
        """3 correct responses in a row: 10 % less than their mean response time (minimum 1 s).
        3 errors in a row: +10 %."""
        if correct:
            self.correct_rts[level].append(rt)
            self.n_incorrect[level] = 0
            if len(self.correct_rts[level]) >= 3:
                mean_rt = sum(self.correct_rts[level]) / len(self.correct_rts[level])
                self.allocated_time[level] = max(1.0, TIME_FACTOR * mean_rt)
                self.correct_rts[level] = []
        else:
            self.n_incorrect[level] += 1
            self.correct_rts[level] = []
            if self.n_incorrect[level] >= 3:
                self.allocated_time[level] *= 1.1
                self.n_incorrect[level] = 0

    # ---------- Trials and blocks ----------

    def run_demo(self):
        """Demonstration trial (2 + 4), with no recording and no feedback."""
        event.clearEvents()
        self.calc_text.text = "2 + 4 = ?"
        self.calc_text.setAutoDraw(True)
        self.set_visible(self.dial_stims, True)
        self.collect_response()
        self.win.flip()
        core.wait(1.5)
        self.calc_text.setAutoDraw(False)
        self.set_visible(self.dial_stims, False)
        self.win.flip()

    def run_trial(self, problem, level, block=0):
        self.clean_screen()
        try:
            solution = int(eval(problem))
        except ZeroDivisionError:
            return   # calculation skipped

        self.calc_text.text = f"{problem} = ?"
        self.calc_text.setAutoDraw(True)
        self.set_visible(self.dial_stims, True)
        timeout = None
        if not self.is_training:
            timeout = self.allocated_time[level]
            self.update_arrow()
            self.set_visible(self.gauge, True)
            self.timer_text.setAutoDraw(True)

        answer, rt = self.collect_response(timeout)
        correct = answer == solution
        self.sheet.append(["Entraînement" if self.is_training else "Test", block,
                           self.trial_number + 1, level, problem, solution,
                           "Timeout" if answer is None else answer,
                           "Oui" if correct else "", "" if correct else "Oui",
                           round(rt, 2), timeout or 0])
        self.workbook.save(self.results_file)
        self.trial_number += 1

        if self.is_training:
            self.training_times[level].append(rt)
            core.wait(TRAINING_PAUSE)
            return

        self.errors.append(0 if correct else 1)
        self.update_time_allocation(level, correct, rt)
        self.update_arrow()
        if answer is None:
            self.feedback_text.text, self.feedback_text.color = "⏰ TEMPS EXPIRÉ !", "orange"
        elif correct:
            self.feedback_text.text, self.feedback_text.color = "✅ CORRECT ", "green"
        else:
            self.feedback_text.text, self.feedback_text.color = "❌ INCORRECT !", "red"
        if not correct:
            self.error_sound.play()
        self.feedback_text.setAutoDraw(True)
        self.win.flip()
        core.wait(FEEDBACK_DURATION)

    def run_block(self, block):
        self.show_message(f"Bloc {block}\n\n (5 minutes)", 3.0)
        target_x = -400 + GROUP_SUCCESS.get(block, 85) * 8
        self.target_arrow.vertices = self.target_vertices(target_x)
        self.errors = []
        block_clock = core.Clock()
        for problem, level in self.block_problems[block]:
            if block_clock.getTime() >= BLOCK_DURATION:
                break
            self.run_trial(problem, level, block)

        self.clean_screen()
        afficher_perf_moyenne(self.win, round(self.percent_correct(), 2),
                              GROUP_SUCCESS.get(block, 0.0))
        self.clean_screen()

    def run(self):
        # Instructions, demonstration and training
        afficher_consignes_entrainement1(self.win, MEDIA_FOLDER / "entrainement.png")
        self.run_demo()
        afficher_consignes_entrainement2(self.win)
        for problem, level in self.training_problems:
            self.run_trial(problem, level)

        # Switch to the test phase
        self.show_message("Fin de la phase d'entrainement", 3.0)
        afficher_consignes_test_2(self.win, MEDIA_FOLDER / "test2.png")
        afficher_consignes_test_3(self.win, MEDIA_FOLDER / "test3.png")
        self.clean_screen()
        self.is_training = False
        self.trial_number = 0
        self.allocated_time = {level: self.initial_time(level) for level in self.levels}
        core.wait(1.0)
        self.show_message("Tâche de calcul mental", 2.0, hide=False)

        # Test blocks
        for block in range(1, N_BLOCKS + 1):
            self.run_block(block)

        self.show_message("Fin de la tâche", 3.0)
        self.quit()

    def quit(self):
        self.win.close()
        core.quit()


if __name__ == "__main__":
    Mist().run()