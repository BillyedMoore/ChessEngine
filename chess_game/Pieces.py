from .Move import Move


class Piece:
    """
    Abstract class to be implemented by the individual piece type

    Properties:
        position - position of the piece on the board form (x:int, y:int)
        colour - colour of the piece, possible colours {"B","W"}
    Methods:
        get_legal_moves() - returns a list of legal moves
    """
    _colour = None
    _position = (None, None)
    _moved = False
    _letter = "F"

    def __init__(self, position, color):
        self._position = position
        self._colour = color

    @property
    def letter(self) -> str:
        if self.colour.lower() == "w":
            return self._letter.lower()
        if self.colour.lower() == "b":
            return self._letter.upper()
        # TODO raise exception if color isn't in the set {"w","b"}

    @property
    def position(self) -> tuple:
        """
        The current position of the piece on the board in the form (x:int,y:int)
        """
        return self._position

    @position.setter
    def position(self, position) -> None:
        """
        sets the position of the piece
        """
        if type(position) == tuple:
            if len(position) == 2:
                if type(position[0]) == int and type(position[1]) == int:
                    self._position = position

    # TODO: raise an exception if the position isn't valid

    @property
    def colour(self) -> str:
        """
        Representation of the color of the piece "B" for black pieces and "W"
        for white pieces
        """
        return self._colour

    @colour.setter
    def colour_setter(self, colour) -> None:
        if colour.upper() in ["B", "W"]:
            self._colour = colour.upper()

    def get_legal_moves(self, game_state):
        pass

    @colour.setter
    def colour(self, value):
        self._colour = value


class Pawn(Piece):
    """
    Implementation of Piece class
    """

    _letter = "P"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color):
        super().__init__(position, color)

    def get_legal_moves(self, game_state):
        # TODO: implement promotion
        legal_moves = []
        if self.position[1] != 7:
            if game_state.square_is_empty((self.position[0], self.position[1] + 1)):
                legal_moves.append(
                    Move(self.position, (self.position[0], self.position[1] + 1)))
        if self.position[1] == 1:
            if game_state.square_is_empty((self.position[0], self.position[1] + 2)):
                legal_moves.append(
                    Move(self.position, (self.position[0], self.position[1] + 2)))

        return legal_moves


class Bishop(Piece):
    """
    Implementation of Piece class
    """

    _letter = "B"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color):
        super().__init__(position, color)

    def get_legal_moves(self, game_state):
        legal_moves = []
        directions = [(1, -1), (1, 1), (-1, 1), (-1, -1)]

        for direction in directions:
            for i in range(1, 8):
                pos = (self.position[0]+(i*direction[0]),
                       self.position[1]+(i*direction[1]))
                if game_state.square_exists(pos):
                    if game_state.square_is_empty(pos):
                        legal_moves.append(Move(self.position, pos))
                    else:
                        break
        return legal_moves


class Queen(Piece):
    """
    Implementation of Piece class
    """

    _letter = "Q"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color):
        super().__init__(position, color)

    def get_legal_moves(self, game_state):
        return []


class King(Piece):
    """
    Implementation of Piece class
    """

    _letter = "K"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color):
        super().__init__(position, color)

    def get_legal_moves(self, game_state):
        return []


class Rook(Piece):
    """
    Implementation of Piece class
    """

    _letter = "R"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color):
        super().__init__(position, color)

    def get_legal_moves(self, game_state):
        return []


class Knight(Piece):
    """
    Implementation of Piece class
    """

    _letter = "N"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color):
        super().__init__(position, color)

    def get_legal_moves(self, game_state):
        return []
