# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked twins technique can be implemented with the following steps
  - Step 1: For a given unit, find all boxes that have a value of length 2
  - Step 2: Among those boxes in Step 1, find all possible pairs of two boxes. Only keep those pairs with identity value
  - Step 3: For a given pair among the kept pairs in Step 2, eliminate the shared value of the pair from the values of their peers in the unit. Iterate over the kept pairs to perform the elimination process
  - Step 4: Iterate the unit list for Step 1 - 3

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: To add diagonal constraints when solving sudoku problem, we first find the 9 boxes in the diagonal unit and the 9 boxes in the anti-diagonal unit. We then append these two units to our unit list which already contains row, column and square units. Applying the same searching procedure with the updated unit list will lead us to the solution.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
