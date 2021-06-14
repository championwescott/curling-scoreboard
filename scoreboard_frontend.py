import sys,os
import curses,json,time
import emoji

blueteam =  ["Smith","Van Hoy","Morrell","Odlevak"]
yellowteam = ["Marshall","Roark","Dacquisto","Fort"]

title = ["SHEET 1","SHEET 2","SHEET 3","SHEET 4"]

hammer = emoji.emojize(":hammer:")

def draw_scoreboard(stdscr):
    k = 0
    global blueteam
    global yellowteam

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    while True:
        # Read in the JSON document
        with open('curling-scores.json','r') as fd:
            jsondata = json.loads(fd.read())
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()


        # Declaration of strings
        bluescoreline = ["","","",""]
        yellowscoreline = ["","","",""]
        i = 0
        while i < 4:
            if len(blueteam[i])>len(yellowteam[i]):
                diff = len(blueteam[i])-len(yellowteam[i])
                temp = yellowteam[i] + " "*diff
                yellowteam[i] = temp
            elif len(yellowteam[i])>len(blueteam[i]):
                diff = len(yellowteam[i])-len(blueteam[i])
                temp = blueteam[i] + " "*diff
                blueteam[i] = temp
            i += 1
        j = 0
        i = 0
        while j < 4:
            bluescoreline[j] = blueteam[j] + " "
            i = 0
            while i < len(jsondata[j]["Blue"]):
                bluescoreline[j] += str(jsondata[j]["Blue"][i]) + "  "
                i += 1
            j += 1
        j = 0
        while j < 4:
            yellowscoreline[j] = yellowteam[j] + " "
            i = 0
            while i < len(jsondata[j]["Yellow"]):
                yellowscoreline[j] += str(jsondata[j]["Yellow"][i]) + "  "
                i += 1
            j += 1

        
        pointsline =  "H  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15"
        pointslinelen = len(pointsline)
        pointsline = ["","","",""]
        i = 0
        while i < 4:
            diff = len(bluescoreline[i])-pointslinelen
            pointsline[i] = " "*(diff-2) + "H  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15"
            i += 1

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_pointsstr = int((width // 2) - (len(pointsline) // 2) - len(pointsline) % 2)
        start_x_bluestr = int((width // 2) - (len(bluescoreline[0]) // 2) - len(bluescoreline[0]) % 2)
        start_x_yellowstr = int((width // 2) - (len(yellowscoreline[0]) // 2) - len(yellowscoreline[0]) % 2)
        start_y = 3

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering scoreboard        
        i = 0
        while i < 4:
            stdscr.attron(curses.color_pair(1))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(start_y + (i*5), start_x_title, title[i])
            stdscr.addstr(start_y + 1+ (i*5), (width // 2) - 2, '-' * 8)
            stdscr.attron(curses.color_pair(2))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(start_y + 2+ (i*5), start_x_bluestr, bluescoreline[i].replace("0"," "))
            stdscr.attroff(curses.color_pair(2))
            stdscr.attroff(curses.A_BOLD)
            stdscr.addstr(start_y + 3+ (i*5), start_x_bluestr, pointsline[i])
            stdscr.attron(curses.color_pair(3))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(start_y + 4+ (i*5), start_x_yellowstr, yellowscoreline[i].replace("0"," "))
            i += 1


        # Refresh the screen
        stdscr.refresh()
        time.sleep(1)


def main():
    curses.wrapper(draw_scoreboard)

if __name__ == "__main__":
    main()
