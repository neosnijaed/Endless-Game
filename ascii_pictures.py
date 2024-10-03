welcoming_screen = (
    "+===========================================================+\n"
    "  ███████╗███╗░░██╗██████╗░██╗░░░░░███████╗░██████╗░██████╗\n"
    "  ██╔════╝████╗░██║██╔══██╗██║░░░░░██╔════╝██╔════╝██╔════╝\n"
    "  █████╗░░██╔██╗██║██║░░██║██║░░░░░█████╗░░╚█████╗░╚█████╗░\n"
    "  ██╔══╝░░██║╚████║██║░░██║██║░░░░░██╔══╝░░░╚═══██╗░╚═══██╗\n"
    "  ███████╗██║░╚███║██████╔╝███████╗███████╗██████╔╝██████╔╝\n"
    "  ╚══════╝╚═╝░░╚══╝╚═════╝░╚══════╝╚══════╝╚═════╝░╚═════╝░\n"
    "+===========================================================+"
)


def full_robot_line(robot_line, robot_num, index=0, full_line=''):
    full_line += robot_line
    if index < robot_num - 1:
        full_line += '|'
        index += 1
        return full_robot_line(robot_line, robot_num, index, full_line)
    else:
        return full_line + ' ' * (81 - (19 * robot_num + robot_num - 1)) + '\n'


def show_hub(titanium_score, robot_num):
    bar = "+==============================================================================+\n"
    line_1 = full_robot_line("  $   $$$$$$$   $  ", robot_num)
    line_2 = full_robot_line("  $$$$$     $$$$$  ", robot_num)
    line_3 = full_robot_line("      $$$$$$$      ", robot_num)
    line_4 = full_robot_line("     $$$   $$$     ", robot_num)
    line_5 = full_robot_line("     $       $     ", robot_num)
    robots = (
            bar + line_1 + line_2 + line_3 + line_4 + line_5 + bar
    )
    explore_menu = (
        "+==============================================================================+\n"
        "|                  [Ex]plore                          [Up]grade                |\n"
        "|                  [Save]                             [M]enu                   |\n"
        "+==============================================================================+"
    )
    titanium_lumps = (
            "| Titanium: " + str(titanium_score) + (" " * (67 - len(str(titanium_score)))) + "|\n"
    )
    print(robots + titanium_lumps + explore_menu)


game_menu = (
    "                          |==========================|\n"
    "                          |            MENU          |\n"
    "                          |                          |\n"
    "                          | [Back] to game           |\n"
    "                          | Return to[Main] Menu     |\n"
    "                          | [Save] and exit          |\n"
    "                          | [Exit] game              |\n"
    "                          |==========================|"
)

saving_successful = (
    "                        |==============================|\n"
    "                        |    GAME SAVED SUCCESSFULLY   |\n"
    "                        |==============================|"
)

loading_successful = (
    "                        |==============================|\n"
    "                        |    GAME LOADED SUCCESSFULLY  |\n"
    "                        |==============================|"
)

upgrade_store = (
    "                       |================================|\n"
    "                       |          UPGRADE STORE         |\n"
    "                       |                         Price  |\n"
    "                       | [1] Titanium Scan         250  |\n"
    "                       | [2] Enemy Encounter Scan  500  |\n"
    "                       | [3] New Robot            1000  |\n"
    "                       |                                |\n"
    "                       | [Back]                         |\n"
    "                       |================================|"
)

game_over = (
    "                        |==============================|\n"
    "                        |          GAME OVER!          |\n"
    "                        |==============================|"
)
