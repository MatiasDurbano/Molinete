"""Implements a HD44780 character LCD connected via PCF8574 on I2C."""

from .lcd_api import LcdApi
#from pyb import I2C, delay
from machine import I2C
import time
# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27

# Defines shifts or masks for the various LCD line attached to the PCF8574

MASK_RS = 0x01
MASK_RW = 0x02
MASK_E = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA = 4

msg= "longitud demasiado grande"

class I2cLcd(LcdApi):
    """Implements a HD44780 character LCD connected via PCF8574 on I2C."""

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.i2c.writeto(self.i2c_addr, 0)
        # Send reset 3 times
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        # Put LCD into 4 bit mode
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        LcdApi.__init__(self, num_lines, num_columns)
        cmd = self.LCD_FUNCTION
        if num_lines > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)

    def hal_write_init_nibble(self, nibble):
        """Writes an initialization nibble to the LCD.
        This particular function is only used during intiialization.
        """
        byte = ((nibble >> 4) & 0x0f) << SHIFT_DATA
        self.i2c.writeto(self.i2c_addr,byte | MASK_E)
        self.i2c.writeto(self.i2c_addr,byte )

    def hal_backlight_on(self):
        """Allows the hal layer to turn the backlight on."""
        self.i2c.writeto(self.i2c_addr,1 << SHIFT_BACKLIGHT)

    def hal_backlight_off(self):
        """Allows the hal layer to turn the backlight off."""
        self.i2c.writeto(self.i2c_addr,0)

    def hal_write_command(self, cmd):
        """Writes a command to the LCD.
        Data is latched on the falling edge of E.
        """
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                (((cmd >> 4) & 0x0f) << SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr,byte | MASK_E)
        self.i2c.writeto(self.i2c_addr,byte)
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                ((cmd & 0x0f) << SHIFT_DATA))
        self.i2c.writeto( self.i2c_addr,byte | MASK_E)
        self.i2c.writeto(self.i2c_addr,byte)
        if cmd <= 3:
            # The home and clear commands require a worst
            # case delay of 4.1 msec
            time.sleep(1)

    def hal_write_data(self, data):
        """Write data to the LCD."""
        byte = (MASK_RS |(self.backlight << SHIFT_BACKLIGHT) |(((data >> 4) & 0x0f) << SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr,byte | MASK_E)
        self.i2c.writeto(self.i2c_addr,byte)
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                ((data & 0x0f) << SHIFT_DATA))
        self.i2c.writeto( self.i2c_addr,byte | MASK_E)
        self.i2c.writeto( self.i2c_addr,byte)

    def string_converter(self,data):
        hexs = []
        for i in data:
            hexs.insert(i,hex(ord(i)))
        return hexs

   #solamente controlo que data sea menor a 32
   #superando la longitud 32 deberia hacer otras cosas
   #como desplazamientos en la fila 2
    def write_data(self,data):
        self.clear()
        length =len(data)
        if(length<=16):
            hexs = self.string_converter(data)
            for i in hexs:
                self.hal_write_data(int(i,16))
        if(length>16 and length<=32):
            msg1=data[0:16]
            msg2=data[16:len(data)]
            hexs1 = self.string_converter(msg1)
            hexs2 = self.string_converter(msg2)
            for i in hexs1:
                self.hal_write_data(int(i,16))
            LcdApi.move_to(self,0,1)
            for i in hexs2:
                self.hal_write_data(int(i,16))
            LcdApi.move_to(self,0,0)
        if(length>32):
            self.write_data(msg)
