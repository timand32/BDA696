import numpy as np


class HeaderPrinter:
    def __init__(self, name: str):
        self.name = name
        return

    def print(self) -> None:
        print(80 * "*")
        print(self.name)
        print(80 * "*")
        return


class FancyHeaderPrinter(HeaderPrinter):
    def __init__(self, name: str, stars: int):
        super().__init__(name)
        self.stars = stars

    def print(self) -> None:
        print(self.stars * "*")
        print(self.name)
        print(self.stars * "*")


def print_junk():
    junk = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    print(junk)
    return


def main() -> int:
    id = np.identity(10)
    print(f"Identity(10):\n{id}")
    printers = [
        HeaderPrinter(name="Printer"),
        FancyHeaderPrinter(name="Fancy Printer", stars=10),
    ]
    for printer in printers:
        printer.print()
    print_junk()
    return 0


if __name__ == "__main__":
    main()
