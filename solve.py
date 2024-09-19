import time
import random
import heapq
import csv
import os
from sys import exit

directions = ['up', 'down', 'right', 'left']

# Creates the board
def init_state(board_as_array, n):
    # Ensure the length of board_as_array is correct and all values are present
    if len(board_as_array) == n * n and set(board_as_array) == set(range(n * n)):
        matrix = tuple(tuple(board_as_array[i:i + n]) for i in range(0, n * n, n))
        return (matrix, -1, -1)  # (matrix, row, column)
    else:
        raise ValueError(f"The array must have exactly {n * n} distinct digits from 0 to {n * n - 1}.")


# Checks for final state
def is_final_state(board, n):
    final_board = tuple(tuple((i * n + j + 1) % (n * n) for j in range(n)) for i in range(n))
    return board == final_board

# Finds the 0 in the board
def find_empty_cell(board):
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == 0:
                return i, j
    raise ValueError("No empty cell found in the board.")

# Determines if the empty cell can move
def can_move(state, direction, n):
    i, j = find_empty_cell(state[0])
    if direction == "up":
        return i > 0 and (i - 1 != state[1])
    elif direction == "down":
        return i < n - 1 and (i + 1 != state[1])
    elif direction == "left":
        return j > 0 and (j - 1 != state[2])
    elif direction == "right":
        return j < n - 1 and (j + 1 != state[2])
    return False

# Swaps the 0 with the cell in the direction it needs to move
def move_cell(board, i, j, direction):
    new_board = [list(row) for row in board]
    if direction == "up":
        new_board[i][j], new_board[i - 1][j] = new_board[i - 1][j], new_board[i][j]
    elif direction == "down":
        new_board[i][j], new_board[i + 1][j] = new_board[i + 1][j], new_board[i][j]
    elif direction == "left":
        new_board[i][j], new_board[i][j - 1] = new_board[i][j - 1], new_board[i][j]
    elif direction == "right":
        new_board[i][j], new_board[i][j + 1] = new_board[i][j + 1], new_board[i][j]
    return tuple(tuple(row) for row in new_board)

# Implements find_empty_cell, checks if can_move, and implements move_cell
def move(state, direction, n):
    board, prev_i, prev_j = state
    i, j = find_empty_cell(board)
    if can_move(state, direction, n):
        new_board = move_cell(board, i, j, direction)
        return new_board, i, j
    return None

# Compute and store the goal positions for each tile to efficiently calculate heuristic distances
def get_goal_positions(n):
    return {value: divmod(value - 1, n) for value in range(1, n * n)}

# Calculates Manhattan Distance Heuristic
def manhattan_distance(state, goal_positions, n):
    board = state[0]
    total_distance = 0
    for i in range(n):
        for j in range(n):
            current_tile = board[i][j]
            if current_tile != 0:
                goal_row, goal_col = goal_positions[current_tile]
                total_distance += abs(i - goal_row) + abs(j - goal_col)
    return total_distance

# Calculates Hamming Distance Heuristic
def hamming_distance(state, goal_positions, n):
    board = state[0]
    goal = tuple(tuple((i * n + j + 1) % (n * n) for j in range(n)) for i in range(n))
    flat_board = [tile for row in board for tile in row]
    flat_goal = [tile for row in goal for tile in row]
    return sum(1 for current_tile, goal_tile in zip(flat_board, flat_goal) if current_tile != 0 and current_tile != goal_tile)

# Calculates Euclidean Distance Heuristic
def euclidean_distance(state, goal_positions, n):
    board = state[0]
    total_distance = 0
    for i in range(n):
        for j in range(n):
            current_tile = board[i][j]
            if current_tile != 0:
                goal_row, goal_col = goal_positions[current_tile]
                total_distance += ((i - goal_row) ** 2 + (j - goal_col) ** 2) ** 0.5
    return total_distance

