import pygatt

# The BGAPI backend will attempt to auto-discover the serial device name of the
# attached BGAPI-compatible USB adapter.
adapter = pygatt.GATTToolBackend()
CHRCT_UUID_READ = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
addrs = "ec:6a:31:5b:17:2d"

try:
    adapter.start()
    device = adapter.connect(addrs)
    value = device.char_read(CHRCT_UUID_READ)
finally:
    adapter.stop()