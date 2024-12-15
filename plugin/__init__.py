#加载异步与通信
#from httpx import AsyncClient
#import asyncio
#加载机器人框架
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.adapters.onebot.v11 import GROUP
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
# from nonebot_plugin_alconna.uniseg import UniMessage, MsgTarget, Target, SupportScope
from nonebot.log import logger
from nonebot import on_command, get_driver, on_fullmatch
from nonebot.params import CommandArg
#加载文件操作系统
import os
from pathlib import Path
import json
#加载读取系统时间相关
import datetime
import time
#加载数学算法相关
import random
#加载KID档案信息
from .list1 import *
from .list2 import *
from .list3 import *
#加载商店信息和商店交互
from .shop import item, today_item
#加载剧情和NPC档案
from .story import npc_da
#加载隐藏kid档案
from .secret import secret_list
#加载抓kid相关的函数
from .function import *
from .event import event_happen, outofdanger, kid_pvp_event
from .kidjd import *
from .pvp import *
from .render import *
from .admin import *

########数据信息#######

#抓kid专用群
group_img = Path() / "data" / "group.jpg"

#除了Kid名字以外的其他key值
other = ["next_time", "next_recover_time", "spike", "date", "buff", "item", "lc"]

#隐藏级别kid
kid_level0 = "Kid0"
kid_level0_path = kid_path_lc1 / kid_level0

#商店数据，商店的数据一天之内对所有玩家共通，每过一天就会刷新一次商品，每天早上6点到晚上10点营业中
shop_database = Path() / "data" / "Shop" / "Shop.json"
shop_open_img = Path() / "data" / "Shop" / "开张图.png"
shop_work_img = Path() / "data" / "Shop" / "营业图.png"

#更新日志
update_text = "详细信息请前往抓kid wiki\n https://docs.qq.com/smartsheet/DVUZtQWlNTG1zZVhN \n进行查看"
#管理员ID
bot_owner_id = ["2153454883", "1047392286", "121096913"]

#用户信息
user_path = Path() / "data" / "UserList"
file_name = "UserData.json"

#赌场信息
duchang_list = Path() / "data" / "DuChang" / "duchang.json"
duchang_open_img = Path() / "data" / "DuChang" / "duchang.png"

##初始化
driver = get_driver()
@driver.on_startup
async def _():
    logger.info("抓Kid系统已经开启...")

