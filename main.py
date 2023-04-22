import asyncio
from bleak import BleakClient
import time
import Xbox_Controller as controller
from math import trunc
import pygame

# The MAC address of the Bluetooth Low Energy peripheral device to connect to
peripheral_address = 'D4:D4:DA:5C:4D:CE'

# The UUID of the Bluetooth Low Energy characteristic to write to
write_characteristic_uuid = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
read_characteristic_uuid = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

# The data to write to the characteristic
#data_to_write = bytes("Little Message :)", 'UTF-8')

array1 = [255, 2, 3, 4]
array2 = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

async def run():
    print("0")
    async with BleakClient(peripheral_address) as client:
        while 1:
            print("3")

            data_to_write = bytes(input("Send a message: "), 'UTF-8')

            #data_to_write = bytearray(array1 + array2)

            #data_to_write = await controller.controllerMessage()
            #print(data_to_write)


            # Write data to the characteristic
            await client.write_gatt_char(write_characteristic_uuid, data_to_write)

            # Read data from the Characteristic and print to terminal
            # print(await client.read_gatt_char(read_characteristic_uuid))

            # Print a message to confirm the data was sent
            print('Data sent to peripheral device:', data_to_write)
            await asyncio.sleep(2)
            #time.sleep(2)

async def joystickInit():
    # initialize pygame
    pygame.init()

    # get the first connected joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # print some information about the joystick
    print("Joystick name:", joystick.get_name())
    print("Number of axes:", joystick.get_numaxes())
    print("Number of buttons:", joystick.get_numbuttons())
    return 0

async def controllerMessage(joystick):
    pygame.event.pump()  # pump the event queue
    axes = [(trunc(((joystick.get_axis(i) + 1) / 2) * 256)) for i in range(joystick.get_numaxes())]
    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
    return axes + buttons

def listToBytearray(list):
    return bytearray(list)

async def main():

    print("0")
    async with BleakClient(peripheral_address) as client:
        print("1")
        joystick = await controller.joystickInit()
        data = controller.controllerMessage(joystick)
        data_to_write = listToBytearray(data)
        await client.write_gatt_char(write_characteristic_uuid, data_to_write)
        print('Data sent to peripheral device:', data_to_write)
        await asyncio.sleep(2)
        print("Disconnecting")


if __name__ == '__main__':
    #main()
    #controller.joystickInit()
    asyncio.run(main())