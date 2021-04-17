from core.player import Player, Color
from seega.seega_rules import SeegaRules
from seega.seega_rules import SeegaAction
from seega.seega_rules import SeegaActionType
from copy import deepcopy
import random

def phase1_sub(self,state):
    board = state.get_board()
    liste = []
    actions = []
    count = 0
    mcolor = Color(self.color.value)
    ecolor = Color(-self.color.value)
    my_cells = board.get_player_pieces_on_board(mcolor)
    ennemy_cells = board.get_player_pieces_on_board(ecolor)

    objective1 = [(0,2),(2,0),(2,4),(4,2)]
    objective2 = [(3,2),(2,3),(2,1),(1,2)]
    objective2_bis = [(1,2),(2,1),(2,3),(3,2)]
    objective3 = [(0,0),(0,4),(4,0),(4,4)]
    objective4 = [(0,1),(1,0),(0,3),(1,4),(3,0),(4,1),(3,4),(4,3)]
    objective4_bis = [(0,1),(0,3),(1,0),(1,4),(3,0),(3,4),(4,1),(4,3)]
    objective5 = [(1,1),(1,3),(3,1),(3,3)]
    objective_first = objective1 + objective2
    objective_second = objective4
    objective_third = objective3 + objective5
    empty_all = board.get_all_empty_cells_without_center()


    for i in range(0, len(objective1)):
        if board.is_empty_cell(objective1[i]):
            liste.append(objective1[i])
            count += 1
            if count == 2:
                break
    
    if count < 2:
        my_info_1 = elem_in_list(my_cells, objective1)
        my_info_2 = elem_in_list(my_cells, objective2)
        e_info_1 = elem_in_list(ennemy_cells, objective1)
        for i in range(0, len(objective2)):
            if self.color.value == -1:    
                if i in e_info_1:
                    continue
                else:
                    if board.is_empty_cell(objective2_bis[i]):
                        liste.append(objective2_bis[i])
                        count += 1
                        if count == 2:
                            break
            else:
                if len(my_info_2) >= 1:
                    break
                elif len(my_info_2) == 0 and len(my_info_1) == 4:
                    if board.is_empty_cell(objective2[i]):
                        liste.append(objective2[i])
                        count += 1
                        break
                else:
                    if i in my_info_1:
                        continue
                    else:
                        if board.is_empty_cell(objective2_bis[i]):
                            liste.append(objective2_bis[i])
                            count += 1
                            break
            
    if count < 2:
        my_info_4 = elem_in_list(my_cells, objective4)
        e_info_4 = elem_in_list(ennemy_cells, objective4)
        for i in range(0, len(objective5)):
            if board.is_empty_cell(objective5[i]):
                if 2*i in e_info_4 or (2*i)+1 in e_info_4:
                    continue
                else:
                    liste.append(objective5[i])
                    count += 1
                    if count == 2:
                        break
    
    if count < 2:
        random.shuffle(objective_third)
        for i in range(0, len(objective_third)):
            if board.is_empty_cell(objective_third[i]):
                liste.append(objective_third[i])
                count += 1
                if count == 2:
                    break
    
    if count < 2:
        random.shuffle(empty_all)
        for i in range(0, len(empty_all)):
            if board.is_empty_cell(empty_all[i]):
                liste.append(empty_all[i])
                count += 1
                if count == 2:
                    break
    
    actions.append(SeegaAction(action_type=SeegaActionType.ADD, to=liste[0]))
    if count == 2:
        actions.append(SeegaAction(action_type=SeegaActionType.ADD, to=liste[1]))
    return actions

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
    ennemy_cells = board.get_player_pieces_on_board(ecolor)
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
    empty_special = empty_cases1 + empty_cases2 + av_liste3 + av_liste1 + av_liste2
    empty_all = board.get_all_empty_cells_without_center()
    random.shuffle(empty_all)
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
        liste.append(empty_special[0])
        board.fill_cell(empty_special[0],mcolor)
        liste.append(empty_special[1])
        board.fill_cell(empty_special[1],mcolor)
        booleane = True


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
    next_to_center = [(center[0]+1,center[1]),(center[0]-1,center[1]),(center[0],center[1]-1),(center[0],center[1]+1)]
    for i in range(len(next_to_center)):
        if next_to_center[i] in my_cells:
            return liste
    if board.is_empty_cell((center[0]-1,shape[1]//2)):
        liste.append((center[0]-1,shape[1]//2))
        return liste
    if board.is_empty_cell((center[0]+1,shape[1]//2)):
        liste.append((center[0]+1,shape[1]//2))
        return liste
    if board.is_empty_cell((shape[0]//2,center[1]-1)):
        liste.append((shape[0]//2,center[1]-1))
        return liste
    if board.is_empty_cell((shape[0]//2,center[1]+1)):
        liste.append((shape[0]//2,center[1]+1))
        return liste
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
        condition, delta_x, delta_y, to_add = is_next_to_2(cells[i], e_cells)
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

def is_next_to_1(cell1, e_cells):
    if add_to_tuple(cell1,1,0) in e_cells:
        return True, 1, 0, [(2,1), (2,-1)]
    if add_to_tuple(cell1,0,1) in e_cells:
        return True, 0, 1, [(1,2), (-1,2)]
    if add_to_tuple(cell1,-1,0) in e_cells:
        return True, -1, 0, [(-2,-1), (-2,1)]
    if add_to_tuple(cell1,0,-1) in e_cells:
        return True, 0, -1, [(-1,-2), (1,-2)]
    return False, None, None, None

def is_next_to_2(cell1, e_cells):

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

def elem_in_list(cells, liste):
    index = []
    for i in range(0,len(liste)):
        if liste[i] in cells:
            index.append(i)
    return index

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
        print("scores", state.score.get(self.color.value), state.score.get(-self.color.value))
        if state.phase == 1:
            this_state = deepcopy(state)
            return phase1_sub(self, this_state)[0]
        else:
            this_state = deepcopy(state)
            action = minimax_search(this_state, self, True)
            #print("end turn")
            return action

    """
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """
    def successors(self, state, condition):
        
        liste = []
        if condition :
            this_player_id = self.color.value
        else:
            this_player_id = -self.color.value
        # print("positions", this_player_id)
        # print(board.get_player_pieces_on_board(mcolor))
        # print("positions", -this_player_id)
        # print(board.get_player_pieces_on_board(Color(-this_player_id)))
        
        all_possible_actions = SeegaRules.get_player_actions(state, this_player_id)
        random.shuffle(all_possible_actions)
        for action in all_possible_actions : 
            this_state=deepcopy(state)
            make_move = SeegaRules.act(this_state, action, this_player_id)
            #if make_move == False : continue
            #if SeegaRules.is_boring(this_state1) : continue
            liste.append((action,this_state))
            #yield (action, this_state1)
        #print("len(actions)",len(liste))
        return liste

    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """
    def cutoff(self, state, depth):
        if SeegaRules.is_end_game(state) : 
            return True
        if depth >= 2:
            return True
        return False
        #return depth >= 2

    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """
    def evaluate(self, state, condition):
        #print("EVALUATE")
        this_player_id = self.color.value
        my_score = state.score.get(this_player_id)
        e_score = state.score.get(-this_player_id)
        # print("positions", this_player_id)
        # print(board.get_player_pieces_on_board(mcolor))
        # print("positions", -this_player_id)
        # print(board.get_player_pieces_on_board(Color(-this_player_id)))
        print("score", state.score.get(this_player_id), "-", state.score.get(-this_player_id))
        comparison_scores = my_score > e_score
        #print(comparison_scores)
        if condition:
            print("------condition TRUE")
            if comparison_scores:
                return 3*state.score.get(this_player_id) - state.score.get(-this_player_id)
            else:
                return 3*state.score.get(this_player_id) - 2*state.score.get(-this_player_id)
        else:
            print("______condition FALSE")
            if comparison_scores:
                return state.score.get(-this_player_id) - 2*state.score.get(this_player_id)
            else:
                return 2*state.score.get(-this_player_id) - 2*state.score.get(this_player_id)

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
        print("---------------------")
        print("max_value",depth)
        if player.cutoff(state, depth):
            evaluation = player.evaluate(state, True)
            print("evaluate cutoff_max", evaluation)
            return evaluation, None
        val = -inf
        action = None
        for a, s in player.successors(state, True):
            print("action_max", a)
            if (
                s.get_latest_player() == s.get_next_player()
            ):  # next turn is for the same player
                v, _ = max_value(s, alpha, beta, depth + 1)
            else:  # next turn is for the other one
                v, _ = min_value(s, alpha, beta, depth + 1)
            print("vvvvv_max", v, val)
            if v > val:
                print("v>val", v, val, alpha, beta)
                val = v
                action = a
                if prune:
                    if v >= beta:
                        print("return_v_max", v)
                        return v, a
                    alpha = max(alpha, v)
        print("val_action_max", val, action)
        return val, action

    def min_value(state, alpha, beta, depth):
        print("---------------------")
        print("min_value",depth)
        if player.cutoff(state, depth):
            evaluation = player.evaluate(state, False)
            print("evaluate cutoff_min", evaluation)
            return evaluation, None
        val = inf
        action = None
        for a, s in player.successors(state, False):
            print("action_min", a)
            if (
                s.get_latest_player() == s.get_next_player()
            ):  # next turn is for the same player
                v, _ = min_value(s, alpha, beta, depth + 1)
            else:  # next turn is for the other one
                v, _ = max_value(s, alpha, beta, depth + 1)
            print("vvvvv_min", v, val)
            if v < val:
                print("v<val", v, val, alpha, beta)
                val = v
                action = a
                if prune:
                    if v <= alpha:
                        print("return_min_v", v)
                        return v, a
                    beta = min(beta, v)
        print("val_action_min", val, action)
        return val, action

    _, action = max_value(state, -inf, inf, 0)
    return action