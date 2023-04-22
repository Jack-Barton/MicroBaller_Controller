from machine import Pin
from machine import Timer
from time import sleep_ms
import ubluetooth

# Event values
_IRQ_CENTRAL_CONNECT                 = 1
_IRQ_CENTRAL_DISCONNECT              = 2
_IRQ_GATTS_WRITE                     = 3


class ESP32_BLE():
    # Initialises the gatt server
    def __init__(self, name):
        # Create internal objects for the onboard LED
        # blinking when no BLE device is connected
        # stable ON when connected
        self.message = []
        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()
        self.connection = 0

    # Returns the message if it is not empty, else return 0
    def get_msg(self):
        if self.message != []:
            return self.message
        else:
            return 0

    # Takes the message and decodes it from a byte array to an array
    def messageDecoder(self, message):
        decodedMessage = []
        for i in message:
            decodedMessage.append(i)
        return decodedMessage

    # Sets the LED to on and turns off the timer to repeat disconnected event
    def connected(self):
        self.led.value(1)
        self.timer1.deinit()

    # Starts a timer that repeats the disconnected and keeps LED flashing
    def disconnected(self):
        self.timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))

    # Event handler
    def ble_irq(self, event, data):
        #print("irq exnet ; data")
        #print("" + str(event) + " ; " + str(data))

        # A central has connected to this peripheral
        if event == _IRQ_CENTRAL_CONNECT:
            self.connection = 1
            self.connected()
            print("Connected")

        # A central has disconnected from this peripheral.
        elif event == _IRQ_CENTRAL_DISCONNECT:
            self.connection = 0
            self.advertiser()
            self.disconnected()
            print("Disconnected")

        # A client has written to this characteristic or descriptor.
        elif event == _IRQ_GATTS_WRITE:
            buffer = self.ble.gatts_read(self.rx)
            print(buffer)
            array = self.messageDecoder(buffer)
            print(array, "\n")

    # Construct and register the server (NUS) and assign its characteristics (RX and TX)
    def register(self):
        # Assign server UUIDs (NUS) and characteristic UUIDs (RX and TX) (Can have multiple servers at once and several
        # characteristics per server)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

        # Assigning permissions to servers and characteristics
        # Rx can be writen to a client
        # Tx can be read from or send notifications to a client
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_READ | ubluetooth.FLAG_NOTIFY,)

        # Assign service (NUS) the characteristics (RX and TX)
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        # Reference all the services
        SERVICES = (BLE_UART, )
        # Register the characteristic variables and their services to gatt
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    # Takes data and sends a notification with data attached to the client
    def send(self, data):
        self.ble.gatts_notify(24, self.tx, data + '\n')

    # Advertise the gatt server to other devices
    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print(adv_data)
        print("\r\n")


if __name__ == "__main__":
    ble = ESP32_BLE("MicroBaller")
    while True:
        sleep_ms(2000)
