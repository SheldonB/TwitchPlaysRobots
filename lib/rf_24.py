import RPi.GPIO as GPIO
from lib.lib_nrf24 import NRF24
import spidev

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


    def send_message(self, msg):
        print(msg)
        self.radio.write(bytes(msg, 'utf-8'))
