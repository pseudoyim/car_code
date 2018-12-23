import cv2
import numpy as np
import os
import socket
import threading
import time


class NeuralNetwork(object):

    global stop_classifier
    global timestr

    def __init__(self, receiving=False, piVideoObject=None):
        self.receiving = receiving
        # PiVideoStream class object is now here.
        self.piVideoObject = piVideoObject
        self.fetch()


    def fetch(self):

        while self.receiving:

            frame = 0

            # There's a chance that the Main thread can get to this point before the New thread begins streaming images.
            # To account for this, we create the jpg variable but set to None, and keep checking until it actually has something.
            jpg = None
            while jpg is None:
                jpg = self.piVideoObject.frame

            # gray  = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
            image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

            # flip the image.
            img = cv2.flip(image, -1 )
            cv2.imshow('Original', img)
            # Show streaming images
            # cv2.imshow('What the model sees', auto)

            cv2.putText(image, "IT WORKS", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .45, (255, 255, 0), 1)
            # cv2.imwrite('test_frames_temp/frame{:>05}.jpg'.format(frame), gray)
            frame += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()
                cv2.destroyAllWindows()

                # Rename the folder that collected all of the test frames. Then make a new folder to collect next round of test frames.
                # os.rename(  './test_frames_temp', './test_frames_SAVED/test_frames_{}'.format(timestr))
                # os.makedirs('./test_frames_temp')


class PiVideoStream(object):

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_socket.bind(('192.168.1.66', 8000)) # The IP address of your computer (Paul's MacBook Air). This script should run before the one on the Pi.
        self.server_socket.bind(('0.0.0.0', 8000)) # 0.0.0.0 means all interfaces

        print 'Listening...'
        self.server_socket.listen(0)

        # Accept a single connection ('rb' is 'read binary')
        self.connection = self.server_socket.accept()[0].makefile('rb')

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False
        self.stream_bytes = ' '
        self.start()


    def start(self):
        # start the thread to read frames from the video stream
        print 'Starting PiVideoStream thread...'
        print ' \"Hold on to your butts!\" '

        # Start a new thread
        t = threading.Thread(target=self.update, args=())
        t.daemon=True
        t.start()
        print '...thread running'

        # Main thread diverges from the new thread and activates the neural_network
        # The piVideoObject argument ('self') passes the PiVideoStream class object to NeuralNetwork.
        NeuralNetwork(receiving=True, piVideoObject=self)
        print 'NN should be activated...'

    def update(self):
        while True:
            self.stream_bytes += self.connection.read(1024)
            first = self.stream_bytes.find('\xff\xd8')
            last = self.stream_bytes.find('\xff\xd9')
            if first != -1 and last != -1:
                self.frame = self.stream_bytes[first:last + 2]
                self.stream_bytes = self.stream_bytes[last + 2:]

        # if the thread indicator variable is set, stop the thread
        # and resource camera resources
        if self.stopped:
            self.connection.close()
            return

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


if __name__ == '__main__':
    try:
        # Create an instance of PiVideoStream class
        video_stream = PiVideoStream()
    except (KeyboardInterrupt, SystemExit):
        print 'Stopping.'
        video_stream.connection.close()
        print '\n! Received keyboard interrupt, quitting threads.\n'
