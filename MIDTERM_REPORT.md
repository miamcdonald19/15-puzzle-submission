# 15-Puzzle Midterm Project Report

## Project Overview

This project implements a functional 15-puzzle game in Python.  
The puzzle allows legal tile movement into the blank space, prevents illegal moves, tracks the number of moves, and includes a scramble function.  
A full test suite using Python’s unittest framework verifies correctness.  
All tests pass successfully.

---

## Time Spent

I spent approximately 12–15 cumulative hours working on this project.  
This includes development, debugging move logic, implementing scramble behavior, writing tests, and preparing the final submission.

---

## Most Time-Consuming Part

The most time-consuming part was debugging the `move()` logic and making sure the function behavior matched the test suite expectations.  
Distinguishing between tile index movement and tile value movement required careful reasoning and debugging.

---

## How I Could Have Worked More Efficiently

In retrospect, I could have written the test suite earlier and used a more test-driven development approach.  
Clearly defining whether `move()` should operate on tile index or tile value from the beginning would have saved significant debugging time.

---

## Libraries and Starter Code

The primary libraries used were:

- `random` for scrambling
- `unittest` for testing

Starter structure code provided the base Puzzle class.  
The movement logic and test integration required significant modification and debugging.

---

## Readability and Structure

The code includes:
- Clear variable naming
- Inline comments explaining logic
- Docstrings for functions
- Separation of puzzle logic from interface logic

---

## Final Status

All unit tests pass.  
The puzzle behaves correctly according to the project proposal.  
There are no known major bugs at the time of submission.
