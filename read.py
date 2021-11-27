#!bin/env python3

import time
import math
import Rpi.GPIO as GPIO
from typing import List
from psutil import cpu_percent


def convert_to_fields(func) -> str:
    """
    This function has to be used as a decoration for function


    This function can be used as following

    >>> @convert_to_fields
    ... def some_function():
            return [ 1, 2 ,3 ]

    >>> fields = some_function()
    >>> fields
    field1=1&field2=2&field3=3
    """

    def wrapper() -> str:
        values = func()
        result = ''
        for idx, value in enumerate(values):
            if idx != 0:
                result += '&'

            result += f'field{idx+1}={str(value)}'
        return result
    return wrapper


class MQ():

    #: MQ135 Pin config {{{
    #: Vcc -> 2
    #: GND -> 6
    #: DO  -> 7 (GPIO 4)
    #: }}

    #: Hardware config {{{
    GPIO.setmode(GPIO.BOARD)
    MQPIN               = 7     # Digital pin
    RL_VALUE            = 5     # Load resistance value from the board, in kilo ohms
    RO_CLEAN_AIR_FACTOR = 9.83  # => (Sensor resistance in air) / RO
                                # RO is from the datasheet
    GPIO.setup(MQPIN, GPIO.IN)
    #: }}}

    #: Calibration config {{{
    CALIBRATION_SAMPLE_TIMES    = 25
    CALIBRATION_SAMPLE_INTERVAL = 500

    READ_SAMPLE_INTERVAL        = 50
    READ_SAMPLE_TIMES           = 5
    #: }}}

    #: Applcation Gas Config {{{
    GAS_LPG     = 0
    GAS_CO      = 1
    GAS_SMOKE   = 2
    #: }}}

    def __init__(self, RO=10, MQPIN=7):
        self.RO = RO
        self.MQPIN = MQPIN

        #: Curve data from datasheet
        self.LPGCurve   = [2.3, 0.21, -0.47]  # (x, y, slope)
        self.COCurve    = [2.3, 0.72, -0.34]  # (x, y, slope)
        self.SmokeCurve = [2.3, 0.53, -0.44]  # (x, y, slope)

        print('Calibrating Sensor...')
        self.RO = self.mq_calibraton(self.MQPIN)
        print("Calibration done")


    ############## Digital Input ######################
    def take_voltage(self) -> float:
        return GPIO.input(self.MQPIN)

    def mq_calibraton(self, mq_pin=7) -> float:
        #: remarks
        #: this take voltage as input return it average

        val = 0.0
        for i in range(self.CALIBRATION_SAMPLE_TIMES):
            val += self.mq_resistance_calculation(
                self.take_voltage()
            )

            time.sleep(
                self.CALIBRATION_SAMPLE_INTERVAL / 100
            )

        val = val / self.CALIBRATION_SAMPLE_TIMES
        val = val / self.RO_CLEAN_AIR_FACTOR

        return val


    def mq_resistance_calculation(self, raw_voltage):
        return float(
            self.RL_VALUE * (1023.0) / raw_voltage
        )

    def mq_read(self):

        rs = 0.0
        for i in range(self.READ_SAMPLE_TIMES):
            rs += self.mq_resistance_calculation(
                self.take_voltage()
            )
            time.sleep(self.READ_SAMPLE_INTERVAL / 1000.0)

        rs = rs / self.READ_SAMPLE_TIMES

        return rs

    def mq_percentage(self):
        val = {}
        read = self.mq_read()

        val["LPG"] = self.mq_get_gas_percentage(
            read / self.RO, self.GAS_LPG
        )
        val["CO"] = self.mq_get_gas_percentage(
            read / self.RO, self.GAS_CO
        )
        val["SMOKE"] = self.mq_get_gas_percentage(
            read / self.RO, self.GAS_SMOKE
        )

    def mq_get_gas_percentage(self, rs_ro_percentage, gas_id):

        if ( gas_id == self.GAS_LPG ):
            return self.mq_get_percentage(
                rs_ro_percentage, self.LPGCurve
            )
        elif ( gas_id == self.GAS_CO ):
            return self.mq_get_percentage(
                rs_ro_percentage, self.COCurve
            )
        elif ( gas_id == self.GAS_SMOKE ):
            return self.mq_get_percentage(
                rs_ro_ratio, self.SmokeCurve
            )

        return 0

    def mq_get_percentage(self, rs_ro_ratio, curve):
        return (
            math.pow(10, (
                (
                    (math.log(rs_ro_ratio) - curve[1]) 
                    / curve[2]
                )
                + curve[0]
        )))


@convert_to_fields
def read_mq135_data() -> List[float]:
    # TODO: Complete ME

    '''
    Reads the data from mq135 sensor and return in a form of array
    '''

    return



@convert_to_fields
def read_bme_data() -> list['float']:
    # TODO: Complete ME
    '''
    Reads the data from BME280 sensor and return in a form of array
    '''


@convert_to_fields
def dummy_data() -> list['float']:
    ''' This function is just for testing perpose'''

    cpu_percentage = cpu_percent(interval=16, percpu=True)
    return cpu_percentage
