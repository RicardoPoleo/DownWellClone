import pygame
import typing   #For extended typehinting

GRAVITATIONAL_FORCE = 9.81

class GameObject():
    """ Generic game object. 
    """

    __slots__ = ("rect", "color") 

    def __init__(self, x, y, height, width, color):
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.color: tuple = color

    def has_collided(self, other: "GameObject") -> bool:
        """ Check that two game objects are colliding with one another
        """
        return self.rect.colliderect(other.rect)
    
    def get_y(self):
        return self.rect.y

    def get_x(self):
        return self.rect.x


class Pawn(GameObject):
    """ Pawn game object. 
    """

    __slots__ = (
        "rect", 
        "speed", 
        "color",
        "fall_frames",
        "prev_position",
        "window",
        "cur_collisions",
        "frames_falling",
        "weight",
    )

    def __init__(
        self, 
        x: int, 
        y: int, 
        height: int,
        width: int, 
        color: tuple, 
        speed: int,
        window: "None|pygame.surface.Surface" = None,
        weight: int = 1 
    ):
        self.window = window
        super().__init__(x, y, height, width, color)
        self.speed = speed
        self.fall_frames: int = 0
        self.cur_collisions: typing.Dict[GameObject, pygame.math.Vector2] = {}
        self.frames_falling = 1
        self.weight: float = 0.1
    
    def check_all_collisions(
        self,
        others: list["GameObject"]
    ) -> typing.Dict["GameObject", pygame.math.Vector2]:
        """ Checks to see which GameObjects a pawn is currently colliding with
        and what distance from the pawn they are
        
        Params:
            others: a list of GameObjects to be checked against
        Returns:
            A dictionary with GameObject: Vector pairs where the vector corresponds
            to the distance of the GameObject to the pawn in (x,y) form
        """
        colliders_distance: typing.Dict["GameObject", pygame.math.Vector2] = {} 
        for other in others:
            if other == self:
                continue
            if self.has_collided(other):
                y_distance = self.rect.height + self.rect.y - other.rect.y
                x_distance = self.rect.width + self.rect.x - other.rect.x
                colliders_distance[other] = pygame.math.Vector2(x_distance, y_distance) 
                print(colliders_distance)
        self.cur_collisions = colliders_distance
        return colliders_distance


    def move(self, direction: dict):

        is_grounded: bool = False
        #Check for collisions
        for collision in self.cur_collisions:
            y_col = self.cur_collisions[collision].y
            x_col = self.cur_collisions[collision].x

            if y_col < 20:
                direction["down"] = 0
                self.rect.y = int(self.rect.y - y_col + 1)
                self.frames_falling = 0
                is_grounded = True
            elif y_col > (self.rect.height + collision.rect.height - 20):
                direction["up"] = 0
                #self.rect.y = int(self.rect.y + y_col)

            if x_col < 10:
                direction["right"] = 0
            elif x_col > (self.rect.width + collision.rect.width - 10):
                direction["left"] = 0

        if not is_grounded: self.frames_falling += 1
        
        #Calculate projected direction
        x_new_location = self.rect.x + direction["left"] + direction["right"]
        y_new_location = self.rect.y + direction["up"] + direction["down"]

        #Check movement to be within bounds
        is_within_x = 0 < x_new_location < (self.window.get_width() - self.rect.width)
        is_within_y = 0 < y_new_location < (self.window.get_height() - self.rect.height)

        #Validate movement
        if is_within_x: 
            self.rect.x = x_new_location
        if is_within_y: 
            self.rect.y = y_new_location


class Controller():
    """ Deals with the movement forces applied to a pawn, including player input
    and gravitational pull.

    Attributes:
        pawn: Object to be controlled by controller.
        up_key: Key that maps unto the "up" direction
        down_key: Key that maps unto the "down" direction
        left_key: Key that maps unto the "left" direction
        right_key: Key that maps unto the "right" direction
    """
    __slots__ = ("pawn", "up_key", "down_key", "left_key", "right_key")

    def __init__(
        self, 
        pawn: Pawn|None = None, 
        up_key = pygame.K_UP, 
        down_key = pygame.K_DOWN, 
        left_key = pygame.K_LEFT, 
        right_key = pygame.K_RIGHT,
    ):

        self.up_key = up_key
        self.down_key = down_key
        self.left_key = left_key
        self.right_key = right_key
        self.pawn: Pawn|None = pawn

    def attach(self, pawn: Pawn):
        """ Attach to Pawn
        """
        if not isinstance(pawn, Pawn):
            raise TypeError("Can only attach Pawns to controllers")
        self.pawn = pawn

    def is_attached(self):
        """ Check whether or not the controller is attached to a Pawn
        """
        return self.pawn is not None

    def listen(self) -> None:
        """ Get all inputs and move pawn accordingly
        Raises:
            AttributeError if the controller is not attached
        """
        
        if not self.is_attached:
            raise AttributeError("Controller must be attached to a pawn to listen")

        movement_dict = {"left": 0, "up": 0, "right": 0, "down": 0} 

        # Gets all the keys that have been pressed in this cycle
        keys = pygame.key.get_pressed()

        if keys[self.left_key]:
            movement_dict["left"] -= self.pawn.speed 
        if keys[self.right_key]:
            movement_dict["right"] += self.pawn.speed 
        if keys[self.up_key]:                           #To be replaced with jump
            movement_dict["up"] -= self.pawn.speed 
        if keys[self.down_key]:                         
            movement_dict["down"] += self.pawn.speed           #To be replaced with shooting ?     

        movement_dict["down"] += min( int(GRAVITATIONAL_FORCE * self.pawn.frames_falling/30), 40)

        self.pawn.move(movement_dict)               #type: ignore (Type was checked before)


class GameInstance:
    """ Manager class for a game session"""
    
    __slots__ = ("game_objects", "pawns", "controllers", "window")

    def __init__(self):
        self.window: "None|pygame.surface.Surface" = None
        self.game_objects: list["GameObject"] = []
        self.pawns: list[Pawn] = []      
        self.controllers: list[Controller] = []

    def create_game_object(self, x, y, height, width, color) -> GameObject:
        """ Creates a new GameObject and adds it to the list of spawned 
        Gameobjects.

        Params:
            x: Position on the X axis at spawn
            y: Position on the Y axis at spawn
            height: height of collision box
            width: width of collision box
            color: color of GameObject
        Returns:
            The spawned GameObject
        """
        new_gameobject = GameObject(x, y, height, width, color)
        self.game_objects.append(new_gameobject)
        return new_gameobject 

    def start_window(self, width: int = 500, height: int = 1000) -> None:
        """ Initialize the window surface
        Params:
            width: width of window
            height: height of window
        Returns:
            None 
        """
        self.window = pygame.display.set_mode((width,height))
        

    def create_player(
        self, 
        x: int = None,
        y: int|None = 0, 
        height: int = 100,
        width: int= 50, 
        color: tuple = (255,0,0), 
        speed: int = 5
    ) -> Pawn:
        """ Creates a new pawn and sets it as the the representation of the
        player.
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
        if x is None:
            x = (self.window.get_width() - width) // 2
        new_player = Pawn(x, y, height, width, color, speed, self.window)
        self.game_objects.append(new_player)
        self.pawns.append(new_player)
        return (new_player)

    # None of this is really done
    def update_collisions(self) -> None:
        """ Run through all possible collisions in scene for each pawn.
        """
        for pawn in self.pawns:
            pawn.check_all_collisions(self.game_objects)

