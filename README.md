# HTTP Tracking Server

Simple HTTP server that logs visitor information and serves a tracking pixel.

![Demo](https://via.placeholder.com/800x400?text=Server+Screenshot)

## Features

- 📊 Logs visitor IP, user agent, referer, and access time
- 🖼️ Serves a 1x1 transparent tracking pixel
- 📨 Discord notifications for pixel access
- 📁 Persistent logging to `access.log`
- 🌐 Basic HTML interface showing visitor info

## Requirements

- Python 3.6+
- `requests` library (for Discord notifications)

## Installation

```bash
git clone https://github.com/your-username/tracking-server.git
cd tracking-server
pip install -r requirements.txt
