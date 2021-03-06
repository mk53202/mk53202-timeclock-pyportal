# The MIT License (MIT)
#
# Copyright (c) 2017 Tony DiCola for Adafruit Industries
#                    refactor by Carter Nelson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`mcp230xx`
====================================================

CircuitPython module for the MCP23017 and MCP23008 I2C I/O extenders.

* Author(s): Tony DiCola
"""

from adafruit_bus_device import i2c_device

__version__ = "2.1.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx.git"

# Global buffer for reading and writing registers with the devices.  This is
# shared between both the MCP23008 and MCP23017 class to reduce memory allocations.
# However this is explicitly not thread safe or re-entrant by design!
_BUFFER = bytearray(3)


# pylint: disable=too-few-public-methods
class MCP230XX:
    """Base class for MCP230xx devices."""

    def __init__(self, i2c, address):
        self._device = i2c_device.I2CDevice(i2c, address)

    def _read_u16le(self, register):
        # Read an unsigned 16 bit little endian value from the specified 8-bit
        # register.
        with self._device as i2c:
            _BUFFER[0] = register & 0xFF
            i2c.write(_BUFFER, end=1, stop=False)
            i2c.readinto(_BUFFER, end=2)
            return (_BUFFER[1] << 8) | _BUFFER[0]

    def _write_u16le(self, register, val):
        # Write an unsigned 16 bit little endian value to the specified 8-bit
        # register.
        with self._device as i2c:
            _BUFFER[0] = register & 0xFF
            _BUFFER[1] = val & 0xFF
            _BUFFER[2] = (val >> 8) & 0xFF
            i2c.write(_BUFFER, end=3)

    def _read_u8(self, register):
        # Read an unsigned 8 bit value from the specified 8-bit register.
        with self._device as i2c:
            _BUFFER[0] = register & 0xFF
            i2c.write(_BUFFER, end=1, stop=False)
            i2c.readinto(_BUFFER, end=1)
            return _BUFFER[0]

    def _write_u8(self, register, val):
        # Write an 8 bit value to the specified 8-bit register.
        with self._device as i2c:
            _BUFFER[0] = register & 0xFF
            _BUFFER[1] = val & 0xFF
            i2c.write(_BUFFER, end=2)
