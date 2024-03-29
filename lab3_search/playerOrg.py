#!/usr/bin/env python3
import random

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR
from fishing_game_core.shared import TYPE_TO_SCORE


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

            # Create the root node of the game tree
            node = Node(message=msg, player=0)
            caught = node.state.get_caught()
            # The player scores: {0: MAX_SCORE, 1: MIN_SCORE}
            player_scores = node.state.get_player_scores()
            # The positions of the two hooks, provided as (x,y) coordinate tuples.
            hook_pos = node.state.get_hook_positions()
            # The positions of the uncaught fishes, provided as (x,y) coordinate tuples.
            fish_pos = node.state.get_fish_positions()
            # The score values associated with each fish index.
            fish_score = node.state.get_fish_scores()


            print("caught = ", caught)
            print("caught0 = ", TYPE_TO_SCORE[caught[0]])
            print("caught1 = ", TYPE_TO_SCORE[caught[1]])
            print("player_scores = ", player_scores)
            print("player_scores0 = ", player_scores[0])
            print("player_scores1 = ", player_scores[1])
            print("hook_pos = ", hook_pos)
            print("hook_pos x = ", hook_pos[0][0])
            print("hook_pos y = ", hook_pos[0][1])
            print("fish_pos = ", fish_pos)
            print("fish1_pos x = ", fish_pos[0][0])
            print("fish1_pos y = ", fish_pos[0][1])
            print("fish_scores = ", fish_score)

            distance = {}
            for fish in fish_pos:
                if fish_score[fish] > 0:
                    distance[fish] = abs(hook_pos[0][0] - fish_pos[fish][0]) + abs(hook_pos[0][1] - fish_pos[fish][1])
            print("distance = ", distance)
            bestDist = min(distance.values())
            print("best distance = ", bestDist)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(
                model=model, initial_tree_node=node)

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

    def search_best_next_move(self, model, initial_tree_node):
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

        random_move = random.randrange(5)
        return ACTION_TO_STR[random_move]