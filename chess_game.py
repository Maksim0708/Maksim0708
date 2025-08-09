#!/usr/bin/env python3
"""Simple command-line chess game for two players.

This program implements basic chess rules for moving pieces and capturing.
It does not handle advanced rules like castling, en passant or checking for
checkmate. Pawns are automatically promoted to queens when they reach the
opponent's back rank.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

FILES = "abcdefgh"
RANKS = "12345678"

@dataclass
class Move:
    src: Tuple[int, int]
    dst: Tuple[int, int]


def initial_board() -> List[List[str]]:
    """Return the initial chess board setup."""
    return [
        list("rnbqkbnr"),
        list("pppppppp"),
        [" "] * 8,
        [" "] * 8,
        [" "] * 8,
        [" "] * 8,
        list("PPPPPPPP"),
        list("RNBQKBNR"),
    ]


def print_board(board: List[List[str]]) -> None:
    """Display the board in a human-readable form."""
    for idx, row in enumerate(board):
        print(8 - idx, " ".join(row))
    print("  " + " ".join(FILES))


def parse_move(text: str) -> Optional[Move]:
    text = text.replace(" ", "").lower()
    if len(text) != 4:
        return None
    try:
        src_col = FILES.index(text[0])
        src_row = 8 - int(text[1])
        dst_col = FILES.index(text[2])
        dst_row = 8 - int(text[3])
    except (ValueError, IndexError):
        return None
    return Move((src_row, src_col), (dst_row, dst_col))


def is_path_clear(board: List[List[str]], src: Tuple[int, int], dst: Tuple[int, int]) -> bool:
    """Check that all squares between src and dst are empty (for sliding pieces)."""
    s_row, s_col = src
    d_row, d_col = dst
    step_row = (d_row - s_row) and (1 if d_row > s_row else -1)
    step_col = (d_col - s_col) and (1 if d_col > s_col else -1)
    cur_row, cur_col = s_row + step_row, s_col + step_col
    while (cur_row, cur_col) != (d_row, d_col):
        if board[cur_row][cur_col] != " ":
            return False
        cur_row += step_row if s_row != d_row else 0
        cur_col += step_col if s_col != d_col else 0
    return True


def is_valid_move(board: List[List[str]], move: Move, white_turn: bool) -> bool:
    s_row, s_col = move.src
    d_row, d_col = move.dst
    piece = board[s_row][s_col]
    target = board[d_row][d_col]
    if piece == " ":
        return False
    if piece.isupper() != white_turn:
        return False
    if target != " " and target.isupper() == piece.isupper():
        return False

    delta_row = d_row - s_row
    delta_col = d_col - s_col
    abs_row = abs(delta_row)
    abs_col = abs(delta_col)

    p = piece.lower()
    if p == "p":
        direction = -1 if piece.isupper() else 1
        start_row = 6 if piece.isupper() else 1
        if delta_col == 0:
            if delta_row == direction and target == " ":
                return True
            if s_row == start_row and delta_row == 2 * direction and target == " " and board[s_row + direction][s_col] == " ":
                return True
        if abs_col == 1 and delta_row == direction and target != " " and target.isupper() != piece.isupper():
            return True
        return False
    if p == "n":
        return (abs_row, abs_col) in {(1, 2), (2, 1)}
    if p == "k":
        return max(abs_row, abs_col) == 1
    if p == "b":
        return abs_row == abs_col and is_path_clear(board, move.src, move.dst)
    if p == "r":
        return (delta_row == 0 or delta_col == 0) and is_path_clear(board, move.src, move.dst)
    if p == "q":
        if abs_row == abs_col or delta_row == 0 or delta_col == 0:
            return is_path_clear(board, move.src, move.dst)
        return False
    return False


def apply_move(board: List[List[str]], move: Move) -> None:
    s_row, s_col = move.src
    d_row, d_col = move.dst
    piece = board[s_row][s_col]
    board[s_row][s_col] = " "
    board[d_row][d_col] = piece
    # simple promotion
    if piece == "P" and d_row == 0:
        board[d_row][d_col] = "Q"
    elif piece == "p" and d_row == 7:
        board[d_row][d_col] = "q"


def main() -> None:
    board = initial_board()
    white_turn = True
    while True:
        print_board(board)
        player = "White" if white_turn else "Black"
        move_str = input(f"{player} move (e2e4 or 'quit'): ")
        if move_str.lower() in {"quit", "exit"}:
            print("Game terminated.")
            break
        move = parse_move(move_str)
        if not move:
            print("Invalid move format.")
            continue
        if not is_valid_move(board, move, white_turn):
            print("Illegal move.")
            continue
        apply_move(board, move)
        white_turn = not white_turn


if __name__ == "__main__":
    main()
