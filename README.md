# 8-Puzzle and NxN Variants Problem Solver using varius Algorithms and Heuristic
Algorithms and Heuristic Approaches for Solving the 8-Puzzle and NxN Variants

# Description
This project explores various algorithms and heuristics to solve the classic 8-puzzle problem and extends these approaches to larger NxN puzzles. The 8-puzzle consists of a 3x3 grid with 8 numbered tiles and one blank space, and the goal is to rearrange the tiles in numerical order using the blank space. We implemented both informed and uninformed search algorithms, including A* with different heuristics such as Manhattan Distance and Euclidean Distance. Our results showed that A* with the Manhattan Distance heuristic was the most efficient in terms of time and moves. The project also highlights the challenges encountered, such as unsolvable start states and the computational complexity of larger puzzles. We developed an interactive user interface to facilitate easy experimentation and automated data collection for performance analysis.

This program is designed to solve the classic sliding tile puzzle, where the goal is to move tiles on an NxN board to match the predefined goal state. The default configuration is the 8-puzzle (3x3 board), but the program allows you to choose larger board sizes.

For a 3x3 board, the goal state is:

1 2 3
4 5 6
7 8 0

The tiles are numbered from 1 to(N*N-1) and the 0 represents the blank space. This program provides four different algorithms to solve the puzzle: A* Search, Breadth-First Search (BFS), Depth-First Search (DFS), and Iterative Deepening Depth-First Search (IDDFS). For A* Search, the user can choose from four different heuristics for the search.

# Features:
- Four Solving Algorithms: A* Search, BFS, DFS, and IDDFS.
- Four Heuristic Options for A*: Manhattan Distance, Hamming Distance, Euclidean Distance, and Chebyshev Distance.
- Customizable Board Size. You can choose the default 3x3 board or choose a custom NxN size. Please note larger puzzles will result in increased state spaces, larger branching factors, and longer path lengths. They could take several minutes or longer to solve.
- Customizable Start States: Choose from predefined initial states, generate a random start state, or enter a custom state.
- Validation for Solvable States: The program ensures that both random and custom start states are solvable.
- Save and Review: After solving a puzzle, you can save the final path to a file and review all solved puzzles at the end.
- Automated Data Collection: You can run all of the algorithms (except DFS due to extreme inefficiency) on a user defined number of start states and save the results to a .csv file for analysis.

# How to Use:

- Launch the Program: Run the program in your preferred Python environment.

- Choose the size of the puzzle (We recommend 3).

- Select Initial State:
	- You will be presented with a menu to choose an initial state.
	- Choose from one of the predefined states, generate a random state, or input a custom state. You may also choose to begin Automated Data Collection.
	- If generating a random state or entering a custom state, the program will check that the state is solvable.
	- Custom Input Guidelines:
		- Matrix Size: 		The custom input must be an NxN matrix. Enter one row of N at a time. 
		- Valid Numbers: 	Only use the numbers 0 to (N*N-1) (inclusive), where 0 represents the empty space.
		- No Duplicates: 	Each number must appear exactly once.
		- Solvability: 		The program will check if the custom state is solvable before proceeding.
		- Example of Custom Input:
			Enter Custom Row 1 (Each number separated by space): 2 8 3
			Enter Custom Row 2 (Each number separated by space): 1 6 4
			Enter Custom Row 3 (Each number separated by space): 7 0 5
	- Automated Data Collection
		- This option allows you to choose a number of randomly generated start states which will automatically be solved using all available algorithms and heuristics (except DFS) and save the results to PuzzleData.csv, which can be found in the same folder where your .py file is stored.

- Choose an Algorithm:
	- Select the algorithm you want to use to solve the puzzle:
		- A* Search (with a choice of heuristics)
		- Breadth-First Search (BFS)
		- Depth-First Search (DFS)
		- Iterative Deepening Depth-First Search (IDDFS)

- Solve the Puzzle:
	- The program will solve the puzzle using the selected algorithm.
	- Once the puzzle is solved, the time taken, total moves attempted, and the actual path moves will be displayed.

- After Solving:
	You can choose to solve another puzzle, run the same start state with a different algorithm, save the moves to a file, or exit the program.
	- Saving Moves to a File:
		- After solving a puzzle, you can save the sequence of moves by selecting the option to save moves to a file.
		- Enter a filename with the .txt extension (e.g., solution.txt).
		- The file will contain the initial state, the sequence of moves, and the resulting states after each move of the current puzzle.
		- The file will be stored in the same folder where this program was run from.
	-If you choose to exit, a summary of all puzzles solved during the session will be displayed in the console.

# Important Notes:
- Solvability Check:	Not all start states are solvable. The program automatically ensures that random and custom states are solvable.
- Performance: 		The time to solve a puzzle may vary depending on the chosen algorithm and the complexity of the start state.
- Error Handling: 	If the program encounters an error while saving to a file, it will print an error message. Make sure the file path and permissions are correct.
- Invalid Input: 	The program validates inputs and will prompt you to try again if the input is invalid or unsolvable.


# Developers
Luz Diaz - https://github.com/Luz-Diaz1 

Uyi Erhabor - https://github.com/ure5001
