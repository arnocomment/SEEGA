from core.player import Player, Color
from seega.seega_rules import SeegaRules
from seega.seega_rules import SeegaAction
from seega.seega_rules import SeegaActionType
from copy import deepcopy


def phase1(self, state):
    board = state.get_board()
    mcolor = Color(self.color.value)
    shape = board.board_shape
    actions = []
    liste = []
    empty_cases1 = cruise(shape,board)
    empty_cases2 = cruise2(shape,board)
    empty_cases3 = next_to_cruise(shape,board)
    empty_cases4 = corner(shape,board)
    empty_special_cases = empty_cases1 + empty_cases2 + empty_cases3 + empty_cases4
    empty_cases5 = board.get_all_empty_cells_without_center()
    booleane = False
    print("empty_special_cases")
    print(empty_special_cases)
    print("empty_cases5")
    print(empty_cases5)
    if len(empty_special_cases)>=2:
        print("if1")
        booleane = True
        liste.append(empty_special_cases[0])
        liste.append(empty_special_cases[1])
        board.fill_cell(empty_special_cases[0],mcolor)
        board.fill_cell(empty_special_cases[1],mcolor)
    elif len(empty_special_cases)==1:
        print("if2")
        booleane = True
        liste.append(empty_special_cases[0])
        liste.append(empty_cases5[0])
        board.fill_cell(empty_special_cases[0],mcolor)
        board.fill_cell(empty_cases5[0],mcolor)
    else:
        print("else")
        if len(empty_cases5) == 2:
            print("last else if")
            booleane = True
            liste.append(empty_cases5[0])
            liste.append(empty_cases5[1])
            board.fill_cell(empty_cases5[0],mcolor)
            board.fill_cell(empty_cases5[1],mcolor)
        else:
            liste.append(empty_cases5[0])
            board.fill_cell(empty_cases5[0],mcolor)
    
    print("liste")
    print(liste)
    print("boolean")
    print(booleane)
    actions.append(SeegaAction(action_type=SeegaActionType.ADD, to=liste[0]))
    if booleane :
        print("if boolean")
        actions.append(SeegaAction(action_type=SeegaActionType.ADD, to=liste[1]))

    print(actions)
    return actions     
            
