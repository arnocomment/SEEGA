from core.player import Player, Color
from seega.seega_rules import SeegaRules
from seega.seega_rules import SeegaAction
from seega.seega_rules import SeegaActionType
from copy import deepcopy
import random


def phase1(self, state):
    board = state.get_board()
    this_id = self.color.value
    ennemy_id = -self.color.value
    mcolor = Color(self.color.value)
    ecolor = Color(-self.color.value)
    shape = board.board_shape
    actions = []
    liste = []
    booleane = False
    my_cells = board.get_player_pieces_on_board(mcolor)
    #print("my_cells")
    #print(my_cells)
    ennemy_cells = board.get_player_pieces_on_board(ecolor)
    #print("ennemy_cells")
    #print(ennemy_cells)
    empty_cases1 = cruise(shape,board)
    empty_cases2 = cruise2(shape,board,my_cells)
    if len(my_cells) > 0: 
        random.shuffle(my_cells)
        av_liste1 = good_emplacement_free1(board,my_cells,ennemy_cells)
    else:
        av_liste1 = []
    av_liste2 = good_emplacement_free2(board,mcolor,ecolor)
    av_liste3 = good_emplacement_free3(board,mcolor,ecolor)
    #av_liste = av_liste1 + av_liste2 + av_liste3
    empty_special = empty_cases1 + empty_cases2 + av_liste3 + av_liste2 + av_liste1
    empty_all = board.get_all_empty_cells_without_center()
    # print("empty_special",empty_special)
    # print("empty_all",empty_all,len(empty_all))
    if len(empty_special)==0:
        liste.append(empty_all[0])
        board.fill_cell(empty_all[0],mcolor)
        if len(empty_all) > 1 :
            liste.append(empty_all[1])
            board.fill_cell(empty_all[1],mcolor)
            booleane = True
    elif len(empty_special)==1:
        liste.append(empty_special[0])
        board.fill_cell(empty_special[0],mcolor)
        if len(empty_all) > 1 :
            liste.append(empty_all[1])
            board.fill_cell(empty_all[1],mcolor)
            booleane = True
    else:
        booleane = True
        liste.append(empty_special[0])
        board.fill_cell(empty_special[0],mcolor)
        liste.append(empty_special[1])
        board.fill_cell(empty_special[1],mcolor)


    # print("liste")
    # print(liste)
    actions.append(SeegaAction(action_type=SeegaActionType.ADD, to=liste[0]))
    if booleane == True:
        actions.append(SeegaAction(action_type=SeegaActionType.ADD, to=liste[1]))

    # print("actions")
    # print(len(actions))
    # print(actions)
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

