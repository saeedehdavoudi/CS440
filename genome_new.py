import time

t = time.process_time()
text_file = open("input.txt", "r")
main_start = text_file.read().split('\n')  # our start position
text_file.close()
new_start = []
main_end = []

for line in main_start:
    if line.strip():  # line contains eol character(s)
        n = int(line)  # assuming single integer on each line
        new_start.append(n)

new_end = list(sorted(new_start))
main_end = list(map(str, new_end))  # our end position


def transposition(array, pos1, pos2, pos3):
    p1 = pos1 - 1
    p2 = pos2 - 1
    p3 = pos3 - 1

    a = array[p1:p2 + 1]
    b = array[p2 + 1:p3 + 1]
    return list(array[:p1]) + list(b) + list(a) + list(array[p3 + 1:])


class Node:
    def __init__(self, parent=None, position=None):

        if position is None:
            position = []
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0


def a_star_algorithm(start, end):
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = 0
    start_node.h = 0
    end_node = Node(None, end)
    end_node.h = 0
    end_node.g = 0
    print("start is: " + str(start_node.position))
    print("end is: " + str(end_node.position))

    for z in range(len(start_node.position)):
        s = end_node.position.index(start_node.position[z])
        if s >= z:
            start_node.h = start_node.h + (s - z)
        elif s < z:
            start_node.h = start_node.h + (z - s)
    start_node.f = start_node.h
    print("start node f is: " + str(start_node.f))

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]

        print("--------the first node is:" + str(current_node.position))
        print("f default is: " + str(current_node.f))
        for item in open_list:
            if item.f < current_node.f:
                current_node = item
        print("the lowest f is: " + str(current_node.f))
        print("current node is: " + str(current_node.position) + str(current_node.g))

        # Pop current off open list, add to closed list
        open_list.remove(current_node)
        closed_list.append(current_node)
        for i in closed_list:
            print("close list is: " + "child:" + str(i.position) + " f:" + str(i.f) + " g:" + str(i.g))

        # Found the goal
        if current_node.position == end_node.position:

                current = current_node
                path = []
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                    f = open("output.txt", "w")
                    f.write(str(len(path) - 1))
                return "The optimal number of transpositions is: " + str(len(path) - 1)

        # Generate children
        children = []

        for i in range(1, len(current_node.position)):
            for j in range(i, len(current_node.position)):
                for k in range(j + 1, len(current_node.position) + 1):
                    # Create new node
                    new_node = Node(current_node, transposition(current_node.position, i, j, k))

                    # Append
                    children.append(new_node)

        # Loop through children
        for child in children:
            print("child is: " + str(child.position) + " and its parent is: " + str(child.parent.position))

            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            for z in range(len(child.position)):
                s = end_node.position.index(child.position[z])
                if s >= z:
                    child.h = child.h + (s - z)
                elif s < z:
                    child.h = child.h + (z - s)
            print("h is: " + str(child.h))

            child.g = child.parent.g + 1
            print("g is: " + str(child.g))

            child.f = child.g + child.h
            print("f child is: " + str(child.f))

            # Child is already in the open list
            for open_child in open_list:
                if child == open_child and child.g >= open_child.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


if __name__ == "__main__":
    print(a_star_algorithm(main_start, main_end))

    elapsed_time = time.process_time() - t
    print(elapsed_time)
