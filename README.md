# Autonomous Thermal Camera using Raspberry Pi Zero 2 W

## 📖 Overview
This repository contains the software, 3D enclosure files, and documentation for a fully autonomous, portable thermal imaging camera.
The project was developed as my Bachelor's Thesis in Applied Electronics.
The device captures raw thermal telemetry, processes it using spatial interpolation, and renders a live dynamic colormap on an integrated display.

## 🛠️ Hardware Components
* **SBC:** Raspberry Pi Zero 2 W
* **Thermal Sensor:** Melexis MLX90640-BAB (32x24 IR array) via I2C
* **Display:** 2.0-inch IPS TFT LCD (ST7789 controller) via SPI
* **Power:** Custom Li-ion Battery Management System (IP5306) with dual 18650 cells (4000mAh)
* **Enclosure:** Custom 3D-printed case designed in Autodesk Tinkercad

## 💻 Software Features
The core script is written in Python and relies on:
* `NumPy` for high-speed matrix normalization and manipulation.
* `Matplotlib` ('inferno' colormap) to dynamically map temperatures.
* `Pillow` (PIL) for bilinear spatial interpolation (upscaling 32x24 to 240x320).
* Hardware interrupts (GPIO) for executing safe OS shutdowns preventing SD card corruption.

## 📄 Full Documentation
For a complete in-depth analysis, including theoretical fundamentals, thermal tracking graphs, and comparisons against a commercial FLIR ETS320 camera, please refer to the attached `VântuMihail_Licenta.pdf`.
