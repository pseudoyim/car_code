import os
import pygame
import RPi.GPIO as GPIO
import datetime
from pygame.locals import *


class Camera(object):
  def __init__(self):
    self.ts = datetime.datetime.now()

  # TODO: Live feed
  def feed(self):
    pass

  # Capture frame
  def capture(self):
    # capture
    # save to folder with timestamp
    pass


class Drive(object):
  def __init__(self):
    self.steer_pin = 12
    self.drive_pin = 13
    self.degree_correction = 0
    GPIO.setwarnings(False)         # Do not show any warnings
    GPIO.setmode (GPIO.BCM)         # Programming the GPIO by BCM pin numbers
    GPIO.setup(self.steer_pin ,GPIO.OUT)  # Initialize pin for steering servo (front)
    GPIO.setup(self.drive_pin ,GPIO.OUT)  # Initialize pin for driving motor (back)
    self.s = GPIO.PWM(self.steer_pin, 50) # steer_pin (s) as PWM output, with 50Hz frequency
    self.s.start(7.5)           # generate PWM signal with 7.5% duty cycle (90 degrees) 
    self.d = GPIO.PWM(self.drive_pin, 50) # drive_pin (d) as PWM output, with 50Hz frequency
    self.d.start(0.0)           # generate PWM signal with 0% duty cycle (continuous servo)

  def _degrees_to_duty(self, degrees):
    self.degrees = degrees + self.degree_correction
    # Got this formula by plotting points in Excel and getting the equation.
    duty = 0.05556 * self.degrees + 2.5
    return duty

  def forward(self):
    print 'Forward'
    self.duty = self._degrees_to_duty(90)   # 90 degrees (straight ahead)
    self.s.ChangeDutyCycle(self.duty)
    self.d.ChangeDutyCycle(30)

  def reverse(self):
    print 'Reverse'
    self.duty = self._degrees_to_duty(90)   # 90 degrees (straight ahead)
    self.s.ChangeDutyCycle(self.duty)
    self.d.ChangeDutyCycle(1)

  def left(self):
    print 'Left'
    self.duty = self._degrees_to_duty(65.0)   # 67.5 degrees is midpt b/n 45 and 90)
    self.s.ChangeDutyCycle(self.duty)
    self.d.ChangeDutyCycle(30)

  def right(self):
    print 'Right'
    self.duty = self._degrees_to_duty(115.0)    # 112.5 degrees is midpt b/n 90 and 135)
    self.s.ChangeDutyCycle(self.duty)
    self.d.ChangeDutyCycle(30)

  def stop(self):
    print 'STOP'
    self.duty = self._degrees_to_duty(90)   # 90 degrees (straight ahead)
    self.s.ChangeDutyCycle(self.duty)
    self.d.ChangeDutyCycle(0)




class ManualControl(object):
  def __init__(self):
    self.send_inst = True
    # self.pygame.init() = pygame
    self.driver()
    self.d = Drive()
    self.c = Camera()

  def driver(self):
    # pygame.init()
    # pygame.display.set_mode((1, 1))
    
    # os.putenv('DISPLAY', ':0.0')
    # pygame.display.init()
    
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    pygame.display.init()
    print 'initiated'

    while self.send_inst:

      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          key_input = pygame.key.get_pressed()

          # FORWARD
          if key_input[pygame.K_UP]:
            self.d.forward()
            print 'forward'

          # FORWARD_RIGHT
          elif key_input[pygame.K_RIGHT]:
            self.d.forward()
            self.d.right()
            print 'forward-right'

          # FORWARD_LEFT
          elif key_input[pygame.K_LEFT]:
            self.d.forward()
            self.d.left()
            print 'forward-left'

          # REVERSE
          elif key_input[pygame.K_DOWN]:
            self.d.reverse()
            print 'reverse'

          # TODO: REVERSE_RIGHT
          
          # TODO: REVERSE_LEFT

          # CAPTURE FRAME
          elif key_input[pygame.K_A]:
            self.c.capture()

          # EXIT
          elif key_input[pygame.K_x] or key_input[pygame.K_q]:
            print 'exit'
            self.d.stop()
            self.send_inst = False
            break

        elif event.type == pygame.KEYUP:
          self.d.stop()
          break

if __name__ == '__main__':
    ManualControl()
