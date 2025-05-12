import asyncio
import logging

from src.common.logger import Logger
from src.clients.system_rpc import SystemRPCClient
from src.logic.actions import Actions
from src.logic.device import Device
from ezRPC import Producer


logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.DEBUG,
)


logger = Logger()
system_rpc = SystemRPCClient("https://vadim-seliukov-quic-server.com:8000", use_tls=False, timeout=None)    # vadim-seliukov-quic-server.com
actions = Actions()
device = Device(4, system_rpc, actions)


async def main():
    try:
        asyncio.run(device.start())
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info(f"App manually stopped.")


if __name__ == '__main__':
    asyncio.run(device.start(60))