# Calculates Chebyshev Distance Heuristic
def chebyshev_distance(state, goal_positions, n):
    board = state[0]
    total_distance = 0
    for i in range(n):
        for j in range(n):
            current_tile = board[i][j]
            if current_tile != 0:
                goal_row, goal_col = goal_positions[current_tile]
                total_distance += max(abs(i - goal_row), abs(j - goal_col))
    return total_distance

# A* algorithm with correct heuristic passed in
def a_star(init_state, heuristic, n):
    pq = []
    goal_positions = get_goal_positions(n)
    heapq.heappush(pq, (heuristic(init_state, goal_positions, n), 0, init_state, []))
    visited = set()
    total_moves = 0

    while pq:
        priority, cost, state, path = heapq.heappop(pq)
        total_moves += 1
        if is_final_state(state[0], n):
            return state, path, total_moves  # Return the final state, path, and total moves
        if state in visited:
            continue
        visited.add(state)
        
        for direction in directions:
            neighbor = move(state, direction, n)
            if neighbor and neighbor not in visited:
                new_cost = cost + 1
                new_priority = new_cost + heuristic(neighbor, goal_positions, n)
                new_path = path + [(direction, neighbor)]
                heapq.heappush(pq, (new_priority, new_cost, neighbor, new_path))

    return None

# Breadth-First Search
def bfs(init_state, n):
    queue = [(init_state, [])]
    visited = set()
    total_moves = 0

    while queue:
        state, path = queue.pop(0)
        total_moves += 1  
        if is_final_state(state[0], n):
            return state, path, total_moves  # Return the final state, path, and total moves
        if state in visited:
            continue
        
        visited.add(state)

        for direction in directions:
            neighbor = move(state, direction, n)
            if neighbor and neighbor not in visited:
                queue.append((neighbor, path + [(direction, neighbor)]))
    return None

# Depth-First Search
def dfs(init_state, n):
    stack = [(init_state, [])]
    visited = set()
    total_moves = 0

    while stack:
        state, path = stack.pop()
        total_moves += 1  
        if is_final_state(state[0], n):
            return state, path, total_moves  # Return the final state, path, and total moves
        if state in visited:
            continue

        visited.add(state)

        for direction in directions:
            neighbor = move(state, direction, n)
            if neighbor and neighbor not in visited:
                stack.append((neighbor, path + [(direction, neighbor)]))

    return None  # If no solution is found


# Global variable to track total moves across all depth-limited searches
iddfs_total_moves = 0

# Depth-Limited Search
def dls(state, limit, n):
    return recursive_dls(state, limit, set(), n)

# Recursively implements DLS and tracks total moves
def recursive_dls(state, limit, visited, n):
    global iddfs_total_moves
    if is_final_state(state[0], n):
        return state, []  # Return the final state and an empty path
    
    if limit <= 0:
        return None
    
    visited.add(state)
    for direction in directions:
        neighbor = move(state, direction, n)
        if neighbor and neighbor not in visited:
            iddfs_total_moves += 1  # Increment the global move counter
            result = recursive_dls(neighbor, limit - 1, visited, n)
            if result:
                final_state, path = result
                return final_state, [(direction, neighbor)] + path
    
    visited.remove(state)
    return None

# Iterative Deepening Depth-First Search
def iddfs(init_state, n):
    global iddfs_total_moves
    iddfs_total_moves = 0  # Initialize the move counter
    depth = 0
    accumulated_path = []
    
    while True:
        result = dls(init_state, depth, n)
        if result:
            final_state, path = result
            accumulated_path.extend(path)
            return final_state, accumulated_path, iddfs_total_moves
        depth += 1

# Computes number of inversions
def count_inversions(board_as_array):
    inv_count = 0
    for i in range(len(board_as_array)):
        for j in range(i + 1, len(board_as_array)):
            if board_as_array[i] > board_as_array[j] and board_as_array[i] != 0 and board_as_array[j] != 0:
                inv_count += 1
    return inv_count

