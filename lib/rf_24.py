import RPi.GPIO as GPIO
from lib.lib_nrf24 import NRF24
import spidev
import time

GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1],
         [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

class Radio:
    def __init__(self):
        self.radio = NRF24(GPIO, spidev.SpiDev())
        self._init_radio()

    def _init_radio(self):
        self.radio.begin(0, 22)
        self.radio.setPayloadSize(32)
        self.radio.setChannel(0x76)
        self.radio.setDataRate(NRF24.BR_1MBPS)
        self.radio.setPALevel(NRF24.PA_MIN)

        self.radio.setAutoAck(True)
        self.radio.enableDynamicPayloads()
        self.radio.enableAckPayload()

        self.radio.openWritingPipe(pipes[0])
        self.radio.openReadingPipe(1, pipes[1])

    def send_message(self, msg):
        print(msg)
        self.radio.write(bytes(msg, 'utf-8'))

    def recieve_message(self):
        print('Here')
        self.radio.startListening()
        #time.sleep(1/10)
        if self.radio.available():
            recieved_message = []
            self.radio.read(recieved_message, self.radio.getDynamicPayloadSize())

            string = ''
            for n in recieved_message:
                if n >= 32 and n <= 126:
                    string += chr(n)
            #time.sleep(1/10)
            self.radio.stopListening()
            return string

        #time.sleep(1/10)
        self.radio.stopListening()
        return None

