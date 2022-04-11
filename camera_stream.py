import socket
import time
import picamera
import datetime as dt


class cycle:
    def __init__(self, c):
        self._c = c
        self._index = -1

    def __next__(self):
        self._index += 1
        if self._index>=len(self._c):
            self._index = 0
        return self._c[self._index]

    def get(self):
        return self._c[self._index]

    def previous(self):
        self._index -= 1
        if self._index < 0:
            self._index = len(self._c)-1
        return self._c[self._index]




camera = picamera.PiCamera()
def init_camera():
    camera.resolution = (1280, 720)
    camera.framerate = 15
    camera.annotate_background = picamera.Color('black')
    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    camera.exposure_mode = 'night'


class CamStream():
    def __init__(self):
        print("Init CamStream")
        self.stop_flag = False
        self.recording = False

        #self.reset_socket()
        self.image_effects = ['none', 'negative', 'solarize', 'sketch', 'denoise', 'emboss', 'oilpaint', 'hatch', 'gpen', 'pastel', 'watercolor', 'film', 'blur', 'saturation', 'colorswap', 'washedout', 'posterise', 'colorpoint', 'colorbalance', 'cartoon', 'deinterlace1', 'deinterlace2']
        self.effects_cycle = cycle(self.image_effects)
        self.effect = 'none'

    def reset_socket(self):
        self.server_socket = socket.socket()
        # Try to reuse address if in TimeWait State
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.settimeout(1) # timeout for listening
        self.server_socket.bind(('0.0.0.0', 5001))
        self.server_socket.listen(0)
        print("Socket reset")

    def runner(self):
        count = 0
        while not self.stop_flag:

            init_camera()
            self.reset_socket()

            # Accept a single connection and make a file-like object out of it
            print(str(count) + ": Video stream: Waiting for connection...")
            self.connected = False
            # Try to accept connections. If timeout, try again
            # Timeout is so this script will be non-blocking for when we want to terminate
            while not ( self.stop_flag or self.connected ):
              try:
                  print("Waiting for connection...")
                  self.connection = self.server_socket.accept()[0].makefile('wb')
              except socket.timeout:
                pass
              except OSError:
                  print("OSError")
                  pass
              else:
                  self.connected = True
                  print(str(count) + ": Video stream: Connected")

            # Break out of outer loop if we are terminating
            if self.stop_flag:
                break

            # Now begin stream recording to the connection
            try:
                print("Trying to start recording")
                camera.start_recording(self.connection, format='h264', quality=23)
                self.recording = True
                while not self.stop_flag:
                    camera.annotate_text = self.effects_cycle.get()
                    camera.wait_recording(0.2)
                camera.stop_recording()
                self.recording = False
            except ConnectionResetError:
                print(str(count) + ": Connection Reset Exception")
                #self.connection.close()
                #self.server_socket.close()
            except BrokenPipeError:
                print(str(count) + "Broken Pipe Error")

            finally:
                self.connection.close()
                self.server_socket.shutdown(socket.SHUT_RD);
                self.server_socket.close()

            if(camera.recording):
                try:
                    camera.wait_recording(0)
                    camera.stop_recording()
                except:
                    pass
                finally:
                    pass
            try:
                print("Camera close near line 72")
                camera.close()
            except:
                pass
            finally:
                pass
            print(str(count) + ": Video stream: Disconnected")
            self.recording = False
            count += 1
            time.sleep(5)
            #self.reset_socket()

    def effect_next(self):
        effect = next(self.effects_cycle)
        try:
            camera.image_effect = effect
        except:
            pass

    def effect_prev(self):
        effect = self.effects_cycle.previous()
        try:
            camera.image_effect = effect
        except:
            pass

    def terminate(self):
        self.stop_flag = True
        if(self.recording):
            time.sleep(2)
        if(camera.recording):
            camera.stop_recording
        if self.connected:
            print("connected, will try to close")
            try:
                self.connection.close()
            except:
                pass
        if(self.server_socket):
            print("server_socket defined")
            self.server_socket.close()
        if not camera.closed:
            camera.close()
            print("Closing camera")

cs = CamStream()
