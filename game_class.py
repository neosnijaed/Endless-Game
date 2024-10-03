import os
import random
import time
from datetime import datetime

import ascii_pictures

SAVE_FILE_NAME = 'save_file.txt'
SCORES_FILE_NAME = 'high_scores.txt'


class MyRandom:
    """The creation of a customized random class"""

    def __init__(self):
        """The initializer of the customized MyRandom object."""
        self.state = int(time.strftime("%H:%M:%S", time.localtime()).replace(":", ""))
        self.multiplier = 1103515245
        self.increment = 12345
        self.modulus = 2 ** 31

    def randint(self, ani_min_dur, ani_max_dur):
        """Apply LCG algorithm to get a pseudo-random number with customized seed"""
        self.state = (self.multiplier * self.state + self.increment) % self.modulus
        return ani_min_dur + (self.state % (ani_max_dur - ani_min_dur + 1))


class Game:
    """The creation of the Game class and the related functionalities."""

    def __init__(self, seed, ani_min_dur, ani_max_dur, loc_names):
        """The initializer of the Game object."""
        self.my_random = MyRandom()
        random.seed(seed) if seed != 'None' else random.seed()
        self.ani_min_dur = ani_min_dur if ani_min_dur != 'None' else 0
        self.ani_max_dur = ani_max_dur if ani_max_dur != 'None' else 0
        self.loc_names = loc_names.replace('_', ' ').split(',')
        self.player_name = ''
        self.titanium_balance = 0
        self.robots = 3
        self.titanium_scan = False
        self.enemy_scan = False

    def game_intro(self):
        """Control sequence of the game intro.

        Show a welcoming screen of the game.
        Show the game intro menu with available options the player can choose from.
        Ask the player for a valid choice from the game intro menu.
        Play, get player's score, get help or exit game based on player's choice.
        Return Values:
        String of information what to do next in the game.
        """
        actions = {
            'New': self.enter_new_game,
            'Load': self.load_game,
            'High': self.show_scores,
            'Help': self.get_help,
            'Exit': self.exit_game
        }
        print(ascii_pictures.welcoming_screen)
        print(
            '[New]  Game\n[Load] Game\n[High] Scores\n[Help]\n[Exit]'
        )
        chosen_opt = self.get_command(('New', 'Load', 'High', 'Help', 'Exit'))
        return actions[chosen_opt]()

    def get_command(self, options):
        """Ask Player for a command until this command is valid.

        Arguments:
        options {tuple(str)} -- Valid options for the command.
        Return Values:
        The option of Player's choice, that is valid.
        """
        if (option := input('\nYour command:\n').strip().title()) not in options:
            print('\nInvalid input')
            return self.get_command(options)
        else:
            return option

    def enter_new_game(self):
        """Ask for Player's name and if he/she is ready to play the game or return to Intro Menu"""
        self.player_name = input('\nEnter your name:\n').strip()
        self.titanium_balance = 0
        self.titanium_scan = False
        self.enemy_scan = False
        print(f'\nGreetings, commander {self.player_name}!')
        print('Are you ready to begin?')
        print(' '.join(f'[{opt}]' if opt != 'Menu' else 'Return to Main[Menu]' for opt in ('Yes', 'No', 'Menu')))
        return self.is_player_ready()

    def is_player_ready(self):
        """Ask Player until he/she is ready to continue or return to Intro Menu."""
        ready = self.get_command(('Yes', 'No', 'Menu'))
        if ready == 'Yes':
            return 'enter game'
        elif ready == 'No':
            print('\nHow about now.')
            print(' '.join(f'[{opt}]' if opt != 'Menu' else 'Return to Main[Menu]' for opt in ('Yes', 'No', 'Menu')))
            return self.is_player_ready()
        elif ready == 'Menu':
            return 'intro menu'

    def load_game(self):
        """Get chosen player's data from file and load player's data to the game."""
        slots, chosen_slot = self.show_load_save_menu()
        if chosen_slot == 'Back':
            return 'intro menu'
        if slots[int(chosen_slot) - 1].strip() == 'empty':
            print('Empty slot!\n')
            return self.load_game()
        else:
            with open(SAVE_FILE_NAME, 'r', encoding='utf-8') as file:
                slots = file.readlines()
            slot_data = slots[int(chosen_slot) - 1].strip().split()
            self.player_name = slot_data[0]
            self.titanium_balance = int(slot_data[2])
            self.robots = int(slot_data[4])
            if len(slot_data) == 11:
                if slot_data[10] == 'titanium_info,enemy_info':
                    self.titanium_scan = True
                    self.enemy_scan = True
                elif slot_data[10] == 'titanium_info':
                    self.titanium_scan = True
                elif slot_data[10] == 'enemy_info':
                    self.enemy_scan = True
            print(ascii_pictures.loading_successful)
            print(f' Welcome back, commander {self.player_name}!')
            return 'enter game'

    def show_load_save_menu(self):
        """Show empty/saved slots and player chooses one among them."""
        with open(SAVE_FILE_NAME, 'r') as file:
            slots = file.readlines()
        print('   Select save slot:')
        for i, slot in enumerate(slots, start=1):
            print(f'    [{i}] {slot.strip()}')
        chosen_slot = self.get_command(('1', '2', '3', 'Back'))
        return slots, chosen_slot

    def show_scores(self):
        """Display players top 10 scores"""
        print('        \nHIGH SCORES\n')
        with open(SCORES_FILE_NAME, 'r') as file:
            for i, line in enumerate(file.readlines(), start=1):
                print(f'({i}) {line.strip()}')
        print('\n       [Back]')
        if self.get_command(('Back',)) == 'Back':
            return 'intro menu'

    @staticmethod
    def get_help():
        print('\nComing SOON! Thanks for playing!')
        return 'exit game'

    @staticmethod
    def exit_game():
        """Exit game."""
        print('\nThanks for playing, bye!')
        return 'exit game'

    def enter_game(self):
        """Control sequence of the game.

        Show menu when player enters the game.
        Ask user for a valid input out of menu options.
        Explore, upgrade, save or exit based on Player's valid input.
        Return Values:
        String for navigating Player to different game states and/or doing actions.
        """
        actions = {
            'Ex': self.explore_locations,
            'Up': self.upgrade,
            'Save': self.save_game,
            'M': self.show_game_menu
        }
        ascii_pictures.show_hub(self.titanium_balance, self.robots)
        chosen_opt = self.get_command(('Ex', 'Up', 'Save', 'M'))
        return actions[chosen_opt]()

    def explore_locations(self):
        """Explore or choose a location where to get Titanium lumps from.

        Game chooses between 1-9 locations at random to explore.
        Generate a random location name if player chooses to explore.
        Each generated location gets between 10-100 titanium lumps at random.
        Show Player a menu with generated locations to choose and with the option to choose to explore more.
        With titanium scan and/or enemy scan upgrade, menu also shows titanium/enemy info for each location.
        If player chooses a location, player gets the titanium lumps from chosen location.
        If player encounters enemy, player loses 1 robot.
        if player has no robots, player loses the gathered titanium and loses the game.
        Save players name and titanium balance to top 10 list, if he/she loses the game.
        If maximum of capable explorations is reached, player can still choose one of the explored locations.
        Player inbetween can choose to go back to game menu whenever possible.

        """
        location_options = list()
        titania = list()
        encounter_rates = list()
        chosen_opt = 'S'
        explore_num = random.randint(1, 9)
        location_generator = (random.choice(self.loc_names) for _ in range(explore_num))
        while chosen_opt == 'S':
            try:
                location_options.append(next(location_generator))
            except StopIteration:
                print('Nothing more in sight')
                print(f'       [Back]')
                chosen_opt = self.get_command(tuple(str(i) for i in range(1, len(location_options) + 1)) + ('Back',))
            else:
                titania.append(random.randint(10, 100))
                encounter_rates.append(random.random())
                self.searching_deploying_time('search')
                self.show_explore_menu(zip(location_options, titania, encounter_rates))
                chosen_opt = self.get_command(
                    tuple(str(i) for i in range(1, len(location_options) + 1)) + ('S', 'Back'))
            finally:
                if chosen_opt == 'Back':
                    return 'enter game'
                elif chosen_opt.isdigit():
                    chosen_location, chosen_titanium, chosen_rate = (
                        tuple(zip(location_options, titania, encounter_rates)))[int(chosen_opt) - 1]
                    self.searching_deploying_time('deploy')
                    if chosen_rate > (second_rate := random.random()) and self.robots > 1:
                        print(f'Enemy encounter\n{chosen_location} explored successfully, 1 robot lost..')
                        self.robots -= 1
                    elif chosen_rate > second_rate and self.robots == 1:
                        print('Enemy encounter!!!')
                        print('Mission aborted, the last robot lost...')
                        print(ascii_pictures.game_over)
                        self.save_top_ten(self.evaluate_final_score())
                        self.player_name = ''
                        self.titanium_balance = 0
                        self.titanium_scan = False
                        self.enemy_scan = False
                        return 'intro menu'
                    else:
                        print(f'{chosen_location} explored successfully, with no damage taken.')
                    print(f'Acquired {chosen_titanium} lumps of titanium')
                    self.titanium_balance += chosen_titanium
                    return 'enter game'

    def searching_deploying_time(self, search_or_deploy):
        """Wait a random amount of seconds until search or deployment is done."""
        ani_dur = self.my_random.randint(self.ani_min_dur, self.ani_max_dur)
        if search_or_deploy == 'search':
            print('Searching', end='')
        elif search_or_deploy == 'deploy':
            print('Deploying robots', end='')
        for _ in range(ani_dur):
            time.sleep(1)
            print('.', end='')
        print('\n', end='')

    def show_explore_menu(self, data: zip):
        """Show explore menu with available locations/options for the Player to choose."""
        for i, (location, titanium, encounter_rate) in enumerate(data, start=1):
            print(f'[{i}] {location.replace("_", " ")} ', end='')
            print(f'Titanium: {titanium} ', end='') if self.titanium_scan is True else ''
            print(f'Encounter rate: {round(encounter_rate * 100)}%', end='') if self.enemy_scan is True else ''
            print()
        print('\n[S] to continue searching')

    def evaluate_final_score(self):
        """Return new top 10 list if new score fits in top 10.

        If no one is in the top 10 return the new player and the new score.
        Insert new player and new score to top 10 if the new score is greater than one of top 10 scores.
        Append new score if new score is the lowest but the top scores are less than 10.
        Return Values:
        list[tuple[str, int]]: Top 10 list with each player's name and score in a tuple.
        """
        with (open(SCORES_FILE_NAME, 'r', encoding='utf-8') as file):
            names_scores = list(map(
                lambda x: (x[0], int(x[1].strip())), [line.strip().split() for line in file.readlines()]
            ))
        if len(names_scores) == 0:
            names_scores.append((self.player_name, self.titanium_balance))
        else:
            for index, name_score in enumerate(names_scores):
                if self.titanium_balance > name_score[1]:
                    names_scores.insert(index, (self.player_name, self.titanium_balance))
                    if len(names_scores) > 10:
                        del names_scores[-1]
                    return names_scores
            if len(names_scores) < 10:
                names_scores.append((self.player_name, self.titanium_balance))
        return names_scores

    @staticmethod
    def save_top_ten(names_scores):
        """Write top 10 list to file."""

        with (open(SCORES_FILE_NAME, 'w', encoding='utf-8') as file):
            for name, score in names_scores:
                file.write(f'{name} {score}\n')

    def upgrade(self):
        """Show available upgrades, player can choose an upgrade and then returns to the game."""

        print(ascii_pictures.upgrade_store)
        self.choose_upgrade()
        return 'enter game'

    def choose_upgrade(self):
        """Ask player to choose an upgrade for titanium scan, enemy scan or buy a new robot."""
        chosen_opt = self.get_command(('1', '2', '3', 'Back'))
        if chosen_opt == 'Back':
            return
        elif chosen_opt == '1' and self.titanium_balance >= 250:
            print('Purchase successful. You can now see how much titanium you can get from each found location.')
            self.titanium_balance -= 250
            self.titanium_scan = True
        elif chosen_opt == '2' and self.titanium_balance >= 500:
            print(
                'Purchase successful. You will now see how likely you will encounter an enemy at each found location.'
            )
            self.titanium_balance -= 500
            self.enemy_scan = True
        elif chosen_opt == '3' and self.titanium_balance >= 1000:
            print('Purchase successful. You now have an additional robot')
            self.titanium_balance -= 1000
            self.robots += 1
        else:
            print('Not enough titanium!')
            self.choose_upgrade()

    def save_game(self):
        """Save game data to file and return to game."""
        self.save_data()
        print(ascii_pictures.saving_successful)
        return 'enter game'

    def save_data(self):
        """Get current player's data, format and write them into file."""
        slots, chosen_slot = self.show_load_save_menu()
        date_time_now = datetime.now()
        slots[int(chosen_slot) - 1] = (
            f'{self.player_name} Titanium: {self.titanium_balance} Robots: {self.robots} '
            f'Last save: {date_time_now.date()} {str(date_time_now.time())[:str(date_time_now.time()).rfind(":")]} '
            f'Upgrades:'
            f'{" titanium_info,enemy_info" if self.titanium_scan is True and self.enemy_scan is True else ""}'
            f'{" titanium_info" if self.titanium_scan is True else ""}'
            f'{" enemy_info" if self.enemy_scan is True else ""}'
        )
        with open(SAVE_FILE_NAME, 'w') as file:
            for slot in slots:
                file.write(f'{slot}\n')

    def show_game_menu(self):
        """Show game menu and based and ask Player's input out of game menu options.
        Return Values:
        String for navigating Player to different game states and/or doing actions.
        """
        print(ascii_pictures.game_menu)
        chosen_opt = self.get_command(('Back', 'Main', 'Save', 'Exit'))
        if chosen_opt == 'Back':
            return 'enter game'
        elif chosen_opt == 'Main':
            return 'intro menu'
        elif chosen_opt == 'Save':
            return self.save_and_exit()
        elif chosen_opt == 'Exit':
            return self.exit_game()

    def save_and_exit(self):
        """Save game data to file and exit game."""
        self.save_data()
        print(ascii_pictures.saving_successful)
        print('\nThanks for playing, bye!')
        return 'exit game'

    @staticmethod
    def set_file():
        """If file doesn't exist, create it.

        Create file with 3 empty slots for the saving functionality.
        Create file for the top 10 scores.
        """
        if not os.path.isfile(SAVE_FILE_NAME):
            with open(SAVE_FILE_NAME, 'w') as file:
                for _ in range(1, 4):
                    file.write('empty\n')
        if not os.path.isfile(SCORES_FILE_NAME):
            open(SCORES_FILE_NAME, 'w').close()
