import sys,os
import curses,json,time
import emoji

blueteam =  ["Smith","Van Hoy","Morrell","Odlevak"]
yellowteam = ["Marshall","Roark","Dacquisto","Fort"]

bluetotalscore = [0,0,0,0]
yellowtotalscore = [0,0,0,0]

title = ["SHEET 1","SHEET 2","SHEET 3","SHEET 4"]

hammer = emoji.emojize(":hammer:")

def draw_scoreboard(stdscr):
    k = 0
    global blueteam
    global yellowteam
    global bluetotalscore
    yellowtotalscore = [0,0,0,0]

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
   
    clubname = "PALMETTO CURLING CLUB"
    clubloc = "The Pavilion, Taylors SC"

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



        j,i = 0,0
        while j < 4:
            blueteam[j] = blueteam[j].ljust(15," ")
            bluescoreline[j] = blueteam[j] + " "
            i = 0
            while i < len(jsondata[j]["Blue"]):
                bluescoreline[j] += str(jsondata[j]["Blue"][i]) + "  "
                if jsondata[j]["Blue"][i] != 0:
                    bluetotalscore[j] = i
                i += 1
            j += 1
        j = 0
        while j < 4:
            yellowteam[j] = yellowteam[j].ljust(15," ")
            yellowscoreline[j] = yellowteam[j] + " "
            i = 0
            while i < len(jsondata[j]["Yellow"]):
                yellowscoreline[j] += str(jsondata[j]["Yellow"][i]) + "  "
                if jsondata[j]["Yellow"][i] != 0:
                    yellowtotalscore[j] = i
                i += 1
            j += 1

        pointsline =  "H  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15"
        pointslinelen = len(pointsline)
        pointsline = ["","","",""]
        i = 0
        while i < 4:
            diff = len(bluescoreline[i])-pointslinelen
            pointsline[i] = " "*16 + "H  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15"
            i += 1
            
        # Centering calculations
        start_x_name = int((width // 2) - (len(clubname) // 2) - len(clubname) % 2)
        start_x_loc = int((width // 2) - (len(clubloc) // 2) - len(clubloc) % 2)
        start_x_title = int((width // 2) - (len(title[0]) // 2) - len(title[0]) % 2)
        start_x_pointsstr = int((width // 2) - (len(pointsline) // 2) - len(pointsline) % 2)
        start_x_bluestr = int((width // 2) - (len(bluescoreline[0]) // 2) - len(bluescoreline[0]) % 2)
        start_x_yellowstr = int((width // 2) - (len(yellowscoreline[0]) // 2) - len(yellowscoreline[0]) % 2)
        start_y = 3
        # Turning on attributes for title
        stdscr.attron(curses.color_pair(4))
        stdscr.attron(curses.A_BOLD)
    
  
######
        stdscr.addstr(0, start_x_name, clubname)
        stdscr.addstr(1, start_x_loc - 2, clubloc)
        
        # Rendering scoreboard       

        i = 0
        while i < 4:
            stdscr.attron(curses.color_pair(1))
            stdscr.attron(curses.A_BOLD)
            rectangle(stdscr,start_y + (i*5),start_x_bluestr-1,start_y + 4+ (i*5),start_x_yellowstr+len(yellowscoreline[i]))     
            stdscr.addstr(start_y + (i*5), start_x_title, title[i])
            stdscr.attron(curses.color_pair(2))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(start_y + 1+ (i*5), start_x_bluestr, bluescoreline[i].replace("0"," "))
            stdscr.addstr(start_y + 1+ (i*5), start_x_bluestr+len(bluescoreline[i])+2, str(bluetotalscore[i]))
            stdscr.attron(curses.color_pair(1))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(start_y + 2+ (i*5), start_x_bluestr, pointsline[i])
            stdscr.attron(curses.color_pair(3))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(start_y + 3+ (i*5), start_x_yellowstr, yellowscoreline[i].replace("0"," "))
            stdscr.addstr(start_y + 3+ (i*5), start_x_yellowstr+len(yellowscoreline[i])+2, str(yellowtotalscore[i]))
            stdscr.attron(curses.color_pair(1))
            stdscr.attron(curses.A_BOLD)           
            rectangle2(stdscr,start_y + (i*5),start_x_bluestr+15,start_y + 4+ (i*5),start_x_bluestr+17)
            i += 1



        # Refresh the screen
        stdscr.refresh()
        time.sleep(1)


######




def rectangle(win, uly, ulx, lry, lrx):
    """Draw a rectangle with corners at the provided upper-left
    and lower-right coordinates.
    """
    win.vline(uly+1, ulx, curses.ACS_VLINE, lry - uly - 1)
    win.hline(uly, ulx+1, curses.ACS_HLINE, lrx - ulx - 1)
    win.hline(lry, ulx+1, curses.ACS_HLINE, lrx - ulx - 1)
    win.vline(uly+1, lrx, curses.ACS_VLINE, lry - uly - 1)
    win.addch(uly, ulx, curses.ACS_ULCORNER)
    win.addch(uly, lrx, curses.ACS_URCORNER)
    win.addch(lry, lrx, curses.ACS_LRCORNER)
    win.addch(lry, ulx, curses.ACS_LLCORNER)

def rectangle2(win, uly, ulx, lry, lrx):
    """Draw a rectangle with corners at the provided upper-left
    and lower-right coordinates.
    """
    win.vline(uly+1, ulx, curses.ACS_VLINE, lry - uly - 1)
    win.hline(uly, ulx+1, curses.ACS_HLINE, lrx - ulx - 1)
    win.hline(lry, ulx+1, curses.ACS_HLINE, lrx - ulx - 1)
    win.vline(uly+1, lrx, curses.ACS_VLINE, lry - uly - 1)
    win.addch(uly, ulx, curses.ACS_TTEE)
    win.addch(uly, lrx, curses.ACS_TTEE)
    win.addch(lry, lrx, curses.ACS_BTEE)
    win.addch(lry, ulx, curses.ACS_BTEE)


def main():
    curses.wrapper(draw_scoreboard)
    #curses.wrapper(test_editbox)

if __name__ == "__main__":
    main()
