import sys,os
import curses,json,time
import emoji

team1 = "Smith"
team2 = "Marshall"

title = ["SHEET 1","SHEET 2","SHEET 3","SHEET 4"]

hammer = emoji.emojize(":hammer:")

def draw_scoreboard(stdscr):
    k = 0
    global team1
    global team2

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while True:

        with open('/home/pi/curling-scores.json','r') as fd:
            jsondata = json.loads(fd.read())
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()


        # Declaration of strings
        #title = "SHEET " + str(jsondata[2]["sheet"])[:width-1]
        subtitle = team1 + " vs " + team2[:width-1]
        bluescoreline = ["","","",""]
        yellowscoreline = ["","","",""]
        if len(team2)>len(team1):
            diff = len(team2)-len(team1)
            temp = team1 + " "*diff
            team1 = temp
        else:
            diff = len(team1)-len(team2)
            temp = team2 + " "*diff
            team2 = temp
        i = 0
        j = 0
        while j < 4:
            bluescoreline[j] = team1 + " "
            while i < len(jsondata[j]["Blue"]):
                bluescoreline[j] += str(jsondata[j]["Blue"][i]) + "  "
                i += 1
            j += 1
        j = 0
        i = 0
        while j < 4:
            yellowscoreline[j] = team2 + " "
            while i < len(jsondata[j]["Yellow"]):
                yellowscoreline[j] += str(jsondata[j]["Yellow"][i]) + "  "
                i += 1
            j += 1

        blueline = bluescoreline
        yellowline = yellowscoreline
        pointsline =  "H  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15"
        diff = len(blueline)-len(pointsline)
        pointsline = " "*(diff-2) + "H  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15"
        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_pointsstr = int((width // 2) - (len(pointsline) // 2) - len(pointsline) % 2)
        start_x_bluestr = int((width // 2) - (len(bluescoreline[0]) // 2) - len(bluescoreline[0]) % 2)
        start_x_yellowstr = int((width // 2) - (len(yellowscoreline[0]) // 2) - len(yellowscoreline[0]) % 2)
        #start_y = int((height // 2) - 2)
        start_y = 3

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        #stdscr.addstr(height-1, 0, statusbarstr)
        #stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y, start_x_title, title[0])
        stdscr.addstr(start_y + 1, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 2, start_x_bluestr, bluescoreline[0])
        stdscr.addstr(start_y + 3, start_x_bluestr, pointsline)
        stdscr.addstr(start_y + 4, start_x_yellowstr, yellowscoreline[0])
        stdscr.addstr(start_y + 5, start_x_title, title[1])
        stdscr.addstr(start_y + 6, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 7, start_x_bluestr, bluescoreline[1])
        stdscr.addstr(start_y + 8, start_x_bluestr, pointsline)
        stdscr.addstr(start_y + 9, start_x_yellowstr, yellowscoreline[1])
        stdscr.addstr(start_y + 10, start_x_title, title[2])
        stdscr.addstr(start_y + 11, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 12, start_x_bluestr, bluescoreline[2])
        stdscr.addstr(start_y + 13, start_x_bluestr, pointsline)
        stdscr.addstr(start_y + 14, start_x_yellowstr, yellowscoreline[2])
        stdscr.addstr(start_y + 15, start_x_title, title[3])
        stdscr.addstr(start_y + 16, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 17, start_x_bluestr, bluescoreline[3])
        stdscr.addstr(start_y + 18, start_x_bluestr, pointsline)
        stdscr.addstr(start_y + 19, start_x_yellowstr, yellowscoreline[3])

        # Refresh the screen
        stdscr.refresh()
        time.sleep(1)


def main():
    curses.wrapper(draw_scoreboard)

if __name__ == "__main__":
    main()
