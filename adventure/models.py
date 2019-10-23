from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid

class World(models.Model):
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
            vari = {'id':i.id, 'desc':i.description, 'name':i.name, 'x':i.x, 'y':i.y, 'n':[i.n_to], 's':[i.s_to], 'e':[i.e_to], 'w':[i.w_to]}
            dic.append(vari)
            counter += 1

        print(self.grid)
        return dic
w = World()
print(w.generate_rooms(10, 10, num_rooms = 100))

class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
            elif direction == "s":
                self.s_to = destinationRoomID
            elif direction == "e":
                self.e_to = destinationRoomID
            elif direction == "w":
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()
    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()
    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()





