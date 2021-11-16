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
        self.master.geometry('500x400')
        print(type(self.master))
        print(dir(self.master))
        #help(seself.master)

        self.commands_frame = None
        self.devices = Devices()
        self.selected_model = ''
        self.selected_manufacturer = ''

        # allowing the widget to take the full space of the root window
        self.master.columnconfigure(0, weight=1)
        #self.columnconfigure(1, weight=2)
        #self.master.rowconfigure(1, weight=1)
        self.device_frame = self.create_device_frame(self.master)
        self.device_frame.grid(column=0, row=0, sticky="NEW")


        #self.columnconfigure(1, weight=2)



        serial_port_lbl = tk.Label(self.master,
                                    text=''.join(SerialPort.list_serial_ports()),
                                    relief="groove",
                                    width=20,
                                    height=1)
        serial_port_lbl.grid(column=0, row=2, sticky="SW")

        # # creating a button instance
        # quit_button = tk.Button(self, text="Quit", command=self.client_exit)
        # # placing the button on my window
        # quit_button.grid(column=1, row=3,sticky=(tk.N, tk.S, tk.E, tk.W))

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

        frame = tk.Frame(container,bg = "#D9D8D7", borderwidth=1)

        frame.columnconfigure(0, weight=1)
        #frame.rowconfigure(0, weight=1) 
        #frame.rowconfigure(1, weight=1) 
        #frame.rowconfigure(2, weight=1) 

        device_commands_lbl = tk.Label(frame, text='Device Commands', relief="groove")
        device_commands_lbl.grid(column=0, row=0, columnspan=2) 

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
            command_frame.grid(column=0, row=count)

            command_lbl = tk.Label(command_frame, text=command_name, padx=5, width=15)
            command_lbl.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

            #value = value.replace('\\x', '\\\\x')
            print(repr(value))
            command_string_lbl = tk.Entry(command_frame, text=repr(value))
            command_string_lbl.delete(0,"end")
            command_string_lbl.insert(0, repr(value))
            command_string_lbl.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
            command_labels.append(command_lbl)

            send_command_btn = tk.Button(command_frame,
                                            text='Send',
                                            padx=10,
                                            #pady=10,
                                            command=lambda c_name = command_name,
                                            command_string = value :self.send_command(c_name,
                                                                        command_string))
            send_command_btn.grid(column=2, row=0, sticky=tk.W, padx=5, pady=5)

        return frame

    def create_bottom_frame(self, container):

        frame = tk.Frame(container,bg = "#D9D8D7", borderwidth=1)          

    def client_exit(self):
        """
        Function to quit the program
        """
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
        model_lbl.grid(row=2, column=0, sticky=tk.W)

    def model_selected(self, model):
        """[summary]

        Args:
            model ([type]): [description]
        """

        print(f'Model Selected ={model}')

        device = self.devices.get_device(self.selected_manufacturer, model)

        self.commands_frame = self.create_commands_frame(self.master, device)

        self.commands_frame.grid(column=0, row=1, sticky="EW")


    def send_command(self, command, command_string):
        """[summary]

        Args:
            command ([type]): [description]
            command_string ([type]): [description]
        """
        print(f'Sending Command {command} {command_string}')

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

    _ = Window(root)
    root.mainloop()

if __name__ == '__main__':
    main()
