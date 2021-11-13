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
        self.commands_frame = None
        self.devices = Devices()
        self.selected_model = ''
        self.selected_manufacturer = ''

        # allowing the widget to take the full space of the root window
        self.pack(fill='both', expand=1)

        self.device_frame = tk.Frame(self, height = 120, width = 400, bg = "#D9D8D7", borderwidth=4)
        self.device_frame.place(x=50,y=20)

        # create label
        output_lbl = tk.Label(self.device_frame,
                                text='Device',
                                borderwidth=2,
                                relief="groove",
                                width=50)
        # place label on the window
        output_lbl.place(x=15,y=2)

        manufacturer_lbl = tk.Label(self.device_frame,
                                    text='Manufacturer',
                                    relief="groove",
                                    width=20,
                                    height=1)
        manufacturer_lbl.place(x=20,y=45)

        # Create the list of options
        #manufacturer_list = ["Philips", "Samsung", "LG", "Extron"]
        manufacturer_list = self.devices.get_manufacturer_list()
        # Variable to keep track of the option
        # selected in OptionMenu
        value_inside = tk.StringVar(master)
        # Set the default value of the variable
        value_inside.set("Select an Manufacturer")
        # Create the optionmenu widget and passing
        # the options_list and value_inside to it.
        manufacturer_menu = tk.OptionMenu(self.device_frame, value_inside,
                                     *manufacturer_list,
                                     command=self.manufacturer_selected)
        manufacturer_menu.config(width=20)
        manufacturer_menu.place(x=200,y=40)

        serial_port_lbl = tk.Label(self,
                                    text=''.join(SerialPort.list_serial_ports()),
                                    relief="groove",
                                    width=20,
                                    height=1)
        serial_port_lbl.place(x=30,y=350)

        # creating a button instance
        quit_button = tk.Button(self, text="Quit", command=self.client_exit)
        # placing the button on my window
        quit_button.place(x=450, y=350)

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
        model_menu.place(x=200,y=80)

        model_lbl = tk.Label(self.device_frame, text='Model', relief="groove", width=20, height=1)
        model_lbl.place(x=20,y=80)

    def model_selected(self, model):
        """[summary]

        Args:
            model ([type]): [description]
        """

        print(f'Model Selected ={model}')

        device = self.devices.get_device(self.selected_manufacturer, model)

        commands = device['commands']

        self.commands_frame = tk.Frame(self,
                                        height = 150,
                                        width = 400,
                                        bg = "#D9D8D7",
                                        borderwidth=2)
        self.commands_frame.place(x=50,y=150)

        device_commands_lbl = tk.Label(self.commands_frame, text='Device Commands', relief="groove")
        device_commands_lbl.place(x=4,y=1)

        command_labels = []

        count = 0

        for key, value in commands.items():
            print(key)
            count += 1
            print(count)

            command_frame = tk.Frame(self.commands_frame,
                                    height = 80,
                                    width = 350,
                                    bg = "#FFFFFF",
                                    borderwidth=0)
            command_frame.place(x=26, y=count*30)

            command_lbl = tk.Label(command_frame, text=key, padx=5, width=15)
            command_lbl.grid(row=1, column=0)

            #value = value.replace('\\x', '\\\\x')
            print(repr(value))
            command_string_lbl = tk.Entry(command_frame, text=repr(value))
            command_string_lbl.delete(0,"end")
            command_string_lbl.insert(0, repr(value))
            command_string_lbl.grid(row=1, column=1)
            command_labels.append(command_lbl)

            send_command_btn = tk.Button(command_frame, text='Send', command=lambda: self.send_command(key, value))
            send_command_btn.grid(row=1, column=2)

    def send_command(self, command, command_string):
        print(f'Sending Command {command} {command_string}')

def main():
    """
    Main Program
    """
    root = tk.Tk()
    #App Title
    root.title('Device Control Tester')
    # set resizing to false
    root.resizable(width=False, height=False)
    # set size of window
    root.geometry('500x400')

    _ = Window(root)
    root.mainloop()

if __name__ == '__main__':
    main()
