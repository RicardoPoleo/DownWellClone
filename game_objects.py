import pygame


class GameObject:
    """ Generic game object. 
    """

    __slots__ = ("collision_rect", "color") 

    def __init__(self, x, y, height, width, color):
        #Should not be called directly
        self.collision_rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.color: tuple = color

    def has_collided(self, other: "GameObject") -> bool:
        """ Check that two game objects are colliding with one another
        """
        return self.collision_rect.colliderect(other.collision_rect)
    
    def get_y(self):
        return self.collision_rect.y

    def get_x(self):
        return self.collision_rect.x


class Pawn(GameObject):
    """ Pawn game object. 
    """

    __slots__ = ("collision_rect", "speed", "color", "fall_frames", "prev_position")

    def __init__(
            self, 
            x: int, 
            y: int, 
            height: int,
            width: int, 
            color: tuple, 
            speed: int 
    ):
        super().__init__(x, y, height, width, color)
        self.speed = speed
        self.fall_frames: int = 0
        prev_position: tuple[int,int]|None = None

    @classmethod
    def _vector_substraction(
            cls, 
            vector1: tuple[int,int], 
            vector2: tuple[int,int]) -> tuple[int,int]:
        x = vector1[0] - vector2[0]
        y = vector1[1] - vector2[1]
        return (x,y)

    # Might be worth moving all these vector things to a vector class of its own

    ## POSITION VECTORS ##
    
    def _get_relative_position(self, other: "GameObject|Pawn") -> tuple[int,int]:
        """ Get the distance between the pawn and another GameObject.
        Params:
            other: the gameobject to be compared against
        Returns:
            A tuple (x,y) with the position of the "other" object in relation
            to the "self" object.
        """
        self_position = (self.collision_rect.x, self.collision_rect.y)
        other_position = (other.collision_rect.x, other.collision_rect.y)
        relative_position: tuple[int,int] = self._vector_substraction(
                                                        other_position, 
                                                        self_position) 
        return relative_position

    ## MOTION VECTORS ##

    def _get_absolute_motion(self) -> tuple:
        x_movement: int = self.collision_rect.x - self.prev_position[0]
        y_movement: int = self.collision_rect.y - self.prev_position[1]
        return (x_movement, y_movement)

    def _get_relative_motion(self, other: "GameObject|Pawn") -> tuple[int,int]:
        """  Get the vector of the relative motion of two GameObjects.
        Returns:
            A tuple (x,y) with the motion of the "other" object in relation
            to the "self" object.
        """
        self_motion = self._get_absolute_motion() 
        if other is Pawn:
            other_motion = other._get_absolute_motion()
        else:
            other_motion = (0,0)

        return_tuple = self._vector_substraction(other_motion, self_motion)
        return return_tuple

    ## COLLISION ##

    def _get_collision_dir(self, other: "GameObject|Pawn") -> None:
        """ Determine the direction from which a collision happened
        """
        relative_position: tuple [int,int] = self._get_relative_position(other)
        relative_motion: tuple [int,int] = self._get_relative_motion(other)
        
        # if relative_position[0] is negative, left, otherwise right
        # if relative_position[1] is negative, down, otherwise up
        return 

    #Not sure if I will use this
    def _is_grounded(self, other: "GameObject") -> bool:
        """ Determine if the player is falling and how long it's been falling for.
        Returns:
            Whether or not the pawn is currently grounded by the other GameObject
        """
        return self.collision_rect.colliderect(other.collision_rect)
   
   # All of this not done
    def check_collision(self,other):
        """"""

    def check_all_collisions(self, others: list["GameObject"]) -> list["GameObject"]|None:
        colliding_objects: list["GameObject"] = []
        for other in others:
            if self.has_collided(other):
                match 
                colliding_objects.append(other)
        return colliding_objects

    def move(self, direction: dict):
        movement = {"left": (-1,0), "right": (1,0), "up": (0,1)}


class Controller():
    __slots__ = ("pawn", "up", "down", "left", "right")

    def __init__(
            self, 
            pawn, 
            up = pygame.K_UP, 
            down = pygame.K_DOWN, 
            left = pygame.K_LEFT, 
            right = pygame.K_RIGHT):

        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.pawn: Pawn = pawn

    def listen(self):
        """ Get all inputs and move pawn accordingly
        """
        # Gets all the keys that have been pressed in this cycle
        keys = pygame.key.get_pressed()
         
        if keys[self.left]:
            player.x -= player.speed
        if keys[self.right]:
            player.x += player.speed
        if keys[self.up]:
            player.y -= player.speed
        pass


class GameInstance:
    """ Manager class for a game session"""
    
    __slots__ = ("window_width", "window_height", "game_objects", "pawns", "controllers")

    def __init__(self, window_width = 500, window_height = 1000):
        self.window_width: int = window_width
        self.window_height: int = window_height
        game_objects: list["GameObject"] = []
        pawns: list[Pawn] = []      
        controllers: list[Controller] = []

    def create_game_object(self, x, y, height, width, color) -> GameObject:
        """ Creates a new GameObject and adds it to the list of spawned Gameobjects
        Params:
            x: Position on the X axis at spawn
            y: Position on the Y axis at spawn
            height: height of collision box
            width: width of collision box
            color: color of GameObject
        Returns:
            The spawned GameObject
        """
        new_game_object = GameObject(x, y, height, width, color)
        self.game_objects.append(new_gameobject)
        return new_game_object 

    def create_player(
            self, 
            x: int = 50, 
            y: int|None = None, 
            height: int = 30,
            width: int= 30, 
            color: tuple = (255,0,0), 
            speed: int = 5) -> tuple[Pawn,Controller]:
        """ Creates a new pawn and sets it as the the representation of the player
        Params:
            x: Position on the X axis at spawn
            y: Position on the Y axis at spawn
            height: height of collision box
            width: width of collision box
            color: color of actor
            speed: movement speed (does not affect gravity)
        Returns:
            Pawn instantiated and set as player.
        """
        if y is None:
            y = (self.window_width - width) // 2
        new_player = Pawn(x, y, height, width, color, speed)
        self.game_objects.append(new_player)
        self.pawns.append(player)
        new_controller = Controller(new_player)
        return (new_player, new_controller)

    # None of this is really done
    def _check_pawns_falling(self) -> None:
        for pawn in self.pawns:
            pawn._update_fall_frames()

    def update(self) -> None:
        for pawn in self.pawns:
            if not pawn.is_moving:
                continue
            pawn.check_all_collisions(self.game_objects)