#切换猎场
qhlc = on_command('qhlc', permission=GROUP, priority=1, block=True)
@qhlc.handle()
async def qhlc_handle(event: GroupMessageEvent, arg: Message = CommandArg()):
    #读入用户主要列表
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    user_id = str(event.user_id)
    number = str(arg)     #猎场编号
    if(user_id in data):
        #特殊的竞技猎场
        if(number=='0'):

            #一些啥都干不了的buff
            if(data[user_id].get('buff')=='lost'): return

            #原本就在这个猎场
            if('lc' in data[user_id]):
                if(data[user_id]['lc']==number):
                    await qhlc.finish("你现在就在这个猎场呀~", at_sender=True)

            #改变lc值
            data[user_id]['lc'] = number
            #写入文件
            with open(user_path / file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            await qhlc.send(f"已经成功切换到0号猎场！有关0号猎场的细则请输入[0场细则]查看！", at_sender=True)
     
        #正常的收集型猎场
        if(number in ['1','2','3']):

            #一些啥都干不了的buff
            if(data[user_id].get('buff')=='lost'): return

            if('lc' in data[user_id]):
                #原本就在这个猎场
                if(data[user_id]['lc']==number):
                    await qhlc.finish("你现在就在这个猎场呀~", at_sender=True)

            #改变lc值
            data[user_id]['lc'] = number
            #写入文件
            with open(user_path / file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            await qhlc.send(f"已经成功切换到{number}号猎场！", at_sender=True)
    else:
        await qhlc.send("你还没尝试抓过kid.....", at_sender=True)

#随机抓出一个Kid，且有时间间隔限制
catch = on_fullmatch('zhuakid', permission=GROUP, priority=1, block=True)
@catch.handle()
async def zhuakid(bot: Bot, event: GroupMessageEvent):
    #如果是在学长群就发出抓kid群二维码
    group = event.group_id
    """if(group==371629608):
        logger.info(group)
        await catch.finish("考虑到学长群过于刷屏特开个专门玩抓kid的群"+MessageSegment.image(group_img))
    """

    answer = -1
    #----------读取用户信息并交互----------
    data = {}
    if(os.path.exists(user_path / file_name)):
        with open(user_path / file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)

        user_id = event.user_id  #qq号
        current_time = datetime.datetime.now()  #读取当前系统时间
        if (str(user_id) in data):

            #读取信息
            next_time_r = datetime.datetime.strptime(data.get(str(user_id)).get('next_time'), "%Y-%m-%d %H:%M:%S")
            
            #加工饰品时无法抓kid
            #防止没有status这个键
            if ('status' in data[str(user_id)]):
                status = data[str(user_id)].get('status')
            else:
                status = 'normal'

            if(status =='working'): 
                if(not 'work_end_time' in data[str(user_id)]):
                    data[str(user_id)]['work_end_time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
                current_time = datetime.datetime.now()
                work_end_time = datetime.datetime.strptime(data.get(str(user_id)).get('work_end_time'), "%Y-%m-%d %H:%M:%S")
                if current_time < work_end_time:
                    text = time_text(str(work_end_time-current_time))
                    await catch.finish(f"你还在加工饰品，还需要{text}", at_sender=True)
                #时间过了自动恢复正常
                else:
                    data[str(user_id)]['status'] = 'normal'
                    with open(user_path / file_name, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)
            
            #如果受伤了则无法抓
            if(data[str(user_id)].get("buff")=="hurt"): 
                if(current_time < next_time_r):
                    delta_time = next_time_r - current_time
                    await catch.finish(f"你受伤了，需要等{time_text(delta_time)}才能抓")
                else:
                    data[str(user_id)]["buff"] = "normal"

            #迷路脱险事件
            await outofdanger(data,str(user_id),catch,current_time,next_time_r)
            
            #debuff清除逻辑
            current_time = datetime.datetime.now()
            if(not 'next_recover_time' in data[str(user_id)]):
                data[str(user_id)]['next_recover_time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
                with open(user_path / file_name, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)

            current_time = datetime.datetime.now()
            recover_time = datetime.datetime.strptime(data.get(str(user_id)).get('next_recover_time'), "%Y-%m-%d %H:%M:%S")
            if recover_time <= current_time:
                data[str(user_id)]["debuff"] = "normal"
                with open(user_path / file_name, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
            
            #正常抓的逻辑
            if(current_time < next_time_r):
                delta_time = next_time_r - current_time
                answer = 0
            else:
                next_time = current_time + datetime.timedelta(minutes=30)
                data[str(user_id)]['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
                answer = 1
        else:
            #注册用户
            data[str(user_id)] = {}
            next_time = current_time + datetime.timedelta(minutes=30)
            data[str(user_id)]['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
            answer = 1
    else:
        ##注册第一个用户
        user_id = event.get_user_id()
        data[str(user_id)] = {}
        current_time = datetime.datetime.now()
        next_time = current_time + datetime.timedelta(minutes=30)
        data[str(user_id)]['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
        answer = 1

    #----------给出回应-----------
    if(answer == 0):
        text = time_text(str(delta_time))
        await catch.send(f"别抓啦，{text}后再来吧", at_sender = True)
    if(answer == 1):
        #正面buff检测逻辑
        #没有就先加上
        if(not 'buff2' in data[str(user_id)]):
            data[str(user_id)]['buff2'] = 'normal'
        if(not 'lucky_times' in data[str(user_id)]):
            data[str(user_id)]['lucky_times'] = 0
        #幸运
        if data[str(user_id)]["lucky_times"] > 0 and data[str(user_id)]['buff2'] == 'lucky':
            #如果有中毒buff(即抓到kid无法获得刺儿)，则直接清除
            try:
                debuff = data[str(user_id)]['debuff']
            except:
                debuff = 'normal'

            if debuff == 'poisoned':
                data[str(user_id)]['debuff'] = 'normal'
            data[str(user_id)]["lucky_times"] -= 1
        else:
            data[str(user_id)]['buff2'] = 'normal'
            data[str(user_id)]["lucky_times"] = 0

        #第一次抓
        if(not 'lc' in data[str(user_id)]):
            data[str(user_id)]['lc'] = '1'

        #特殊猎场kid竞技场内事件
        if(data[str(user_id)]['lc']=='0'):
            nickname = event.sender.nickname
            await kid_pvp_event(data,str(user_id),nickname,catch,bot)
            #后面的程序不执行
            return

        #触发事件
        await event_happen(data,str(user_id),catch)

        #如果是2号猎场以上需要存到另外的表中
        data2 = {}
        if(data[str(user_id)]['lc']!='1'):
            with open(user_path / f"UserList{data[str(user_id)]['lc']}.json", 'r', encoding='utf-8') as f:
                data2 = json.load(f)

        #确定抓到哪个kid
        kid = zhua_random(liechang_number=data[str(user_id)]['lc'])
        level       = kid[0]   #等级
        name        = kid[1]   #名字
        img         = kid[2]   #图片
        description = kid[3]   #描述
        num         = kid[4]   #编号
        #奖励刺儿
        try:
            debuff = data[str(user_id)].get('debuff')
        except:
            debuff = 'normal'

        if (debuff=='poisoned'):
            spike_give = 0
        else:
            if(level==1): spike_give = 5
            if(level==2): spike_give = 10
            if(level==3): spike_give = 15
            if(level==4): spike_give = 20
            if(level==5): spike_give = 25   

        if(not 'spike' in data[str(user_id)]):
            data[str(user_id)]['spike'] = 0
        
        if (data[str(user_id)]["lucky_times"] > 0):
            spike_give += 15

        data[str(user_id)]['spike'] += spike_give
        #将抓到的结果加入库存
        new_print = ""
        if(data[str(user_id)]['lc']=='1'):
            if(not name in data[str(user_id)]):
                new_print = "\n恭喜你抓出来一个新kid！\n"  #如果出新就添加文本
                data[str(user_id)][name] = 0
            data[str(user_id)][name] += 1  #数量+1
        else:
            if(str(user_id) in data2):
                if(not (str(level)+'_'+str(num)) in data2[str(user_id)]):
                    new_print = "\n恭喜你抓出来一个新kid！\n"  #如果出新就添加文本
                    data2[str(user_id)][str(level)+'_'+str(num)] = 0
                data2[str(user_id)][str(level)+'_'+str(num)] += 1  #数量+1
        
        #写入kid收集表(副统计表)
        if(data[str(user_id)]['lc']=='2'):
            with open(user_path / f"UserList{data[str(user_id)]['lc']}.json", 'w', encoding='utf-8') as f:
                json.dump(data2, f, indent=4)

        #写入主数据表
        with open(user_path / file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        #发送消息
        if(debuff!='poisoned'):
            lucky_num = data[str(user_id)].get('lucky_times') - 1
            text = str(lucky_num)
            if (lucky_num == -1):
                data[str(user_id)]['buff2'] = 'normal'
                data[str(user_id)]['lucky_times'] = 0
            if (data[str(user_id)].get('buff2')=='lucky'):
                await catch.send(new_print+
                            f'\n等级: {level}\n'+
                            f'{name}'+
                            MessageSegment.image(img)+
                            f'{description}'+
                            '\n\n本次奖励'+f'{spike_give}刺儿\n'+
                            f'幸运加成剩余{text}次',
                            at_sender = True)
            else:
                await catch.send(new_print+
                                f'\n等级: {level}\n'+
                                f'{name}'+
                                MessageSegment.image(img)+
                                f'{description}'+
                                '\n\n本次奖励'+f'{spike_give}刺儿',
                                at_sender = True)
        else:
            await catch.send(new_print+
                            f'\n等级: {level}\n'+
                            f'{name}'+
                            MessageSegment.image(img)+
                            f'{description}',
                            at_sender = True)

##每日签到
qd = on_fullmatch('签到', permission=GROUP, priority=1, block=True)
@qd.handle()
async def dailyqd(event: GroupMessageEvent):
    data = {}
    if(os.path.exists(user_path / file_name)):
        #读取刺儿数量
        with open(user_path / file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)

        user_id = event.get_user_id() #获取qq号
        nickname = event.sender.nickname  #获取昵称
        #如果注册账号了就可以签到
        if(str(user_id) in data):

            #一些啥都干不了的buff
            if(data[str(user_id)].get('buff')=='lost'): return

            #若不存在spike，则开一个信息存储
            if(not 'spike' in data[str(user_id)]):
                data[str(user_id)]['spike'] = 0
            
            #获取日期信息
            current_date = datetime.date.today()  #返回今天日期
            current_date_str = current_date.strftime("%Y-%m-%d")  #日期时间对象转字符串
            prevous_date_str = data.get(str(user_id)).get('date', -1)  #读取日期信息
            #判断签到条件
            if(prevous_date_str==-1):
                #随机奖励刺儿数量
                spike = random.randint(1,100)
                if(not 'item' in data[str(user_id)]):
                    data[str(user_id)]['item'] = {}
                if('招财猫' in data[str(user_id)]['item']):
                    num_of_extra_spike = data[user_id]['item']['招财猫'] * 4
                    spike += num_of_extra_spike
                data[str(user_id)]['spike'] += spike  #刷新刺儿数量
                data[str(user_id)]['date'] = current_date.strftime("%Y-%m-%d")  #日期时间对象转字符串
                #发送消息
                await qd.send(MessageSegment.image(draw_qd(nickname,spike)), at_sender=True)
            else:
                #随机奖励刺儿数量
                if (current_date_str!=prevous_date_str):
                    spike = random.randint(1,100)
                    original_spike = spike
                    num_of_extra_spike = 0
                    if('招财猫' in data[str(user_id)]['item']):
                        num_of_extra_spike = data[user_id]['item']['招财猫'] * 3
                        spike += num_of_extra_spike
                    data[str(user_id)]['spike'] += spike  #刷新刺儿数量
                    data[str(user_id)]['date'] = current_date.strftime("%Y-%m-%d")  #刷新日期，日期时间对象转字符串
                    #发送信息
                    await qd.send(MessageSegment.image(draw_qd(nickname,original_spike,num_of_extra_spike)), at_sender=True)
                else:
                    await qd.send("一天只能签到一次吧......")
        else:
            #提醒用户去注册账号
            await qd.send("你还没尝试抓过kid.....")

        #写入刺儿数量
        with open(user_path / file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    else:
        await qd.send("你还没尝试抓过kid.....", at_sender=True)

##查看余额
ck = on_fullmatch('ck', permission=GROUP, priority=1, block=True)
@ck.handle()
async def cha_spike(event: Event):
    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    #读取刺儿水昂
    user_id = event.get_user_id()
    if(str(user_id) in data):
        spike = data.get(str(user_id)).get('spike', 0)
        await qd.send("你还剩"+f"{spike}刺儿", at_sender=True)
    else:
        await ck.send("你还没尝试抓过kid.....", at_sender=True)

#查看kid库存
mykid = on_fullmatch('mykid lc1', permission=GROUP, priority=1, block=True)
@mykid.handle()
async def mykid_handle(bot:Bot, event: GroupMessageEvent):
    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    user_id = event.get_user_id()

    if(str(user_id) in data):

        #查看当前时间时，分，秒
        current_time = datetime.datetime.now().time()
        hour = current_time.hour
        minute = current_time.minute
        second = current_time.second

        #隐藏内容：半夜0点整查看库存会出现隐藏
        if(hour==0 and minute==0 and second>=0 and second<=30):
            msg_list = []
            msg_list.append(
                {
                    "type": "node",
                    "data":{
                        "name": "库存查询室",
                        "uin": event.self_id,
                        "content": 'please give me your eyes'
                    }
                }
            )
            await bot.call_api("send_group_forward_msg", group_id = event.group_id, messages = msg_list)
            #到此为止......
            return

        #读取拥有kid和kid个数并另外存储
        text_arr = ["", "", "", "", ""]  #创建空字典
        level_str = ["一", "二", "三", "四", "五"]
        for k, v in data[str(user_id)].items():
            if(not k in other):
                nums = find_kid_single_lc(k.lower(), '1')
                if(nums!=0):
                    level = int(nums[0])
                    #根据等级进行添加
                    for i in range(5):
                        if(level==i+1):
                            if(text_arr[i]==""): text_arr[i] += f"{level_str[i]}级：\n"
                            text_arr[i] += f"{v}个{k}\n"

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

#展示Kid
zs = on_command('zs ', permission=GROUP, priority=1, block=True)
@zs.handle()
async def zhanshi(event: Event, arg: Message = CommandArg()):
    level = 0
    number = 0
    #获取输入的名字
    name = str(arg).lower()
    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    #查找Kid
    user_id = event.get_user_id()
    #查找该名字的Kid的图像文件坐标
    nums = find_kid(name)
    if(nums==0): return
    #打开应该查询的表
    data2 = {}
    data3 = {}
    if(nums[2]=='2'):
        with open(user_path / f"UserList{nums[2]}.json", 'r', encoding='utf-8') as f:
            data2 = json.load(f)
    if(nums[2]=='3'):
        with open(user_path / f"UserList{nums[2]}.json", 'r', encoding='utf-8') as f:
            data3 = json.load(f)

    #进入表中进行查询
    if(str(user_id) in data):
        if(nums[2]=='1'):
            if(name in data[str(user_id)] and (not name in other)):
                #根据等级确定坐标
                level = int(nums[0])
                number = int(nums[1])

                kid = print_zhua(level,number,'1')
                img         = kid[2]
                description = kid[3]

                #发送图片
                await zs.finish(MessageSegment.image(img) + description, at_sender=True)
            else:
                await zs.finish(f"你还没抓到过{name}", at_sender=True)
        elif(nums[2]=='2'):
            if(str(user_id) in data2):
                if((nums[0]+'_'+nums[1]) in data2[str(user_id)]):
                    #根据等级确定坐标
                    level = int(nums[0])
                    number = int(nums[1])

                    kid = print_zhua(level,number,nums[2])
                    img         = kid[2]
                    description = kid[3]

                    #发送图片
                    await zs.finish(MessageSegment.image(img) + description, at_sender=True)
                else:
                    await zs.finish(f"你还没抓到过{name}", at_sender=True)
            else:
                await zs.finish(f"你还没抓到过{name}", at_sender=True)
        elif(nums[2]=='3'):
            if(str(user_id) in data3):
                if((nums[0]+'_'+nums[1]) in data3[str(user_id)]):
                    #根据等级确定坐标
                    level = int(nums[0])
                    number = int(nums[1])

                    kid = print_zhua(level,number,nums[2])
                    img         = kid[2]
                    description = kid[3]

                    #发送图片
                    await zs.finish(MessageSegment.image(img) + description, at_sender=True)
                else:
                    await zs.finish(f"你还没抓到过{name}", at_sender=True)
            else:
                await zs.finish(f"你还没抓到过{name}", at_sender=True)

    else:
        await zs.finish("你还没尝试抓过kid.....")

#查看某Kid数量
cknum = on_command('ck', permission=GROUP, priority=1, block=True)
@cknum.handle()
async def cha_kid_number(event: Event, arg: Message = CommandArg()):
    number = 0
    #获取输入的名字
    name = str(arg).lower()
    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    #查找该名字的Kid的图像文件坐标
    nums = find_kid(name)
    if(nums==0): return
    #打开应该查询的表
    data2 = {}
    data3 = {}
    if(nums[2]=='2'):
        with open(user_path / f"UserList{nums[2]}.json", 'r', encoding='utf-8') as f:
            data2 = json.load(f)
    if(nums[2]=='3'):
        with open(user_path / f"UserList{nums[2]}.json", 'r', encoding='utf-8') as f:
            data3 = json.load(f)

    user_id = event.get_user_id()
    if(str(user_id) in data):
        #查看Kid数量
        if(nums[2]=='1'):
            if(name in data[str(user_id)] and (not name in other)):
                number = data[str(user_id)][name]
                await cknum.finish(f"你有{str(number)}个{name}", at_sender=True)
            else:
                await cknum.send(f"你还没抓到过{name}", at_sender=True)
        elif(nums[2]=='2'):
            if(str(user_id) in data2):
                if((nums[0]+'_'+nums[1]) in data2[str(user_id)]):
                    number = data2[str(user_id)][nums[0]+'_'+nums[1]]
                    await cknum.finish(f"你有{str(number)}个{name}", at_sender=True)
                else:
                    await cknum.finish(f"你还没抓到过{name}", at_sender=True)
            else:
                await cknum.finish(f"你还没抓到过{name}", at_sender=True)
        elif(nums[2]=='3'):
            if(str(user_id) in data3):
                if((nums[0]+'_'+nums[1]) in data3[str(user_id)]):
                    number = data3[str(user_id)][nums[0]+'_'+nums[1]]
                    await cknum.finish(f"你有{str(number)}个{name}", at_sender=True)
                else:
                    await cknum.finish(f"你还没抓到过{name}", at_sender=True)
            else:
                await cknum.finish(f"你还没抓到过{name}", at_sender=True)

    else:
        await cknum.finish("你还没尝试抓过kid.....")

#查看Kid进度
jd = on_fullmatch('kidjd', permission=GROUP, priority=1, block=True)
@jd.handle()
async def zhuajd(event: Event):
    user_id = event.get_user_id()

    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    data2 = {}
    with open(user_path / f"UserList2.json", 'r', encoding='utf-8') as f:
        data2 = json.load(f)

    #计数
    count = [0, 0, 0, 0, 0] #抓的数量
    max   = [0, 0, 0, 0, 0] #总数

    jindu = 0  #抓的进度
    maxjindu = 0  #总进度

    #计算总数
    for k, v in kid_name_list.items():
        max[int(k)-1] = len(v)

    for k, v in kid_name_list2.items():
        max[int(k)-1] += len(v)
    
    for k, v in kid_name_list3.items():
        max[int(k)-1] += len(v)


    #计算收集数
    if(str(user_id) in data):
        #一号猎场进度
        for k, v in kid_name_list.items():
            #收集数
            for name in v:
                for j in data[str(user_id)]:
                    if(name.lower()==j.lower()):
                        count[int(k)-1] += 1
                        jindu += int(k)

        #二号猎场及其以后进度
        for lc in range(2, 4):
            #打开文件
            with open(user_path / f"UserList{lc}.json", 'r', encoding='utf-8') as f:
                data2 = json.load(f)
            #计入进度
            if(str(user_id) in data2):
                for k in data2[str(user_id)].keys():
                    level = k[0]
                    count[int(level)-1] += 1
                    jindu += int(level)

        #计算总进度
        maxjindu = max[0]+2*max[1]+3*max[2]+4*max[3]+5*max[4]
        jindu = int(jindu/maxjindu*10000)/100

        #发送消息
        await jd.send(f"\n进度：{jindu}%\n\n"+
                      f"五级KID：{count[4]}/{max[4]}\n\n"+
                      f"四级KID：{count[3]}/{max[3]}\n\n"+
                      f"三级KID：{count[2]}/{max[2]}\n\n"+
                      f"二级KID：{count[1]}/{max[1]}\n\n"+
                      f"一级KID：{count[0]}/{max[0]}", at_sender = True)
    else:
        await jd.finish("你还没尝试抓过kid.....")

#商店商品查看
shop = on_fullmatch('shop', permission=GROUP, priority=1, block=True)
@shop.handle()
async def kid_shop(bot: Bot, event: Event):
    logger.info("商店系统开启成功")  #日志

    shop_data = {}
    #比较营业时间与时间点
    current_time = datetime.datetime.now().time()
    hour = current_time.hour
    if(hour < 7): await shop.finish("便利店还没开门，请再等一会吧")
    if(hour >= 23): await shop.finish("便利店已经打烊了，明天再来吧")
    #输出商店仓库
    current_date = datetime.date.today()  #返回今天日期
    current_date_str = current_date.strftime("%Y-%m-%d")  #日期时间对象转字符串
    if(os.path.exists(shop_database)):

        #打开商店仓库
        with open(shop_database, 'r', encoding='utf-8') as f:
            shop_data = json.load(f)

        #根据是否为同一天来查看是否刷新商品
        previous_date_str = shop_data["date"]

        if (previous_date_str!=current_date_str):
            shop_data["item"] = today_item
            shop_data["date"] = current_date_str

        #写入商店库存
        with open(shop_database, 'w', encoding='utf-8') as f:
            json.dump(shop_data, f, indent=4)

    else:
        shop_data["item"] = today_item
        shop_data["date"] = current_date_str
        
        #写入商店库存
        with open(shop_database, 'w', encoding='utf-8') as f:
            json.dump(shop_data, f, indent=4)
    # 创建转发消息内容
    item_text = shop_list(shop_data["item"])
    forward_messages = [
        {
            "type": "node",
            "data": {
                "name": "商店图片",
                "uin": event.self_id,  # 设置为机器人的QQ号
                "content": MessageSegment.image(shop_work_img)  # 这里可以放入商店相关图片
            }
        },
        {
            "type": "node",
            "data": {
                "name": "商品列表",
                "uin": event.self_id,  # 设置为机器人的QQ号
                "content": item_text
            }
        }
    ]
        
    # 转发消息
    if forward_messages:
        await bot.send_forward_msg(
            group_id=event.group_id,  # 转发到当前群组
            messages=forward_messages
        )

#购买商品
buy = on_command('buy', permission=GROUP, priority=1, block=True)
@buy.handle()
async def buy_handle(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    #打开文件
    #比较营业时间与时间点
    current_time = datetime.datetime.now().time()
    hour = current_time.hour
    if(hour < 7): await buy.finish("便利店还没开门，请再等一会吧")
    if(hour > 22): await buy.finish("便利店已经打烊了，明天再来吧")

    ######若在营业时间内则继续######

    shop_data = {}
    
    current_date = datetime.date.today()  #返回今天日期
    current_date_str = current_date.strftime("%Y-%m-%d")  #日期时间对象转字符串
    if(os.path.exists(shop_database)):

        #读取商店仓库信息
        with open(shop_database, 'r', encoding='utf-8') as f:
            shop_data = json.load(f)
        
        #根据是否为同一天来查看是否刷新商品
        previous_date_str = shop_data["date"]

        if (previous_date_str!=current_date_str):
            shop_data["item"] = today_item
            shop_data["date"] = current_date_str

    else:
        shop_data["item"] = today_item
        shop_data["date"] = current_date_str
    
    #商店与用户的交互
    data = {}
    user_id = event.get_user_id()
    #读取用户信息
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if(str(user_id) in data):

        #一些啥都干不了的buff
        if(data[str(user_id)].get('buff')=='lost'): return

        #获取购买指令参数
        text = str(arg)
        #解析购买参数
        buy_arg = decode_buy_text(today_item, text)
        #正式购买
        if(buy_arg!=None):
            n = int(buy_arg[0])  #买的数量
            buy_item_name = buy_arg[1]  #买的商品的名字

            #输入负数则失败：你在搞笑呢？
            if(n <= 0):
                await buy.finish(f"你在搞笑呢？买{str(n)}个是什么意思？")

            if(shop_data["item"][buy_item_name]==0):
                await buy.finish(f"来晚啦，{buy_item_name}已经售空啦！")

            if(shop_data["item"][buy_item_name] - n >= 0):
                pay_per = item[buy_item_name][0]  #查看物品单价
                pay = n * pay_per  #本次需要支付多少
                #给于商品
                if(data[str(user_id)]['spike'] >= pay):
                    #消耗刺儿
                    data[str(user_id)]['spike'] -= pay

                    ####道具栏添加道具###

                    #判断是否开辟道具栏
                    if(not 'item' in data[str(user_id)]):
                        data[str(user_id)]['item'] = {}

                    #判断是否有开辟该道具
                    if(not buy_item_name in data[str(user_id)]['item']):
                        data[str(user_id)]['item'][buy_item_name] = 0

                    data[str(user_id)]['item'][buy_item_name] += n  #计数
                    if buy_item_name=='指南针':
                        if(data[str(user_id)]['item'][buy_item_name] > 1):
                            await buy.finish("该道具已经到达数量上限啦，不能再买了！")
                    elif buy_item_name=='kid充能器':
                        if(data[str(user_id)]['item'][buy_item_name] > 1):
                            await buy.finish("该道具已经到达数量上限啦，不能再买了！")
                    elif buy_item_name=='时间提取器':
                        if(data[str(user_id)]['item'][buy_item_name] > 1):
                            await buy.finish("该道具已经到达数量上限啦，不能再买了！")
                    elif buy_item_name=='刺儿加工器':
                        if(data[str(user_id)]['item'][buy_item_name] > 1):
                            await buy.finish("该道具已经到达数量上限啦，不能再买了！")
                    elif buy_item_name=='招财猫':
                        if(data[str(user_id)]['item'][buy_item_name] > 20):
                            await buy.finish("该道具已经到达数量上限啦，不能再买了！")
                    elif buy_item_name=='神秘碎片':
                        current_fragments = data[str(user_id)].get("buy_fragments_num", 0)
                        num_of_fragments = data[str(user_id)].get("buy_fragments_num", 0) +n
                        text = str(current_fragments)
                        if (num_of_fragments > 7):
                            await buy.finish(f"你不能买这么多，该道具终身限购7个，你已经购买了{text}个")
                        else:
                            if (not 'buy_fragments_num' in data[str(user_id)]):
                                data[str(user_id)]['buy_fragments_num'] = 0
                            data[str(user_id)]['buy_fragments_num'] += n
                        if(data[str(user_id)]['item'][buy_item_name] > 7):
                            await buy.finish("该道具已经到达数量上限(7个)或者购买后到达数量上限，不能再买了！")

                    #商店库存减少道具
                    shop_data["item"][buy_item_name] -= n

                    #写入用户文件
                    with open(user_path / file_name, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)

                    #写入商店查询账单
                    today = datetime.date.today().strftime("%Y-%m-%d")
                    bili = Path()/"data"/"Shop"/f"{today}.json"
                    if(os.path.exists(bili)):
                        data_bili = {}
                        #读入存在的账单文件
                        with open(bili, 'r', encoding='utf-8') as f:
                            data_bili = json.load(f)

                        data_bili['list'].append(f"{event.sender.nickname}购买了{n}个{buy_item_name}")                  

                        #保存账单文件
                        with open(bili, 'w', encoding='utf-8') as f:
                            json.dump(data_bili, f, indent=4)

                    else:
                        data_bili = {}
                        data_bili['list'] = []

                        data_bili['list'].append(f"{event.sender.nickname}购买了{n}个{buy_item_name}")             

                        #保存账单文件
                        with open(bili, 'w', encoding='utf-8') as f:
                            json.dump(data_bili, f, indent=4)

                    #写入商店库存文件
                    with open(shop_database, 'w', encoding='utf-8') as f:
                        json.dump(shop_data, f, indent=4)       
                    
                    #发送消息
                    await buy.send(f"购买成功！你还剩{str(data[str(user_id)]['spike'])}刺儿", at_sender=True)
                else:
                    await buy.send(f"本次你需要花费{str(pay)}刺儿，你只有{str(data[str(user_id)]['spike'])}刺儿", at_sender=True)
            else:
                await buy.send(f"没有呢么多{buy_item_name}了......", at_sender=True)
        else:
            await buy.send("请检查购买指令参数~")
    else:
        await buy.finish("你还没尝试抓过kid.....")

#祈愿功能，用于小号能量以换取kid，必须持有kid充能器
pray = on_command('祈愿', permission=GROUP, priority=1, block=True)
@pray.handle()
async def pray_handle(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    data = {}
    user_id = event.get_user_id()
    #读取用户信息
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if (not 'buff' in data[str(user_id)]):
        data[str(user_id)].get('buff')=='normal'
    #一些啥都干不了的buff
    if(data[str(user_id)].get('buff')=='lost'): return
    if(data[str(user_id)].get('buff')=='confuse'): return

    #如果受伤了则无法祈愿
    if(data[str(user_id)].get("buff")=="hurt"): 
        #一些额外操作：如果还没过下次时间，计算与下次的时间间隔，如果过了，可以使用道具
        current_time = datetime.datetime.now()
        next_time_r = datetime.datetime.strptime(data.get(str(user_id)).get('next_time'), "%Y-%m-%d %H:%M:%S")
        if(current_time < next_time_r):
            delta_time = next_time_r - current_time
            await pray.finish(f"你受伤了，需要等{time_text(delta_time)}才能继续")
        else:
            data[str(user_id)]["buff"] = "normal"

    #是否在加工状态

    #防止没有status这个键
    if ('status' in data[str(user_id)]):
        status = data[str(user_id)].get('status')
    else:
        status = 'normal'

    if(status =='working'): 
        current_time = datetime.datetime.now()
        #如果没有就写入，虽说这段代码完全不可能发生
        if(not 'work_end_time' in data[str(user_id)]):
            data[str(user_id)]['work_end_time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")

        work_end_time = datetime.datetime.strptime(data.get(str(user_id)).get('work_end_time'), "%Y-%m-%d %H:%M:%S")
        if current_time < work_end_time:
            text = time_text(str(work_end_time-current_time))
            await pray.finish(f"你还在加工饰品，还需要{text}", at_sender=True)
        #时间过了自动恢复正常
        else:
            data[str(user_id)]['status'] = 'normal'
            with open(user_path / file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
    
    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_id = event.get_user_id()

    #先检测有没有道具列表
    #判断是否开辟道具栏
    if(not 'item' in data[str(user_id)]):
        data[str(user_id)]['item'] = {}
    #检查是否有充能器
    if(data[str(user_id)].get("item").get('kid充能器', 0) > 0):
        current_time = datetime.datetime.now()
        energy = data[str(user_id)].get("energy")
        try:
            energy = int(energy)
        except:
            energy = 0
        try:
            next_time = datetime.datetime.strptime(data.get(str(user_id)).get('next_time'), "%Y-%m-%d %H:%M:%S")
        except:
            next_time = current_time
        #检查祈愿cd是否已到
        if current_time >= next_time:
            #查看能量有没有600
            if energy >= 600:
                liechang_number = data[str(user_id)].get('lc')
                #未解锁三猎场抓不了
                if liechang_number=='3':
                        if data[str(user_id)].get("item").get('神秘碎片', 0) < 7:
                            await pray.finish("你还未解锁通往第三猎场的道路...", at_sender=True)
                
                information = zhua_random(120, 360, 900, 999, liechang_number=liechang_number)
                data[str(user_id)]["energy"] -= 600
                #把冷却cd加上
                next_time_r = current_time + datetime.timedelta(minutes=30)
                data[str(user_id)]['next_time'] = next_time_r.strftime("%Y-%m-%d %H:%M:%S")
                new_print = ""
                #得到Kid信息
                level       = information[0]   #等级
                name        = information[1]   #名字
                img         = information[2]   #图片
                description = information[3]   #描述
                num         = information[4]   #编号
                lc          = information[5]   #所属猎场
 
                #打开副表
                data2 = {}
                if(lc!='1'):
                    with open(user_path / f"UserList{lc}.json", 'r', encoding='utf-8') as f:
                        data2 = json.load(f)

                #计数
                if(lc=='1'):
                    if(not name in data[str(user_id)]):
                        new_print = "\n恭喜你抓出来一个新kid！\n"  #如果出新就添加文本
                        data[str(user_id)][name] = 0                   
                    data[str(user_id)][name] += 1
                else:
                    if(str(user_id) in data2):
                        if(not (str(level)+'_'+str(num)) in data2[str(user_id)]):
                            new_print = "\n恭喜你抓出来一个新kid！\n"  #如果出新就添加文本
                            data2[str(user_id)][str(level)+'_'+str(num)] = 0
                        data2[str(user_id)][str(level)+'_'+str(num)] += 1  #数量+1
                    else:
                        new_print = "\n恭喜你抓出来一个新kid！\n"  #如果出新就添加文本
                        data2[str(user_id)] = {}
                        data2[str(user_id)][str(level)+'_'+str(num)] = 1              

                #写入副表
                if(lc!='1'):
                    with open(user_path / f"UserList{lc}.json", 'w', encoding='utf-8') as f:
                        json.dump(data2, f, indent=4)                  

                #写入文件
                with open(user_path / file_name, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                #发送消息
                await pray.send(new_print+
                                 f'\n等级: {level}\n'+
                                f'{name}'+
                                MessageSegment.image(img)+
                                f'{description}',
                                at_sender = True)
            else:
                text = str(energy)
                await pray.finish(f"你的能量只有{text}，不足600，无法祈愿...")
        else:
            text = time_text(str(next_time-current_time))
            await daoju.finish(f"请{text}后再来祈愿吧~", at_sender=True)
    else:
        await pray.finish("你还没有kid充能器，无法祈愿...")

#使用道具，整个抓Kid里最繁琐的函数，且会持续更新
daoju = on_command('use', permission=GROUP, priority=1, block=True)
@daoju.handle()
async def daoju_handle(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_id = event.get_user_id()
    if(str(user_id) in data):

        #假如在0号猎场
        liechang_number = data[str(user_id)].get('lc')
        if(liechang_number=='0'): 
            await daoju.finish("0号猎场还没法使用道具哦~~后续将推出0号猎场特有的道具系统~")

        if("item" in data[str(user_id)]):
            use_item_name = str(arg)  #获取使用道具名称
            success = 0  #0代表没有效果，1代表成功，2代表失败
            fail_text = "失败！"   #失败文本

            if(use_item_name=="时间秒表"):
                if(data.get(user_id).get('item').get('时间秒表',0) > 0):
                    current_time = datetime.datetime.now()
                    next_time_r = datetime.datetime.strptime(data.get(str(user_id)).get('next_time'), "%Y-%m-%d %H:%M:%S")
                    try:
                        work_end_time_r = datetime.datetime.strptime(data.get(str(user_id)).get('work_end_time'), "%Y-%m-%d %H:%M:%S")
                    except:
                        work_end_time_r = current_time
                    #首先判断有没有冷却
                    if(current_time < next_time_r or current_time < work_end_time_r):
                        next_time = get_time_from_data(data[str(user_id)])
                        try:
                            next_clock_time = datetime.datetime.strptime(data.get(str(user_id)).get('next_clock_time'), "%Y-%m-%d %H:%M:%S")
                        except:
                            next_clock_time = current_time
                        #然后判断是否能使用秒表
                        if current_time >= next_clock_time:
                            data[str(user_id)]["item"][use_item_name] -= 1 
                            #清除全部冷却时长
                            next_time_r = current_time + datetime.timedelta(seconds=1)
                            next_clock_time_r = current_time + datetime.timedelta(minutes=30)
                            data[str(user_id)]['next_time'] = next_time_r.strftime("%Y-%m-%d %H:%M:%S")
                            data[str(user_id)]['next_charge_time'] = next_time_r.strftime("%Y-%m-%d %H:%M:%S")
                            data[str(user_id)]['work_end_time'] = next_time_r.strftime("%Y-%m-%d %H:%M:%S")
                            data[str(user_id)]['next_clock_time'] = next_clock_time_r.strftime("%Y-%m-%d %H:%M:%S")
                            if(data[str(user_id)]["item"].get(use_item_name)<=0): del data[str(user_id)]["item"][use_item_name]
                            #写入文件
                            with open(user_path / file_name, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=4)
                            await daoju.finish("使用成功，冷却被全部清除了！", at_sender=True)
                        else:
                            text = time_text(str(next_clock_time-current_time))
                            await daoju.finish(f"不久前使用的时间秒表似乎使你所有的秒表都停止运转了。请{text}后再尝试使用", at_sender=True)
                    else:
                        await daoju.finish("你现在没有冷却呀，无需使用此道具", at_sender=True)
                else:
                    await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)

            #一些啥都干不了的buff
            if ('status' in data[str(user_id)]):
                status = data[str(user_id)].get('status')
            else:
                status = 'normal'

            if(data[str(user_id)].get('buff')=='lost'): return
            elif(data[str(user_id)].get('buff')=='confuse'): return

            #刺儿饰品的使用判定，要写在加工物品的判定之前
            #两个参数的指令(判定于是否加工之前)
            cmd_sell = use_item_name.split("/")
            use_name = cmd_sell[0]   #参数1
            if(use_name.lower()=="刺儿饰品"):
                #可以不输入售卖数量
                try:
                    num_of_sell = cmd_sell[1]   #参数2
                except:
                    num_of_sell = 1

                #判定是否是整数
                try:
                    num_of_sell = int(num_of_sell)
                except:
                    await daoju.finish("请输入一个正确的整数", at_sender=True)
                
                #判定是否是非正数
                if (num_of_sell <= 0):
                    await daoju.finish(f"你为什么会想售卖{str(num_of_sell)}个饰品呢？别想卡bug了！", at_sender=True)
                    
                if(data[str(user_id)].get("item").get(use_name, 0) >= num_of_sell):
                    price_total=0
                    for _ in range(num_of_sell):
                        spike = random.randint(228,265)
                        price_total += spike
                    data[user_id]['spike'] += price_total
                    data[str(user_id)]["item"][use_name] -= num_of_sell
                    if(data[str(user_id)]["item"].get(use_name)<=0): del data[str(user_id)]["item"][use_name]
                    #写入文件
                    with open(user_path / file_name, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)
                    await daoju.finish(f"恭喜！{str(num_of_sell)}个小饰品卖出了{str(price_total)}刺儿！", at_sender=True)
                else:
                    await daoju.finish(f"你现在没有这么多{use_name}", at_sender=True)
                
            #加工饰品时无法使用道具
            if(status =='working'): 
                current_time = datetime.datetime.now()
                work_end_time = datetime.datetime.strptime(data.get(str(user_id)).get('work_end_time'), "%Y-%m-%d %H:%M:%S")
                if current_time < work_end_time:
                    text = time_text(str(work_end_time-current_time))
                    await daoju.finish(f"你还在加工饰品，还需要{text}", at_sender=True)
                #时间过了自动恢复正常
                else:
                    data[str(user_id)]['status'] = 'normal'
                    with open(user_path / file_name, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)

            #如果受伤了则无法使用道具(时间秒表除外)
            if(data[str(user_id)].get("buff")=="hurt"): 
                #一些额外操作：如果还没过下次时间，计算与下次的时间间隔，如果过了，可以使用道具
                current_time = datetime.datetime.now()
                next_time_r = datetime.datetime.strptime(data.get(str(user_id)).get('next_time'), "%Y-%m-%d %H:%M:%S")
                if(current_time < next_time_r):
                    delta_time = next_time_r - current_time
                    await daoju.finish(f"你受伤了，需要等{time_text(delta_time)}才能继续")
                else:
                    data[str(user_id)]["buff"] = "normal"

            #道具功能列表
            if(use_item_name=="万能解药"):
                if(data[str(user_id)].get("item").get(use_item_name, 0) > 0):

                    """
                    万能解药：解除不良状态
                    """
                    try:
                        debuff = data[str(user_id)].get("debuff")
                    except:
                        debuff = 'normal'
                        data[str(user_id)]["debuff"] = "normal"
                        with open(user_path / file_name, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=4)

                    if(debuff!="normal"):
                        data[str(user_id)]["debuff"] = "normal"
                        current_time = datetime.datetime.now()
                        data[user_id]['next_recover_time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
                        #写入文件
                        data[str(user_id)]["item"][use_item_name] -= 1 
                        with open(user_path / file_name, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=4)
                        await daoju.finish(f"不良状态已清除", at_sender=True)    
                    else:
                        await daoju.finish(f"你现在没有不良状态", at_sender=True)               
                else:
                    await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)
            
            
            #debuff清除逻辑(使用其他抓kid道具前判定)
            current_time = datetime.datetime.now()
            if(not 'next_recover_time' in data[str(user_id)]):
                data[str(user_id)]['next_recover_time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
                with open(user_path / file_name, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)

            recover_time = datetime.datetime.strptime(data.get(str(user_id)).get('next_recover_time'), "%Y-%m-%d %H:%M:%S")
            if recover_time <= current_time:
                data[str(user_id)]["debuff"] = "normal"
                with open(user_path / file_name, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)

            if(use_item_name=="胡萝卜"):
                if(data[str(user_id)].get("item").get(use_item_name, 0) > 0):

                    """
                    胡萝卜：打破cd额外抓一次，使用的时候有50%的概率抓出兔类Kid,
                    也有50%概率正常抓取
                    """

                    #随机选择是正常抓取还是从兔类Kid里抓
                    if liechang_number=='3':
                        if data[user_id]['item'].get('神秘碎片',0) < 7:
                            await daoju.finish("你还未解锁通往第三猎场的道路...", at_sender=True)   
                    rnd = random.randint(1,10)
                    if(rnd <= 5):
                        #从兔类里抓
                        weights = {
                            3: 35,  # 3级的概率为35%
                            4: 45,  # 4级的概率为45%
                            5: 15   # 5级的概率为15%
                        }
                        weighted_choices = []
                        for level, weight in weights.items():
                            weighted_choices.extend([level] * weight)
                        chosen_level = random.choice(weighted_choices)
                        if liechang_number=='1':
                            rabbit = [rabbit for rabbit in rabbit_kid1 if rabbit[0] == chosen_level]
                        elif liechang_number=='2':
                            rabbit = [rabbit for rabbit in rabbit_kid2 if rabbit[0] == chosen_level]
                        elif liechang_number=='3':
                            rabbit = [rabbit for rabbit in rabbit_kid3 if rabbit[0] == chosen_level]
                        else:
                            raise KeyError('Not a valid lc number')
                        #rabbit = eval(f"rabbit_kid{liechang_number}")

                        rabbit_rnd = random.randint(0, len(rabbit)-1)  #随机选择一个
                        information = print_zhua(rabbit[rabbit_rnd][0], rabbit[rabbit_rnd][1], liechang_number)
                        success = 1
                    else:
                        #正常抓取
                        information = zhua_random(30, 150, 600, 850, liechang_number=data[str(user_id)]['lc'])
                        success = 1
                    data[str(user_id)]["item"][use_item_name] -= 1                
                else:
                    await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)
            if(use_item_name=="弹弓"):
                """
                没啥特殊的，只是额外正常地再抓一次
                """
                if(data[str(user_id)].get("item").get(use_item_name, 0) > 0):
                    if liechang_number=='3':
                        if data[str(user_id)].get("item").get('神秘碎片', 0) < 7:
                            await daoju.finish("你还未解锁通往第三猎场的道路...", at_sender=True)
                    information = zhua_random(liechang_number=liechang_number)
                    data[str(user_id)]["item"][use_item_name] -= 1
                    success = 1  
                else:
                    await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)
            if(use_item_name=="一次性小手枪"):
                if(data[str(user_id)].get("item").get(use_item_name, 0) > 0):
                    """
                    没啥特殊的，只是额外正常地再抓一次
                    """
                    if liechang_number=='3':
                        if data[str(user_id)].get("item").get('神秘碎片', 0) < 7:
                            await daoju.finish("你还未解锁通往第三猎场的道路...", at_sender=True)
                    information = zhua_random(20, 100, 500, 800, liechang_number=liechang_number)
                    data[str(user_id)]["item"][use_item_name] -= 1
                    success = 1 
                else:
                    await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)
            if(use_item_name=="幸运药水"):
                """
                提升运气的小道具，虽说不知道有没有真的提升...
                """
                if(data[str(user_id)].get("item").get(use_item_name, 0) > 0):
                    #确保自身没有幸运状态
                    if data[str(user_id)].get('buff2')!='lucky':
                        if liechang_number=='3':
                            if data[str(user_id)].get("item").get('神秘碎片', 0) < 7:
                                await daoju.finish("你还未解锁通往第三猎场的道路...", at_sender=True)
                        data[str(user_id)]["buff2"]='lucky'
                        data[str(user_id)]["lucky_times"] = 21
                        data[str(user_id)]["item"][use_item_name] -= 1
                        #写入文件
                        with open(user_path / file_name, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=4)
                        await daoju.finish("使用成功，现在正常抓kid可额外获得15刺儿，持续20次。", at_sender=True)
                    else:
                        await daoju.finish("你已经有幸运buff了~", at_sender=True)
                else:
                    await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)
            if(use_item_name=="赌徒之眼"):
                """
                在进du局前使用这个道具可以查看该局是否有人想狙你的某个kid
                """

                #没有这个道具
                if(data[str(user_id)].get("item").get(use_item_name, 0) == 0):
                    await daoju.finish(f"你现在没有{use_item_name}")

                #先查看当前为哪个赌场
                data_du = {}
                with open(duchang_list, 'r', encoding='utf-8') as f:
                    data_du = json.load(f)
    
                group = event.group_id
                if(not str(group) in data_du):
                    await daoju.finish("当前还没有du局哦~~~", at_sender=True)

                liechang_number = data_du[str(group)]['lc']

                #是否已经在du局中
                if(str(user_id) in data_du[str(group)]['member']):
                    await daoju.finish("你脑子是不是坏掉了，这个道具不应该在进du场前用吗？", at_sender=True)
                
                data[str(user_id)]["item"][use_item_name] -= 1
                #写入文件
                with open(user_path / file_name, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)

                if(liechang_number=='1'):
                    for k in data_du[str(group)]['want']:
                        if(k in data[str(user_id)]):
                            await daoju.finish(f"你的{k}面临被掠夺的风险.....", at_sender=True)
                    await daoju.finish("当前du局非常安全，你可以放心进入", at_sender=True)
                else:
                    data2 = {}
                    with open(user_path / f"UserList{liechang_number}.json", 'r', encoding='utf-8') as f:
                        data2 = json.load(f)
                    for k in data_du[str(group)]['want']:
                        if(data2[str(user_id)].get(k,0)>0):
                            k = k.split('_')
                            name = eval(f"kid_data{liechang_number}.get(k[0]).get(k[1]).get('name')")
                            await daoju.finish(f"你的{name}面临被掠夺的风险.....", at_sender=True)
                    await daoju.finish("当前du局非常安全，你可以放心进入", at_sender=True)                 
            if(use_item_name=="时间提取器"):
                if(data.get(user_id).get('item').get('时间提取器',0) > 0):
                    if liechang_number=='3':
                        if data[str(user_id)].get("item").get('神秘碎片', 0) < 7:
                            await daoju.finish("你还未解锁通往第三猎场的道路...", at_sender=True)
                    next_time = get_time_from_data(data[str(user_id)])
                    current_time = datetime.datetime.now()
                    #没到下一次抓的时间
                    if(current_time < next_time):
                        text = time_text(str(next_time-current_time))
                        await daoju.finish(f"别抓啦，{text}后再来吧", at_sender = True)
                    
                    #延长下次抓的cd
                    if(user_id!=bot_owner_id):
                        next_time = current_time + datetime.timedelta(minutes=60)
                        data[str(user_id)]['next_time'] = time_decode(next_time)
                    #zhuakid并增加爆率
                    information = zhua_random(50,200,500,999,liechang_number=liechang_number)
                    success = 1
                else:
                    await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)

            #两个参数的指令
            command = use_item_name.split("/")
            if(len(command)==2):
                use_item_name = command[0]   #参数1
                arg2 = command[1]   #参数2
                if(use_item_name.lower()=="kid提取器"):
                    if(data[str(user_id)].get("item").get(use_item_name, 0) > 0):
                        """
                        隐藏kid和一些隐藏线索
                        """
                        if(arg2.lower()=="kid提取器"):
                            await daoju.finish("---------------------------------------\n" + "滋滋——已截获情报——滋滋——正在启动……启动失败——请输入密码：/password ________\n" + "错误！！错误！！！WARNING！！！\n" + "VGhpc0lzVGhlUGFzc3dvcmQ=")

                        #隐藏kid线索
                        for k in range(len(secret_list)):
                            if(arg2.lower()==secret_list[k][0]):
                                img = kid_level0_path / f"Kid{str(k+1)}.png"
                                description = secret_list[k][1]
                                await daoju.finish("等级：？？？\n" + f"{arg2}\n" + MessageSegment.image(img) + description)

                        """
                        可以提取特定的一个kid，但是等级越高成功概率越低，且若失败了会给与更长的冷却时间
                        """
                        nums = find_kid(arg2.lower())
                        if liechang_number=='3' or nums[2] == "3":
                            if data[str(user_id)].get("item").get('神秘碎片', 0) < 7:
                                await daoju.finish("你还未解锁通往第三猎场的道路...", at_sender=True)
                        if(nums!=0):
                            rnd = random.randint(1,100)
                            if(rnd <= 20+15*(5-int(nums[0]))):
                                success = 1
                                information = print_zhua(int(nums[0]), int(nums[1]), nums[2])
                            else:
                                #受伤，更新下次抓的时间
                                cd_time = random.randint(int(nums[0])*60, int(nums[0])*60+120)
                                current_time = datetime.datetime.now()
                                next_time = current_time + datetime.timedelta(minutes=cd_time)
                                data[str(user_id)]['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
                                data[str(user_id)]["buff"] = "hurt"  #受伤
                                fail_text = f"提取失败！提取器爆炸了，你受伤了，需要休息{str(cd_time)}分钟"  #失败文本
                                success = 2
                            data[str(user_id)]["item"][use_item_name] -= 1
                        else:
                            return 
                    else:
                        await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)
                    
                if(use_item_name=="刺儿加工器"):
                    if(data[str(user_id)].get("item").get(use_item_name, 0) > 0):

                        """
                        刺儿加工器：使用后进入4h道具加工期，期间不能抓kid，不能用道具(但是立刻给饰品)
                        """

                        #首先判定有没有开辟这一栏
                        if (not '刺儿饰品' in data[str(user_id)].get("item")):
                            data[str(user_id)]["item"]['刺儿饰品'] = 0  

                        #首先判定是不是整数
                        try:
                            num = int(arg2)
                        except:
                            await daoju.finish(f"请输入一个1-4之间的整数", at_sender=True)
                        #其次判定是不是1-4之间的
                        if num<1 or num>4:
                            await daoju.finish(f"请输入一个1-4之间的整数", at_sender=True)

                        #依然是不可能的代码，但我还是写上了
                        if(not 'spike' in data[str(user_id)]):
                            data[str(user_id)]['spike'] = 0
                        #检测刺儿数量是否足够
                        if (data[str(user_id)].get('spike', 0) >= 190 * num):
                            data[str(user_id)]['spike'] -= 190 * num
                        else:
                            spike_in_need = str(190 * num)
                            spike_you_have = str(data[str(user_id)].get('spike', 0))
                            await daoju.finish(f"你的刺儿不足，总共需要{spike_in_need}刺儿，你只有{spike_you_have}刺儿", at_sender=True)

                        current_time = datetime.datetime.now()
                        if(not 'work_end_time' in data[str(user_id)]):
                            data[str(user_id)]['work_end_time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
                        data[str(user_id)]["item"]['刺儿饰品'] += num    #直接给饰品
                        work_end_time = current_time + datetime.timedelta(minutes=135*num)
                        data[str(user_id)]['work_end_time'] = time_decode(work_end_time)
                        data[str(user_id)]['status'] = 'working'    
                        if(data[str(user_id)]["item"].get(use_item_name)<=0): del data[str(user_id)]["item"][use_item_name]
                        #写入文件
                        with open(user_path / file_name, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=4)
                        text_time = str(135*num)
                        await daoju.finish(f"使用成功，预计需要加工{text_time}分钟，可获得{str(num)}个刺儿饰品。", at_sender=True)
                    else:
                        await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)
            #三个参数的指令
            command = use_item_name.split("/")
            if (len(command)==3):
                use_item_name = command[0]   #参数1(一般是使用的道具名)
                arg2 = command[1]   #参数2(充能的kid)
                arg3 = command[2]   #参数2(充能的数量)
                if (use_item_name.lower()=="kid充能器"):
                    #首先判定有没有
                    if(data[str(user_id)].get("item").get(use_item_name, 0) > 0):
                        #选中kid
                        nums = find_kid(arg2.lower())
                        #查不到这个kid的档案，终止
                        if(nums==0): 
                            logger.info("因为不存在该kid献祭被中断")
                            return
                        #统计充能个数
                        try:
                            num_of_charge = int(arg3)
                        except:
                            await daoju.finish("请输入一个整数，谢谢。", at_sender=True)
                        #这不能是个负数或零
                        if num_of_charge <= 0:
                            await daoju.finish("我也想这么做，但是不允许。", at_sender=True)
                        #进行充能
                        if(nums[2]=='1'):
                            #一号猎场
                            if(data[str(user_id)].get(arg2.lower(),0) >= num_of_charge):
                                data[str(user_id)][arg2.lower()] -= num_of_charge
                            else:
                                await daoju.finish(f"你没有这么多{arg2.lower()}可以拿来充能了！", at_sender=True)
                        elif(nums[2]=='2'):
                            #二号猎场及其以后，按等级和编号确定
                            data2 = open_data(user_path/f"UserList2.json")
                            level_num = nums[0]+'_'+nums[1]
                            if(data2[str(user_id)].get(level_num,0) >= num_of_charge):
                                data2[str(user_id)][level_num] -= num_of_charge
                                save_data(user_path/f"UserList2.json",data2)
                            else:
                                await daoju.finish(f"你没有这么多{arg2.lower()}可以拿来充能了！", at_sender=True)
                        elif(nums[2]=='3'):
                            data3 = open_data(user_path/f"UserList3.json")
                            level_num = nums[0]+'_'+nums[1]
                            if(data3[str(user_id)].get(level_num,0) >= num_of_charge):
                                data3[str(user_id)][level_num] -= num_of_charge
                                save_data(user_path/f"UserList3.json",data3)
                            else:
                                await daoju.finish(f"你没有这么多{arg2.lower()}可以拿来充能了！", at_sender=True)
                        if nums[0]=='5':
                            energy = 1800
                        elif nums[0]=='4':
                            energy = 600
                        elif nums[0]=='3':
                            energy = 200
                        elif nums[0]=='2':
                            energy = 100
                        elif nums[0]=='1':
                            energy = 60
                        else:
                            raise KeyError("Not an invalid kid level")
                        #尝试加上能量
                        try:
                            data[str(user_id)]["energy"] += num_of_charge * energy
                        except:
                            #否则直接等于
                            data[str(user_id)]["energy"] = num_of_charge * energy
                        #写入文件
                        with open(user_path / file_name, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=4)
                        text = str(num_of_charge * energy)
                        total_energy = str(data[str(user_id)]["energy"])
                        await daoju.finish(f"使用成功，你获得了{text}点能量值，你现在拥有{total_energy}点能量", at_sender=True)
                    else:
                        await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)
            if(use_item_name.lower()=="kid献祭器"):
                if(data[str(user_id)].get("item").get(use_item_name, 0) > 0):
                    data[user_id]['spike'] += 300
                    data[str(user_id)]["item"][use_item_name] -= 1
                    success = 1
                    if(data[str(user_id)]["item"].get(use_item_name)<=0): del data[str(user_id)]["item"][use_item_name]
                    #写入文件
                    with open(user_path / file_name, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)
                    await daoju.finish("使用成功，你获得了300个刺儿", at_sender=True)
                else:
                    await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)
            
            if(use_item_name.lower()=="时间献祭器"):
                if(data[str(user_id)].get("item").get(use_item_name, 0) > 0):
                    data[user_id]['spike'] += 200
                    data[str(user_id)]["item"][use_item_name] -= 1
                    success = 1
                    if(data[str(user_id)]["item"].get(use_item_name)<=0): del data[str(user_id)]["item"][use_item_name]
                    #写入文件
                    with open(user_path / file_name, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)
                    await daoju.finish("使用成功，你获得了200个刺儿", at_sender=True)
                else:
                    await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)
                    
            #使用成功
            if(success==1):
                new_print = ""
                #得到Kid信息
                level       = information[0]   #等级
                name        = information[1]   #名字
                img         = information[2]   #图片
                description = information[3]   #描述
                num         = information[4]   #编号
                lc          = information[5]   #所属猎场
 
                #打开副表
                data2 = {}
                if(lc!='1'):
                    with open(user_path / f"UserList{lc}.json", 'r', encoding='utf-8') as f:
                        data2 = json.load(f)

                #计数
                if(lc=='1'):
                    if(not name in data[str(user_id)]):
                        new_print = "\n恭喜你抓出来一个新kid！\n"  #如果出新就添加文本
                        data[str(user_id)][name] = 0                   
                    data[str(user_id)][name] += 1
                else:
                    if(str(user_id) in data2):
                        if(not (str(level)+'_'+str(num)) in data2[str(user_id)]):
                            new_print = "\n恭喜你抓出来一个新kid！\n"  #如果出新就添加文本
                            data2[str(user_id)][str(level)+'_'+str(num)] = 0
                        data2[str(user_id)][str(level)+'_'+str(num)] += 1  #数量+1
                    else:
                        new_print = "\n恭喜你抓出来一个新kid！\n"  #如果出新就添加文本
                        data2[str(user_id)] = {}
                        data2[str(user_id)][str(level)+'_'+str(num)] = 1             

                #如果道具归0则将该项置空
                if(data[str(user_id)]["item"].get(use_item_name)<=0): del data[str(user_id)]["item"][use_item_name]

                #写入副表
                if(lc=='2'):
                    with open(user_path / f"UserList{lc}.json", 'w', encoding='utf-8') as f:
                        json.dump(data2, f, indent=4)     

                if(lc=='3'):
                    with open(user_path / f"UserList{lc}.json", 'w', encoding='utf-8') as f:
                        json.dump(data3, f, indent=4)                

                #写入文件
                with open(user_path / file_name, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                #发送消息
                await daoju.send(new_print+
                                 f'\n等级: {level}\n'+
                                f'{name}'+
                                MessageSegment.image(img)+
                                f'{description}',
                                at_sender = True)
            #使用失败
            if(success==2):
                #如果道具归0则将该项置空
                if(data[str(user_id)]["item"][use_item_name]==0): del data[str(user_id)]["item"][use_item_name]
                
                #写入文件
                with open(user_path / file_name, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)

                await daoju.finish(fail_text, at_sender=True)

        else:
            await daoju.finish("你还没有任何道具哦", at_sender=True)
    else:
        await daoju.finish("你还没尝试抓过kid.....")

#查看道具信息
ckdj = on_command('item', permission=GROUP, priority=1, block=True)
@ckdj.handle()
async def ckdj_handle(arg: Message = CommandArg()):
    dj_name = str(arg)
    if(dj_name in item):
        await ckdj.finish(dj_name+":\n"+item[dj_name][2])
    
########赌场系统#######

#买刮刮乐
ticket = on_fullmatch('/cp', permission=GROUP, priority=1, block=True)
@ticket.handle()
async def ticket_handle(bot: Bot, event: GroupMessageEvent):

    current_time = datetime.datetime.now().time()
    hour = current_time.hour
    if(hour > 5 and hour < 18): await ticket.finish("棋牌室的门已经关了")

    #打开文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_id = event.get_user_id()

    if(str(user_id) in data):

        #一些啥都干不了的buff
        if(data[str(user_id)].get('buff')=='lost'): return

        if(data[str(user_id)]['spike'] >= 150):
            spike = 0
            rnd = random.randint(1,100)
            if(rnd <= 5): spike = 500
            if(rnd > 5 and rnd <= 15): spike = 300
            if(rnd > 15 and rnd <= 35): spike = 155
            if(rnd > 35 and rnd <= 75): spike = 75
            if(rnd > 75 and rnd <= 100): spike = 35

            data[str(user_id)]['spike'] += (spike - 150)

            #写入文件
            with open(user_path / file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            
            time.sleep(3)   #延时三秒

            await ticket.finish(f"本次刮刮乐你获得{str(spike)}刺儿", at_sender=True)
        else:
            await ticket.finish(f"你没钱买刮刮乐了，你需要150刺儿，你只有{str(data[str(user_id)]['spike'])}刺儿", at_sender=True)
    else:
        await ticket.finish("你还没尝试抓过kid......", at_sender=True)

#5人场赌博
dubo = on_command('du', permission=GROUP, priority=1, block=True)
@dubo.handle()
async def dubo_handle(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):

    person_num = 5  #一局最多人数

    user_id = event.get_user_id()
    group = event.group_id

    current_time = datetime.datetime.now().time()
    hour = current_time.hour
    if(hour > 5 and hour < 18): await dubo.finish("棋牌室的门已经关了")

    #打开用户文件
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    #打开赌场信息文件
    data_du = {}
    with open(duchang_list, 'r', encoding='utf-8') as f:
        data_du = json.load(f)

    if(str(user_id) in data):

        #一些啥都干不了的buff
        if(data[str(user_id)].get('buff')=='lost'): return

        want_kid = str(arg).lower()

        nums = find_kid(want_kid)

        if(nums==0): return

        #如果不是du池里的kid就被踢出
        if(str(group) in data_du):
            if(nums[2]!=data_du[str(group)]['lc']):
                await dubo.finish("当前局du不了这个kid", at_sender=True)       

        #如果赌的不是一号猎场就打开副数据表
        data2 = {}
        data3 = {}
        if(nums[2]=='2'):
            with open(user_path / f"UserList{nums[2]}.json", 'r', encoding='utf-8') as f:
                data2 = json.load(f)

            #没有开通二猎场
            if(not str(user_id) in data2):
                await dubo.finish("你现在du不了这个猎场的kid，请至少拥有该猎场的一个kid", at_sender=True)
        
        if(nums[2]=='3'):
            with open(user_path / f"UserList{nums[2]}.json", 'r', encoding='utf-8') as f:
                data3 = json.load(f)
            
            #没有开通三猎场
            if(not str(user_id) in data3):
                await dubo.finish("你现在du不了这个猎场的kid，请至少拥有该猎场的一个kid", at_sender=True)


        #加入赌场
        if(not str(group) in data_du):
            data_du[str(group)] = {}
            data_du[str(group)]['lc'] = nums[2]
            data_du[str(group)]['person'] = 0
            data_du[str(group)]['member'] = []
            data_du[str(group)]['want'] = []
        else:
            if(nums[2]!=data_du[str(group)]['lc']):
                await dubo.finish("当前局du不了这个kid", at_sender=True)

        if(not user_id in data_du[str(group)]['member']):

            if(data[str(user_id)]['spike'] < 20):
                await dubo.finish("你需要花费20刺儿进入该局，你的刺儿不够了")

            data_du[str(group)]['person'] += 1   #加入一人
            data_du[str(group)]['member'].append(user_id)

            if(nums[2]=='1'):
                data_du[str(group)]['want'].append(want_kid)
            else:
                data_du[str(group)]['want'].append(nums[0]+'_'+nums[1])

            data[str(user_id)]['spike'] -= 20

        else:
            await dubo.finish("你已经加入该局啦！", at_sender=True)

        #如果满5个人了就开赌
        if(data_du[str(group)]['person']==person_num):
            msg = ""  #消息段
            point = []
            #给出5个点数
            for i in range(person_num):
                point.append(random.randint(10000, 20000))

            #如果不是一猎场就对副数据表进行修改
            if(nums[2]=='2'): data = data2
            if(nums[2]=='3'): data = data3

            #根据点数大小来决定数据交换
            for i in range(person_num):
                self_id = data_du[str(group)]['member'][i]
                for j in range(person_num):
                    if(point[j]<point[i]):
                        #查询输家的ID
                        other_id = data_du[str(group)]['member'][j]
                        #查询赢家想要的kid
                        k = data_du[str(group)]['want'][i]

                        #若有则进行分配
                        if(data[str(other_id)].get(k,0) > 0):
                            #对手减少kid
                            data[str(other_id)][k] -= 1
                            #你增加kid
                            if(not k in data[str(self_id)]): data[str(self_id)][k] = 0
                            data[str(self_id)][k] += 1
                            #增加消息段
                            msg += MessageSegment.at(self_id)
                            msg += "获得了"
                            msg += MessageSegment.at(other_id)
                            if(nums[2]!='1'):
                                k = k.split('_')
                                k = eval(f"kid_data{nums[2]}.get(k[0]).get(k[1]).get('name')")
                            msg += f"的{k}一个\n"

                            break  #结束该循环

        
            #写入文件
            del data_du[str(group)]

            with open(duchang_list, 'w', encoding='utf-8') as f:
                json.dump(data_du, f, indent=4)

            #更新用户数据文件
            if(nums[2]=='1'):
                with open(user_path / file_name, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
            else:
                with open(user_path / f"UserList{nums[2]}.json", 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)             

            #发送消息
            await dubo.send("正在结算本场赌局.....")  #加载消息

            time.sleep(3)    #延时三秒

            if(msg==""): await dubo.finish("本局没有人得到任何东西。")
            await dubo.finish(msg)

        else:

            #写入用户主文件
            with open(user_path / file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            #写入文件
            with open(duchang_list, 'w', encoding='utf-8') as f:
                json.dump(data_du, f, indent=4)

            await dubo.finish(f"成功进入该局！当前共{data_du[str(group)]['person']}人，本局du池为猎场{data_du[str(group)]['lc']}", at_sender=True)


    else:
        await dubo.finish("你还没尝试抓过kid......", at_sender=True)

    
