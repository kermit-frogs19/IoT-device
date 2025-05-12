from ezRPC import Producer


class SystemRPCClient(Producer):
    def __init__(
            self,
            url: str,
            *args,
            **kwargs
    ):
        super().__init__(url, *args, **kwargs)
        self.service_name = "SystemRPC"

    async def get_commands(self, device_id: int, **kwargs) -> list:
        return await self.call(f"{self.service_name}.get_commands", device_id)

    async def command_completed(self, command_id: int, status: int, **kwargs) -> None:
        return await self.call(f"{self.service_name}.command_completed", command_id, status)

    async def new_event(self, device_id: int, event: dict, **kwargs) -> None:
        return await self.call(f"{self.service_name}.new_event", device_id, event)

    async def test(self, message: str, **kwargs) -> str:
        return await self.call(f"{self.service_name}.test", message)
