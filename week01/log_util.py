#!/usr/bin/env python
# 编写一个函数, 当函数被调用时，将调用的时间记录在日志中, 日志文件的保存位置建议为：
# /var/log/python- 当前日期 /xxxx.log

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