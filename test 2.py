# -*- coding: utf-8 -*-
"""
Notifications
-------------

Example showing how to add notifications to a characteristic and handle the responses.

Updated on 2019-07-03 by hbldh <henrik.blidh@gmail.com>

"""

import logging
import asyncio
import platform

from bleak import BleakClient
from bleak import _logger as logger

notify_uuid = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
write_uuid = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
service = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
addr = "ec:6a:31:5b:17:2d"
addrs = "DA:82:22:7A:A8:82"
CHARACTERISTIC_UUID = notify_uuid  # <--- Change to the characteristic you want to enable notifications from.


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    print("{0}: {1}".format(sender, data))


async def run(address, debug=False):
    if debug:
        import sys

        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        l.addHandler(h)
        logger.addHandler(h)

    async with BleakClient(address) as client:
        logger.info(f"Connected: {client.is_connected}")

        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        await asyncio.sleep(15.0)
        await client.stop_notify(CHARACTERISTIC_UUID)


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    address = addr
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(run(address, True))