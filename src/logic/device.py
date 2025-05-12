import asyncio

from src.clients.system_rpc import SystemRPCClient
from src.logic.actions import Actions
from src.common.logger import Logger
from src.common.config import STATUS_NEW, STATUS_READ, STATUS_ERROR, STATUS_SUCCESS


class Device:
    def __init__(
            self,
            device_id: int,
            rpc: SystemRPCClient,
            actions: Actions,
    ):
        self.device_id = device_id
        self.rpc = rpc
        self.actions = actions

        self.logger = Logger()
        self._task = None
        self._running = False

    async def start(self, interval: int = 30) -> None:
        self.logger.info(f"Device {self.device_id} started.")
        self._running = True
        while self._running:
            try:
                await self.get_and_run_commands()
            except BaseException as e:
                self.logger.error(f"Error in command loop: {e}")
            self.logger.info(f"Sleeping {interval}s...")
            await asyncio.sleep(interval)  # wait 20 seconds between command pulls

    async def stop(self) -> None:
        self.logger.info(f"Device {self.device_id} stopped.")

    async def get_and_run_commands(self) -> None:
        try:
            commands: list[dict] = await self.rpc.get_commands(self.device_id, timeout=None)
            if not commands:
                self.logger.info(f"Got no commands for device {self.device_id}")
                return

            for command in commands:
                function = getattr(self.actions, command["command"])
                if not function:
                    self.logger.warning(f"Unknown command: {command['command']}")
                    continue
                kwargs = command["kwargs"]
                self.logger.info(f"Executing command {command["id"]} : {command["command"]}({", ".join([f"{k}={v}" for k, v in kwargs.items()])})")

                try:
                    function(**kwargs)
                except (ConnectionError, OSError) as e:
                    self.logger.warning(f"Device {self.device_id} failed to connect to the server - {e.__class__.__name__}. {str(e)}")
                    return
                except BaseException as e:
                    self.logger.error(f"Error when executing command {command["id"]}: {e.__class__.__name__}. {str(e)}")
                    await self.rpc.command_completed(command["id"], STATUS_ERROR, timeout=None)
                    continue

                await self.rpc.command_completed(command["id"], STATUS_SUCCESS, timeout=None)
        except (ConnectionError, OSError):
            self.logger.warning(f"Device {self.device_id} failed to connect to the server - {e.__class__.__name__}. {str(e)}")
            return
        except BaseException as e:
            print(e)
            return





