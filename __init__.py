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
from .config import *
from .list2 import *
#加载商店信息和商店交互
from .shop import item, today_item
#加载剧情和NPC档案
from .story import npc_da
#加载隐藏kid档案
from .secret import secret_list
#加载抓kid相关的函数
from .function import *
from .event import event_happen, outofdanger
from .kidjd import *

########数据信息#######

#抓kid专用群
group_img = Path() / "data" / "group.jpg"

#除了Kid名字以外的其他key值
other = ["next_time", "spike", "date", "buff", "item", "lc"]

#隐藏级别kid
kid_level0 = "Kid0"
kid_level0_path = kid_path_lc1 / kid_level0

#商店数据，商店的数据一天之内对所有玩家共通，每过一天就会刷新一次商品，每天早上6点到晚上10点营业中
shop_database = Path() / "data" / "Shop" / "Shop.json"
shop_open_img = Path() / "data" / "Shop" / "开张图.png"
shop_work_img = Path() / "data" / "Shop" / "营业图.png"

#更新日志
update_text = "整改一些事情啊。"
#管理员ID
bot_owner_id = "1047392286"

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

#查看帮助菜单和更新信息
help = on_fullmatch('/help', permission=GROUP, priority=1, block=True)
@help.handle()
async def zhua_help():
    await help.finish(f"该机器人目前尚在开发中\n\n"+
          "更新："+update_text+
          "\n\nzhuakid:  抓一个Kid\n签到： 每日签到\n/zs (Kid名字):  展示抓过的Kid\n/ck (Kid名字):  查看该Kid数量\nck: 查看刺儿余额\nkidjd： 查看抓Kid进度"
          +"\nshop:  查看今日商品\n/buy (数量)（道具名):  购买道具\n/use (道具名):  使用道具")

#更新公告
gong_gao = on_fullmatch('公告', permission=GROUP, priority=1, block=True)
@gong_gao.handle()
async def gong_gao_handle():
    text = "“中央广场传来一声巨响，发生什么事情了？旅行者去看看吧！”Roris说到。\n回小镇的路上远远就能看到中央广场那有一束直冲云霄的黑柱.....\n嗯...看来，远古kid的灵魂被激活了。中央广场浮着一团黑色旋涡。“Roris！解释一下啊！”\n“这么多年了，kid祖先所在之地封印终于被解除了，旅行者，你也许能回家了哦~~不过现在还没有进入这个最终猎场的条件呢，一旦你真的进入了，或许就真能回到原先的世界了！”\n“真的？啊这不是一个长线运营的休闲游戏吗，原来真的有会完结的主线啊！”\n嗯呐，可路还很长~旅行者继续加油zhuakid吧！"        
    await gong_gao.finish(text)

#NPC档案
npc = on_command('npc', permission=GROUP, priority=1, block=True)
@npc.handle()
async def npc_handle(arg: Message = CommandArg()):
    name = str(arg)
    if(name in npc_da): 
        await npc.finish(npc_da[name])


##########################管理员指令###########################

