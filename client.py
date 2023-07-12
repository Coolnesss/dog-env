# Adapted from https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi
import io
import socket
import struct
import numpy as np
from PIL import Image
import cv2
from command import COMMAND as cmd

class Client:
    def __init__(self, ip: str, move_speed: int):
        self.ip = ip
        self.move_speed = move_speed

    def turn_on_client(self):
        self.client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_socket1.connect((self.ip, 5001)) # Accepts control commands
        self.client_socket.connect((self.ip, 8001)) # Streams video
        self.connection = self.client_socket.makefile('rb')

    def turn_off_client(self):
        try:
            self.client_socket.shutdown(2)
            self.client_socket1.shutdown(2)
            self.client_socket.close()
            self.client_socket1.close()
        except Exception as e:
            print(e)

    def is_valid_image_4_bytes(self, buf): 
        bValid = True
        if buf[6:10] in (b'JFIF', b'Exif'):     
            if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):
                bValid = False
        else:        
            try:  
                Image.open(io.BytesIO(buf)).verify() 
            except:  
                bValid = False
        return bValid
    
    # A single frame from the video stream
    def get_image(self):
        try:
            stream_bytes = self.connection.read(4)
            leng=struct.unpack('<L', stream_bytes[:4])
            jpg=self.connection.read(leng[0])
            
            if self.is_valid_image_4_bytes(jpg):
                image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Convert BGR to RGB
                return image
            
        except Exception as e:
            print(e)
    
    # Distance to object in front in CM
    def get_distance(self):
        command = cmd.SONIC+'\n'
        self.send_data(command)
        distance = int(self.receive_data().split("CMD_SONIC#")[1])
        return distance

    def send_data(self, data):
        try:
            self.client_socket1.send(data.encode('utf-8'))
        except Exception as e:
            print(e)

    def receive_data(self):
        data = self.client_socket1.recv(1024).decode('utf-8')
        return data
 
    # -----------------
    # Motion primitives
    # -----------------

    def relax(self):
        command = cmd.RELAX
        self.send_data(command)

    def forward(self):
        command = f'{cmd.MOVE_FORWARD}#{self.move_speed}\n'
        self.send_data(command)
    
    def backward(self):
        command = f'{cmd.MOVE_BACKWARD}#{self.move_speed}\n'
        self.send_data(command)

    def turn_left(self):
        command = f'{cmd.TURN_LEFT}#{self.move_speed}\n'
        self.send_data(command)

    def turn_right(self):
        command = f'{cmd.TURN_RIGHT}#{self.move_speed}\n'
        self.send_data(command)    

    def step_left(self):
        command = f'{cmd.MOVE_LEFT}#{self.move_speed}\n'
        self.send_data(command)    

    def step_right(self):
        command = f'{cmd.MOVE_RIGHT}#{self.move_speed}\n'
        self.send_data(command)

if __name__ == '__main__':
    pass
