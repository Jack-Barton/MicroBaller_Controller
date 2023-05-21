import asyncio

from bleak import BleakClient

import Controller
import Xbox_One_Constants as Button

microballer_address = 'D4:D4:DA:5C:4D:CE'
"""
The MAC address of the MicroBaller server.
"""

write_characteristic_uuid = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
"""
The UUID of the MicroBaller Bluetooth Low Energy characteristic to write to.
"""

read_characteristic_uuid = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
"""
The UUID of the Bluetooth Low Energy characteristic to read from
"""


# Takes an int list with elements 0 to 256 and returns the list as a byte array
def listToBytearray(listToChange):
    """
    Converts the given list into a byte array.

    :param listToChange: The list to be changed
    :return: A byte array of the given list with values from 0 to 255
    """

    return bytearray(listToChange)


async def main():
    """
    Creates the BLE client and sends the controller outputs to the BLE server at 10Hz indefinitely.
    """
    print("Connecting to Microballer")
    async with BleakClient(microballer_address) as client:  # Create bleak client
        # The client has connected to the server
        print("Microballer Connected")
        print("Connecting to Controller")

        activeController = Controller.controllerInit()  # Initialise the activeController reader
        # Joystick has been initiated
        print(activeController.get_name(), "Connected \n")

        while 1:

            messageList = Controller.controllerMessage(activeController)  # Get the controller output array

            # If the start button is pressed then disconnect from the server
            if messageList[Button._Disconnect] != 0:
                break

            messageToSend = listToBytearray(messageList)  # Convert controller output array to byte array

            await client.write_gatt_char(write_characteristic_uuid,
                                         messageToSend)  # Write the messageList to the write characteristic of the server

            print('Data sent to peripheral device integer:', messageList)  # Print int message array
            print('Data sent to peripheral device hexadecimal:', messageToSend, '\n')  # Print message byte array

            await asyncio.sleep(0.1)  # Wait 100ms before sending another message

        print("Disconnecting from Microballer")  # Print disconnection status
        # Disconnect from the server


if __name__ == '__main__':
    asyncio.run(main())
