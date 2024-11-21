#kid竞技场功能
#加载机器人框架
from nonebot.adapters.onebot.v11 import GROUP
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot import on_fullmatch
from pathlib import Path
from .function import open_data
from .list2 import kid_data2

__all__ = [
    'ck'
]

pvp_path = Path() / "data" / "UserList" / "pvp.json"

ck = on_fullmatch('ck0', permission=GROUP, priority=1, block=True)
@ck.handle()
async def ck_handle():
    pvp_data = {}
    pvp_data = open_data(pvp_path)
    if(pvp_data=={}):
        await ck.finish("0号猎场游戏还未开始！")

    i = 0
    text = "当前战况：\n\n"
    for v in pvp_data['list']:
        i += 1  #编号
        nickname = v[2]   #qq号
        kid = v[1].split('_')
        level = kid[0]
        num = kid[1]
        name = kid_data2.get(level).get(num).get('name')
        text += f"{i}. "+nickname+f"的{level}级{name}\n"

    await ck.finish(text)

        


