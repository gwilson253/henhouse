import random
import uuid

from dataclasses import dataclass

DATA_FILE_PATH = 'data.csv'

class Dice():

    def __init__(self):
        self.sides = [1, 2, 3, 4, 5, 6]
        self.value = None

    def roll(self):
        self.value = random.choice(self.sides)
    
class WhiteDice(Dice):

    def __init__(self):
        super().__init__()
        self.color = 'white'
        self.sides = ['fox', 'chicken', 'egg', 'egg', 'egg', 'blank']
    
class YellowDice(Dice):

    def __init__(self):
        super().__init__()
        self.color = 'yellow'
        self.sides = ['fox', 'chicken', 'chicken', 'egg', 'egg', 'blank']
    
class OrangeDice(Dice):

    def __init__(self):
        super().__init__()
        self.color = 'orange'
        self.sides = ['fox', 'fox', 'double chicken', 'double chicken', 'blank', 'blank']

class DiceSet():

    def __init__(self):
        self.dice_set = []
        self.reset_dice_set()

    def reset_dice_set(self):
        print('\nresetting dice set...\n')
        self.dice_set = [WhiteDice(), WhiteDice(), WhiteDice(), WhiteDice()]

    def reset_dice_values(self):
        print('\nresetting dice VALUES...\n')
        for d in self.dice_set:
            d.value = None

    def show_dice(self):
        print('-' * 25)
        for dice in self.dice_set:
            print(f'{dice.color} | {dice.value}')

    def count_dice(self):
        return len(self.dice_set)
    
    def roll_dice(self):
        for dice in self.dice_set:
            if dice.value not in ('chicken', 'double chicken', 'fox'):
                dice.roll()
        self.show_dice()

    def add_dice(self):
        eggs = len([_ for _ in self.dice_set if _.value == 'egg'])
        yellows = len([_ for _ in self.dice_set if _.color == 'yellow'])
        oranges = len([_ for _ in self.dice_set if _.color == 'orange'])

        yellows_to_add = min(eggs, 4-yellows)
        
        oranges_to_add = 0
        if yellows + yellows_to_add == 4:
            oranges_to_add = min(eggs - yellows_to_add, 4 - oranges)

        for _ in range(yellows_to_add):
            self.dice_set.append(YellowDice())
        
        for _ in range(oranges_to_add):
            self.dice_set.append(OrangeDice())

    def count_chickens(self):
        chickens = len([_ for _ in self.dice_set if _.value == 'chicken'])
        chickens += 2 * len([_ for _ in self.dice_set if _.value == 'double chicken'])
        return chickens

    def count_foxes(self):
        return len([_ for _ in self.dice_set if _.value == 'fox'])

@dataclass
class TurnRecord:
    game_id: str = None
    round: str = None
    player_id: str = None
    roll_1_dice_count: int = None # number of die passed to the player at the start of their turn
    roll_1_reset_dice_set: int = 0 # whether the player reset the dice set at the start of their turn
    roll_1_chickens: int = None # count of chickens from first roll
    roll_1_foxes: int = None # count of foxes from first roll
    roll_1_bust: int = 0 # whether roll 1 was a bust (i.e. 3+ foxes)
    roll_2_dice_count: int = 0 # number of die in play for the second roll of the turn
    roll_2_pass: int = 0 # whether the player declines their second roll
    roll_2_chickens: int = 0 # count of chickens from second roll
    roll_2_foxes: int = 0 # count of foxes from second roll
    roll_2_bust: int = 0 # whether roll 1 was a bust (i.e. 3+ foxes)
    turn_score: int = None # total points earned in the turn

    def __str__(self):\
       return ','.join(str(v) if v is not None else '' for v in self.__dict__.values())

class Turn():

    def __init__(self, dice_set: DiceSet, turn_record: TurnRecord):
        self.dice_set = dice_set
        self.turn_record = turn_record
        self.dice_set.reset_dice_values()
        self.score = 0

    def play(self):
        self.turn_record.roll_1_dice_count = self.dice_set.count_dice()

        # r1: decide whether to reset dice set
        if self.dice_set.count_dice() > 4 and random.choice([False, True]):
            self.score = -1
            self.dice_set.reset_dice_set()
            self.turn_record.roll_1_reset_dice_set = 1

        # r1: roll
        self.dice_set.roll_dice()

        self.turn_record.roll_1_chickens = self.dice_set.count_chickens()
        self.turn_record.roll_1_foxes = self.dice_set.count_foxes()
            
        # r1: cash-out decision
        if (self.dice_set.count_chickens() > 0
            and self.dice_set.count_foxes() < 3
            and random.choice([False, True])):
                self.score += self.dice_set.count_chickens()
                self.turn_record.roll_2_pass = 1

        # r1: bust?
        elif self.dice_set.count_foxes() >= 3:
            self.dice_set.reset_dice_set()
            self.score = 0
            self.turn_record.roll_1_bust = 1

        # r2...
        else:
            self.dice_set.add_dice()
            self.dice_set.roll_dice()

            self.turn_record.roll_2_dice_count = self.dice_set.count_dice()
            self.turn_record.roll_2_chickens = self.dice_set.count_chickens()
            self.turn_record.roll_2_foxes = self.dice_set.count_foxes()
            
            if self.dice_set.count_foxes() >= 3:
                self.dice_set.reset_dice_set()
                self.score = 0
                self.turn_record.roll_2_bust = 1
            else:
                self.score += self.dice_set.count_chickens()
                self.dice_set.add_dice()
        
        print(f'Turn Score: {self.score}')
        self.turn_record.turn_score = self.score
        return self.score

@dataclass
class Player():
    id: str = str(uuid.uuid4())
    score: int = 0

class Game():

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.players = [Player() for _ in range(random.choice(range(2, 9)))]
        self.round = 0
        self.dice_set = DiceSet()

    def play(self):
        print(f'\nGame ID: {self.id}')
        while max([_.score for _ in self.players]) < 25:
            print(f'\nRound: {self.round}')
            for player in self.players:
                tr = TurnRecord(game_id=self.id, round=self.round, player_id=player.id)
                print(f'\nPlayer ID: {player.id}')
                print(f'score: {player.score}')
                turn = Turn(self.dice_set, tr)
                player.score += turn.play()
                write_turn_record(tr)
                if player.score >= 25:
                    print(f'Player ID {player.id} wins!')
                    break
            self.round += 1

def init_data_file():
    tr = TurnRecord()
    with open(DATA_FILE_PATH, 'w') as f:
        f.write(','.join(tr.__dict__.keys())+'\n')

def write_turn_record(turn_record):
    with open(DATA_FILE_PATH, 'a') as f:
        f.write(str(turn_record) + '\n')

if __name__ == '__main__':
    init_data_file()
    for i in range(5):
        g = Game()
        g.play()
