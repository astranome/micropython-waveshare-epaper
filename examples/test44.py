import framebuf
import epaper2in13b
from machine import Pin, SPI
from writer import Writer
import freesans20

# SPIV on ESP32
sck = Pin(18)
miso = Pin(19)
mosi = Pin(23)
dc = Pin(32)
cs = Pin(33)
rst = Pin(19)
busy = Pin(35)
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)
e = epaper2in13b.EPD(spi, cs, dc, rst, busy)
e.init()

class DummyDisplay(framebuf.FrameBuffer):
    def __init__(self, buffer, width, height, format):
        self.height = height
        self.width = width
        self.buffer = buffer
        self.format = format
        super().__init__(buffer, width, height, format)

w=104; h=212
buf_black = bytearray(w * h // 8)
buf_red   = bytearray(w * h // 8)
black_red = 0 # will be black on buf_black, red on buf_red
white     = 1

d_b = DummyDisplay(buf_black, w, h, framebuf.MONO_HLSB)
d_r = DummyDisplay(buf_red, w, h, framebuf.MONO_HLSB)
d_b.fill(white)
d_r.fill(white)

wri_b = Writer(d_b, freesans20, False)
Writer.set_textpos(d_b, 0, 0)  # verbose = False to suppress console output
wri_b.printstring('E-MOE!\n', True)
wri_b.printstring('OHA PA6OTAET!\n',True)
wri_b.printstring('CjiABA KTTCC !\n', True)
wri_b.printstring('CjiABA MHE', True)

wri_r = Writer(d_r, freesans20, False)
Writer.set_textpos(d_r, 132, 0)
wri_r.printstring('uPython\n', True)
wri_r.printstring('    :-)\n', True)
wri_r.printstring('DA YPA!!!!! :-)', True)

print('Sending to display')
e.display_frame(buf_black, buf_red)
print('Done!.......')
e.sleep()  # recommended by manufacturer to avoid damage to display
print('E-paper sleeping!...')

print('END')