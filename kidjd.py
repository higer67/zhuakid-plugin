from nonebot.adapters.onebot.v11 import GROUP
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot import on_fullmatch
from pathlib import Path
import json

__all__ = [
    'mykid'
]

#载入kid一猎场之后的档案
from .list2 import kid_data2

user_path = Path() / "data" / "UserList"
file_name = "UserData.json"

user_list2 = Path() / "data" / "UserList" / "UserList2.json"

#查看kid库存(二猎场以后)
mykid = on_fullmatch('mykid lc2', permission=GROUP, priority=1, block=True)
@mykid.handle()
async def mykid_handle(bot: Bot, event: GroupMessageEvent):
    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    user_id = event.get_user_id()

    data2 = {}
    with open(user_list2, 'r', encoding='utf-8') as f:
        data2 = json.load(f)

    if(str(user_id) in data):

        #读取拥有kid和kid个数并另外存储
        text_arr = ["", "", "", "", ""]  #创建空字典
        level_str = ["一", "二", "三", "四", "五"]
        for k, v in data2[str(user_id)].items():
            k = k.split('_')
            level = k[0]
            num = k[1]
            if(text_arr[int(level)-1]==""): text_arr[int(level)-1] += f"{level_str[int(level)-1]}级：\n"
            text_arr[int(level)-1] += f"{v}个{kid_data2.get(level).get(num).get('name')}\n"

        #合并并转发消息
        msg_list = []    #全部消息列表
        #给消息列表填充信息
        for i in range(4, -1, -1):
            if(text_arr[i]!=""):
                msg_list.append(
                    {
                        "type": "node",
                        "data":{
                            "name": "库存查询室",
                            "uin": event.self_id,
                            "content": text_arr[i]
                        }
                    }
                )
        #转发发送消息
        await bot.call_api("send_group_forward_msg", group_id = event.group_id, messages = msg_list)
    else:
        await mykid.finish("你还没尝试抓过kid......", at_sender = True)