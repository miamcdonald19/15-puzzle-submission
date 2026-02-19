# 15-puzzle
Foundations of Programming project
## Midterm Checkpoint 2

### Test Suite
I created a unit test file called `test_puzzle.py` using Python’s unittest framework. 
The tests verify:
- The board starts solved
- Legal adjacent moves work
- Illegal moves fail
- Scramble changes the board
- Move count resets after scramble

All tests currently pass.

### What I’m Stuck On
I am working on improving the scramble method to guarantee solvable boards and improving the UI interaction with puzzle logic.

### Known Bugs
Scramble currently randomizes without guaranteeing solvability.

### Most Time-Consuming Part
The most time-consuming part was debugging the move logic and making sure the test cases matched the intended behavior.
