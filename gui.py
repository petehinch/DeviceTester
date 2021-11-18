"""
Gui tester


TODO:
Add web sync
Update panel
USB to serial adaptor connection
add abilty to tab navigate

add view commands as hex

"""
import sys
import tkinter as tk
import binascii
from devices_ver_1_0 import Devices
from serial_port_ver_1_0 import SerialPort

class Window(tk.Frame):
    """[summary]

    Args:
        Frame ([type]): [description]
    """
    def __init__(self, master=None) -> None:

        tk.Frame.__init__(self, master)
        self.master = master
        self.serial_port = None
        
        self.master.geometry('500x400')
        print(type(self.master))
        print(dir(self.master))
        #help(seself.master)

        self.commands_frame = None
        self.settings_frame = None
        self.devices = Devices()
        self.selected_model = ''
        self.selected_manufacturer = ''

        # allowing the widget to take the full space of the root window
        self.master.columnconfigure(0, weight=1)
        #self.columnconfigure(1, weight=2)
        self.master.rowconfigure(0, weight=1)
        self.device_frame = self.create_device_frame(self.master)
        self.device_frame.grid(column=0, row=0, sticky="NEW")


        #self.columnconfigure(1, weight=2)


        self.bottom_frame = self.create_bottom_frame(self.master)
        self.bottom_frame.grid(column=0, row=3,sticky="SEW")




    def create_device_frame(self, container):
        """
        Function to create the frame for chosen the device to control

        Args:
            container (frame): container to hold the device frame

        Returns:
            frame: frame holding device options
        """

        frame = tk.Frame(container,bg="#D9D8D7", borderwidth=4)

        frame.columnconfigure(0, weight=1)
        
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # create label
        output_lbl = tk.Label(frame,
                                text='Device',
                                borderwidth=2,
                                relief="groove")
        # place label on the window
        output_lbl.grid(column=0, row=0, columnspan=2,sticky=(tk.E, tk.W))

        manufacturer_lbl = tk.Label(frame,
                                    text='Manufacturer',
                                    relief="groove",
                                    width=20,
                                    height=1)
        manufacturer_lbl.grid(column=0, row=1, sticky=(tk.E, tk.W))

        # Create the list of options
        #manufacturer_list = ["Philips", "Samsung", "LG", "Extron"]
        manufacturer_list = self.devices.get_manufacturer_list()
        # Variable to keep track of the option
        # selected in OptionMenu
        value_inside = tk.StringVar(self.master)
        # Set the default value of the variable
        value_inside.set("Select an Manufacturer")
        print('value_inside=', value_inside)
        # Create the optionmenu widget and passing
        # the options_list and value_inside to it.
        manufacturer_menu = tk.OptionMenu(frame, value_inside,
                                     *manufacturer_list,
                                     command=self.manufacturer_selected)
        manufacturer_menu.config(width=20)
        manufacturer_menu.grid(column=1, row=1,padx=3, pady=10,sticky=(tk.N, tk.S, tk.E, tk.W))

        # tk.Button(frame, text='Replace').grid(column=0, row=1)
        # tk.Button(frame, text='Replace All').grid(column=0, row=2)
        # tk.Button(frame, text='Cancel').grid(column=0, row=3)

        # for widget in frame.winfo_children():
        #     widget.grid(padx=0, pady=3)

        return frame

    def create_commands_frame(self, container, device):

        frame = tk.Frame(container,bg = "BLUE", borderwidth=1)

        frame.columnconfigure(0, weight=1)

        #frame.rowconfigure(0, weight=1) 
        #frame.rowconfigure(1, weight=1) 
        #frame.rowconfigure(2, weight=1) 

        device_commands_lbl = tk.Label(frame, text='Device Commands', relief="groove")
        device_commands_lbl.grid(column=0, row=0, columnspan=1) 

        commands = device['commands']

        command_labels = []

        count = 0

        for command_name, value in commands.items():
            print(command_name)
            count += 1
            print(count)

            command_frame = tk.Frame(frame,
                                    height = 100,
                                    bg = "#FFFFFF",
                                    borderwidth=0)
            command_frame.grid(column=0, row=count,sticky="NEW")

            command_frame.columnconfigure(0, weight=1)
            command_frame.columnconfigure(1, weight=2)
            command_frame.columnconfigure(2, weight=2)
            command_frame.columnconfigure(3, weight=1)

            command_lbl = tk.Label(command_frame, text=command_name, padx=5, width=15)
            command_lbl.grid(column=0, row=0, sticky="NW", padx=5, pady=5)

            #value = value.replace('\\x', '\\\\x')
            #value = value[1:-1]
            print('pete')
            print(value)
            command_string_lbl = tk.Entry(command_frame, text=value)
            command_string_lbl.delete(0,"end")
            command_string_lbl.insert(0, repr(value)[1:-1])
            command_string_lbl.grid(column=1, row=0, sticky="NEW", padx=5, pady=5)
            command_labels.append(command_lbl)

            bytes_value = value.encode('utf-8')

            hex_string = '\\x' + binascii.hexlify(bytes_value, ' ').decode('utf-8').replace(' ', '\\x')

            

            print(f'Hex Command string = {hex_string}')

            command_hex_lbl = tk.Entry(command_frame, text=hex_string)
            command_hex_lbl.delete(0, "end")
            command_hex_lbl.insert(0, hex_string)
            command_hex_lbl.grid(column=2, row=0, padx=5, pady=5, sticky="NEW")

            bytes_value = value.encode('utf-8')

            send_command_btn = tk.Button(command_frame,
                                            text='Send',
                                            padx=10,
                                            #pady=10,
                                            command=lambda c_name = command_name,
                                            command_string = bytes_value :self.send_command(c_name,
                                                                        command_string))
            send_command_btn.grid(column=4, row=0, sticky="W", padx=5, pady=5)

        return frame

    def create_settings_frame(self, container, device):

        frame = tk.Frame(container,bg='orange', borderwidth=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        device_settings_lbl = tk.Label(frame, text='Device Settings', relief="groove")
        device_settings_lbl.grid(column=1, row=0, columnspan=2, sticky="EW")

        buad_rate_title_lbl = tk.Label(frame, text='Baud Rate', relief="groove")
        buad_rate_title_lbl.grid(column=1, row=1, columnspan=1, sticky="EW")

        buad_rate_lbl = tk.Label(frame, text=device['settings']['baudrate'], relief="groove")
        buad_rate_lbl.grid(column=2, row=1, columnspan=1, sticky="EW")

        return frame

    def create_bottom_frame(self, container):

        frame = tk.Frame(container,bg="#FFFFFF", borderwidth=1, height=50) 

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        self.serial_port_lbl = tk.Label(frame,
                                    text=''.join(SerialPort.list_serial_ports()),
                                    relief="groove",
                                    width=20,
                                    height=1)
        self.serial_port_lbl.grid(column=0, row=0, sticky="SW")


        # creating a button instance
        open_port_button = tk.Button(frame, text="Open", command=self.serial_port_connect)
        # placing the button on my window
        open_port_button.grid(column=0, row=0,sticky="SE")


        # creating a button instance
        quit_button = tk.Button(frame, text="Quit", command=self.client_exit)
        # placing the button on my window
        quit_button.grid(column=2, row=0,sticky="SE")

        return frame         

    def serial_port_connect(self):

        if self.serial_port is None:
            self.serial_port = SerialPort(None)
            self.serial_port.port = SerialPort.list_serial_ports()[0]
            self.serial_port.port_state_changed_callback = self.port_state_changed

        if self.device:
            self.serial_port.baudrate = self.device['settings']['baudrate']

        if self.serial_port.open_port():
            print('Port opened successfully')
            self.serial_port_lbl.config(bg='green')
        else:
            print('Port did not open!')

    def client_exit(self):
        """
        Function to quit the program
        """
        if self.serial_port is not None:
            self.serial_port.close_port()
        sys.exit()

    def manufacturer_selected(self, option):
        """
        callback when a new Manufacturer option is selected

        Args:
            option (stry): selected option
        """
        self.selected_manufacturer = option
        if self.commands_frame is not None:
            self.commands_frame.destroy()
        if self.settings_frame is not None:
            self.settings_frame.destroy()
        print('Option selected', option)
        model_list = self.devices.get_models_by_manufacture(option)
        model_value = tk.StringVar(self.master)
        model_value.set("Select an Model")
        model_menu = tk.OptionMenu(self.device_frame, model_value,
                                *model_list,
                                command=self.model_selected
                                )
        model_menu.config(width=20)
        model_menu.grid(row=2, column=1)

        model_lbl = tk.Label(self.device_frame, text='Model', relief="groove", width=20, height=1)
        model_lbl.grid(row=2, column=0, sticky=(tk.E, tk.W))

    def model_selected(self, model):
        """[summary]

        Args:
            model ([type]): [description]
        """

        print(f'Model Selected ={model}')

        if self.commands_frame is not None:
            self.commands_frame.destroy()

        self.device = self.devices.get_device(self.selected_manufacturer, model)

        self.commands_frame = self.create_commands_frame(self.master, self.device)
        self.commands_frame.grid(column=0, row=2, sticky="SEW")

        self.settings_frame = self.create_settings_frame(self.master, self.device)
        self.settings_frame.grid(column=0, row=1, sticky="SEW")


    def send_command(self, command, command_bytes):
        """[summary]

        Args:
            command ([type]): [description]
            command_string ([type]): [description]
        """
        print(type(command_bytes))
        print(f'Sending Command {command} {command_bytes}')

        print(len(command_bytes))

        self.serial_port.send(command_bytes)

    def port_state_changed(self, state):
        print(f'The port has chagnge its state to {state}')

        if state: 
            self.serial_port_lbl.configure(bg ='green')
        else:
            self.serial_port_lbl.configure(bg ='red')
            self.serial_port.close()

def on_closing():
    print('Window close button pressed')

def main():
    """
    Main Program
    """
    root = tk.Tk()
    #App Title
    root.title('Device Control Tester')
    # set resizing to false
    #root.resizable(width=True, height=True)
    # set size of window
    root.geometry('500x400')
    root.config(bg="#D9D8D7")

    app = Window(root)
    root.protocol("WM_DELETE_WINDOW", app.client_exit)
    root.mainloop()

if __name__ == '__main__':
    main()
