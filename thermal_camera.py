import os
import time
import board
import busio
import digitalio
import numpy as np
import matplotlib
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import adafruit_mlx90640
# Initialize hardware shutdown switch on GPIO 21
buton = digitalio.DigitalInOut(board.D21)
buton.direction = digitalio.Direction.INPUT
buton.pull = digitalio.Pull.UP
stare_initiala_buton = buton.value
# Initialize the 2.0-inch ST7789 IPS display over SPI bus
spi = board.SPI()
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D24)
reset_pin = digitalio.DigitalInOut(board.D25)
disp = st7789.ST7789(
 spi, width=240, height=320,
 x_offset=0, y_offset=0, baudrate=24000000,
 cs=cs_pin, dc=dc_pin, rst=reset_pin
)
# Initialize the MLX90640 thermal sensor over I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
mlx = None
time.sleep(2)
# Establish robust connection with the I2C sensor
while mlx is None:
 try:
 mlx = adafruit_mlx90640.MLX90640(i2c)
 except Exception:
 time.sleep(0.01)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ
frame = [0] * 768
color_map = matplotlib.colormaps['inferno']
font = ImageFont.load_default()
55
# Main continuous video processing loop
while True:

 # Check for hardware shutdown interrupt
 if buton.value != stare_initiala_buton:
 img_stop = Image.new("RGB", (240, 320), (0, 0, 0))
 draw_stop = ImageDraw.Draw(img_stop)
 draw_stop.text((70, 150), "SHUTTING DOWN...", font=font, fill=(255, 50, 50))
 disp.image(img_stop)
 os.system("sudo shutdown -h now")
 time.sleep(20)
 try:
 # 1. PULL SENSOR DATA: Read the raw temperatures into a 1D array of 768 elements
 mlx.getFrame(frame)

 # 2. NUMPY MATH: Reshape the 1D array into a 24x32 2D matrix for spatial
processing
 data = np.array(frame).reshape((24, 32))

 # Extract minimum, maximum, and center point temperatures for the interface
 d_min = np.min(data)
 d_max = np.max(data)
 temp_centru = data[11, 15]

 # Normalize the temperature data to a 0.0 - 1.0 scale to apply the color map
 norm = (data - d_min) / (d_max - d_min + 0.01)
 rgba = color_map(norm)
 rgb = (rgba[:, :, :3] * 255).astype(np.uint8)

 # 3. PILLOW SMOOTHING: Convert to an image, rotate to portrait, and interpolate
 img = Image.fromarray(rgb, 'RGB')
 img = img.rotate(90, expand=True)
 img = img.transpose(Image.FLIP_LEFT_RIGHT)

 # Resize stretches the 32x24 pixel grid to the 240x320 screen, blending the harsh edges
 img = img.resize((240, 320), Image.BILINEAR)

 # Generate the Display overlay (Temperatures and Crosshair)
 draw = ImageDraw.Draw(img)

 txt_max = f"Max: {d_max:.1f} C"
 txt_min = f"Min: {d_min:.1f} C"
 draw.rectangle([(5, 5), (95, 35)], fill=(0, 0, 0))
 draw.text((10, 8), txt_max, font=font, fill=(255, 100, 100))
 draw.text((10, 20), txt_min, font=font, fill=(100, 150, 255))

 cx, cy = 120, 160
 draw.line([(cx - 5, cy), (cx + 5, cy)], fill=(255, 255, 255), width=1)
 draw.line([(cx, cy - 5), (cx, cy + 5)], fill=(255, 255, 255), width=1)

56
 txt_centru = f"{temp_centru:.1f} C"
 draw.rectangle([(cx + 8, cy + 8), (cx + 55, cy + 22)], fill=(0, 0, 0))
 draw.text((cx + 10, cy + 10), txt_centru, font=font, fill=(255, 255, 255))

 # Send the final rendered frame to the hardware display
 disp.image(img)

 except Exception:
continue