# The MIT License (MIT)
#
# Copyright (c) 2019 Melissa LeBlanc-Williams for Adafruit Industries LLC
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
`adafruit_featherwing.matrix_featherwing`
====================================================

Helper for using the `Adafruit 8x16 LED Matrix FeatherWing
<https://www.adafruit.com/product/3155>`_.

* Author(s): Melissa LeBlanc-Williams
"""

__version__ = "1.9.1"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_FeatherWing.git"

import board
import adafruit_ht16k33.matrix as matrix

class MatrixFeatherWing:
    """Class representing an `Adafruit 8x16 LED Matrix FeatherWing
       <https://www.adafruit.com/product/3155>`_.

       Automatically uses the feather's I2C bus."""
    def __init__(self, address=0x70, i2c=None):
        if i2c is None:
            i2c = board.I2C()
        self._matrix = matrix.Matrix16x8(i2c, address)
        self._matrix.auto_write = False
        self.columns = 16
        self.rows = 8
        self._auto_write = True

    def __getitem__(self, key):
        """
        Get the current value of a pixel
        """
        x, y = key
        return self.pixel(x, y)

    def __setitem__(self, key, value):
        """
        Turn a pixel off or on
        """
        x, y = key
        self.pixel(x, y, value)
        self._update()

    def _update(self):
        """
        Update the Display automatically if auto_write is set to True
        """
        if self._auto_write:
            self._matrix.show()

    def pixel(self, x, y, color=None):
        """
        Turn a pixel on or off or retrieve a pixel value

        :param int x: The pixel row
        :param int y: The pixel column
        :param color: Whether to turn the pixel on or off
        :type color: int or bool
        """
        value = self._matrix.pixel(x, y, color)
        self._update()
        return value

    def show(self):
        """
        Update the Pixels. This is only needed if auto_write is set to False
        This can be very useful for more advanced graphics effects.
        """
        self._matrix.show()

    def fill(self, fill):
        """
        Turn all pixels on or off

        :param bool fill: True turns all pixels on, False turns all pixels off

        """
        if isinstance(fill, bool):
            self._matrix.fill(1 if fill else 0)
            self._update()
        else:
            raise ValueError('Must set to either True or False.')

    def shift_right(self, rotate=False):
        """
        Shift all pixels right

        :param rotate: (Optional) Rotate the shifted pixels to the left side (default=False)
        """
        for y in range(0, self.rows):
            last_pixel = self._matrix[self.columns - 1, y] if rotate else 0
            for x in range(self.columns - 1, 0, -1):
                self._matrix[x, y] = self._matrix[x - 1, y]
            self._matrix[0, y] = last_pixel
        self._update()

    def shift_left(self, rotate=False):
        """
        Shift all pixels left

        :param rotate: (Optional) Rotate the shifted pixels to the right side (default=False)
        """
        for y in range(0, self.rows):
            last_pixel = self._matrix[0, y] if rotate else 0
            for x in range(0, self.columns - 1):
                self._matrix[x, y] = self._matrix[x + 1, y]
            self._matrix[self.columns - 1, y] = last_pixel
        self._update()

    def shift_up(self, rotate=False):
        """
        Shift all pixels up

        :param rotate: (Optional) Rotate the shifted pixels to bottom (default=False)
        """
        for x in range(0, self.columns):
            last_pixel = self._matrix[x, self.rows - 1] if rotate else 0
            for y in range(self.rows - 1, 0, -1):
                self._matrix[x, y] = self._matrix[x, y - 1]
            self._matrix[x, 0] = last_pixel
        self._update()

    def shift_down(self, rotate=False):
        """
        Shift all pixels down

        :param rotate: (Optional) Rotate the shifted pixels to top (default=False)
        """
        for x in range(0, self.columns):
            last_pixel = self._matrix[x, 0] if rotate else 0
            for y in range(0, self.rows - 1):
                self._matrix[x, y] = self._matrix[x, y + 1]
            self._matrix[x, self.rows - 1] = last_pixel
        self._update()

    @property
    def auto_write(self):
        """
        Whether or not we are automatically updating
        If set to false, be sure to call show() to update
        """
        return self._auto_write

    @auto_write.setter
    def auto_write(self, write):
        if isinstance(write, bool):
            self._auto_write = write

    @property
    def blink_rate(self):
        """
        Blink Rate returns the current rate that the pixels blink.
        0 = Not Blinking
        1-3 = Successively slower blink rates
        """
        return self._matrix.blink_rate

    @blink_rate.setter
    def blink_rate(self, rate):
        self._matrix.blink_rate = rate

    @property
    def brightness(self):
        """
        Brightness returns the current display brightness.
        0-15 = Dimmest to Brightest Setting
        """
        return self._matrix.brightness

    @brightness.setter
    def brightness(self, brightness):
        self._matrix.brightness = brightness
