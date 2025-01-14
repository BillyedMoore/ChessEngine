from . import GameState


class BaseMove:
    """
    A class to represent a move.
    Move is not aware of the game board ∴ doesn't validate anything.

    Properties:
        position_from - The current location of the piece
        position_to - Were the piece will be moved to
    """
    file_values = ["a", "b", "c", "d", "e", "f", "g", "h"]
    rank_values = ["8", "7", "6", "5", "4", "3", "2", "1"]
    performed = False
    _pos_after_move = ""

    def __init__(self, gamestate):
        self._gamestate = gamestate

    def clone(self):
        pass

    @staticmethod
    def is_valid_position(position: tuple):
        for i in position:
            if type(i) != int:
                return False
            if i in range(0, 8):
                return True

    def print(self):
        pass

    def perform(self):
        """
        Perform the move on the 'gamestate'
        """
        pass

    def unperform(self):
        if not self._gamestate._moves.peek() == self:
            raise Exception("Can only unperform the last move.")
        self._unperform()

    def _unperform(self):
        pass

    @property
    def gamestate(self):
        return self._gamestate

    @gamestate.setter
    def gamestate(self, gamestate):
        self._gamestate = gamestate

    @ property
    def promotion(self):
        return (type(self) == PromotionMove)

    @ property
    def normal(self):
        return (type(self) == Move)

    @ property
    def castling(self):
        return (type(self) == CastlingMove)

    @staticmethod
    def coord_to_pos(coord):
        try:
            return (BaseMove.file_values.index(coord[0]), BaseMove.rank_values.index(coord[1]))
        except ValueError:
            return None

    @staticmethod
    def pos_to_coord(pos):
        return f"{BaseMove.file_values[pos[0]]}{BaseMove.rank_values[pos[1]]}"

    @staticmethod
    def from_algebraic_notation(gamestate, colour_moving, algebraic_move):
        """
        returns a Move formulated from an algebraic notation
        """
        # This is the worst function I have ever written
        piece_letters = ["R", "N", "P", "B", "K", "Q"]

        def get_king(colour):
            king = [p for p in gamestate.get_pieces_by_colour(colour)
                    if p.letter.upper() == "K"][0]
            return king

        if not algebraic_move:
            return None

        # ignore captures and checks as not relevant or helpful
        algebraic_move = "".join(
            [char for char in algebraic_move if char != "+" and char != "x"])

        # if no piece is stated then a pawn is moving
        if algebraic_move[0] in BaseMove.file_values:
            algebraic_move = "P" + algebraic_move

        # denotes a promotion move
        if "=" in algebraic_move:
            # pos = algebraic_move[-2:]
            # coord = BaseMove.coord_to_pos(pos)
            # splice = algebraic_move[1:-2]
            promote_to_letter = algebraic_move[-1]
            promote_to = GameState.GameState.piece_letters[promote_to_letter.lower(
            )]
            algebraic_move = algebraic_move.split("=")[0]
            # return PromotionMove(gamestate, coord, promote_to=promote_to_class)

        if algebraic_move[0] in piece_letters:
            coord = BaseMove.coord_to_pos(algebraic_move[-2:])
            if not coord:
                return None
            possible_moves = [
                m for m in gamestate.get_legal_moves(colour_moving)
                if (type(m) == Move or type(m) == PromotionMove) and
                m.position_to == coord
                and gamestate.get_square(m.position_from).get_piece().letter.upper() == algebraic_move[0]]
            if len(possible_moves) >= 1:
                splice = algebraic_move[1:-2]
                if len(splice) == 2:
                    possible_moves = [
                        m for m in possible_moves if m.position_from == BaseMove.coord_to_pos(splice)]
                    if len(possible_moves) != 1:
                        return None
                    else:
                        return possible_moves[0]
                elif len(splice) == 0:
                    if len(possible_moves) != 1:
                        return None
                    else:
                        return possible_moves[0]
                elif len(splice) == 1:
                    possible_moves_cpy = list(possible_moves)
                    possible_moves = []
                    if splice in BaseMove.file_values:
                        for m in possible_moves_cpy:
                            if m.position_from[0] == BaseMove.file_values.index(splice):
                                possible_moves.append(m)

                        if len(possible_moves) != 1:
                            return None
                        else:
                            return possible_moves[0]
                    if splice in Move.rank_values:
                        for m in possible_moves_cpy:
                            if m.position_from[1] == Move.rank_values.index(splice):
                                possible_moves.append(m)
                        if len(possible_moves) != 1:
                            return None
                        else:
                            return possible_moves[0]
                else:
                    return None

        elif algebraic_move.strip() == "O-O":
            king = get_king(colour_moving)
            return CastlingMove(gamestate, king.position, "k")
        elif algebraic_move.strip() == "O-O-O":
            king = get_king(colour_moving)
            return CastlingMove(gamestate, king.position, "q")
        else:
            pass


