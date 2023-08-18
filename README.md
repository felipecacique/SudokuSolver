# Sudoku Solver
Project for my Artificial Intelligence class at UFMG in 2018 in which we had to solve a Constraint Satisfactory Problem (CSP).

This work implements different [algorithms](https://github.com/felipecacique/SudokuSolver/blob/main/sudoku_solver.py) to solve a Sudoku of sizes 9x9, 16x16, and 25x25, including backtracking, arc consistency algorithm (AC3), and some heuristics. 
The [notebook](https://github.com/felipecacique/SudokuSolver/blob/main/sudoku_solver.ipynb) demonstrates an example of how to use the developed functions to solve a Sudoku so that you can solve yours! :)

The method AC3HB (AC_3 + Heuristics + Backtracking) was found to be the fastest and the most complete one. 

For more details on the project, algorithms, pseudocode, and time complexity, check the [paper](https://github.com/felipecacique/SudokuSolver/blob/main/Sudoku%20Solver%20-%20Felipe%20Vital.pdf).


We will show a few Sudoku puzzles solved by the algorithm AC3HB. The bold characters are the initially filled cells.

Very Hard Sudoku 9x9 solved by AC3HB in 0.11s.

<img src="https://github.com/felipecacique/SudokuSolver/blob/main/img/sudoku_9x9.png" />

Medium Sudoku 16x16 solved by AC3HB in 14s.

<img src="https://github.com/felipecacique/SudokuSolver/blob/main/img/sudoku_16x16.png" />

Very Hard Sudoku 25x25 solved by AC3HB in 37s.

<img src="https://github.com/felipecacique/SudokuSolver/blob/main/img/sudoku_25x25.png" />


### Sudoku Solver API
We have made available the use of our sudoku solver through an [API](https://github.com/felipecacique/SudokuSolver). The domain/route is http://felipecacique.pythonanywhere.com/sudoku/solve. Use the method PUT and send the sudoku in the JSON format like this [example](https://github.com/felipecacique/SudokuSolver/blob/main/json_example.txt).

### Sudoku Solver APP
We have created a simple sudoku app on https://felipecacique.pythonanywhere.com/.
##
