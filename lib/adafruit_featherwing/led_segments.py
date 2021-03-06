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
`adafruit_featherwing.led_segments`
====================================================

Base Class for the AlphaNumeric FeatherWing and 7-Segment FeatherWing helpers_.

* Author(s): Melissa LeBlanc-Williams
"""

__version__ = "1.9.1"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_FeatherWing.git"

from time import sleep

#pylint: disable-msg=unsubscriptable-object, unsupported-assignment-operation

class Segments:
    """Class representing an `Adafruit 14-segment AlphaNumeric FeatherWing
       <https://www.adafruit.com/product/3139>`_.

       Automatically uses the feather's I2C bus."""
    def __init__(self):
        self._segments = None

    def print(self, value):
        """
        Print a number or text to the display

        :param value: The text or number to display
        :type value: str or int or float

        """
        self._segments.print(value)
        self._segments.show()

    def marquee(self, text, delay=0.25, loop=True):
        """
        Automatically scroll the text at the specified delay between characters

        :param str text: The text to display
        :param float delay: (optional) The delay in seconds to pause before scrolling
                            to the next character (default=0.25)
        :param bool loop: (optional) Whether to endlessly loop the text (default=True)

        """
        if isinstance(text, str):
            self.fill(False)
            if loop:
                while True:
                    self._scroll_marquee(text, delay)
            else:
                self._scroll_marquee(text, delay)

    def _scroll_marquee(self, text, delay):
        """
        Scroll through the text string once using the delay
        """
        char_is_dot = False
        for character in text:
            self._segments.print(character)
            # Add delay if character is not a dot or more than 2 in a row
            if character != '.' or char_is_dot:
                sleep(delay)
            char_is_dot = (character == '.')
            self._segments.show()

    def fill(self, fill):
        """Change all Segments on or off

        :param bool fill: True turns all segments on, False turns all segments off

        """
        if isinstance(fill, bool):
            self._segments.fill(1 if fill else 0)
            self._segments.show()
        else:
            raise ValueError('Must set to either True or False.')

    @property
    def blink_rate(self):
        """
        Blink Rate returns the current rate that the text blinks.
        0 = Off
        1-3 = Successively slower blink rates
        """
        return self._segments.blink_rate

    @blink_rate.setter
    def blink_rate(self, rate):
        self._segments.blink_rate = rate

    @property
    def brightness(self):
        """
        Brightness returns the current display brightness.
        0-15 = Dimmest to Brightest Setting
        """
        return self._segments.brightness

    @brightness.setter
    def brightness(self, brightness):
        self._segments.brightness = brightness