def cruise(shape,board):
    liste = []
    if board.is_empty_cell((0,shape[1]//2)):
        liste.append((0,shape[1]//2))
    if board.is_empty_cell((shape[0]-1,shape[1]//2)):
        liste.append((shape[0]-1,shape[1]//2))
    if board.is_empty_cell((shape[0]//2,0)):
        liste.append((shape[0]//2,0))
    if board.is_empty_cell((shape[0]//2,shape[1]-1)):
        liste.append((shape[0]//2,shape[1]-1))
    return liste

def cruise2(shape,board):
    liste = []
    center = (shape[0] // 2, shape[1] // 2)
    if board.is_empty_cell((center[0]-1,shape[1]//2)):
        liste.append((center[0]-1,shape[1]//2))
    if board.is_empty_cell((center[0]+1,shape[1]//2)):
        liste.append((center[0]+1,shape[1]//2))
    if board.is_empty_cell((shape[0]//2,center[1]-1)):
        liste.append((shape[0]//2,center[1]-1))
    if board.is_empty_cell((shape[0]//2,center[1]+1)):
        liste.append((shape[0]//2,center[1]+1))
    return liste

def next_to_cruise(shape,board):
    liste = []
    center = (shape[0] // 2, shape[1] // 2)
    if board.is_empty_cell((center[0]-1,center[1]-1)):
        liste.append((center[0]-1,center[1]-1))
    if board.is_empty_cell((center[0]-1,center[1]+1)):
        liste.append((center[0]-1,center[1]+1))
    if board.is_empty_cell((center[0]+1,center[1]-1)):
        liste.append((center[0]+1,center[1]-1))
    if board.is_empty_cell((center[0]+1,center[1]+1)):
        liste.append((center[0]+1,center[1]+1))
    return liste

def corner(shape,board):
    liste = []
    if board.is_empty_cell((0,0)):
        liste.append((0,0))
    if board.is_empty_cell((0,shape[1]-1)):
        liste.append((0,shape[1]-1))
    if board.is_empty_cell((shape[0]-1,0)):
        liste.append((shape[0]-1,0))
    if board.is_empty_cell((shape[0]-1,shape[1]-1)):
        liste.append((shape[0]-1,shape[1]-1))
    return liste

class AI(Player):

    in_hand = 12
    score = 0
    name = "Smart"

    def __init__(self, color):
        super(AI, self).__init__(color)
        self.position = color.value
        self.player = Color(color.value)

    def play(self, state, remain_time):
        print("")
        print(f"Player {self.position} is playing.")
        print("time remain is ", remain_time, " seconds")
        return minimax_search(state, self)

    """
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """
    def successors(self, state):
        this_players_id = self.color.value
        mcolor = Color(self.color.value)
        ecolor = Color(-self.color.value)
        if state.phase == 1:
            this_state1 = deepcopy(state)
            this_state2 = deepcopy(state)
            actions = phase1(self,this_state1)
            if len(actions) == 2 :
                yield(actions[0], this_state1)
                yield(actions[1], this_state2)
            else:
                yield(actions[0],this_state1)

        else:
            # myscore = state.score.get(mcolor)
            # escore = state.score.get(ecolor)
            # ratio = myscore - escore
            # if ratio > 0 : 
            #     self.player = mcolor
            # else :
            #     self.player = ecolor
            # this_state = deepcopy(state)
            # all_possible_actions = SeegaRules.get_player_actions(state, self.player)
            all_possible_actions = SeegaRules.get_player_actions(state, this_players_id)
            this_state=deepcopy(state)
            for action in all_possible_actions : 
                make_move = SeegaRules.act(this_state, action, this_players_id)
                if make_move == False : continue
                # print("-----")
                # print(action, make_move[0])
                yield (action, make_move[0])

    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """
    def cutoff(self, state, depth):
        if SeegaRules.is_end_game(state) : 
            return True
        return depth >= 1

    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """
    def evaluate(self, state, booleane):
        this_players_id = self.color.value
        ecolor = Color(-this_players_id)
        board = state.get_board()
        if booleane:
            return state.score.get(this_players_id)
        else:
            if state.score.get(ecolor) == None:
                return 0
            return state.score.get(ecolor)

    """
    Specific methods for a Seega player (do not modify)
    """
    def set_score(self, new_score):
        self.score = new_score

    def update_player_infos(self, infos):
        self.in_hand = infos['in_hand']
        self.score = infos['score']
        
    def reset_player_informations(self):
        self.in_hand = 12
        self.score = 0



"""
MiniMax and AlphaBeta algorithms.
Adapted from:
    Author: Cyrille Dejemeppe <cyrille.dejemeppe@uclouvain.be>
    Copyright (C) 2014, Universite catholique de Louvain
    GNU General Public License <http://www.gnu.org/licenses/>
"""

inf = float("inf")

def minimax_search(state, player, prune=True):
    """Perform a MiniMax/AlphaBeta search and return the best action.

    Arguments:
    state -- initial state
    player -- a concrete instance of class AI implementing an Alpha-Beta player
    prune -- whether to use AlphaBeta pruning

    """
    def max_value(state, alpha, beta, depth):
        if player.cutoff(state, depth):
            return player.evaluate(state, True), None
        val = -inf
        action = None
        for a, s in player.successors(state):
            if s.get_latest_player() == s.get_next_player():  # next turn is for the same player
                v, _ = max_value(s, alpha, beta, depth + 1)
            else:                                             # next turn is for the other one
                v, _ = min_value(s, alpha, beta, depth + 1)
                #v, _ = max_value(s, alpha, beta, depth + 1)
            if v > val:
                val = v
                action = a
                if prune:
                    if v >= beta:
                        return v, a
                    alpha = max(alpha, v)
        return val, action

    def min_value(state, alpha, beta, depth):
        if player.cutoff(state, depth):
            return player.evaluate(state, False), None
        val = inf
        action = None
        for a, s in player.successors(state):
            if s.get_latest_player() == s.get_next_player():  # next turn is for the same player
                v, _ = min_value(s, alpha, beta, depth + 1)
            else:                                             # next turn is for the other one
                v, _ = max_value(s, alpha, beta, depth + 1)
                #v, _ = min_value(s, alpha, beta, depth + 1)
            if v < val:
                val = v
                action = a
                if prune:
                    if v <= alpha:
                        return v, a
                    beta = min(beta, v)
        return val, action

    _, action = max_value(state, -inf, inf, 0)
    return action