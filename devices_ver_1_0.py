"""
Module to handle the devices
"""
import json

class Devices():
    """A class for controlled devices
    """
    def __init__(self):

        self.device_list = {'devices': [
                                {
                                    'manufacturer': 'Philips',
                                    'model': 'BDL1101',
                                    'commands':
                                        {
                                            'Power On': '\x01\x02\x03',
                                            'Power Off': '\x01\x02\x04',
                                            'HDMI 1': '\x03\x02\x06'
                                        }
                                },
                                {
                                    'manufacturer': 'Philips',
                                    'model': 'BDL3001',
                                    'commands':
                                        {
                                            'Power On': '\x01\x02\x03',
                                            'Power Off': '\x01\x02\x04'
                                        }
                                },
                                {
                                    'manufacturer': 'A Company',
                                    'model': 'UX12345',
                                    'commands':
                                        {
                                            'Power On': 'PWR ON',
                                            'Power Off': 'PWR OFF'
                                        }
                                },
                                {
                                    'manufacturer': 'LG',
                                    'model': 'Series 1',
                                    'commands':
                                        {
                                            'Power On': 'POWER ON',
                                            'Power Off': 'POWER OFF'
                                        }
                                }
                                ]
                            }

        print('Started')

    def get_list_devices(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self.device_list

    def get_manufacturer_list(self) -> list:
        """[summary]

        Returns:
            list: [description]
        """

        manufacturer_list = []

        for device in self.device_list['devices']:
            print(device['manufacturer'])
            manufacturer_list.append(device['manufacturer'])

        manufacturer_list = list(set(manufacturer_list))

        manufacturer_list.sort()

        return manufacturer_list

    def get_models_by_manufacture(self, manufacturer) -> list:
        """[summary]

        Args:
            manufacturer ([type]): [description]

        Returns:
            list: [description]
        """

        models = []

        for device in self.device_list['devices']:
            if device['manufacturer'] == manufacturer:
                print(device['model'])
                models.append(device['model'])

        return models

    def get_device(self, manufacturer, model) -> dict:
        """[summary]

        Args:
            manufacturer ([type]): [description]
            model ([type]): [description]

        Returns:
            dict: [description]
        """
        for device in self.device_list['devices']:
            if device['manufacturer'] == manufacturer and device['model'] == model:
                return device


    def devicelist_to_json(self):
        """coverts devices to json string into
        """
        devices_json = json.dumps(self.device_list)
        print(devices_json)


def main():
    """
    main program
    """
    devices = Devices()

    print(devices.get_list_devices())
    devices.devicelist_to_json()
    #print(devices.get_manufacturer_list())

    print(devices.get_models_by_manufacture('Philips'))

    device = devices.get_device('Philips', 'BDL1101')

    print(device['commands'])

if __name__ == '__main__':
    main()
