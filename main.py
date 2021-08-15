from chess_game.Pieces import Pawn, Queen
from chess_game.Move import Move, PromotionMove, CastlingMove
from chess_game.GameState import GameState
from chess_game.Player import TerminalPlayer
from chess_game.Game import Game

# g = GameState(
# fen_string="1nbqkbn1/8/r6r/8/8/1PPP1BN1/PPNBQPPP/R3K2R w KQ - 0 1")

g = GameState()

moves = ["c4", "g6", "Nc3", "Bg7", "Nf3", "Nf6", "g3", "O-O",
         "Bg2", "d6", "O-O", "Nc6", "Rb1", "e5", "d3", "Nd4",
         "b4", "c6", "b5", "Nxf3+", "Bxf3", "d5", "bxc6", "bxc6", "Qa4", "Be6", "Ba3", "Re8", "cxd5", "cxd5",
         "Rfc1", "a6", "Bc5", "Rc8", "Bb6", "Qd6", "Ba5", "Bd7", "Bb4", "Qe6", "Qb3", "e4", "dxe4", "dxe4",
         "Qxe6", "Rxe6", "Bg2", "Rec6", "Rd1", "Bf5", "Nd5", "Nxd5", "Rxd5", "Rc2", "a3", "e3", "Rbd1", "Bf8",
         "Bf3", "exf2+", "Kxf2", "Bc5+", "Rxc5", "R8xc5", "Bxc5", "Rxc5", "Rd5", "Rc2", "Ra5", "Bd3",
         "Re5", "Bb5", "Bd5", "Kf8", "Re3", "h6", "g4", "Bc4", "Bxc4", "Rxc4", "Kg3", "Kg7", "Rf3", "Re4",
         "h4", "Rxe2", "g5", "hxg5", "hxg5", "Re5", "Kg4", "Re4+", "Kg3", "Kf8", "Rb3", "Ke7", "Kf3", "Ra4",
         "Kg3", "Ke6", "Rf3", "a5", "Rf6+", "Ke7", "Rf3", "Re4", "Rb3", "Re5", "Kf4", "Rf5+", "Kg4", "Kd6",
         "Rb7", "Kc5", "a4", "Kd5", "Rb5+", "Ke4", "Rb7", "Kd4", "Rc7", "Kd5", "Rb7", "Kc6", "Re7", "Rf1",
         "Re5", "Kb6", "Rb5+", "Ka6", "Rd5", "Rb1", "Kf4", "Rb4+", "Ke5", "Rxa4", "Rd7", "Rg4", "Kf6", "Rf4+",
         "Kg7", "a4", "Rd8", "Kb5", "Rb8+", "Kc4", "Ra8", "Kb3", "Rb8+", "Rb4", "Re8", "Rb7", "Re3+"]
colour_moving = True
g.print()
for mv in moves:
    move = Move.from_algebraic_notation(g, ("w" if colour_moving else "b"), mv)
    if move:
        g.make_move(move)
    else:
        # g.print()
        print(f"move failed {mv}")
    colour_moving = not colour_moving
print("finished")
g.print()
print(g.check("w"))
print(g.check("b"))
# print(g.check("w"))
