'''
MUNE engine created by  u/Bionicle_fanatic
Translated to python by u/Oakforthevines
'''

###modules used###
from colorama import Fore as F, Back as B, init
from sys import platform
import random as r
import sf_rand_words as rw
import textwrap
import glob


#Game class includes most back-end work of program
class game:
    #values used in menu functions
    mod_rolls = 0
    interv_points = 0

    #stuff for files
    if platform == 'win32':  #temlorary solution
        init(convert=True)
        path = 'C:/Users/Stephen/Documents/Code Stuff/Personal Projects/MUNE/mune_python'
    else:
        path = '/sdcard/code/mune/mune_python'
    profile_path = path + '/saves/'
    session_name = ''
    session_filename = ''

    #lists used in menu functions
    entities = []
    open_plots = []
    closed_plots = []
    input_history = []

    #saves user input to log
    def save(to_save):
        #ensures no blank or new line characters added to log
        if to_save not in ['', '\n']:
            game.input_history.append(to_save)

        #saves all lists to file with delimeters
        with open(game.session_filename, 'w') as f:
            #saves non-blank entries to file with | as delimeter
            for entity in range(len(game.entities)):
                if game.entities[entity] != '':
                    f.write(game.entities[entity] + '|')
            #prevents nothing from being written to file
            #if no delimeter is written, code breaks after 2 runs
            if game.entities == ['']:
                f.write('|')
            #delimeter between info read into different lists
            f.write('^')
            #rinse and repeat for each list
            for open_plot in range(len(game.open_plots)):
                if game.open_plots[open_plot] != ['']:
                    f.write(game.open_plots[open_plot] + '|')
            if game.open_plots == ['']:
                f.write('|')
            f.write('^')
            for closed_plot in range(len(game.closed_plots)):
                if game.closed_plots[closed_plot] != ['']:
                    f.write(game.closed_plots[closed_plot] + '|')
            if game.closed_plots == ['']:
                f.write('|')
            f.write('^')
            for line in range(len(game.input_history)):
                if game.input_history[line] != ['']:
                    f.write(game.input_history[line] + '|')
            if game.input_history == ['']:
                f.write('|')
            f.write('^')

    def load():
        #getting filenames in directory
        files = glob.glob(game.profile_path + '*.txt')
        profiles = [file[len(game.profile_path): -4] for file in files]
        profile = -1
        #^ensures new profile option has correct number if no files in save

        #printing profile names
        print('\n')
        formatting.center('PROFILES', '*')
        for profile in range(len(profiles)):
            print(str(profile + 1) + '. ' + profiles[profile])
        print('\n' + str(profile + 2) + '. New profile')
        print(('*' * formatting.screen_width) + '\n\n')

        #picking profile
        try:
            choice = int(input('\nWhich profile would you like to use?\n>>'))
        except:
            errors.error1()
            game.load()
            return

        #making a new profile
        if choice == (profile + 2):
            new_profile = input('\nWhat is the name of the new profile?\n>>')
            if '|' in new_profile or '^' in new_profile:
                errors.error3()
                game.load()
                return
            game.session_name = new_profile
            game.session_filename = game.profile_path+game.session_name+'.txt'

            #creates new save file
            with open(game.session_filename, 'w') as new:
                new.write('|^|^|^|')

            print('\n\n')
            formatting.center('A new adventure begins...')
            print(('~' * formatting.screen_width) + '\n\n')

        #picking existing profile
        elif choice in [x + 1 for x in range(len(profiles))]:
            game.session_name = profiles[choice - 1]
            game.session_filename = game.profile_path+game.session_name+'.txt'

            #reading in info from file
            with open(game.session_filename) as f:
                read_in = f.readlines()
            #splits text into large chunks
            read_in = read_in[0].split('^')
            #each chunk is split into individual entries
            game.entities = read_in[0].split('|')
            #last entry (always blank) is trimmed to prevent errors
            game.entities = game.entities[:-1]
            #rinse and repeat
            game.open_plots = read_in[1].split('|')
            game.open_plots = game.open_plots[:-1]
            game.closed_plots = read_in[2].split('|')
            game.closed_plots = game.closed_plots[:-1]
            game.input_history = read_in[3].split('|')
            game.input_history = game.input_history[:-1]

            #printing log of previous sessions
            print('\n\n')
            formatting.center('When last we left our heroes...')
            print(('~' * formatting.screen_width) + '\n')
            for line in game.input_history:
                print(line + '\n')
            print(('~' * formatting.screen_width) + '\n\n')

        #if user enters number out of range
        else:
            errors.error2()
            game.load()
            return

    def intro():
        #gives user an introduction to the program
        #lines go over pep8 char limit, but its the best i can do
        print('\n\n' + formatting.green + ('=' * formatting.screen_width))
        formatting.center('Welcome to the Python automated version of the MUNE engine by')
        formatting.center('u/Bionicle_fanatic. This program will read in what you type')
        formatting.center('in the console, and execute an action based on the first')
        formatting.center('character entered. For a list of commands, type "!" and press')
        formatting.center('ENTER at any time after picking a profile. Find the emulator at')
        formatting.center('http://homebrewery.naturalcrit.com/share/rkmo0t9k4Q.')
        formatting.center('If you find any bugs, please PM me on Reddit at u/Oakforthevines.')
        formatting.center('Safe travels, adventurer.')
        print('=' * formatting.screen_width)


