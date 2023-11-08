from dice import four_sided_dice, six_sided_dice, make_test_dice
from ucb import main, trace, log_current_line, interact
goal = 100 # The goal of Hog is to score 100 points.
commentary = False # Whether to display commentary for every roll.

def roll_dice(num_rolls, dice= six_sided_dice, who = "Boss Hogg"):
    assert type(num_rolls) == int
    assert num-rolls > 0
    total , k , x = 0, 1, 0
    while k <= num_rolls:
        outcome = dice()
        if outcome == 1:
            total, k ,x = 1, k+1, 1
        else:
            total, k = total + outcome, k+1
        if commentary:
            announce(outcome, who)
    if x == 1:
        total = 1
    return total

def take_turn(num_rolls, opponent_score, dice=six_sided_dice, who='Boss Hogg'):

    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    if commentary:
        print(who, 'is going to roll', num_rolls, 'dice')
    if num_rolls == 0:
        if opponent_score < 10:
            total = 1
        else:
            total = opponent_score//10 +1
        return total
    return roll_dice(num_rolls, dice, who)
def take_turn_test():

    print('-- Testing roll_dice with deterministic test dice --')
    dice = make_test_dice(4, 6, 1)
    assert roll_dice(2, dice) == 10, 'First two rolls total 10'
    dice = make_test_dice(4, 6, 1)
    assert roll_dice(3, dice) == 1, 'Third roll is a 1'
    dice = make_test_dice(1, 2, 3)
    assert roll_dice(3, dice) == 1, 'First roll is a 1'
    print('-- Testing take_turn --')
    dice = make_test_dice(4, 6, 1)
    assert take_turn(2, 0, dice) == 10, 'First two rolls total 10'
    dice = make_test_dice(4, 6, 1)
    assert take_turn(3, 20, dice) == 1, 'Third roll is a 1'
    assert take_turn(0, 34) == 4, 'Opponent score 10s digit is 3'
    assert take_turn(0, 71) == 8, 'Opponent score 10s digit is 7'
    assert take_turn(0, 7) == 1, 'Opponont score 10s digit is 0'
    '*** You may add more tests here if you wish ***'
    print('Tests for roll_dice and take_turn passed.')

    

def select_dice(score, opponent_score):

    if ((score+opponent_score)%7 == 0):
        return four_sided_dice
    else:
        return six_sided_dice

def other(who):
    return (who + 1) % 2


def name(who):
    if who == 0:
        return 'Player 0'
    elif who == 1:
        return 'Player 1'
    else:
        return 'An unknown player'


def play(strategy0, strategy1):

    who = 0 # Which player is about to take a turn, 0 (first) or 1 (second)
    global opponent_score
    global score
    score, opponent_score = 0,0
    while score < goal and opponent_score < goal:
        dice = select_dice(score, opponent_score)
        if num_allowed_dice(score, opponent_score) == 1:
            num_dice = 1
        else:
            if name(who) == 'Player 0':
                num_dice = strategy0(score, opponent_score)
            else :
                num_dice = strategy1(score, opponent_score)
            num_rolls = num_dice
            one_round_score = take_turn(num_rolls, opponent_score, dice=select_dice(score, opponent_score), who=name(who))
            score, opponent_score = opponent_score, score + one_round_score
            who = other(who)
    who = other(who)
    return who


def always_roll(n):
    def strategy(score, opponent_score):
        return n
    return strategy


def make_average(fn, num_samples=100000):

    def average_value(*args):
        result, k = 0, 1
        while k <= num_samples:
            result, k = fn(*args) + result, k+1
        return result/num_samples
    return average_value


def compare_strategies(strategy, baseline=always_roll(5)):
    as_first = 1 - make_average(play)(strategy, baseline)
    as_second = make_average(play)(baseline, strategy)
    return (as_first + as_second) / 2 


def eval_strategy_range(make_strategy, lower_bound, upper_bound):

    best_value, best_win_rate = 0, 0
    value = lower_bound
    while value <= upper_bound:
        strategy = make_strategy(value)
        win_rate = compare_strategies(strategy)
        print('Win rate against the baseline using', value, 'value:', win_rate)
        if win_rate > best_win_rate:
            best_win_rate, best_value = win_rate, value
        value += 1
    return best_value


def run_experiments():

    result = eval_strategy_range(always_roll, 1, 10)
    print('Best always_roll strategy:', result)
    if False: 
        result = eval_strategy_range(make_comeback_strategy, 5, 15)
        print('Best comeback strategy:', result)
    if False: 
        result = eval_strategy_range(make_mean_strategy, 1, 10)
        print('Best mean strategy:', result)

def make_mean_strategy(min_points, num_rolls=5):

    def mean_strategy(score, opponent_score):
        if opponent_score//10 +1 >= min_points:
            new_score = opponent_score//10 + 1 + score
            if ((new_score + opponent_score)%7 ==0 or (new_score + opponent_score)%10 == 7):
                return 0
        return num_rolls
    return mean_strategy


def final_strategy(score, opponent_score):

    be_a_meanie = make_mean_strategy(4, num_rolls=5)
    comeback_time_baby = make_comeback_strategy(8, num_rolls=5)
    if opponent_score//10+1+score >= goal :
        result = 0
    elif score >= 86 :
        result = 4
    elif opponent_score - score >= 22:
        result = be_a_meanie(score, opponent_score)
        if result == 0:
            return 0
        result=result+3
    elif score - opponent_score >= 5:
        if score - opponent_score > 34:
            result = 4
        result = be_a_meanie(score, opponent_score)
    elif opponent_score >= 30 and opponent_score <= 96:
        result = be_a_meanie(score, opponent_score)
    else :
        result = 5
    return result


def final_strategy_test():

    print('-- Testing final_strategy --')
    print('Win rate:', compare_strategies(final_strategy))

def interactive_strategy(score, opponent_score):

    print('Current score:', score, 'to', opponent_score)
    while True:
        response = input('How many dice will you roll? ')
        try:
            result = int(response)
        except ValueError:
            print('Please enter a positive number')
            continue
        if result < 0:
            print('Please enter a non-negative number')
        else:
            return result

        
def play_interactively():
    global commentary
    commentary = True
    print("Shall we play a game?")
    winner = play(interactive_strategy, always_roll(5))
    if winner == 0:
        print("You win!")
    else:
        print("The computer won.")

        
def play_basic():

    global commentary
    commentary = True
    winner = play(always_roll(5), always_roll(6))
    if winner == 0:
        print("Player 0, who always wants to roll 5, won.")
    else:
        print("Player 1, who always wants to roll 6, won.")



def run(*args):

    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--take_turn_test', '-t', action='store_true')
    parser.add_argument('--play_interactively', '-p', action='store_true')
    parser.add_argument('--play_basic', '-b', action='store_true')
    parser.add_argument('--run_experiments', '-r', action='store_true')
    parser.add_argument('--final_strategy_test', '-f', action='store_true')
    args = parser.parse_args()
    for name, execute in args.__dict__.items():
        if execute:
            globals()[name]()
