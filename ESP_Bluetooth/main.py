from machine import Pin
from machine import Timer
from time import sleep_ms
import ubluetooth

_IRQ_CENTRAL_CONNECT                 = 1
_IRQ_CENTRAL_DISCONNECT              = 2
_IRQ_GATTS_WRITE                     = 3



class ESP32_BLE():
    def __init__(self, name):
        # Create internal objects for the onboard LED
        # blinking when no BLE device is connected
        # stable ON when connected
        self.message = ""
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

    def get_msg(self):
        #new_message = ""

        #if self.message == "STATUS":
            #message = ""
            #print('LED is ON.' if led.value() else 'LED is OFF')
            #ble.send('LED is ON.' if led.value() else 'LED is OFF')

        #if self.message == "!B516":
        #    new_message = "accelerate"
        #elif self.message == "!B615":
        #    new_message = "brake"
        #elif self.message == "!B714":
        #    new_message = "left"
        #elif self.message == "!B813":
        #    new_message = "right"
        #elif self.message == "!B11":
        #    new_message = "1"
        #elif self.message == "!B219":
        #    new_message = "2"
        #elif self.message == "!B318":
        #    new_message = "3"
        #elif self.message == "!B417":
        #    new_message = "4"

        # self.message = ""

        if self.message != "":
            print("The message recieved was: ", self.message)
            #print(self.message)

        self.message = ""
        #return new_message

    def connected(self):
        self.led.value(1)
        self.timer1.deinit()

    def disconnected(self):
        self.timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))

    def ble_irq(self, event, data):
        #print("irq exnet ; data")
        #print("" + str(event) + " ; " + str(data))

        if event == _IRQ_CENTRAL_CONNECT:
                       # A central has connected to this peripheral
            self.connection = 1
            self.connected()
            print("Connected")

        elif event == _IRQ_CENTRAL_DISCONNECT:
                         # A central has disconnected from this peripheral.
            self.connection = 0
            self.advertiser()
            self.disconnected()
            print("Disconnected")

        elif event == _IRQ_GATTS_WRITE:
                         # A client has written to this characteristic or descriptor.
            buffer = self.ble.gatts_read(self.rx)
            print(buffer)
            array = []
            for x in buffer:
                array.append(x)
            print(array, "\n")
            #self.message = buffer.decode('UTF-8').strip()
            #print(self.message)

    def register(self):
        # Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_READ | ubluetooth.FLAG_NOTIFY,)

        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(24, self.tx, data + '\n')

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
