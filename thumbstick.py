__author__ = 'srkiyengar'

import serial
import time
import sys


JOY_DEADZONE_A0 = 0.2
JOY_DEADZONE_A1 = 0.1

class Thumbstick():
    def __init__(self,port='/dev/ttyACM0', baud=9600):
        self.axes = 2
        self.hats = 0
        self.name = "Arduino Thumstick"
        self.buttons = 1
        self.button_press = 0
        self.x = 0.0
        self.y = 0.0
        self.min_val = [-JOY_DEADZONE_A0,-JOY_DEADZONE_A1]
        self.max_val = [JOY_DEADZONE_A0,JOY_DEADZONE_A1]
        try:
            self.ser = serial.Serial(port,baud,timeout=.0001)   # 100 micro second to read timeout
        except IOError as e:
            print "I/O error: {}".format(e)
            self.connect = False
            raise
        else:
            self.connect = True

    def read_byte(self):
        try:
            my_byte = self.ser.read(1)   # Will try to read one byte within timeout second; return is str type
        except IOError as e:
            print "I/O error in read_byte: {}".format(e)
            raise
        except:
            print "Unexpected error in read_byte: {}", sys.exc_info()[0]
            raise
        else:
            return my_byte

    def get_response(self,cmd):
        response = []
        try:
            self.ser.write(chr(cmd))
        except IOError as e:
            print "I/O error in get_response: {}".format(e)
            raise
        except:
            print "Unexpected error in get_response: {}", sys.exc_info()[0]
            raise
        else:
            keep_reading = True
            while (keep_reading):
                try:
                    this_byte = self.read_byte()
                except IOError as e:
                    print "I/O error: {}".format(e)
                    raise
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
                else:
                    if (this_byte == '\n'):
                        keep_reading = False
                        response.remove('\r')
                        response.append(this_byte)
                    else:
                        response.append(this_byte)

            y = int("".join(response))
            return y




if __name__ == '__main__':

    try:
        my_joy = Thumbstick()
    except:
        print "Unexpected error:", sys.exc_info()[0]

    else:
        while(my_joy.connect):

            k = 0
            try:
                value_x = my_joy.get_response(k)
            except ValueError as e:
                print "Command error {} while getting x axis:".format(sys.exc_info()[0])
                my_joy.connect = False
            except:
                print "Error {} while getting x axis:".format(sys.exc_info()[0])
                my_joy.connect = False
            else:
                print("For k = {} String read from serial: {}".format(k,value_x))

            k = 1
            try:
                value_y = my_joy.get_response(k)
            except ValueError as e:
                print "Command error {} while getting y axis:".format(sys.exc_info()[0])
                my_joy.connect = False
            except:
                print "Error {} while getting y axis:".format(sys.exc_info()[0])
                my_joy.connect = False
            else:
                print("For k = {} String read from serial: {}".format(k,value_y))

            k = 255
            try:
                button = my_joy.get_response(k)
            except ValueError as e:
                print "Command error {} while getting button status:".format(sys.exc_info()[0])
                my_joy.connect = False
            except:
                print "Error {} while getting Button value:".format(sys.exc_info()[0])
                my_joy.connect = False
            else:
                print("For k = {} String read from serial: {}".format(k,button))



