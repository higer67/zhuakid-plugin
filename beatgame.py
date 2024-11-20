####通关一次游戏####
####进入多周目阶段####
#加载机器人框架
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.adapters.onebot.v11 import GROUP
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
# from nonebot_plugin_alconna.uniseg import UniMessage, MsgTarget, Target, SupportScope
from nonebot.log import logger
from nonebot import on_command, get_driver, on_fullmatch
from nonebot.params import CommandArg

bot_owner_id = 1047392286 

#查看当前周目的升级面板
upgrade = on_fullmatch('升级面板', permission=GROUP, priority=1, block=True)
@upgrade.handle()
async def upgrade_handle(bot: Bot, event: GroupMessageEvent):
    #暂时只有管理员能用
    user_id = event.user_id
    if(user_id==bot_owner_id):
        await upgrade.finish("升级彩蛋：\n当前该功能未开发",at_sender=True)


