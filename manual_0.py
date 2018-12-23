import curses
from curses import wrapper
import datetime
import RPi.GPIO as GPIO
# import picamera


ts = datetime.datetime.now()

""" ################# CAMERA ################### """
# TODO: Live feed
def feed():
    pass

# Capture frame
def capture():
    # capture
    # save to folder with timestamp
    pass


""" ################# DRIVER HELPERS ################### """

steer_pin = 12
drive_pin = 13
degree_correction = 0
GPIO.setwarnings(False)         # Do not show any warnings
GPIO.setmode (GPIO.BCM)         # Programming the GPIO by BCM pin numbers
GPIO.setup(steer_pin ,GPIO.OUT)  # Initialize pin for steering servo (front)
GPIO.setup(drive_pin ,GPIO.OUT)  # Initialize pin for driving motor (back)
s = GPIO.PWM(steer_pin, 50) # steer_pin (s) as PWM output, with 50Hz frequency
s.start(7.5)           # generate PWM signal with 7.5% duty cycle (90 degrees) 
d = GPIO.PWM(drive_pin, 50) # drive_pin (d) as PWM output, with 50Hz frequency
d.start(0.0)           # generate PWM signal with 0% duty cycle (continuous servo)

seconds = 0.5

def _degrees_to_duty(degrees):
    degrees = degrees + degree_correction
    # Got this formula by plotting points in Excel and getting the equation.
    duty = 0.05556 * degrees + 2.5
    return duty

def forward():
    # print 'Forward'
    duty = _degrees_to_duty(90)   # 90 degrees (straight ahead)
    s.ChangeDutyCycle(duty)
    d.ChangeDutyCycle(30)
    time.sleep(seconds)
    d.ChangeDutyCycle(0)

def reverse():
    # print 'Reverse'
    duty = _degrees_to_duty(90)   # 90 degrees (straight ahead)
    s.ChangeDutyCycle(duty)
    d.ChangeDutyCycle(1)
    time.sleep(seconds)
    d.ChangeDutyCycle(0)

def left():
    # print 'Left'
    duty = _degrees_to_duty(65.0)   # 67.5 degrees is midpt b/n 45 and 90)
    s.ChangeDutyCycle(duty)
    d.ChangeDutyCycle(30)
    time.sleep(seconds)
    d.ChangeDutyCycle(0)

def right():
    # print 'Right'
    duty = _degrees_to_duty(115.0)    # 112.5 degrees is midpt b/n 90 and 135)
    s.ChangeDutyCycle(duty)
    d.ChangeDutyCycle(30)
    time.sleep(seconds)
    d.ChangeDutyCycle(0)

# def stop():
    # print 'STOP'
    # duty = _degrees_to_duty(90)   # 90 degrees (straight ahead)
    # s.ChangeDutyCycle(duty)
    # d.ChangeDutyCycle(0)



""" ################# DRIVER ################### """
def driver(stdscr):
    
    stdscr.clear()
    driving = True
    
    while driving:

        # Store the key value in the variable 'key'
        stdscr = curses.initscr()
        key = stdscr.getch()
        stdscr.clear()

        # FORWARD
        if key == curses.KEY_UP:
            forward()
            stdscr.addstr('Forward')

        # FORWARD_RIGHT
        elif key == curses.KEY_RIGHT:
            forward()
            right()
            stdscr.addstr('Forward-right')

        # FORWARD_LEFT
        elif key == curses.KEY_LEFT:
            forward()
            left()
            stdscr.addstr('Forward-left')

        # REVERSE
        elif key == curses.KEY_DOWN:
            reverse()
            stdscr.addstr('Reverse')

        # TODO: REVERSE_RIGHT

        # TODO: REVERSE_LEFT


        # CAPTURE FRAME
        elif key == ord('a'):
            c.capture()
        
        # QUIT
        elif key == ord('q'):
            driving = False
            break

wrapper(driver)


if __name__ == '__main__':
    print 'You\'re the driver now!'
    driver(stdscr)