# Determines whether a given puzzle is solvable based on even or odd number of inversions
def is_solvable(board_as_array, n):
    inversions = count_inversions(board_as_array)
    if n % 2 != 0:  # Odd grid width
        return inversions % 2 == 0
    else:  # Even grid width
        blank_row_from_bottom = (n - (board_as_array.index(0) // n))
        if blank_row_from_bottom % 2 == 0:
            return inversions % 2 != 0
        else:
            return inversions % 2 == 0

# Checks for duplicate tiles in custom puzzles
def check_duplicates(board):
    flat_list = [item for sublist in board for item in sublist]
    return len(flat_list) != len(set(flat_list))

# Prints the matrix in correct format
def print_matrix(state):
    for row in state:
        print(' '.join(map(str, row)))

# Saves final solution path moves to a file named by the user
def save_moves_to_file(init_state, moves_results, filename):
    try:
        with open(filename, 'w') as file:
            file.write("Initial State:\n")
            for row in init_state:
                file.write(' '.join(map(str, row)) + '\n')
                file.write('\n')
            for move_number, (direction, resulting_state) in enumerate(moves_results, start=1):
                file.write(f"Move: {move_number}\n")
                file.write(f"Direction: {direction}\n")
                file.write("Resulting State:\n")
                for row in resulting_state[0]:
                    file.write(' '.join(map(str, row)) + '\n')
                file.write('\n')
        print(f"Moves have been saved to {filename}.")
    except Exception as e:
        print(f"An error occurred while saving moves to file: {e}")

# Runs all algorithms/heuristics on each puzzle for automated data collection
def run_algorithms_on_state(initial_state, n, results, state_number, total_states):
    print(f"Running tests for puzzle {state_number}/{total_states}: {initial_state[0]}")

    heuristics = {
        "Manhattan Distance": manhattan_distance,
        "Hamming Distance": hamming_distance,
        "Euclidean Distance": euclidean_distance,
        "Chebyshev Distance": chebyshev_distance
    }
    
    algorithms = [
        ("A*", a_star, heuristics),
        ("BFS", bfs, None),
        ("IDDFS", iddfs, None)
    ]
    
    for algo_name, algo_func, algo_heuristics in algorithms:
        if algo_heuristics:
            for heuristic_name, heuristic_func in algo_heuristics.items():
                print(f"Running {algo_name} with {heuristic_name}...")
                start_time = time.time()
                result = algo_func(initial_state, heuristic_func, n)
                end_time = time.time()
                if result:
                    solution, path, total_moves = result
                    num_moves = len(path)
                    results.append((initial_state[0], algo_name, heuristic_name, end_time - start_time, total_moves, num_moves))
        else:
            print(f"Running {algo_name}...")
            start_time = time.time()
            result = algo_func(initial_state, n)
            end_time = time.time()
            if result:
                solution, path, total_moves = result
                num_moves = len(path)
                results.append((initial_state[0], algo_name, None, end_time - start_time, total_moves, num_moves))

# Saves results of automated data collection in PuzzleData.csv file
def save_results_to_csv(results, filename="PuzzleData.csv"):
    # Check if the file already exists
    file_exists = os.path.isfile(filename)
    
    print(f"File exists: {file_exists}, saving results to {filename}")
    
    # Open the file in append mode ('a')
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # If the file does not exist, write the header first
            if not file_exists:
                print("Writing header...")
                writer.writerow(["Puzzle", "Algorithm", "Heuristic", "Time (seconds)", "Total Moves", "Path Moves"])
            
            # Append the results
            for result in results:
                if len(result) == 6:
                    start_state, algo, heuristic, time_taken, total_moves, num_moves = result
                    writer.writerow([start_state, algo, heuristic, time_taken, total_moves, num_moves])
        print("Results successfully saved.")
    except Exception as e:
        print(f"Error while writing to file: {e}")



# Main Program
if __name__ == "__main__":
    
    results = []  # To store results of each puzzle
    print("******************************************************************")
    print("\nWelcome to the n-Puzzle Problem solver by Uyi Erhabor & Luz Diaz.")
    print("\n******************************************************************\n")
    default_n = 3  # Default size
    print("The default puzzle size is 3x3. Do you want to use the default or choose your own size?")
    print("1. Default 3x3")
    print("2. Choose size (Please note: Expect extended wait times for larger puzzles)")
    change_size = input("\nEnter your choice: ")
    if change_size == '2':
        n = int(input("Enter the size of the puzzle (e.g., 4 for 4x4): "))
    else:
        n = default_n

    while True:
        if n == 3:
            # Use hard-coded start states for 3x3 puzzle
            initial_states = {
                "1": [2, 7, 5, 0, 8, 4, 3, 1, 6],
                "2": [8, 6, 7, 2, 5, 4, 0, 3, 1],
                "3": [2, 5, 3, 1, 0, 6, 4, 7, 8]
            }
        else:
            # Random start states for larger puzzles
            initial_states = {}
            for i in range(1, 4):
                while True:
                    state = random.sample(range(n * n), n * n)
                    if is_solvable(state, n):
                        initial_states[str(i)] = state
                        break
        # Defines the goal state as a 2D tuple where tiles are in sequential order with 0 in the last position
        goal_state = tuple(tuple((i * n + j + 1) % (n * n) for j in range(n)) for i in range(n))
        print("\n******************************************************************\n")
        print("\nThe Goal State is:")
        print_matrix(goal_state)
        while True:
            print("\nAvailable Puzzles:")
            for key, value in initial_states.items():
                print(f"{key}: {value}")
        
            print("4. Random Puzzle")
            print("5. Custom Puzzle")
            print("6. Automate Data Collection")
            choice = input("\nEnter your choice: ")
        
            if choice == "4":  # Random start state
                while True:
                    initial_state = random.sample(range(n * n), n * n)
                    if is_solvable(initial_state,n):
                        initial_state = init_state(initial_state, n)  # Correctly initialize the state
                        break  # Ensure the random state is solvable
                break  # Exit the loop with a valid choice
            elif choice == "5": # Custom start state
                custom_loop = True
                while custom_loop:
                    custom_state = [
                        [
                            int(x)
                            for x in input(f"Enter Custom Row {i + 1} (Each number separated by space): ").split()
                        ]
                        for i in range(n)
                    ]
                    flat_custom_state = [item for sublist in custom_state for item in sublist]
                    # Ensures correct amount of tiles entered
                    if len(custom_state) != n or any(len(row) != n for row in custom_state): 
                        print(f"\nOut of range, Matrix must be {n}x{n}, please enter one line at a time: ")
                    # Ensures no tiles are duplicated
                    elif check_duplicates(custom_state): 
                        print("\nCan't repeat same value in tiles. Matrix must be n x n. Please try again")
                    # Ensures there is a blank tile
                    elif 0 not in flat_custom_state:
                        print("\nMatrix must contain the number 0. Please try again.")
                    # Ensures only (n*n)-1 number
                    elif any(tile not in range(n * n) for tile in flat_custom_state): 
                        print(f"\nTiles must be numbers from 0 to {n * n - 1}. Please try again.")
                    else:
                        if is_solvable(flat_custom_state,n):
                            initial_state = init_state(flat_custom_state, n)
                            custom_loop = False  # Exit the loop with a valid, solvable custom state
                        else:
                            print("The custom puzzle is not solvable. Please try again.")
                break  # Exit the loop after a valid custom state is provided
            elif choice == "6": # Automated data collection
                num_states = int(input("Enter the number of different puzzles to test: "))
                print("Solving... This may take a while, please be patient.")
                for i in range(num_states):
                    while True:
                        initial_state = random.sample(range(n * n), n * n)
                        if is_solvable(initial_state,n):
                            initial_state = init_state(initial_state, n)
                            break
                    run_algorithms_on_state(initial_state, n, results, state_number=i+1, total_states=num_states)
                save_results_to_csv(results)
                exit()  # Exit after collecting and saving the data
            elif choice in initial_states:
                initial_state = init_state(initial_states[choice], n)
                break  # Exit the loop with a valid choice
            else:
                print("Invalid choice. Please try again.")

        while True:
            print("\nSelect the algorithm:")
            print("1. A* Search")
            print("2. Breadth-First Search (BFS)")
            print("3. Depth-First Search (DFS)")
            print("4. Iterative Deepening DFS (IDDFS)")

        
            algo_choice = input("\nEnter your algorithm choice: ")
        
            if algo_choice == "2":
                print("Solving using BFS. Please wait...")
                start_time = time.time()
                result = bfs(initial_state, n)
                end_time = time.time()
            elif algo_choice == "3":
                print("Solving using DFS. Please wait...")
                start_time = time.time()
                result = dfs(initial_state, n)
                end_time = time.time()
            elif algo_choice == "1":
                while True:
                    print("\nSelect a heuristic function:")
                    print("1. Manhattan Distance")
                    print("2. Hamming Distance")
                    print("3. Euclidean Distance")
                    print("4. Chebyshev Distance")
        
                    heuristic_choice = input("\nEnter your heuristic choice: ")
        
                    if heuristic_choice == "1":
                        heuristic = manhattan_distance
                        break
                    elif heuristic_choice == "2":
                        heuristic = hamming_distance
                        break
                    elif heuristic_choice == "3":
                        heuristic = euclidean_distance
                        break
                    elif heuristic_choice == "4":
                        heuristic = chebyshev_distance
                        break
                    else:
                        print("Invalid heuristic choice. Please try again.")
            
                print("Solving. Please wait...")
                start_time = time.time()
                result = a_star(initial_state, heuristic, n)
                end_time = time.time()
            elif algo_choice == "4":
                print("Solving using IDDFS. Please wait...")
                start_time = time.time()
                result = iddfs(initial_state, n)
                end_time = time.time()
            else:
                print("Invalid algorithm choice. Please try again.")
                continue
            
            if result:
                solution, path, total_moves = result
                num_moves = len(path)
                if algo_choice == "1":
                    heuristic_name = {"1": "Manhattan Distance", "2": "Hamming Distance", "3": "Euclidean Distance", "4": "Chebyshev Distance"}.get(heuristic_choice, "")
                    print(f"\nPuzzle solved using A* with {heuristic_name} heuristic in about {end_time - start_time:.4f} seconds.")
                    results.append((f"A* with {heuristic_name}", end_time - start_time, total_moves, num_moves))
                elif algo_choice == "4":
                    print(f"\nPuzzle solved using IDDFS in about {end_time - start_time:.4f} seconds.")
                    results.append(("IDDFS", end_time - start_time, total_moves, num_moves))
                else:
                    algo_name = ["BFS", "DFS"][int(algo_choice) - 2]
                    print(f"\nPuzzle solved using {algo_name} in about {end_time - start_time:.4f} seconds.")
                    results.append((algo_name, end_time - start_time, total_moves, num_moves))
                
                print(f"Total moves attempted: {total_moves}")
                print(f"Actual path moves: {num_moves}")            
                
                while True:
                    print("\nWhat would you like to do next?")
                    print("1. Solve another puzzle")
                    print("2. Run the same puzzle with a different algorithm")
                    print("3. Save final path moves to file")
                    print("4. Exit\n")
                    action = input("Enter your choice: ")
                    
                    if action == "1":
                        break  # Exit the loop to solve another puzzle
                    elif action == "2":
                        break  # Exit to choose a different algorithm with the same state
                    elif action == "3":
                        filename = input("Enter the filename to save moves using .txt extension: ")
                        save_moves_to_file(initial_state[0], path, filename)
                    elif action == "4":
                        print("\nSummary of all puzzles solved:\n")
                        for i, (algo, time_taken, total_moves, num_moves) in enumerate(results, 1):
                            print(f"Puzzle {i}:")
                            print(f"Algorithm: {algo}")
                            print(f"Time taken: {time_taken:.4f} seconds")
                            print(f"Total moves attempted: {total_moves}")
                            print(f"Actual path moves: {num_moves}\n")
                        exit()  # Exit the program
                    else:
                        print("\nInvalid choice. Please try again.")
                if action != "2":
                    break  # Exit to choose a new puzzle if not continuing with the same puzzle
            
            else:
                print("No solution found.")
