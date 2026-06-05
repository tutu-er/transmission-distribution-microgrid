"""TDM 命令行入口."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="tdm",
        description="Transmission-Distribution-Microgrid Coordination (主配微协调)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    parser.parse_args()
    print("TDM — 主配微协调平台")


if __name__ == "__main__":
    main()
