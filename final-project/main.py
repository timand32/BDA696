import sys

import pythagorean_report


def main() -> int:
    pythagorean_report.report_pythagoreans()
    return 0


if __name__ == "__main__":
    sys.exit(main())
