from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
import heapq
from collections import deque

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

#dict of mapped rooms/vertex
mapped_rooms = {}

#queue
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

#bfs to search path 
def bfs(cur_room, dest):
    q = deque()
    visited = set()
    q.appendleft([cur_room]) #list of room ids keeps gettting appended

    while len(q) > 0:
        current_path = q.pop()
        current_node = current_path[-1] #this is the room id

        #check if in current nodes dictionary
        if dest in mapped_rooms[current_node].values():
            return current_path

        if current_node not in visited:
            visited.add(current_node)

            # get neighbors add to queue
            for neighbor in mapped_rooms[current_node].values():
                new_path = current_path.copy()
                new_path.append(neighbor)
                q.appendleft(new_path)
    return None

def get_opposite(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    else:
        return 'e'

#add first room to stack
s = deque([player.current_room.id])

while len(s) > 0:
    current_room = s.pop()
    if current_room not in mapped_rooms:
        mapped_rooms[player.current_room.id] = {key: '?' for key in player.current_room.get_exits()}
        # check values
        if current_room in mapped_rooms:
            if '?' in mapped_rooms[current_room].values():
                for k, v in mapped_rooms[current_room].items():
                    if v == '?':
                        player.travel(k)
                        traversal_path.append(k)
                        new_room = player.current_room.id
                        #creat key of new room with value of old room dir
                        if new_room not in mapped_rooms:
                            mapped_rooms[new_room] = {key: '?' for key in player.current_room.get_exits()}
                        #update values for directions to and from in new/old keys for rooms
                        mapped_rooms[current_room][k] = new_room
                        mapped_rooms[new_room][get_opposite(k)] = current_room
                        #apend new room player is in s
                        s.append(new_room)
                        break
                    else:
                        pass
            # finished with room
            else:
                #next path
                if current_room != player.current_room.id:
                    print(f'Error check this room: {current_room}, {player.current_room.id}')
                path = bfs(current_room, '?')

                if path is not None:
                    # translate the path to movements
                    for node in path[1:]:
                        try:
                            for k, v in mapped_rooms[current_room].items():
                                if v == node:
                                    player.travel(k)
                                    traversal_path.append(k)
                                    current_room = player.current_room.id
                        except KeyError:
                            print(f'{traversal_path} = traversal path')
                            print(f'pathlength = {len(traversal_path)}, dictlen{len(mapped_rooms)}')
                            print(mapped_rooms)
                            print('KEYERROR')
                    if current_room not in s:
                        s.append(current_room)

                else:
                    #search cant get any additional ?
                    print(f'traversal path = {traversal_path} \n length = {len(traversal_path)}')
                    break


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