class Move(BaseMove):
    # set to the piece captured in this move if one is to allow move to be undone
    _captured_piece = None

    def __init__(self, gamestate, from_pos, to_pos, en_passant=None):
        super().__init__(gamestate)
        self.en_passant = en_passant
        self._position_from = from_pos
        self._position_to = to_pos
        self.moving_piece = self._gamestate.get_square(
            self.position_from)._piece

    def print(self):
        print(f"Move - {self.position_from} -> {self.position_to}")

    def clone(self):
        return Move(self.gamestate, self.position_from, self.position_to)

    @ property
    def captured(self):
        return self._captured_piece

    @ captured.setter
    def captured(self, piece):
        self._captured_piece = piece

    def is_legal_move(self):
        square_from = self._gamestate.get_square(self.position_from)
        piece = square_from.get_piece()
        square_to = self._gamestate.get_square(self.position_to)
        formated_moves = [(m.position_from, m.position_to)
                          for m in self.gamestate.get_legal_moves(piece.colour) 
                          if m.normal]
        return ((square_from.position, square_to.position) in formated_moves)

    def perform(self):
        square_from = self._gamestate.get_square(self.position_from)
        square_to = self._gamestate.get_square(self.position_to)
        move_to = square_to
        if self.en_passant:
            print("making enpassant move")
            square_to = self.gamestate.get_square(self.en_passant)
        piece = square_from.pop_piece()
        if not self._gamestate.square_is_empty(square_to.position):
            captured_piece = square_to.pop_piece()
            self._captured_piece = (captured_piece)
        piece.make_move(move_to.position)
        move_to.set_piece(piece)

    def _unperform(self):
        square_from = self.get_square(self.position_from)
        square_to = self.get_square(self.position_to)
        piece = square_to.pop_piece()
        if self.en_passant:
            en_passant = self.get_square(self.en_passant)
            en_passant.set_piece(self.captured)
        if self.captured:
            square_to.set_piece(self.captured)
        piece.forget_move()
        square_from.set_piece(piece)

    @ property
    def position_from(self):
        return self._position_from

    @ position_from.setter
    def position_from(self, pos):
        if self.is_valid_position(pos):
            self._position_from = pos

    @ property
    def position_to(self):
        return self._position_to

    @ position_to.setter
    def position_to(self, pos):
        if self.is_valid_position(pos):
            self._position_to = pos

    def to_algebraic_notation(self):
        piece = self.moving_piece
        if not piece:
            return None
        return f"{piece.letter.upper()}{BaseMove.pos_to_coord(self.position_from)}{BaseMove.pos_to_coord(self.position_to)}"


class CastlingMove(BaseMove):
    _king_pos = (-1, -1)
    _side = ""

    def __init__(self, gamestate, king_pos, side):
        super().__init__(gamestate)
        self.king_position = king_pos
        self.side = side
        directions = {"q": -1, "k": 1}
        rook_positions = {
            "q": (0, self._king_pos[1]), "k": (7, self._king_pos[1])}
        self._king_to_pos = ((self.king_position[0] +
                              2*directions[self.side.lower()]), self.king_position[1])
        self._rook_to_pos = ((self.king_position[0] +
                              directions[self.side.lower()]), self.king_position[1])
        self._rook_from_pos = rook_positions[self.side.lower()]

    def clone(self):
        return CastlingMove(self.gamestate, self.king_position, self.side)

    def is_legal_move(self):
        # print(self.king_position)
        square = self._gamestate.get_square(self.king_position)
        piece = square.get_piece()
        formated_moves = [(m.king_position, m.side)
                          for m in [p for p in piece.get_legal_moves(self._gamestate) if p.castling]]
        return ((square.position, self.side) in formated_moves)

    def print(self):
        print(f"CastlingMoves - {self.king_position} {self.side}")

    def perform(self):
        king_from_square = self._gamestate.get_square(self._king_pos)
        rook_from_square = self._gamestate.get_square(self._rook_from_pos)
        king = king_from_square.get_piece()
        rook = rook_from_square.get_piece()

        king_to_square = self._gamestate.get_square(self._king_to_pos)
        king_to_square.set_piece(king)
        rook_to_square = self._gamestate.get_square(self._rook_to_pos)
        rook_to_square.set_piece(rook)

        king_from_square.pop_piece()
        rook_from_square.pop_piece()

    def _unperform(self):
        king_to_square = self._gamestate.get_square(self._king_to_pos)
        rook_to_square = self._gamestate.get_square(self._rook_to_pos)
        king = king_to_square.get_piece()
        rook = rook_to_square.get_piece()

        king_from_square = self._gamestate.get_square(self.king_pos)
        king_from_square.set_piece(king)
        rook_from_square = self._gamestate.get_square(self.rook_from_pos)
        rook_from_square.set_piece(rook)

        king_to_square.pop_piece()
        rook_to_square.pop_piece()

    @ property
    def position_from(self):
        """
        legacy
        """
        return self._king_pos

    @ property
    def king_position(self):
        return self._king_pos

    @ king_position.setter
    def king_position(self, king_pos):
        if self.is_valid_position(king_pos):
            self._king_pos = king_pos

    @ property
    def side(self):
        return self._side

    @ side.setter
    def side(self, side):
        if side.lower() in ["k", "q"]:
            self._side = side

    def to_algebraic_notation(self):
        if self.side.lower() == "q":
            return "O-O-O"
        elif self.side.lower() == "k":
            return "O-O"


