from time import sleep

from nonebot import get_driver

from .config import Config
import psutil
import GPUtil
from nonebot import on_command

global_config = get_driver().config
config = Config.parse_obj(global_config)

check_server = on_command(cmd='checks', priority=2, block=True)


@check_server.handle()
async def check_():
    def change_size(byte, suffix="B"):
        divisor = 1024
        for unit in ['', 'K', 'M', 'G', 'T']:
            if byte < divisor:
                size = f"{byte:.2f}{unit}{suffix}"
                return size
            byte /= divisor

    await check_server.send(f"当前服务器的CPU使用率: {psutil.cpu_percent()}%")
    mem = psutil.virtual_memory()
    await check_server.send(f"当前服务器的总内存：{change_size(mem.total)}" + '\n'
                            f"当前服务器已被使用的内存：{change_size(mem.used)}"+ '\n'
                            f"当前服务器内存占用率：{mem.percent}%")
    sleep(1)
    diskC = psutil.disk_usage('C:\\')
    diskD = psutil.disk_usage('D:\\')
    await check_server.send(f"当前服务器的总存储：C盘：{change_size(diskC.total)},D盘：{change_size(diskD.total)}" + '\n'
                            f"当前服务器已被使用的存储：C盘：{change_size(diskC.used)},D盘：{change_size(diskD.used)}" + '\n'
                            f"当前服务器磁盘存储占用率：C盘：{diskC.percent},D盘：{diskD.percent}%")
    sleep(1)
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        gpu_name = gpu.name
        gpu_load = gpu.load
        gpu_temperature = gpu.temperature
        gpu_memoryTotal = gpu.memoryTotal
        await check_server.send(f"当前服务器使用的显卡：{gpu_name}" + '\n'
                                f"当前服务器使用的显卡总显存：{gpu_memoryTotal}MB" + '\n'
                                f"当前服务器使用的显卡使用率：{gpu_load}%" + '\n'
                                f"当前服务器使用的显卡温度：{gpu_temperature}℃")
