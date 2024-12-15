#kid竞技场功能
#加载机器人框架
from nonebot.adapters.onebot.v11 import GROUP
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot import on_fullmatch
from pathlib import Path
from .function import open_data
from .list2 import kid_data2
from .list3 import kid_data3
import datetime

__all__ = [
    'ck'
]

pvp_path = Path() / "data" / "UserList" / "pvp.json"

ck = on_fullmatch('ck0', permission=GROUP, priority=1, block=True)
@ck.handle()
async def ck_handle(bot: Bot, event: GroupMessageEvent):
    pvp_data = open_data(pvp_path)
    current_time_2 = datetime.datetime.now()
    # 当前时间戳
    timestamp_2= int(current_time_2.timestamp())
    start_time = pvp_data.get('startTime', 0)
    time_diff = (timestamp_2 - start_time) / 3600
    count = pvp_data.get('count', 0)
    totalCount = pvp_data.get('totalCount', 0)
    if totalCount < 40:
        reward = 50
    elif totalCount < 60:
        reward  = 100
    elif totalCount < 80:
        reward  = 150
    elif totalCount <= 100:
        reward  = 200

    if time_diff <= 1:
        timeReward = 25
    elif time_diff <= 2:
        timeReward = 50
    else:
        timeReward = 100
    total = reward + timeReward


    if pvp_data == {}:
        await ck.finish("0号猎场游戏还未开始！")

    i = 0
    text = f"总回合数：{totalCount}\n"
    text += f"当前回合数：{count}\n"
    text += f"本回合持续时间：{time_diff:.2f}h\n"
    text += f"本次回合奖励：{reward}刺儿\n"
    text += f"当前时间奖励：{timeReward}刺儿\n"
    text += f"本局目前总奖励：{total}刺儿\n"
    text += "当前战况："
    for v in pvp_data['list']:
        text += "\n\n"
        i += 1  # 编号
        lie3 = "否"
        lie = v[4]
        if (lie == 5):
            lie3 = "是"
        rank = v[3]
        nickname = v[2]  # QQ号
        kid = v[1].split('_')
        level = kid[0]
        num = kid[1]
        if (lie != 5):
            name = kid_data2.get(level, {}).get(num, {}).get('name', "未知名称")
        elif (lie == 5):
            name = kid_data3.get(level, {}).get(num, {}).get('name', "未知名称")
        text += f"擂台{i}：\n[{nickname}] 的 [{level}级{name}]\n该kid的常驻战力为：[{rank}]\n该kid是否为3猎kid：[{lie3}]"

    # 创建转发消息
    forward_message = [
        {
            "type": "node",
            "data": {
                "name": "0猎擂台详情",
                "uin": event.self_id,  # 设置为机器人的 QQ 号
                "content": text
            }
        }
    ]

    # 转发消息
    if forward_message:
        await bot.send_forward_msg(
            group_id=event.group_id,  # 转发到当前群组
            messages=forward_message
        )


        