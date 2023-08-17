# Creating an API that solves sudoku using the endpoit localhost/sudoku/solve (PUT)

# Importing libraries
from flask import Flask, jsonify, request
import numpy as np
import time
import queue
import numpy as np
import random
import copy
import sudoku_solver


app = Flask(__name__)

sudoku_example = [
    {
    '1': ['', '', '3', '', '2', '', '6', '', ''], 
    '2': ['9', '', '', '3', '', '5', '', '', '1'], 
    '3': ['', '', '1', '8', '', '6', '4', '', ''], 
    '4': ['', '', '8', '1', '', '2', '9', '', ''], 
    '5': ['7', '', '', '', '', '', '', '', '8'],
    '6': ['', '', '6', '7', '', '8', '2', '', ''], 
    '7': ['', '', '2', '6', '', '9', '5', '', ''], 
    '8': ['8', '', '', '2', '', '3', '', '', '9'], 
    '9': ['', '', '5', '', '1', '', '3', '', '']
    }
]

# editar
@app.route('/sudoku/solve',methods=['PUT'])
def solve_sudoku():
    sudoku_json = request.get_json()

    # json to list of lists that is used by our framework
    sudoku = []
    for key, item in sudoku_json.items():
        sudoku.append(item)

    # Formating sudoku
    sudoku = sudoku_solver.FormatSudoku(sudoku)

    # Getting the sudoku's size 
    a =  int(len(sudoku)**.5) # sudoku size (eg., 3x3, 4x4, 5x5)
    n = int(len(sudoku)) # number of columns x rows (eg., 9X9, 16x16, 25x25)

    # Soving the sudoku by the method AC3HB (AC_3 + Heuristics + Backtracking)
    # At every interaction, the algorithm changes the sudoku object. In order to preserve the original we will do a copy.
    sudoku = copy.deepcopy(sudoku)
    # Create the Constraint Satisfactory Problem (CSP) object. It will be usd by the solver algorithms
    csp=sudoku_solver.Csp()
    # Fill de csp object with the given sudoku
    status = sudoku_solver.SudokuToCsp(sudoku,csp,a)
    # Do the AC_3 + Heuristics + Backtracking
    status = sudoku_solver.AC_3_and_Heuristics(csp,a)
    # If the sudoku was not solved yet, do the Backtracking
    status = sudoku_solver.Backtrack_Search(csp, ac_3=True, heuristics = False)
    # Count how many sudoku blocks is already solved
    status = sudoku_solver.n_domain_complete(csp)

    sudoku_solver.PrintSolvedSudoku(csp,sudoku)

    sudoku_solved = sudoku_solver.FormatSolvedSudoku(csp,sudoku) 
    print(sudoku_solved)

    # Convert sudoku list of lists to a dictionary
    sudoku_json = {}
    for i, item in enumerate(sudoku):
        sudoku_json[str(i+1)] = list(item)


    return jsonify(sudoku_json), 200

        

if __name__ == "__main__":
    app.run(port=5000, host='localhost', debug=True)

#     sdk_json = [
#     {
#         "1": [
#             "",
#             "",
#             "3",
#             "",
#             "2",
#             "",
#             "6",
#             "",
#             ""
#         ],
#         "2": [
#             "9",
#             "",
#             "",
#             "3",
#             "",
#             "5",
#             "",
#             "",
#             "1"
#         ],
#         "3": [
#             "",
#             "",
#             "1",
#             "8",
#             "",
#             "6",
#             "4",
#             "",
#             ""
#         ],
#         "4": [
#             "",
#             "",
#             "8",
#             "1",
#             "",
#             "2",
#             "9",
#             "",
#             ""
#         ],
#         "5": [
#             "7",
#             "",
#             "",
#             "",
#             "",
#             "",
#             "",
#             "",
#             "8"
#         ],
#         "6": [
#             "",
#             "",
#             "6",
#             "7",
#             "",
#             "8",
#             "2",
#             "",
#             ""
#         ],
#         "7": [
#             "",
#             "",
#             "2",
#             "6",
#             "",
#             "9",
#             "5",
#             "",
#             ""
#         ],
#         "8": [
#             "8",
#             "",
#             "",
#             "2",
#             "",
#             "3",
#             "",
#             "",
#             "9"
#         ],
#         "9": [
#             "",
#             "",
#             "5",
#             "",
#             "1",
#             "",
#             "3",
#             "",
#             ""
#         ]
#     }
# ]

#     solve_sudoku(sdk_json)