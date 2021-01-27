# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:06:43 2021

@author: Joshua Evans

Based on rules from https://www.wikihow.com/Play-LCR

"""


# Left Right Center
import random


class game_state:

    def __init__(self):
        self.player_count = 0
        self.players = {}
        self.starting_player = ''
        self.player_order = []
        self.center_pot = 0
        self.max_chips = 0


    def player_setup(self, max_players=9):
        # Arrange at least three players around the tabletop in a circle.
        # Make sure there is plenty of open space in the middle of the 
        #   circle for players to place their poker chips for the “pot”.
        
        # Give each player three poker chips to start.
        # If playing with more than three players make sure each player
        #   has three chips to start the game.

        self.player_count = random.randint(3,max_players)
        
        for player in range(1, self.player_count+1):
            player = "Player " + str(player)
            self.players[player] = 3
        
    
    def dice_roll(self):
    
        result = random.randint(1,6)
        
        result_dict = {
            1 : 1,
            2 : 2,
            3 : 3,
            4 : "Left",
            5 : "Center",
            6 : "Right"
            }
        
        return result_dict[result]
    
    
    def pick_starting_player(self):
        # THE PLAY
        # Each player rolls the dice and counts the number of dots rolled (numbers 1-3). 
        # The player who rolls the most dots is the first player.

        highest_player_roll = 0
        
        for player in self.players:
            tally = 0
            for roll in range(3):
                result = self.dice_roll()
                if isinstance(result, int):
                    tally += result
            if tally > highest_player_roll:
                highest_player_roll = tally
                self.starting_player = player
     
    def player_name_to_number(self, player_name):
        # Conver the player's name to a number
        # Assumes "Player X" format where X is an Int
        return int(player_name.lstrip("Player "))
    
    
    def player_num_to_name(self, player_num):
        # Conver the player's number to a name
        # Assumes "Player X" format where X is an Int
        return "Player " + str(player_num)
    
    
    def get_left_player(self, player_num):
        # Take the player's number and return person 1 less in index
        # Wrap for 1st player
        if player_num > 1:
            left = player_num - 1
        else:
            left = self.player_count
            
        return self.player_num_to_name(left)
    
    
    def get_right_player(self, player_num):
        # Take the player's number and return person 1 less in index
        # Wrap for last player
        if player_num < self.player_count:
            right = player_num + 1
        else:
            right = 1
          
        return self.player_num_to_name(right)
        
    
    def set_player_order(self):
        # Create a list of players with the starting person as index 0
        # clockwise will assume next player is the +1 index
        players_list_num = []
        
        self.player_order.append(self.starting_player)        
        starting_player_num = int(self.starting_player.lstrip("Player "))
        
        players_list = list(self.players.keys())
        for i in players_list:
            players_list_num.append(i.lstrip("Player ") )
        
    
        for j in range(starting_player_num, (starting_player_num + self.player_count - 1) ):
             self.player_order.append( players_list[j % self.player_count] )
    
    
    
    def process_alt_result(self, roll_value, player_name):
        # For a 4 (Left) – give 1 chip to the player on the left
        # For a 5 (Center) -give 1 chip to the center pot
        # For a 6 (Right) – give 1 chip to the player on the right
        # For every dot rolled keep that same number of chips
        
        player_num = self.player_name_to_number(player_name)
        # print(player_num)
        # print(roll_value)
        
        if roll_value == "Left":
            self.players[self.get_left_player(player_num)] += 1
            # print("Processed left")
            
        
        elif roll_value == "Right":
            self.players[self.get_right_player(player_num)] += 1
            # print("Processed right")
            
        elif roll_value == "Center":
            self.center_pot += 1
            # print("Processed center")
            
        else:
            print("error")
                    
      
    def player_action(self, player):
        
        # In Left, Center, Right players only roll as many dice as they have in their possession. 
        # For the first roll, each player will roll three dice.
                           
        roll_count = self.players[player]
        # print("Rolls: " + str(roll_count))
        results = []

        for roll in range(roll_count):
            results.append(self.dice_roll())
        
        self.round_rolls[player][(self.current_round)] = results
        
        # print("Results:" + str(results))
        
        keep_count = 0
        
        for result in results:
            # print(result)
            
            if isinstance( result, int):
                keep_count += 1
            
            else:
                if self.players[player] == 0:
                    break
                self.process_alt_result(result, player)
                
        self.players[player] = keep_count
   
        
    def run_game(self):
        
        self.max_chips = self.player_count * 3
        
        self.current_player = self.starting_player
        self.current_round = 0
        
        self.round_rolls = {}
        
        for player in list(self.players.keys()):
            self.round_rolls[player] = {}
            
        
        while ( max(self.players.values()) < self.max_chips and 
                self.center_pot < self.max_chips-1 ) :
                        
            # print(self.current_player + "'s turn")
            self.player_action(self.current_player)
            try:
                self.current_player = self.player_order[ 
                    (self.player_order.index(self.current_player) + 1 )]
            except:
                self.current_player = self.player_order[0]
                self.current_round += 1
                
        print("Game Complete")
        self.detect_winner()
        print("The winner is: " + self.winner)
         
    def detect_winner(self):
        self.winner = ""
        for player in self.players:
            if self.players[player] > 0:
                self.winner = player

    

def main():
    
    game1 = game_state()
    game1.player_setup()
    game1.pick_starting_player()
    game1.set_player_order()
    game1.run_game()
    

    
    
        
main()     
        






        
    




# After the first roll look at the dice to see which sides face up. There are four possibilities:

# For a 4 (Left) – give 1 chip to the player on the left
# For a 5 (Center) -give 1 chip to the center pot
# For a 6 (Right) – give 1 chip to the player on the right
# For every dot rolled keep that same number of chips
# For example, if the first player rolls two dots and one 4(Left) they will give 1 chip to the player to their left and keep 2 chips.

# Play continues clockwise and the first round is complete once every player has completed their turn.

# After the first round is complete each player rolls the amount of dice that matches the amount of chips they have in their possession.

# If a player does not have any chips they do not roll the dice that round. Even though you cannot roll the dice you aren’t out of the game until someone wins. There is a chance that the player to your right or left will have to pass you a chip during each round of play.





