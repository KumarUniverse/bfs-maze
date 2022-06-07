# By Akash Kumar and Dr. Burns

import time
from collections import deque

class Maze():
    """A pathfinding problem."""

    possible_directions = ['N', 'S', 'E', 'W']
    dirs_to_moves = {'N':(-1,0), 'S':(1,0), 'E':(0,1), 'W':(0,-1)}
    moves_to_dirs = {value:key for key, value in dirs_to_moves.items()}

    def __init__(self, grid, location):
        """Instances differ by their current agent locations."""
        self.grid = grid
        self.location = location  # Tuple containing x, y coords.

    def display(self):
        """Print the maze, marking the current agent location."""
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if (r, c) == self.location:
                    print('\033[96m*\x1b[0m', end=' ')   # print a blue *
                else:
                    print(self.grid[r][c], end=' ')      # prints a space or wall
            print()
        print()

    def moves(self):
        """Return a list of possible moves given the current agent location."""
        # YOU FILL THIS IN
        move_list = []
        for direction in Maze.possible_directions:
            move = Maze.dirs_to_moves[direction]
            if (0 <= (self.location[0]+move[0]) < len(self.grid) and
                    0 <= (self.location[1]+move[1]) < len(self.grid[0]) and
                    self.grid[self.location[0]+move[0]][self.location[1]+move[1]] != 'X'):
                move_list.append(direction)

        return move_list

    def neighbor(self, move):
        """Return another Maze instance with a move made."""
        # YOU FILL THIS IN
        move_coord = Maze.dirs_to_moves[move]
        return Maze(self.grid, (self.location[0]+move_coord[0], self.location[1]+move_coord[1]))

class Agent():
    """Knows how to find the exit to a maze with BFS."""

    # Keep track of previously visited locations.
    visited_locations = set()

    class Node():
        """The Node class is used to create a BFS tree to make path tracing efficient."""

        def __init__(self, data, parent=None):
            self.data = data
            self.children = []
            self.parent = parent  # parent is a Node reference to the child's parent.

    def bfs(self, maze, goal):
        """Return an ordered list of moves to get the maze to match the goal."""
        # YOU FILL THIS IN
        initial_maze_location = maze.location
        root = Agent.Node(maze.location)  # The root node has no parent.
        node = None
        frontier = deque([(root, maze.location)])  # The frontier is a queue.
        Agent.visited_locations = set()
        Agent.visited_locations.add((initial_maze_location))

        # Keep popping nodes from the frontier until the node popped is the goal node
        # or we run out of nodes to pop.
        while frontier:
            node, maze.location = frontier.popleft()
            if maze.location == goal.location:
                break
            possible_moves = [Maze.dirs_to_moves[direction] for direction in maze.moves()]
            for move in possible_moves:
                new_coord = (maze.location[0]+move[0], maze.location[1]+move[1])
                if new_coord in Agent.visited_locations:
                    continue
                child_node = Agent.Node(new_coord,node)
                node.children.append(child_node)
                frontier.append((child_node, new_coord))
                Agent.visited_locations.add(new_coord)
        # Reset the location in the maze back to the start position.
        maze.location = initial_maze_location

        # Get the path from the start to the goal node by traversing up the tree, all the way to root.
        path_moves = []
        while node:
            path_moves.append(node.data)
            node = node.parent
        path_moves.reverse()

        # Convert the path moves to path directions.
        path_directions = []
        for i in range(len(path_moves)-1):
            path_directions.append(Maze.moves_to_dirs[(path_moves[i+1][0]-path_moves[i][0],
                                                       path_moves[i+1][1]-path_moves[i][1])])

        return path_directions

    def get_visited_locations(self):
        return Agent.visited_locations.copy()

    def get_num_explored_nodes(self):
        """Return the total number of explored nodes."""
        return len(Agent.visited_locations)



