#!/usr/bin/env python3
import random
from time import time
import math

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR
from fishing_game_core.shared import TYPE_TO_SCORE

Max_Time = 75*1e-2


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()
        self.start_time = None

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate game tree object
        first_msg = self.receiver()
        # Initialize your minimax model
        model = self.initialize_model(initial_data=first_msg)

        while True:
            msg = self.receiver()
            self.start_time = time()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            #best_move = self.search_best_next_move(node, )


            #print(node.state.player_scores)
            #print(node.state.player_caught)
            #print(node.state.hook_positions)
            #print(node.state.fish_positions)
            #print(node.state.fish_scores)



            # Possible next moves: "stay", "left", "right", "up", "down"
            for iter_depth in range(1, 4):
                scores = []
                score, best_move = self.search_best_next_move(node, iter_depth, -math.inf, math.inf, 0, scores)
               # print("best move = ", best_move)
                #print(iter_depth)
                #print(scores)
            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def initialize_model(self, initial_data):
        """
        Initialize your minimax model 
        :param initial_data: Game data for initializing minimax model
        :type initial_data: dict
        :return: Minimax model
        :rtype: object

        Sample initial data:
        { 'fish0': {'score': 11, 'type': 3}, 
          'fish1': {'score': 2, 'type': 1}, 
          ...
          'fish5': {'score': -10, 'type': 4},
          'game_over': False }

        Please note that the number of fishes and their types is not fixed between test cases.
        """
        # EDIT THIS METHOD TO RETURN A MINIMAX MODEL ###
        return None

    def search_best_next_move(self, node, depth, alpha, beta, player, scores):
        """
        Use your minimax model to find best possible next move for player 0 (green boat)
        :param model: Minimax model
        :type model: object
        :param initial_tree_node: Initial game tree node 
        :type initial_tree_node: game_tree.Node 
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE FROM MINIMAX MODEL ###
        
        # NOTE: Don't forget to initialize the children of the current node 
        #       with its compute_and_get_children() method!

        child_nodes = node.compute_and_get_children()

        if time() - self.start_time >= (Max_Time*0.09):
            score = self.heuristic(node)
            print("time")
            if node.move is not None:
                move = node.move
            else:
                move = 0
            return score, ACTION_TO_STR[move]


        if depth == 0 or len(child_nodes) == 0:
            score = self.heuristic(node)
            scores.append(score)
            return score, ACTION_TO_STR[node.move] #return score and move that lead to the score

        if player == 0: #green boat max turn

            maxEval = -math.inf
            for c_state in child_nodes:
                mm_eval, action = self.search_best_next_move(c_state, depth-1, alpha, beta, 1, scores)
                if mm_eval > maxEval:
                    maxEval = mm_eval
                    bestMove = action
                alpha = max(alpha, mm_eval)
                #print("alpha = ", alpha)
                if beta <= alpha:
                    break
            return maxEval, bestMove
        else: #red boat min turn
            minEval = math.inf
            #order move
            for c_state in child_nodes:
                mm_eval, action = self.search_best_next_move(c_state, depth-1, alpha, beta, 0, scores)
                if mm_eval < minEval:
                    minEval = mm_eval
                    bestMove = action
                beta = min(minEval, mm_eval)
                #print("beta = ", beta)
                if beta <= alpha:
                    break
            return minEval, bestMove




        #random_move = random.randrange(5)
        #return ACTION_TO_STR[random_move]

    def heuristic(self, node):

        # The index of the caught fish for the two players in a dict.
        # The fish index -1 means that no fish has been caught.
        caught = node.state.get_caught()
        # The player scores: {0: MAX_SCORE, 1: MIN_SCORE}
        player_scores = node.state.get_player_scores()
        # The positions of the two hooks, provided as (x,y) coordinate tuples.
        hook_pos = node.state.get_hook_positions()
        # The positions of the uncaught fishes, provided as (x,y) coordinate tuples.
        fish_pos = node.state.get_fish_positions()
        # The score values associated with each fish index.
        fish_score = node.state.get_fish_scores()

        #print(caught)
        #print(player_scores)
        #print(hook_pos)
        #print(fish_pos)
        #print(fish_score)
        bestDist = 0

        #block for fish boat
        #wrap around for distance calculation
        sub = 20

        if caught[0] is not None:
            caught_fish0 = TYPE_TO_SCORE[caught[0]]
        else:
            caught_fish0 = 0
            distance = {}
            for fish in fish_pos:
                flag = 1
                if fish_score[fish] > 0:
                    x1 = hook_pos[0][0]
                    x2 = fish_pos[fish][0]
                    x3 = hook_pos[1][0]
                    dx = min ( abs(x2 - x1) , sub - abs(x2 - x1) )
                    dx2 = min ( abs(x3 - x1) , sub - abs(x3 - x1) )
                    dy = abs(hook_pos[0][1] - fish_pos[fish][1])
                    if dx2 < dx:
                        flag = -1
                    distance[fish] =  flag*(fish_score[fish]/(dx + dy + 0.5)) #manhattan distance with fish value with wrap around on x axis
            if distance.values():
                bestDist = max(distance.values()) #find closest fish in that state
            #print("best distance = ", bestDist)

        if caught[1] is not None:
            caught_fish1 = TYPE_TO_SCORE[caught[1]]
        else:
            caught_fish1 = 0


        score = caught_fish0 + player_scores[0] - caught_fish1 - player_scores[1] + bestDist
        #print(score)
        return score

