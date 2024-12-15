from .config import user_path, file_name, bot_owner_id, shop_database
from nonebot.adapters.onebot.v11 import GROUP
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageSegment
from nonebot import on_command, on_fullmatch
from nonebot.params import CommandArg
import json
import datetime
import os
from pathlib import Path

import psutil
import platform

__all__ = [
    'len_user',
    'fafang',
    'ck_admin_single',
    'fafang_single',
    'set_single',
    'deduct_single',
    'ck_admin_single',
    'admin_timeClear',
    'admin_Restock'
]

# 状态
status = on_fullmatch('状态', priority=5)
@status.handle()
async def handle_status(event: GroupMessageEvent):
    #判断是不是主人
    if str(event.user_id) not in bot_owner_id:
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
    await status.send(f"\n系统：{system_info}.{system_version}\nCPU使用率：{cpu_percent}%\n内存使用率：{memory_percent}%\n磁盘使用率：{disk_percent}%", at_sender=True)

#查看用户数量
len_user = on_command("用户数", permission=GROUP, priority=1, block=True)
@len_user.handle()
async def len_user_handle(event: GroupMessageEvent, arg: Message = CommandArg()):
    #判断是不是管理员账号
    if str(event.user_id) not in bot_owner_id:
        return

    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    #统计数量
    count = len(data)

    await len_user.finish(f"zhuakid游戏目前共有{count}个用户！", at_sender=True)