def main():
    """Create a maze, solve it with BFS, and console-animate."""

    grid = ["XXXXXXXXXXXXXXXXXXXX",
            "X     X    X       X",
            "X XXXXX XXXX XXX XXX",
            "X       X      X X X",
            "X X XXX XXXXXX X X X",
            "X X   X        X X X",
            "X XXX XXXXXX XXXXX X",
            "X XXX    X X X     X",
            "X    XXX       XXXXX",
            "XXXXX   XXXXXX     X",
            "X   XXX X X    X X X",
            "XXX XXX X X XXXX X X",
            "X     X X   XX X X X",
            "XXXXX     XXXX X XXX",
            "X     X XXX    X   X",
            "X XXXXX X XXXX XXX X",
            "X X     X  X X     X",
            "X X XXXXXX X XXXXX X",
            "X X                X",
            "XXXXXXXXXXXXXXXXXX X"]

    maze = Maze(grid, (1, 1))
    maze.display()

    agent = Agent()
    goal = Maze(grid, (19, 18))
    path = agent.bfs(maze, goal)

    while path:
        move = path.pop(0)
        maze = maze.neighbor(move)
        time.sleep(0.50)
        maze.display()

    # Time and space analysis of BFS:
    '''
    num_runs = 1000

    # Grid 1 time and space:
    grid1_total_time = 0
    for i in range(num_runs):
        grid1_start_time = time.time()
        path = agent.bfs(maze, goal)
        grid1_end_time = time.time()
        grid1_time_elapsed = grid1_end_time - grid1_start_time
        grid1_total_time += grid1_time_elapsed
    print("Grid 1: ")
    print("Time taken to find the solution path using BFS: %.3f µs." % (grid1_total_time/num_runs * 10**6))
    print("Total number of nodes explored: " + str(agent.get_num_explored_nodes()))
    print("Length of the solution path: " + str(len(path)) + "\n")

    # Grid 2 time and space:
    grid2 = ['XXXXXX', 'X   XX', 'X X XX', 'X X XX', 'XXXXXX', 'XXXXXX']
    maze = Maze(grid2, (1,1))
    goal = Maze(grid2, (3,3))
    grid2_total_time = 0
    for i in range(num_runs):
        grid2_start_time = time.time()
        path = agent.bfs(maze, goal)
        grid2_end_time = time.time()
        grid2_time_elapsed = grid2_end_time - grid2_start_time
        grid2_total_time += grid2_time_elapsed
    print("Grid 2: ")
    print("Time taken to find the solution path using BFS: %.3f µs." % (grid2_total_time/num_runs * 10**6))
    print("Total number of nodes explored: " + str(agent.get_num_explored_nodes()))
    print("Length of the solution path: " + str(len(path)) + "\n")
    #print("Visited nodes: " + str(agent.get_visited_locations()))

    # Grid 3 time and space:
    grid3 = ['XXXXXX', 'X   XX', 'X XXXX', 'X   XX', 'X X XX', 'X X XX', 'X X XX', 'X X XX', 'X XXXX', 'X   XX', 'XXXXXX', 'XXXXXX']
    maze = Maze(grid3, (1, 1))
    goal = Maze(grid3, (9, 3))
    grid3_total_time = 0
    for i in range(num_runs):
        grid3_start_time = time.time()
        path = agent.bfs(maze, goal)
        grid3_end_time = time.time()
        grid3_time_elapsed = grid3_end_time - grid3_start_time
        grid3_total_time += grid3_time_elapsed
    print("Grid 3: ")
    print("Time taken to find the solution path using BFS: %.3f µs." % (grid3_total_time/num_runs * 10**6))
    print("Total number of nodes explored: " + str(agent.get_num_explored_nodes()))
    print("Length of the solution path: " + str(len(path)) + "\n")

    # Grid 4 time and space:
    grid4 = ['XXXXXXXXXX', 'X     X XX', 'X X XXX XX', 'X X     XX', 'X XXXXXXXX', 'X       XX', 'X XXXXXXXX', 'X       XX', 'XXXXXXXXXX', 'XXXXXXXXXX']
    maze = Maze(grid4, (1, 1))
    goal = Maze(grid4, (7, 7))
    grid4_total_time = 0
    for i in range(num_runs):
        grid4_start_time = time.time()
        path = agent.bfs(maze, goal)
        grid4_end_time = time.time()
        grid4_time_elapsed = grid4_end_time - grid4_start_time
        grid4_total_time += grid4_time_elapsed
    print("Grid 4: ")
    print("Time taken to find the solution path using BFS: %.3f µs." % (grid4_total_time/num_runs * 10**6))
    print("Total number of nodes explored: " + str(agent.get_num_explored_nodes()))
    print("Length of the solution path: " + str(len(path)) + "\n")

    # Grid 5 time and space:
    grid5 = ['XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'X                                                                              X',
             'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX X']
    maze = Maze(grid5, (1, 1))
    goal = Maze(grid5, (79, 39))
    grid5_total_time = 0
    for i in range(num_runs):
        grid5_start_time = time.time()
        path = agent.bfs(maze, goal)
        grid5_end_time = time.time()
        grid5_time_elapsed = grid5_end_time - grid5_start_time
        grid5_total_time += grid5_time_elapsed
    print("Grid 5: ")
    print("Time taken to find the solution path using BFS: %.3f µs." % (grid5_total_time / num_runs * 10 ** 6))
    print("Total number of nodes explored: " + str(agent.get_num_explored_nodes()))
    print("Length of the solution path: " + str(len(path)) + "\n")
    '''

if __name__ == '__main__':
    main()