def cruise2(shape,board,my_cells):
    liste = []
    center = (shape[0] // 2, shape[1] // 2)
    if board.is_empty_cell((center[0]-1,shape[1]//2)):
        if is_next_to((center[0]-1,shape[1]//2),my_cells)[0]==False:
            liste.append((center[0]-1,shape[1]//2))
    if board.is_empty_cell((center[0]+1,shape[1]//2)):
        if is_next_to((center[0]+1,shape[1]//2),my_cells)[0]==False:
            liste.append((center[0]+1,shape[1]//2))
    if board.is_empty_cell((shape[0]//2,center[1]-1)):
        if is_next_to((shape[0]//2,center[1]-1),my_cells)[0]==False:
            liste.append((shape[0]//2,center[1]-1))
    if board.is_empty_cell((shape[0]//2,center[1]+1)):
        if is_next_to((shape[0]//2,center[1]+1),my_cells)[0]==False:
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

def good_emplacement_free1(board,cells,e_cells):
    # print("free1")
    liste = []
    empty_cells = board.get_all_empty_cells()
    # print("empty_cells")
    # print(empty_cells,cells)
    for i in range(0,len(cells)):
        #print(cells[i])
        condition, delta_x, delta_y, to_add = is_next_to(cells[i], e_cells)
        if condition:
            possibilities = [(add_to_tuple(cells[i],to_add[0][0],to_add[0][1])),
                        (add_to_tuple(cells[i],to_add[1][0],to_add[1][1]))]
            for j in range(0, len(empty_cells)):
                if empty_cells[j] in possibilities and empty_cells[j] != (2,2):
                    liste.append(empty_cells[j])
    # print("free1",liste)
    return liste
       
def good_emplacement_free2(board,mcolor,ecolor):
    # print("free2")
    liste = []
    m_cells = board.get_player_pieces_on_board(mcolor)
    e_cells = board.get_player_pieces_on_board(ecolor)
    empty_cells = board.get_all_empty_cells()
    for i in range(0, len(empty_cells)):
        if empty_cells[i] != (2,2):
            if add_to_tuple(empty_cells[i],1,0) in e_cells and add_to_tuple(empty_cells[i],-1,0) in e_cells:
                liste.append(empty_cells[i])
            if add_to_tuple(empty_cells[i],0,1) in e_cells and add_to_tuple(empty_cells[i],0,-1) in e_cells:
                liste.append(empty_cells[i])
    # print("free2", liste)
    return liste

def good_emplacement_free3(board,mcolor,ecolor):
    #print("free3")
    liste = []
    m_cells = board.get_player_pieces_on_board(mcolor)
    e_cells = board.get_player_pieces_on_board(ecolor)
    empty_cells = board.get_all_empty_cells()
    for i in range(0, len(empty_cells)):
        if empty_cells[i] != (2,2):
            if add_to_tuple(empty_cells[i],1,0) in e_cells and add_to_tuple(empty_cells[i],-1,0) in e_cells and add_to_tuple(empty_cells[i],2,0) in m_cells and add_to_tuple(empty_cells[i],-2,0) in m_cells:
                liste.append(empty_cells[i])
            if add_to_tuple(empty_cells[i],0,1) in e_cells and add_to_tuple(empty_cells[i],-1,0) in e_cells and add_to_tuple(empty_cells[i],0,2) in m_cells and add_to_tuple(empty_cells[i],-2,0) in m_cells:
                liste.append(empty_cells[i])
            if add_to_tuple(empty_cells[i],1,0) in e_cells and add_to_tuple(empty_cells[i],0,-1) in e_cells and add_to_tuple(empty_cells[i],2,0) in m_cells and add_to_tuple(empty_cells[i],0,-2) in m_cells:
                liste.append(empty_cells[i])
            if add_to_tuple(empty_cells[i],0,1) in e_cells and add_to_tuple(empty_cells[i],0,-1) in e_cells and add_to_tuple(empty_cells[i],0,2) in m_cells and add_to_tuple(empty_cells[i],0,-2) in m_cells:
                liste.append(empty_cells[i])
    #print("free3",liste)
    return liste

def add_to_tuple(cell,a,b):
    return (cell[0]+a,cell[1]+b)

def is_next_to(cell1, e_cells):
    if add_to_tuple(cell1,1,0) in e_cells:
        return True, 1, 0, [(2,1), (2,-1)]
    if add_to_tuple(cell1,1,1) in e_cells:
        return True, 1, 1, [(2,1), (1,2)]
    if add_to_tuple(cell1,0,1) in e_cells:
        return True, 0, 1, [(1,2), (-1,2)]
    if add_to_tuple(cell1,-1,-1) in e_cells:
        return True, -1, -1, [(-2,-1), (-1,-2)]
    if add_to_tuple(cell1,-1,0) in e_cells:
        return True, -1, 0, [(-2,-1), (-2,1)]
    if add_to_tuple(cell1,0,-1) in e_cells:
        return True, 0, -1, [(-1,-2), (1,-2)]
    if add_to_tuple(cell1,-1,1) in e_cells:
        return True, -1, 1, [(-2,1), (-1,2)]
    if add_to_tuple(cell1,1,-1) in e_cells:
        return True, 1, -1, [(2,-1), (1,-2)]
    return False, None, None, None

class AI(Player):

    in_hand = 12
    score = 0
    name = "Smart"

    def __init__(self, color):
        super(AI, self).__init__(color)
        self.position = color.value
        self.player = Color(color.value)

    def play(self, state, remain_time):
        # print("")
        # print(f"Player {self.position} is playing.")
        # print("time remain is ", remain_time, " seconds")
        return minimax_search(state, self)

    """
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """
    def successors(self, state):
        #print("latest move", state._latest_move)
        this_players_id = self.color.value
        mcolor = Color(self.color.value)
        ecolor = Color(-self.color.value)
        if state.in_hand == 0:
            state.phase = 2
        if state.phase == 1:
            this_state1 = deepcopy(state)
            this_state2 = deepcopy(state)
            try :      
                actions = phase1(self,this_state1)
                if len(actions) == 2 :
                    yield(actions[0], this_state1)
                    yield(actions[1], this_state1)
                else:
                    yield(actions[0],this_state1)
            except:
                state.phase = 2
                all_possible_actions = SeegaRules.get_player_actions(state, this_players_id)
                random.shuffle(all_possible_actions)
                for action in all_possible_actions : 
                    this_state=deepcopy(state)
                    make_move = SeegaRules.act(this_state, action, this_players_id)
                    #if make_move == False : continue
                    yield (action, this_state)

        else:
            all_possible_actions = SeegaRules.get_player_actions(state, this_players_id)
            random.shuffle(all_possible_actions)
            for action in all_possible_actions : 
                this_state=deepcopy(state)
                make_move = SeegaRules.act(this_state, action, this_players_id)
                #if make_move == False : continue
                yield (action, this_state)

    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """
    def cutoff(self, state, depth):
        #print("cutoff",depth)
        if SeegaRules.is_end_game(state) : 
            return True
        if depth >= 3:
            #print("True")
            return True
        return False
        #return depth >= 2

    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """
    def evaluate(self, state, booleane):
        #print("EVALUATE")
        this_players_id = self.color.value
        if booleane:
            if state.score.get(this_players_id) == None:
                return 0
            return 3*state.score.get(this_players_id)
        else:
            if state.score.get(-this_players_id) == None:
                return 0
            return state.score.get(-this_players_id)

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