#全服发放刺儿
fafang = on_command("全服发放", permission=GROUP, priority=1, block=True)
@fafang.handle()
async def fafang_handle(event: GroupMessageEvent, arg: Message = CommandArg()):
    #判断是不是管理员账号
    if str(event.user_id) not in bot_owner_id:
        return

    #解析参数
    jiangli = int(str(arg))
    if(jiangli <= 0):
        return
    
    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    #给每个账户发刺儿
    for v in data.values():
        v['spike'] += jiangli

    #写入文件
    with open(user_path / file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

#查询某个用户的刺儿
ck_admin_single = on_command("查询", permission=GROUP, priority=1, block=True)
@ck_admin_single.handle()
async def ck_admin_single_handle(event: GroupMessageEvent, arg: Message = CommandArg()):
    #判断是不是管理员账号
    if str(event.user_id) not in bot_owner_id:
        return

    arg = str(arg).split(" ")
    #得到at的人的qq号
    user_id = arg[0]

    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    #没有这个用户
    if(not user_id in data):
        await fafang_single.finish("此人还没有注册zhuakid账号", at_sender=True)

    #有这个用户
    spike = data[user_id]['spike']
    await ck_admin_single.finish(f"该用户目前拥有{spike}刺儿！", at_sender=True)

#给某个用户发放刺儿
fafang_single = on_command("发放", permission=GROUP, priority=1, block=True)
@fafang_single.handle()
async def fafang_handle(event: GroupMessageEvent, arg: Message = CommandArg()):
    #判断是不是管理员账号
    if str(event.user_id) not in bot_owner_id:
        return

    #得到at的人的qq号
    arg = str(arg).split(" ")
    user_id = arg[0]

    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    #没有这个用户
    if(not user_id in data):
        await fafang_single.finish("找不到该用户信息", at_sender=True)

    #有这个用户
    try:
        jiangli = int(arg[1])
    except:
        await fafang_single.finish("格式错误，请按照/发放 (用户QQ号)(数量)的格式输入！", at_sender=True)
    else:
        if(jiangli <= 0):
            return
        data[user_id]['spike'] += jiangli

        #写入文件
        with open(user_path / file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        await fafang_single.finish(f"给"+MessageSegment.at(user_id)+f"发放{jiangli}刺儿成功！", at_sender=True)

#给某个用户设定指定刺儿
set_single = on_command("设定", permission=GROUP, priority=1, block=True)
@set_single.handle()
async def set_handle(event: GroupMessageEvent, arg: Message = CommandArg()):
    #判断是不是管理员账号
    if str(event.user_id) not in bot_owner_id:
        return

    #得到at的人的qq号
    arg = str(arg).split(" ")
    user_id = arg[0]

    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    #没有这个用户
    if(not user_id in data):
        await set_single.finish("找不到该用户信息", at_sender=True)

    #有这个用户
    try:
        jiangli = int(arg[1])
    except:
        await set_single.finish("格式错误，请按照/设定 (用户QQ号)(数量)的格式输入！", at_sender=True)
    else:
        if(jiangli <= 0):
            return
        data[user_id]['spike'] = jiangli

        #写入文件
        with open(user_path / file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        await set_single.finish(MessageSegment.at(user_id)+f"的刺儿已设定为{jiangli}！", at_sender=True)

#给某个用户扣除刺儿
deduct_single = on_command("扣除", permission=GROUP, priority=1, block=True)
@deduct_single.handle()
async def deduct_handle(event: GroupMessageEvent, arg: Message = CommandArg()):
    #判断是不是管理员账号
    if str(event.user_id) not in bot_owner_id:
        return

    #得到at的人的qq号
    arg = str(arg).split(" ")
    user_id = arg[0]

    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    #没有这个用户
    if(not user_id in data):
        await deduct_single.finish("找不到该用户信息", at_sender=True)

    #有这个用户
    try:
        jiangli = int(arg[1])
    except:
        await deduct_single.finish("格式错误，请按照/设定 (用户QQ号)(数量)的格式输入！", at_sender=True)
    else:
        if(jiangli <= 0):
            return
        data[user_id]['spike'] -= jiangli
        if data[user_id]['spike'] < 0:
            data[user_id]['spike'] = 0

        #写入文件
        with open(user_path / file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        await deduct_single.finish(f"已扣除"+MessageSegment.at(user_id)+f"{jiangli}刺儿！", at_sender=True)

#查询超市购买历史记录
ck_admin_history = on_command("账单", permission=GROUP, priority=1, block=True)
@ck_admin_history.handle()
async def ck_admin_history_handle(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    #判断是不是管理员账号
    if str(event.user_id) not in bot_owner_id:
        return

    #打开文件
    data_bili = {}
    today = ""
    if(len(str(arg))==0):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        today = str(arg)
    
    bili = Path()/"data"/"Shop"/f"{today}.json"
    if(os.path.exists(bili)):
        with open(bili, 'r', encoding='utf-8') as f:
            data_bili = json.load(f)

        text = f"{today}\n"
        for v in data_bili['list']:
            text += f"{v}\n"
            
        # 创建转发消息
        forward_messages = [
            {
                "type": "node",
                "data": {
                    "name": "商品列表",
                    "uin": event.self_id,  # 设置为机器人的QQ号
                    "content": text
                }
            }
        ]
        
        # 转发消息
        if forward_messages:
            await bot.send_forward_msg(
                group_id=event.group_id,  # 转发到当前群组
                messages=forward_messages
            )
        # await ck_admin_history.finish(text, at_sender=True)
    else:
        await ck_admin_history.finish("没有找到该日期的账单！", at_sender=True)

#神权！清除zhuakid的cd
admin_timeClear = on_command("清除冷却", permission=GROUP, priority=1, block=True)
@admin_timeClear.handle()
async def timeClear_Admin(event: GroupMessageEvent, arg: Message = CommandArg()):
    
    #判断是不是管理员账号
    if str(event.user_id) not in bot_owner_id:
        return
    
    arg = str(arg).split(" ")
    #清除冷却目标的qq号
    user_id = arg[0]

    data = {}
    if(os.path.exists(user_path / file_name)):
        with open(user_path / file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    #没有这个用户
    if(not user_id in data):
        await fafang_single.finish("找不到该用户信息", at_sender=True)
    
    current_time = datetime.datetime.now()
    next_time_r = current_time + datetime.timedelta(seconds=1)
    data[str(user_id)]['next_time'] = next_time_r.strftime("%Y-%m-%d %H:%M:%S")
    data[str(user_id)]['next_clock_time'] = next_time_r.strftime("%Y-%m-%d %H:%M:%S")
    data[str(user_id)]['work_end_time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")

    #写入文件
    with open(user_path / file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    await admin_timeClear.finish(MessageSegment.at(user_id)+f"的冷却已清除", at_sender=True)

#手动进行商店的补货(刷新)
admin_Restock = on_command("补货", permission=GROUP, priority=1, block=True)
@admin_Restock.handle()
async def Restock_Admin():
    shop_data ={}
    current_date = datetime.date.today()  #返回今天日期
    last_date = current_date - datetime.timedelta(days=1)
    if(os.path.exists(shop_database)):
        #打开商店仓库
        with open(shop_database, 'r', encoding='utf-8') as f:
            shop_data = json.load(f)
    else:
        await admin_Restock.finish("商店不存在。", at_sender=True)       

    shop_data["date"] = last_date.strftime("%Y-%m-%d %H:%M:%S")
    #写入文件
    with open(shop_database, 'w', encoding='utf-8') as f:
        json.dump(shop_data, f, indent=4)
    await admin_Restock.finish("补货已完成", at_sender=True)
