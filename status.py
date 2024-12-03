from nonebot import on_fullmatch
from nonebot.log import logger
import psutil
import platform
from nonebot.adapters.onebot.v11 import GroupMessageEvent

__all__ = ['status']

status = on_fullmatch('状态', priority=5)
@status.handle()
async def handle_status(event: GroupMessageEvent):
    #判断是不是主人
    if(event.user_id!=1047392286):
        logger.info("非主人发送状态")
        return

    #获取系统信息
    system_info = platform.system()
    #获取系统版本
    system_version = platform.version()
    #获取系统CPU使用率
    cpu_percent = psutil.cpu_percent(interval=1)
    #获取系统内存使用率
    memory_percent = psutil.virtual_memory().percent
    #获取系统磁盘使用率
    disk_percent = psutil.disk_usage('/').percent

    #发送信息
    await status.send(f"系统：{system_info}.{system_version}\nCPU使用率：{cpu_percent}%\n内存使用率：{memory_percent}%\n磁盘使用率：{disk_percent}%", at_sender=True)