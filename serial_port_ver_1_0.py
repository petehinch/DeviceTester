"""[summary]

Raises:
    EnvironmentError: [description]

Returns:
    [type]: [description]
"""
import sys
import glob
import threading
import time
import serial
import timeit



class SerialPort(serial.Serial):

    def __init__(self, port_name = None) -> None:
        """[summary]
        """

        super().__init__(port = port_name)

        self.port_open = False
        self.port_state_changed_callback = self.__no_callback_defined
        self.rcv_callback = self.__no_callback_defined

    def open_port(self):
        print('Opening Port')
        try:
            self.open()
            self.port_open = True
            self.rcv = threading.Thread(target=self.recieve_data)
            self.rcv.start()
            return True
        except serial.serialutil.SerialException as e:
            print(e)
            return False


    def close_port(self):
        self.port_open = False
        self.close()

    def send(self, data):

        if self.is_open:
            try:
                self.write(data)
            except serial.serialutil.SerialException as e:
                if 'WriteFile failed' in str(e):
                    print('Writing to port failed - Is the port still open??')
                    self.port_open = False
                    self.port_state_changed_callback(self.port_open)
        else:
            print('Port Closed')

    def recieve_data(self):

        while self.port_open:
            #print('Running')
            if self.in_waiting:
                data = self.read_all()
                #print(f'Recieved >{data}')
                self.rcv_callback(data)
            time.sleep(0.1)
            


    def list_serial_ports():
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result



    def __no_callback_defined(*args):
        print('No callback defined for event')


if __name__ == '__main__':
    
    if SerialPort.list_serial_ports():
        port = SerialPort.list_serial_ports()[0]

        sp = SerialPort()
        sp.port = port
        sp.open_port()
    
