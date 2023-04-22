import asyncio
from bleak import BleakClient
import time
#import Xbox_Controller as controller

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
    async with BleakClient(peripheral_address) as client:
        while 1:

            data_to_write = bytes(input("Send a message: "), 'UTF-8')

            #data_to_write = bytearray(array1 + array2)
            # Write data to the characteristic
            await client.write_gatt_char(write_characteristic_uuid, data_to_write)

            # Read data from the Characteristic and print to terminal
            # print(await client.read_gatt_char(read_characteristic_uuid))

            # Print a message to confirm the data was sent
            print('Data sent to peripheral device:', data_to_write)
            time.sleep(1)
            await asyncio.sleep(1)


asyncio.run(run())
