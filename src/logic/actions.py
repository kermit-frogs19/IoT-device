



class Actions:
    def __init__(self) -> None:
        pass

    def turn_on(self) -> None:
        print("turn_on command completed")

    def turn_off(self) -> None:
        print("turn_off command completed")

    def update(self, running: bool) -> None:
        print(f"update(running={running}) command completed")

    def restart(self) -> None:
        print(f"restart command completed")

