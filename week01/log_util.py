#!/usr/bin/env python
from pathlib import Path
import logging
import time

def write_time():
    current_date = time.strftime("%Y-%m-%d", time.localtime())
    p = Path("/var/log/")
    new_p = p / f"python-{current_date}"
    if not new_p.exists():
        new_p.mkdir()
    file = new_p / "func_time.log"
    if not file.exists():
        file.touch()
    logging.basicConfig(
        filename=str(file),
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s %(name)-8s %(levelname)-8s [line: %(lineno)d] %(message)s'
    )
    logging.info(f'called')


if __name__ == "__main__":
    for i in range(10):
        write_time()
        time.sleep(1)