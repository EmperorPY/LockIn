# LockIn

This is a Python project I made while learning Python.

## What it does

LockIn is a clean, distraction-free desktop study timer built with CustomTkinter. It uses the Pomodoro technique — 25 minutes of focused work followed by a 5-minute break — to help you concentrate and avoid burnout. It also includes a motivational quote generator for when you're feeling tired.

## Features

- 25-minute work / 5-minute rest Pomodoro cycle that switches automatically
- Start, pause, resume, and reset controls
- Large full-screen countdown display with a clear work/rest phase indicator
- "Motivate Me!" button that shows a random motivational quote from a list of 200
- Dark mode UI with a clean, modern layout

## What I learned

- How to build a GUI with CustomTkinter and lay out widgets using `grid`, `pack`, and `place`
- How to run a non-blocking countdown using `root.after()` instead of `while` loops
- How to manage app state with global variables (`remaining`, `phase`, `running`, `after_id`) and cancel scheduled callbacks with `after_cancel()`
- How to structure a larger file with helper functions and keep logic separate from UI

## How to run

1. Install Python 3.8 or newer.
2. Install CustomTkinter:
   ```bash
   pip install customtkinter
   ```
3. Run the file:
   ```bash
   python lockin.py
   ```

**Made with:** Python

## Future improvements

- Add an audio alert when a work or rest phase ends
- Add a circular progress ring showing time remaining
- Add a session counter to track how many Pomodoros you complete
- Save daily session history to a file
- Let users customize work/rest durations (25/5, 50/10, 90/20)
