import asyncio

from bleak import BleakClient

import Controller as controller
import Xbox_One_Constants as button

# The MAC address of the Bluetooth Low Energy peripheral device to connect to
# (Run the scaner to detect your device address)
peripheral_address = 'D4:D4:DA:5C:4D:CE'

# The UUID of the Bluetooth Low Energy characteristic to write to
write_characteristic_uuid = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
# The UUID of the Bluetooth Low Energy characteristic to read from
read_characteristic_uuid = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'


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

    :return:
    """
    print("Connecting to Microballer")
    # Create Bleak client (when function finished it will disconnect)
    async with BleakClient(peripheral_address) as client:
        # The client has connected to the server
        print("Microballer Connected")

        print("Connecting to Controller")
        # Initialise the activeController reader
        activeController = controller.controllerInit()
        # Joystick has been initiated
        print(activeController.get_name(), "Connected \n")

        while 1:

            # Get the controller output array
            messageList = controller.controllerMessage(activeController)

            # If the start button is pressed then disconnect from the server
            if messageList[button._Disconnect] != 0:
                break

            # The messageList to write to the characteristic
            messageToSend = listToBytearray(messageList)

            # Write the messageList to the write characteristic of the server
            await client.write_gatt_char(write_characteristic_uuid, messageToSend)

            # Print the 0 to 256 activeController integer values
            print('Data sent to peripheral device integer:', messageList)
            # Print the hexadecimal activeController values
            print('Data sent to peripheral device hexadecimal:', messageToSend, '\n')

            # Wait 100ms before sending another message
            await asyncio.sleep(0.1)

        # Print disconnection status
        print("Disconnecting from Microballer")
        # Disconnect from the server


if __name__ == '__main__':
    asyncio.run(main())
