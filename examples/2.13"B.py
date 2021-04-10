"""
	Example for 2.13 inch black & white & red Waveshare 2.13B E-ink screen
	Run on ESP32 Waveshare driver board (software SPI)
	Adapted by Guy -- April 2019
    We used the 2.13" E-paper in landscape mode
"""

import epaper2in13b
from machine import Pin, SPI

# software SPI on ESP32 Waveshare driver board
sck = Pin(13); mosi = Pin(14); cs = Pin(15); busy = Pin(25); rst = Pin(26); dc = Pin(27)
# miso is not used but must be declared. Let's take any unused gpio: 12
miso = Pin(12)
spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

e = epaper2in13b.EPD(spi, cs, dc, rst, busy)
e.init()

h = 104;  w = 212 # e-paper heigth and width. It will be used in landscape mode

buf_black        = bytearray(w * h // 8) # used by frame buffer (landscape)
buf_red          = bytearray(w * h // 8) # used by frame buffer (landscape)
buf_epaper_black = bytearray(w * h // 8) # used to display on e-paper after bytes have been 
buf_epaper_red   = bytearray(w * h // 8) # moved from frame buffer to match e-paper (portrait) 

import framebuf
fb_black = framebuf.FrameBuffer(buf_black, w, h, framebuf.MONO_VLSB)
fb_red   = framebuf.FrameBuffer(buf_red,   w, h, framebuf.MONO_VLSB)
black_red = 0 # will be black on buf_black, red on buf_red
white     = 1

#clear red & black screens, write in black on top left and in red bootom right 
fb_black.fill(white)
fb_red.fill(white)
fb_black.text('Hello world!', 0, 0,black_red)
fb_red.text('Hello world!', 110, 90,black_red)

# Let's draw rectangles, one black one red
fb_black.fill_rect(5, 40, 75, 10, black_red)
fb_red.fill_rect(5, 60, 75, 10, black_red)

# Move frame buffer bytes to e-paper buffer to match e-paper bytes oranisation.
# That is landscape mode to portrait mode. (for red and black buffers) 
x=0; y=0; n=1; R=0
for i in range(1, 14):
    for j in range(1, 213):
        R = (n-x)+((n-y)*12)
        buf_epaper_black[R-1] = buf_black[n-1]
        buf_epaper_red[R-1] = buf_red[n-1]
        n +=1
    x = n+i-1
    y = n-1
    
# We can use EPD class to draw circle(not available in framebuf class) 
# but only after we have moved bytes from framebuffers to e-paper buffers
e.draw_filled_circle(buf_epaper_black, 50, 110, 30, 1)
e.draw_filled_circle(buf_epaper_black, 50, 110, 20, 0)
e.draw_filled_circle(buf_epaper_red, 50, 150, 30, 1)
e.draw_filled_circle(buf_epaper_red, 50, 150, 20, 0)

print('Sending to display')
e.display_frame(buf_epaper_black, buf_epaper_red)
print('Done!.......')
#e.sleep()  # recommended by manufacturer to avoid damage to display
#print('E-paper sleeping!...') 
# also recommended by manufacturer: min. 180s between 2 refresh screen
