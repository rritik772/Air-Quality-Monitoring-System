#!bin/env python3

import os
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


@convert_to_fields
def read_mq135_data() -> list['float']:
    # TODO: Complete ME

    '''
    Reads the data from mq135 sensor and return in a form of array
    '''



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
