import curses
import datetime
import RPi.GPIO as GPIO
import time
from car import Drive

drive = Drive()


def manual_driver(stdscr):
    
    stdscr.clear()
    print 'Press Q to quit.\n'

    driving = True
    
    while driving:

        # Store the key value in the variable 'key'
        stdscr = curses.initscr()
        key = stdscr.getch()
        stdscr.clear()

        stdscr.addstr('Direction: ')

        # FORWARD
        if key == curses.KEY_UP:
            forward()
            stdscr.addstr('Forward')

        # FORWARD_RIGHT
        elif key == curses.KEY_RIGHT:
            right()
            stdscr.addstr('Forward-right')

        # FORWARD_LEFT
        elif key == curses.KEY_LEFT:
            left()
            stdscr.addstr('Forward-left')

        # REVERSE
        elif key == curses.KEY_DOWN:
            reverse()
            stdscr.addstr('Reverse')

        # TODO: REVERSE_RIGHT

        # TODO: REVERSE_LEFT

        # QUIT
        elif key == ord('q'):
            driving = False
            print 'Quitting! Smell you later!'
            break

curses.wrapper(manual_driver)


if __name__ == '__main__':
    # stdscr = curses.initscr()
    # manual_driver(stdscr)
    manual_driver()