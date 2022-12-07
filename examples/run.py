import asyncio
import logging

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from ld2410_ble import LD2410BLE, LD2410BLEState

_LOGGER = logging.getLogger(__name__)

ADDRESS = "D0291B39-3A1B-7FF2-787B-4E743FED5B25"
ADDRESS = "D0291B39-3A1B-7FF2-787B-4E743FED5B25"

async def run() -> None:
    scanner = BleakScanner()
    future: asyncio.Future[BLEDevice] = asyncio.Future()

    def on_detected(device: BLEDevice, adv: AdvertisementData) -> None:
        if future.done():
            return
        _LOGGER.info("Detected: %s", device)
        if device.address.lower() == ADDRESS.lower():
            _LOGGER.info("Found device: %s", device.address)
            future.set_result(device)

    scanner.register_detection_callback(on_detected)
    await scanner.start()

    def on_state_changed(state: LD2410BLEState) -> None:
        _LOGGER.info("State changed: %s", state)

    device = await future
    ld2410b = LD2410BLE(device)
    cancel_callback = ld2410b.register_callback(on_state_changed)
    await ld2410b.initialise()
    await asyncio.sleep(10)
    cancel_callback()
    await scanner.stop()


logging.basicConfig(level=logging.INFO)
logging.getLogger("ld2410_ble").setLevel(logging.DEBUG)
asyncio.run(run())