class PromotionMove(BaseMove):
    _promote_to = None
    _promote_from = None
    _captured_piece = None
    _position = (-1, -1)

    def __init__(self, gamestate, from_pos, to_pos, promote_to=None):
        super().__init__(gamestate)
        self._from_pos = from_pos
        self._to_pos = to_pos
        self._promote_from = type(
            gamestate.get_square(self._from_pos)._piece)
        self._promote_to = promote_to

    def clone(self):
        return PromotionMove(self.gamestate, self.position_from, self.position_to, promote_to=self.promote_to)

    def is_legal_move(self):
        piece = self.gamestate.get_square(self.position_from).get_piece()
        if not piece:
            return False
        formated_moves = [(m.position_from, m.position_to)
                          for m in self.gamestate.get_legal_moves(piece.colour)]
        print(formated_moves)
        return ((self.position_from, self.position_to) in formated_moves)

    def print(self):
        print(
            f"PromotionMove - promote on {self.position} to {self.promote_to}")

    def perform(self):
        square_from = self._gamestate.get_square(self.position_from)
        square_to = self._gamestate.get_square(self.position_to)
        piece_from = square_from.pop_piece()
        if not self._gamestate.square_is_empty(square_to.position):
            captured_piece = square_to.pop_piece()
            self._captured_piece = (captured_piece)
        if self.promote_to:
            piece_to_type = self.promote_to
        else:
            piece_to_type = self.gamestate.piece_letters["q"]
        piece_to = piece_to_type(
            piece_from.number, square_to.position, piece_from.colour, move_count=piece_from.move_count)
        piece_to.make_move(square_to.position)
        square_to.set_piece(piece_to)

    def _unperform(self):
        square_from = self._gamestate.get_square(self.position_from)
        square_to = self._gamestate.get_square(self.position_to)
        piece_from = square_to.pop_piece()  # new piece
        if self.captured:
            square_to.set_piece(self.captured)
        piece_to = self._promote_from(
            square_from.position, self.piece_to.colour, move_count=self.piece_to.move_count)
        piece_to.forget_move()
        square_to.set_piece(piece_to)

    @ property
    def captured(self):
        return self._captured_piece

    @ captured.setter
    def captured(self, piece):
        self._captured_piece = piece

    @ property
    def promote_to(self):
        return self._promote_to

    @ property
    def position_from(self):
        return self._from_pos

    @ position_from.setter
    def position_from(self, pos):
        if self.is_valid_position(pos):
            self._from_pos

    @ property
    def position_to(self):
        return self._to_pos

    @ position_to.setter
    def position_to(self, pos):
        if self.is_valid_position(pos):
            self._to_pos = pos

    def to_algebraic_notation(self):
        if self.promote_to:
            return f"P{self.pos_to_coord(self.position_from)}{self.pos_to_coord(self.position_to)}={promote_to.letter.upper()}"
        else:
            # assumes promotion to a Queen because you have to promote to
            # something to denote a promotion move
            return f"P{self.pos_to_coord(self.position_from)}{self.pos_to_coord(self.position_to)}=Q"
