"""
347
A CLI-based game by Hassaan Shaikh
"""

import random
import os

current_round = 1

# Initial and end condition scores, can be changed
p1_score = 174
p2_score = 174
goal_score = 347
loss_score = 0

p1_turn = True # Oscillates between the two players

p1_jackpot_list = []
p2_jackpot_list = []
p1_jackpot_complete = False
p2_jackpot_complete = False

def clear_screen(): # To clear the console interface for clean visuals
  if os.name == 'nt':
        _ = os.system('cls')
  else:
        _ = os.system('clear')

def end_game_check():
  return (p1_score >= goal_score or p1_score <= loss_score) or (p2_score >= goal_score or p2_score <= loss_score) or p1_jackpot_complete or p2_jackpot_complete

def roll_green_dice():
  return random.randint(1, 6)

def roll_red_dice():
  return random.randint(1, 6)

def event3():
  print("Event-3 triggered! You get a second roll.")
  game_loop(True)

def event4():
  print("Event-4 triggered! Choose your move.")
  print("1. Roll a dice to add 2x of it to your score")
  print("2. Roll a dice to subtract 2x of it from your opponent's score")

  global p1_score, p2_score, p1_turn

  choice = 0
  while choice not in [1, 2]:
    user_input = input("Enter your choice (1 or 2): ")
    try:
      choice = int(user_input)
      if choice not in [1, 2]:
        print("Invalid choice. Please enter 1 or 2.")
    except ValueError:
      print("Invalid input. Please enter a number (1 or 2).")
      choice = 0 # Reset choice to keep loop running

  roll = random.randint(1, 6)
  print(f"You rolled a {roll}.")
  roll *= 2
  print(f"Event-4 score: {roll}")

  if choice == 1:
    if p1_turn:
      p1_score += roll
    else:
      p2_score += roll
  else:
    if p1_turn:
      p2_score -= roll
    else:
      p1_score -= roll

def event7(green, red):
  print("Event-7 triggered!")
  global p1_score, p2_score

  additional_score = (green - red) * 4 # Potentially dangerous formula
  print(f"Additional score: ({green} - {red}) * 4 = {additional_score}")
  if p1_turn:
    p1_score += additional_score
  else:
    p2_score += additional_score

def jackpot_listing(p1_turn, sum_dice):
  global p1_jackpot_list, p2_jackpot_list

  if p1_turn:
    if sum_dice not in [3, 4, 7] and len(p1_jackpot_list) >= 1:
      p1_jackpot_list.clear()
      print("347 Streak has been broken!")
    else:
      if sum_dice == 3 and 3 not in p1_jackpot_list:
        p1_jackpot_list.append(3)
        print("3 _ _ !")
      if 3 in p1_jackpot_list and sum_dice == 4 and 4 not in p1_jackpot_list:
        p1_jackpot_list.append(4)
        print("3 4 _ !")
      if [3, 4] in p1_jackpot_list and sum_dice == 7 and 7 not in p1_jackpot_list:
        p1_jackpot_list.append(7)
        print("3 4 7 !")
        print("Player 1 has completed the 347 Jackpot!")
        p1_jackpot_complete = True
  else:
    if sum_dice not in [3, 4, 7] and len(p2_jackpot_list) >= 1:
      p2_jackpot_list.clear()
      print("347 Streak has been broken!")
    else:
      if sum_dice == 3 and 3 not in p2_jackpot_list:
        p2_jackpot_list.append(3)
        print("3 _ _ !")
      if 3 in p2_jackpot_list and sum_dice == 4 and 4 not in p2_jackpot_list:
        p2_jackpot_list.append(4)
        print("3 4 _ !")
      if [3, 4] in p2_jackpot_list and sum_dice == 7 and 7 not in p2_jackpot_list:
        p2_jackpot_list.append(7)
        print("3 4 7 !")
        print("Player 2 has completed the 347 Jackpot!")
        p2_jackpot_complete = True

def print_scores():
  print(f"Player 1's score: {p1_score}")
  print(f"Player 2's score: {p2_score}")

'''
Game loop procedure:
1. Player rolls both dice.
2. Check for Rule of Triples.
3. Update player scores. Use Rule of Triples to double scores if applicable.
4. Check for Event-X conditions and execute applicable ones.
'''

def game_loop(skip_events = False):
    global p1_score, p2_score, p1_turn, current_round, p1_jackpot_list, p2_jackpot_list

    if not skip_events:
      if p1_turn:
        print(f"\tRound {current_round}")
        print_scores()
      current_round += 1 if not p1_turn else 0
      print()
      
      if p1_turn:
        print("Player 1's turn")
      else:
        print("Player 2's turn")
      input("Press 'ENTER' to roll the dice.")

    green = roll_green_dice()
    red = roll_red_dice()
    print()

    if not skip_events:
      print("Green Dice: ", green)
      print("Red Dice: ", red)
      if green == red: # Rule of Triples
        print("Rule of Triples triggered! Triple scores.")
        green *= 3
        red *= 3
        print("Green Dice: ", green)
        print("Red Dice: ", red)
    else:
      print("Second Roll for Event-3:")
      print("Green Dice: ", green)
      print("Red Dice: ", red)

    # Update player scores
    if p1_turn:
      p1_score += green
      p2_score -= red
    else:
      p2_score += green
      p1_score -= red

    print()
    # Event-X checks
    if not skip_events:

      # RoT, if triggered, Triples the values of the dice.
      # This step halves the values, bringing them back the original values.
      # We know this works because RoT has to trigger earlier above
      # for this to trigger, or else it gets skipped.
      if green == red:
        green /= 3
        green = int(green)
        red /= 3
        red = int(red)

      if green + red == 3:
        event3()
      if green + red == 4:
        event4()
      if green + red == 7:
        event7(green, red)
      

    if not skip_events:
      jackpot_listing(p1_turn, green + red)
      print_scores()
      if not p1_turn:
        input("\nPress 'ENTER' to begin the next round.")
        clear_screen()
      p1_turn = not p1_turn

print("\t347 — The Game")
while True:
  if end_game_check(): break
  game_loop()

clear_screen()
if p1_score >= goal_score or p2_score <= loss_score:
  print("\tPlayer 1 wins!")
elif p2_score >= goal_score or p1_score <= loss_score:
  print("\tPlayer 2 wins!")
print("\n\tMatch Stats")
print("Number of rounds played: ", current_round)
if p1_jackpot_complete or p2_jackpot_complete:
  if p1_jackpot_complete:
    print("Player 1 completed the 347 Jackpot.")
  elif p2_jackpot_complete:
    print("Player 2 completed the 347 Jackpot.")
else:
  print("Final Scores:")
  print_scores()
input("\nThanks for playing! :D\nPress 'ENTER' to quit the game.")