#全服发放刺儿
fafang = on_command("全服发放", permission=GROUP, priority=1, block=True)
@fafang.handle()
async def fafang_handle(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    #判断是不是管理员账号
    if(str(event.user_id)!=bot_owner_id):
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
    for k, v in data.items():
        v['spike'] += jiangli

    #写入文件
    with open(user_path / file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


##########################玩家游玩指令#########################

#猎场信息
cklc = on_fullmatch('cklc', permission=GROUP, priority=1, block=True)
@cklc.handle()
async def cklc_handle():
    text = "#######猎场信息######\n1号猎场：田园\n危险等级：0\n\n2号猎场：迷雾森林\n危险等级：2\n\n？号猎场：虚数空间\n危险等级：5"
    await cklc.finish(text)

#切换猎场
qhlc = on_command('qhlc', permission=GROUP, priority=1, block=True)
@qhlc.handle()
async def qhlc_handle(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    #读入用户主要列表
    data = {}
    with open(user_path / file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    user_id = str(event.user_id)
    number = str(arg)     #猎场编号
    if(user_id in data):
        if(number in ['1','2']):

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
            #如果受伤了则无法抓
            if(data[str(user_id)].get("buff")=="hurt"): 
                if(current_time < next_time_r):
                    delta_time = next_time_r - current_time
                    await catch.finish(f"你受伤了，需要等{time_text(delta_time)}才能抓")
                else:
                    data[str(user_id)]["buff"] = "normal"

            #迷路脱险事件
            await outofdanger(data,str(user_id),catch,current_time,next_time_r)
            
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
        #第一次抓
        if(not 'lc' in data[str(user_id)]):
            data[str(user_id)]['lc'] = '1'

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
        if(level==1): spike_give = 5
        if(level==2): spike_give = 10
        if(level==3): spike_give = 15
        if(level==4): spike_give = 20
        if(level==5): spike_give = 25
        if(not 'spike' in data[str(user_id)]):
            data[str(user_id)]['spike'] = 0

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
                if(data2[str(user_id)][str(level)+'_'+str(num)] < 20):
                    data2[str(user_id)][str(level)+'_'+str(num)] += 1  #数量+1
            else:
                new_print = "\n恭喜你抓出来一个新kid！\n"  #如果出新就添加文本
                data2[str(user_id)] = {}
                data2[str(user_id)][str(level)+'_'+str(num)] = 1
            
        #写入kid收集表(副统计表)
        if(data[str(user_id)]['lc']!='1'):
            with open(user_path / f"UserList{data[str(user_id)]['lc']}.json", 'w', encoding='utf-8') as f:
                json.dump(data2, f, indent=4)

        #写入主数据表
        with open(user_path / file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        #发送消息
        await catch.send(new_print+
                        f'\n等级: {level}\n'+
                        f'{name}'+
                        MessageSegment.image(img)+
                        f'{description}'+
                        '\n\n本次奖励'+f'{spike_give}刺儿',
                        at_sender = True)

##每日签到
qd = on_fullmatch('签到', permission=GROUP, priority=1, block=True)
@qd.handle()
async def dailyqd(bot: Bot, event: Event):
    data = {}
    if(os.path.exists(user_path / file_name)):
        #读取刺儿数量
        with open(user_path / file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)

        user_id = event.get_user_id() #获取qq号
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
                data[str(user_id)]['spike'] += spike  #刷新刺儿数量
                data[str(user_id)]['date'] = current_date.strftime("%Y-%m-%d")  #日期时间对象转字符串
                #发送消息
                await qd.send("签到成功，奖励你"+f'{spike}刺儿')
            else:
                #随机奖励刺儿数量
                if(current_date_str!=prevous_date_str):
                    spike = random.randint(1,100)
                    data[str(user_id)]['spike'] += spike  #刷新刺儿数量
                    data[str(user_id)]['date'] = current_date.strftime("%Y-%m-%d")  #刷新日期，日期时间对象转字符串
                    #发送信息
                    await qd.send("签到成功，奖励你"+f'{spike}刺儿')
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
async def cha_spike(bot: Bot, event: Event):
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
async def mykid_handle(bot: Bot, event: GroupMessageEvent):
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
        if(hour==0 and minute==0 and second>=0 and second<=2):
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
async def zhanshi(bot: Bot, event: Event, arg: Message = CommandArg()):
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
    if(nums[2]!='1'):
        with open(user_path / f"UserList{nums[2]}.json", 'r', encoding='utf-8') as f:
            data2 = json.load(f)

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
        else:
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

    else:
        await zs.finish("你还没尝试抓过kid.....")

#查看某Kid数量
cknum = on_command('ck', permission=GROUP, priority=1, block=True)
@cknum.handle()
async def cha_kid_number(bot: Bot, event: Event, arg: Message = CommandArg()):
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
    if(nums[2]!='1'):
        with open(user_path / f"UserList{nums[2]}.json", 'r', encoding='utf-8') as f:
            data2 = json.load(f)

    user_id = event.get_user_id()
    if(str(user_id) in data):
        #查看Kid数量
        if(nums[2]=='1'):
            if(name in data[str(user_id)] and (not name in other)):
                number = data[str(user_id)][name]
                await cknum.finish(f"你有{str(number)}个{name}", at_sender=True)
            else:
                await cknum.send(f"你还没抓到过{name}", at_sender=True)
        else:
            if(str(user_id) in data2):
                if((nums[0]+'_'+nums[1]) in data2[str(user_id)]):
                    number = data2[str(user_id)][nums[0]+'_'+nums[1]]
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
async def zhuajd(bot: Bot, event: Event):
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

        #二号猎场进度
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
    if(hour < 6): await shop.finish("便利店还没开门，请再等一会吧")
    if(hour > 21): await shop.finish("便利店已经打烊了，明天再来吧")
    #输出商店仓库
    current_date = datetime.date.today()  #返回今天日期
    current_date_str = current_date.strftime("%Y-%m-%d")  #日期时间对象转字符串
    if(os.path.exists(shop_database)):

        #打开商店仓库
        with open(shop_database, 'r', encoding='utf-8') as f:
            shop_data = json.load(f)

        #根据是否为同一天来查看是否刷新商品
        previous_date_str = shop_data["date"]

        if(previous_date_str!=current_date_str):
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

    item_text = shop_list(shop_data["item"])
    await shop.send(item_text + MessageSegment.image(shop_work_img), at_sender=True)

#购买商品
buy = on_command('buy', permission=GROUP, priority=1, block=True)
@buy.handle()
async def buy_handle(bot: Bot, event: Event, arg: Message = CommandArg()):
    #打开文件
    #比较营业时间与时间点
    current_time = datetime.datetime.now().time()
    hour = current_time.hour
    if(hour < 6): await buy.finish("便利店还没开门，请再等一会吧")
    if(hour > 21): await buy.finish("便利店已经打烊了，明天再来吧")

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

        if(previous_date_str!=current_date_str):
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
                    if(data[str(user_id)]['item'][buy_item_name] > 20):
                        await buy.finish("该道具已经到达数量上限啦，不能再买了！")

                    #商店库存减少道具
                    shop_data["item"][buy_item_name] -= n

                    #写入用户文件
                    with open(user_path / file_name, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)
                    
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

        #一些啥都干不了的buff
        if(data[str(user_id)].get('buff')=='lost'): return

        if("item" in data[str(user_id)]):
            use_item_name = str(arg)  #获取使用道具名称
            success = 0  #0代表没有效果，1代表成功，2代表失败
            fail_text = "失败！"   #失败文本
            #如果受伤了则无法使用道具
            if(data[str(user_id)].get("buff")=="hurt"): 
                #一些额外操作：如果还没过下次时间，计算与下次的时间间隔，如果过了，可以使用道具
                current_time = datetime.datetime.now()
                next_time_r = datetime.datetime.strptime(data.get(str(user_id)).get('next_time'), "%Y-%m-%d %H:%M:%S")
                if(current_time < next_time_r):
                    delta_time = next_time_r - current_time
                    await daoju.finish(f"你受伤了，需要等{time_text(delta_time)}才能抓")
                else:
                    data[str(user_id)]["buff"] = "normal"

            #道具功能列表
            if(use_item_name=="胡萝卜"):
                if(data[str(user_id)].get("item").get(use_item_name, 0) > 0):

                    """
                    胡萝卜：打破cd额外抓一次，使用的时候有80%的概率抓出兔类Kid,
                    也有20%概率正常规则抓取，是抓伊维的利器
                    """

                    #随机选择是正常抓取还是从兔类Kid里抓
                    rnd = random.randint(1,10)
                    if(rnd <= 8):
                        #二号猎场还没有兔类kid
                        liechang_number = data[str(user_id)]['lc']
                        #从兔类里抓
                        rabbit = eval(f"rabbit_kid{liechang_number}")
                        rabbit_rnd = random.randint(0, len(rabbit)-1)  #随机选择一个
                        information = print_zhua(rabbit[rabbit_rnd][0], rabbit[rabbit_rnd][1], liechang_number)
                        success = 1
                    else:
                        #正常抓取
                        information = zhua_random(liechang_number=data[str(user_id)]['lc'])
                        success = 1
                    data[str(user_id)]["item"][use_item_name] -= 1                      
                else:
                    await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)
            if(use_item_name=="弹弓"):
                if(data[str(user_id)].get("item").get(use_item_name, 0) > 0):
                    """
                    没啥特殊的，只是额外正常地再抓一次
                    """
                    information = zhua_random(liechang_number=data[str(user_id)]['lc'])
                    data[str(user_id)]["item"][use_item_name] -= 1
                    success = 1
                else:
                    await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)
            if(use_item_name=="一次性小手枪"):
                if(data[str(user_id)].get("item").get(use_item_name, 0) > 0):
                    """
                    没啥特殊的，只是额外正常地再抓一次
                    """
                    information = zhua_random(20, 100, 500, 800, liechang_number=data[str(user_id)]['lc'])
                    data[str(user_id)]["item"][use_item_name] -= 1
                    success = 1
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
            if(use_item_name=="时间献祭器"):
                if(data.get(user_id).get('item').get('时间献祭器',0) > 0):
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
                    information = zhua_random(50,200,500,999,liechang_number=data[str(user_id)]['lc'])
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
                            await daoju.finish("-----------------------")

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
                        await daoju.finish(f"你现在没有{use_item_name}", at_sender=True)
                if(use_item_name.lower()=="kid献祭器"):
                    if(data.get(user_id).get('item').get('kid献祭器',0) > 0):
                        next_time = get_time_from_data(data[str(user_id)])
                        current_time = datetime.datetime.now()
                        #没到下一次抓的时间
                        if(current_time < next_time):
                            text = time_text(str(next_time-current_time))
                            await daoju.finish(f"别抓啦，{text}后再来吧", at_sender = True)
                        #将时间更新
                        if(user_id!=bot_owner_id):
                            next_time = current_time + datetime.timedelta(minutes=30)
                            data[str(user_id)]['next_time'] = time_decode(next_time)
                        #将选中的kid清零
                        nums = find_kid(arg2.lower())
                        #查不到这个kid的档案，终止
                        if(nums==0): 
                            logger.info("因为不存在该kid献祭被中断")
                            return
                        #进行献祭
                        if(nums[2]!=data[str(user_id)]['lc']):
                            await daoju.finish(f"你不能献祭别的猎场的kid！", at_sender=True)
                        if(nums[2]=='1'):
                            #一号猎场
                            if(data[str(user_id)].get(arg2.lower(),0) >= 1):
                                data[str(user_id)][arg2.lower()] -= 1
                            else:
                                await daoju.finish(f"你没有{arg2.lower()}可以拿来献祭了！", at_sender=True)
                        else:
                            #二号猎场及其以后，按等级和编号确定
                            data2 = open_data(user_path/f"UserList{data[str(user_id)]['lc']}.json")
                            level_num = nums[0]+'_'+nums[1]
                            if(data2[str(user_id)].get(level_num,0) >= 1):
                                data2[str(user_id)][level_num] -= 1
                                save_data(user_path/f"UserList{data[str(user_id)]['lc']}.json",data2)
                            else:
                                await daoju.finish(f"你没有{arg2.lower()}可以拿来献祭了！", at_sender=True)

                        #zhuakid并增加爆率
                        information = zhua_random(10*2*int(nums[0]), 50*1.5*int(nums[0]), 200*1.2*int(nums[0]), 500*int(nums[0]), liechang_number=data[str(user_id)]['lc'])
                        success = 1

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
                    
                    if(data[str(user_id)][name] < 20):
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
                if(lc!='1'):
                    with open(user_path / f"UserList{lc}.json", 'w', encoding='utf-8') as f:
                        json.dump(data2, f, indent=4)                

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
                #消耗道具
                data[str(user_id)]["item"][use_item_name] -= 1
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
            if(rnd <= 1): spike = 500
            if(rnd > 1 and rnd <= 10): spike = 300
            if(rnd > 10 and rnd <= 30): spike = 150
            if(rnd > 30 and rnd <= 60): spike = 80
            if(rnd > 60 and rnd <= 100): spike = 35

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
        if(nums[2]!='1'):
            with open(user_path / f"UserList{nums[2]}.json", 'r', encoding='utf-8') as f:
                data2 = json.load(f)

            #没有开通二猎场
            if(not str(user_id) in data2):
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
            if(nums[2]!='1'): data = data2

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

    
