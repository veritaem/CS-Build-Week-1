import random
class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y
    #def __repr__(self):
    #    return f'(x: {self.x}, y: {self.y}, desc: {self.description}, id: {self.id},  name: {self.name}, n: {self.n_to}, s: {self.s_to}, e: {self.e_to}, w: {self.w_to})'
    
    def __repr__(self):
        return f'{self.x},{self.y}'
    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")
class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
    
    def generate_rooms(self, size_x, size_y, num_rooms):
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range( len(self.grid) ):                                        # make 100 rooms
            self.grid[i] = [None] * size_x


        room_list = []
        dic = []
        room_count = 0


        for i in range(num_rooms):
            room_list.append(Room(room_count, 'generic', 'a room', 0, 0))
            room_count += 1
            choicex = [i for i in range(size_x)]
            choicey = [i for i in range(size_y)]
        for room in room_list:                                                   # give each room an x and y
            x = random.choice(choicex)
            y = random.choice(choicey)
            while self.grid[y][x] is not None:
                x = random.choice(choicex)
                y = random.choice(choicey)
            self.grid[y][x] = room                                                 # add to grid in pos x, y          
            room.x = x
            room.y = y
        #---------------------------------------------------------------------
        #---------------------------------------------------------------------
        #---------------------------------------------------------------------


        counter = 0
        for i in room_list:
            # touch all 100 room
            current = []
            if i.n_to:
                current.append('n')
            if i.s_to:
                current.append('s')
            if i.e_to:
                current.append('e')
            if i.w_to:
                current.append('w')
            compass = ['n', 's', 'e', 'w']
            thing = set(compass) ^ set(current)
            choice = random.choice(list(thing))
            if choice == 'n' and i.y+1 <10:
                connect_rom = self.grid[i.y+1][i.x]
                print(connect_rom, 'THIS IS GRID X Y')
                i.connect_rooms(connect_rom, choice)
            elif choice == 's' and i.y-1 >-1:
                    connect_rom = self.grid[i.y-1][i.x]
                    i.connect_rooms(connect_rom, choice)
            elif choice == 'e' and i.x+1 <10:
                    connect_rom = self.grid[i.y][i.x+1]
                    i.connect_rooms(connect_rom, choice)
            elif choice == 'w' and i.x-1 > -1:
                    connect_rom = self.grid[i.y][i.x-1]
                    i.connect_rooms(connect_rom, choice)

            vari = {'id':i.id, 'description':i.description, 'name':i.name, 'x':i.x, 'y':i.y, 'n':i.n_to, 's':i.s_to, 'e':i.e_to, 'w': i.w_to}
            dic.append(vari)
            counter += 1
        for x, y in enumerate(dic):
            print(x, 'X')
        return dic
w = World()
print(w.generate_rooms(10, 10, num_rooms = 100))