#menu class includes most of what user interacts with
class menu:

    #The main feature, gives response to user's questions
    def oracle(user_in):
        #auto-saves user input
        game.save(user_in)

        responses = ['No, and...', 'No', 'No, but...',
                     'Yes, but...', 'Yes', 'Yes, and...']
        results = [r.randint(0, 5), r.randint(0, 5)]
        #+ mode gives user better chance of a positive result
        if user_in[0] == '+':
            result = max(results)
        #- mode does the opposite
        elif user_in[0] == '-':
            result = min(results)
        #default mode is just whatever is rolled first
        else:
            result = results[0]

        #keeps track of modified rolls
        #that is, results with 'and' or 'but'
        if result in [0, 2, 3, 5]:
            game.mod_rolls += 1
        #ensures user gets a max of 2 modified rolls in a row
        #changes result to unmodified form
        if game.mod_rolls >= 2:
            game.mod_rolls = 0
            if result in [0, 2]:
                result = 1
            else:
                result = 4

        #tracks intervention points
        if result == 5:
            game.interv_points += 1
        #ignores result and calls for intervention
        if game.interv_points == 3:
            game.interv_points = 0
            menu.intervention()
            return

        #prints and saves result
        result = responses[result]
        print(result + '\n')
        game.save(result)

    #called after 3 rolls of 'yes, and...'
    #introduces more random element of engine
    def intervention():
        intervs = ['A new entity has appeared',
                   'Something positive has happened to a known entity',
                   'Something negative has happened to a known entity',
                   'A plot line has advanced', 'A plot line has been regressed',
                   'Something unexpected has occured. Call for a portent to divine its nature']
        result = r.choice(intervs)
        #prints and saves result
        game.save(result)
        formatting.center('An intervention has occured!', '•')
        formatting.center(result)
        print()

    #prints list of known entities
    def entity_list():
        formatting.center('KNOWN ENTITIES', '*')
        #prevents index errors
        if game.entities != ['']:
            for entity in range(0, len(game.entities), 3):
                print('Entity #' + str((entity // 3) + 1))
                print('Name: ' + game.entities[entity])
                print('Disposition: ' + game.entities[entity + 1])
                print('Description: ' + game.entities[entity + 2] + '\n')
        print('Type & to add a new entity')
        print('Type $ to edit a known entity')
        print(('*' * formatting.screen_width) + '\n\n')

    #adds new entity to list
    def add_entity():
        #getting new name
        new_name = input('\nWhat is the name of the new entity?\n>>')
        #prevents delimeters in name
        if '|' in new_name or '^' in new_name:
            errors.error3()
            return

        #getting new disposition
        dispositions = ['Friendly', 'Neutral', 'Hostile']
        print('\nWhat is the disposition of the new entity?\n')
        print('1.) Friendly\n2.) Neutral\n3.) Hostile\n4.) Unsure (randomly determine)')
        try:
            new_disp = int(input('\n>>'))
        except:
            #catches non-number values
            errors.error1()
            return
        #when user picks from list
        if new_disp in [1, 2, 3]:
            new_disp = dispositions[new_disp - 1]
        #picks randomly from list
        elif new_disp == 4:
            new_disp = dispositions[r.randint(0, 2)]
        else:
            #If user picks out of range
            errors.error2()
            return

        #getting new description
        new_desc = input('\nDescribe the new entity\n>>')
        #prevents delimeters in description
        if '|' in new_desc or '^' in new_desc:
            errors.error3()
            return

        #saves new entry, and prints list
        game.entities.extend([new_name, new_disp, new_desc])
        game.save('')
        print()
        menu.entity_list()

    #allows user to edit an entry
    def edit_entity():
        menu.entity_list()
        try:  #selects entity to edit
            to_edit = int(input('\nWhich entity would you like to edit?\n>>'))
        except:  #if user inputs non number value
            errors.error1()
            return
        #if user enters number not in range
        if to_edit not in [x + 1 for x in range(len(game.entities)//3)]:
            errors.error2()
            return
        #prints components of entity
        to_edit = ((to_edit - 1) * 3)
        print('\nWhich part would you like to edit?\n')
        print('1.) ' + game.entities[to_edit])
        print('2.) ' + game.entities[to_edit + 1])
        print('3.) ' + game.entities[to_edit + 2])
        try:  #gets which component to edit
            to_edit_for_real = int(input('\n>>'))
        except:  #same as error1 above
            errors.error1()
            return
        if to_edit_for_real not in [1, 2, 3]:
            errors.error2()  #for out of range
            return
        if to_edit_for_real == 1:  #if editing name
            new_name = input('\nWhat is the new name of the entity?\n>>')
            if '|' in new_name or '^' in new_name:
                errors.error3()  #prevents delimeters in name
                return
            game.entities[to_edit] = new_name  #saves new name
        elif to_edit_for_real == 2:  #if editing disposition
            dispositions = ['Friendly', 'Neutral', 'Hostile']
            print('\nWhat is the new disposition of the entity?\n')
            print('1.) Friendly\n2.) Neutral\n3.) Hostile\n4.) Unsure (randomly determine)')
            try:  #catches non number input
                new_disp = int(input('\n>>'))
            except:
                errors.error1()
                return
            if new_disp in [1, 2, 3]:  #assigns new disposition
                game.entities[to_edit + 1] = dispositions[new_disp - 1]
            elif new_disp == 4:
                game.entities[to_edit + 1] = dispositions[r.randint(0, 2)]
            else:  #catches out of range
                errors.error2()
                return
        elif to_edit_for_real == 3:  #if editing description
            new_desc = input('\nDescribe the new entity\n>>')
            if '|' in new_desc or '^' in new_desc:
                errors.error3()  #prevents delimeters in description
                return
            game.entities[to_edit + 2] = new_desc  #assignes new description
        game.save('')  #saves changes
        print()  #for readability
        menu.entity_list()

    #prints open plot lines
    def open_plots():
        formatting.center('OPEN PLOTS', '*')
        if game.open_plots != ['']:
            for plot in range(len(game.open_plots)):
                print(str(plot + 1) + '.) ' + game.open_plots[plot])
        print('\nType ( to open a new plot line')
        print('Type > to edit a plot line')
        print('Type ) to close a plot line')
        print(('*' * formatting.screen_width) + '\n\n')

    def open_new_plot():
        new_plot = input('\nDescribe the new plot line:\n>>')
        if '|' in new_plot or '~' in new_plot:
            errors.error3()
            return
        game.open_plots.append(new_plot)
        game.save('')
        print()
        menu.open_plots()

    def edit_plot():
        menu.open_plots()
        try:
            to_edit = int(input('\nWhich plot line would you like to edit?\n>>'))
        except:
            errors.error1()
            return
        if to_edit not in [x + 1 for x in range(len(game.open_plots))]:
            errors.error2()
            return
        game.open_plots[to_edit - 1] = input('\nDescribe the plot change:\n>>')
        game.save('')
        menu.open_plots()

    def close_open_plot():
        menu.open_plots()
        try:
            to_close = int(input('\nWhich plot line would you like to close?\n>>'))
        except:
            errors.error1()
            return
        if to_close not in [x + 1 for x in range(len(game.open_plots))]:
            errors.error2()
            return
        game.closed_plots.append(game.open_plots[to_close - 1])
        del game.open_plots[to_close - 1]
        game.save('')
        print()
        menu.open_plots()

    def closed_plots():
        formatting.center('CLOSED PLOTS', '*')
        for plot in range(len(game.closed_plots)):
            print(str(plot + 1) + '.) ' + game.closed_plots[plot])
        print(('*' * formatting.screen_width) + '\n\n')

    #calls for 2 random words, saves them, and prints them
    def portent():
        words = rw.rand_words(2)
        game.save('# ' + words[0] + ' ' + words[1] + ' #')
        print('# ' + words[0] + ' ' + words[1] + ' #\n')

    #rolls on Table for When Everyting is Not as Expected
    def twene():
        #Results are too long to be in a single list
        #broken up for efficiency
        pre_text = ['A simple element (something of minimal importance to the scene)',
                    'A major element (something of great importance to the scene)']
        post_text = [' has increased in scale or importance',
                     ' has decreased in scale or importance',
                     ' has been added to the scene', ' has been removed from the scene']
        result = r.randint(1, 10)
        #combines text
        if result == 1:
            result = pre_text[0] + post_text[0]
        elif result == 2:
            result = pre_text[0] + post_text[1]
        elif result == 3:
            result = pre_text[0] + post_text[2]
        elif result == 4:
            result = pre_text[0] + post_text[3]
        elif result == 5:
            result = pre_text[1] + post_text[0]
        elif result == 6:
            result = pre_text[1] + post_text[1]
        elif result == 7:
            result = pre_text[1] + post_text[2]
        elif result == 8:
            result = pre_text[1] + post_text[3]
        elif result == 9:
            result = 'The unexpected element is positive in nature. Call for a portent to divine further'
        elif result == 10:
            result = 'The unexpected element is positive in nature. Call for a portent to divine further'

        #prints and saves result
        formatting.center_multi(result, formatting.screen_width)
        print()
        game.save(result)

    #prints list of high-level functions user can call with key
    def help_menu():
        formatting.center('HELP', '*')
        print(' Character:' + (' ' * 18) + 'Command:')
        print((' ' * 5) + '?' + (' ' * 8) + 'Queries the Oracle for a normal outcome')
        print((' ' * 5) + '+' + (' ' * 8) + 'Queries the Oracle for a likely outcome')
        print((' ' * 5) + '-' + (' ' * 8) + 'Queries the Oracle for an unlikely outcome')
        print((' ' * 5) + '@' + (' ' * 8) + 'Displays a list of known entities')
        print((' ' * 5) + '[' + (' ' * 8) + 'Displays a list of open plot lines')
        print((' ' * 5) + ']' + (' ' * 8) + 'Displays a list of closed plot lines')
        print((' ' * 5) + '#' + (' ' * 8) + 'Calls for a portent')
        print((' ' * 5) + '*' + (' ' * 8) + 'Rolls on Table for When Everything is Not as Expected')
        print((' ' * 5) + '!' + (' ' * 8) + 'Opens the help page (current page)')
        print((' ' * 5) + '~' + (' ' * 8) + 'Quits the program')
        print(('*' * formatting.screen_width) + '\n\n')

    #saves lists to file, and exits the game
    def quit_game():
        game.save('')
        quit()

    #names of functions mapped to their input keys
    commands = {'?': 'oracle', '+': 'oracle',
                '-': 'oracle', '@': 'entity_list',
                '&': 'add_entity', '$': 'edit_entity',
                '[': 'open_plots', '(': 'open_new_plot',
                '>': 'edit_plot', ')': 'close_open_plot',
                ']': 'closed_plots', '#': 'portent',
                '*': 'twene',
                '!': 'help_menu', '~': 'quit_game'}

    #driving force of menu functions
    def switch(self, user_in):
        #gets function name from dictionary using key
        func_name = menu.commands[user_in[0]]
        #makes function so it can be called
        func = getattr(self, func_name)
        #passes input to oracle function
        #since oracle function is only one that uses it
        if user_in[0] in ['?', '+', '-']:
            func(user_in)
        else:
            func()


class formatting:  #to easily format output text
    red = F.RED  #because I'm lazy and this is easier to type
    green = F.LIGHTGREEN_EX  #same as above
    screen_width = 67  #can be changed to your desired width

    def center(text, char=' '):
        width1 = (formatting.screen_width // 2) - (len(text) // 2)
        print((char * width1) + text + (char * (formatting.screen_width - len(text) - width1)))

    def center_multi(text, lineLen):
        for line in textwrap.wrap(text, width=lineLen):
            print(line.center(formatting.screen_width))


class errors:  #catching common errors
    def error1():  #when a user inputs something that should be an int
        print(formatting.red + '\nERROR: non-numerical value entered.')
        print(formatting.green + '\n')

    def error2():  #when a user inputs an int out of range
        print(formatting.red + '\nERROR: number entered is out of range')
        print(formatting.green + '\n')

    def error3():  #when a user inputs a delimeter in their text
        print(formatting.red + '\nERROR: text cannot contain "|" or "^"')
        print(formatting.green + '\n')

    #forbidden characters for future reference
    forbidden = ['', '\n', '|', '^']


#primary interface the user interacts with
#takes user input, and decides what to do with it
def main():
    game.intro()
    game.load()

    while False == False:  #to run until user exits the game
        user_in = input('>>')  #takes input
        print()  #to increase readbility of game
        if len(user_in) == 0:  #makes sure there is some input to avoid errors
            user_in = '\n'
        #prevents delimeters from being used in text
        if '|' in user_in or '^' in user_in:
            errors.error3()
            continue
        if user_in[0] in menu.commands.keys():  #checks if first char is a key
            menu.switch(menu, user_in)  #executes function if ^ is true
        else:
            game.save(user_in)  #otherwise, input is saved to log

main()

'''
###To-do###

*generalise path using os module
*make sure errors are accounted for
*properly comment everything
*refine algorithms
*allow for user options menu:
    -select default color
    -change command characters
'''