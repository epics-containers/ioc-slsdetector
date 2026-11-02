#!/usr/bin/env python3

import argparse
import socket
import sys
import time
from ruamel.yaml import YAML


CONFIG_FILE = "/epics/generic-source/ioc/config/ioc.yaml"


def get_num_modules(config_file):
    """Read numModules from the SLS detector configuration."""

    yaml = YAML(typ="safe")

    with open(config_file) as f:
        config = yaml.load(f)

    detectors = [
        entity for entity in config["entities"]
        if entity.get("type") == "slsDetector.slsDetectorConfigure"
    ]

    if len(detectors) != 1:
        raise ValueError(
            f"Expected one slsDetectorConfigure entity, "
            f"found {len(detectors)}"
        )

    num_modules = int(detectors[0]["numModules"])

    if num_modules < 1:
        raise ValueError(f"Invalid numModules: {num_modules}")

    return num_modules


def check_port(host, port, timeout=1):
    """Return True if a TCP connection can be established."""

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def main():

    parser = argparse.ArgumentParser(
        description="Wait for all SLS receiver module ports"
    )

    parser.add_argument("--config", default=CONFIG_FILE)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--base-port", type=int, default=1954)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--interval", type=int, default=2)

    args = parser.parse_args()

    num_modules = get_num_modules(args.config)

    ports = range(
        args.base_port,
        args.base_port + num_modules
    )

    deadline = time.monotonic() + args.timeout

    print(
        f"Checking {num_modules} SLS receiver module ports "
        f"({args.base_port}-{args.base_port + num_modules - 1})",
        flush=True
    )

    while True:

        unavailable = [
            port for port in ports
            if not check_port(args.host, port)
        ]

        if not unavailable:
            print(
                "All SLS receiver module ports are accepting connections",
                flush=True
            )
            return 0

        remaining = deadline - time.monotonic()

        if remaining <= 0:
            print(
                f"ERROR: Receiver startup timeout. "
                f"Unavailable ports: {unavailable}",
                file=sys.stderr,
                flush=True
            )
            return 1

        print(
            f"Waiting for receiver ports: {unavailable}",
            flush=True
        )

        time.sleep(min(args.interval, remaining))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr, flush=True)
        sys.exit(1)
