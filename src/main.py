import random
import uuid

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


class Hand():

    def __init__(self, dice_set: DiceSet):
        self.dice_set = dice_set
        self.dice_set.reset_dice_values()
        self.score = 0

    def play(self):
        for turn in range(2):
            self.dice_set.add_dice()

            # possibly reset dice if first turn and more than 4 dice in play
            if turn == 0 and self.dice_set.count_dice() > 4 and random.choice([False, True]):
                self.score = -1
                self.dice_set.reset_dice_set()
            
            # roll dice
            self.dice_set.roll_dice()

            # bust
            if self.dice_set.count_foxes() >= 3:
                self.dice_set.reset_dice_set()
                self.score = 0
                break
            
            # if score, possibly cash out on first turn
            if turn == 0 and self.dice_set.count_chickens() > 0 and random.choice([False, True]):
                break

        self.dice_set.add_dice()
        self.score += self.dice_set.count_chickens()
        return self.score

class Player():

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.score = 0

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
                print(f'\nPlayer ID: {player.id}')
                print(f'score: {player.score}')
                hand = Hand(self.dice_set)
                player.score += hand.play()
                if player.score >= 25:
                    print(f'Player ID {player.id} wins!')
                    break
                self.round += 1


if __name__ == '__main__':
    g = Game()
    g.play()
