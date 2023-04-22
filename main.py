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
def listToBytearray(list):
    return bytearray(list)

async def main():
    print("Connecting to Microballer")
    # Create Bleak client (when function finished it will disconnect)
    async with BleakClient(peripheral_address) as client:
        # The client has connected to the server
        print("Microballer Connected")

        print("Connecting to Controller")
        # Initialise the joystick reader
        joystick = await controller.joystickInit()
        # Joystick has been initiated
        print(joystick.get_name(), "Connected \n")

        while 1:

            # Get the controller output array
            data = controller.controllerMessage(joystick)

            # If the start button is pressed then disconnect from the server
            if data[button._Button_Start] != 0:
                break

            # The data to write to the characteristic
            data_to_write = listToBytearray(data)

            # Write the data to the write characteristic of the server
            await client.write_gatt_char(write_characteristic_uuid, data_to_write)

            # Print the 0 to 256 joystick integer values
            print('Data sent to peripheral device integer:', data)
            # Print the hexadecimal joystick values
            print('Data sent to peripheral device hexadecimal:', data_to_write, '\n')

            # Wait 100ms before sending another message
            await asyncio.sleep(0.1)

        # Print disconnection status
        print("Disconnecting from Microballer")
        # Disconnect from the server


if __name__ == '__main__':
    asyncio.run(main())