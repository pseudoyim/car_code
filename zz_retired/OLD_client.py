import io
import socket
import struct
import time
import picamera

# create socket and bind host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('10.0.0.121', 8000)) # This should be the IP for your computer (not the Pi).
connection = client_socket.makefile('wb')

if __name__ == '__main__':
    
    try:
        with picamera.PiCamera() as camera:            

            # camera.resolution = (320, 240)      # pi camera resolution
            camera.resolution = (640, 480)      # pi camera resolution
            camera.framerate = 10               # 10 frames/sec
            time.sleep(2)                       # give 2 secs for camera to initilize
            # start = time.time()
            stream = io.BytesIO()

            # send jpeg format video stream
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                stream.seek(0)
                connection.write(stream.read())
                stream.seek(0)
                stream.truncate()
        connection.write(struct.pack('<L', 0))

    finally:
        connection.close()
        client_socket.close()
