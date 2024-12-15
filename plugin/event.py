import datetime
import json
import random
from pathlib import Path
from nonebot.adapters.onebot.v11 import MessageSegment
from .function import open_data, save_data, print_zhua, time_decode
from .config import *
#事件系统
#在道具使用和普通的抓kid中会触发

pvp_path = Path() / "data" / "UserList" / "pvp.json"
user_path = Path() / "data" / "UserList" / "UserData.json"
user_liste2 = Path() / "data" / "UserList" / "UserList2.json"
user_liste3 = Path() / "data" / "UserList" / "UserList3.json"
forest_path = Path() / "data" / "UserList" / "Forest.json"
crystal_path = Path() / "data" / "UserList" / "Crystal.json"

#脱险事件
async def outofdanger(data, user_id, message, current_time, next_time_r):

    #迷路脱险事件
    if(data[user_id].get("buff")=="lost"):
        #打开森林被困名单
        stuckdata = {}
        with open(forest_path, 'r', encoding='utf-8') as f:
            stuckdata = json.load(f)

        #打开矿洞被困名单
        crystalStuckdata = {}
        with open(crystal_path, 'r', encoding='utf-8') as f:
            crystalStuckdata = json.load(f)

        #正面buff检测逻辑
        #没有就先加上
        if(not 'buff2' in data[str(user_id)]):
            data[str(user_id)]['buff2'] = 'normal'
        if(not 'lucky_times' in data[str(user_id)]):
            data[str(user_id)]['lucky_times'] = 0
        #幸运
        if data[str(user_id)]["lucky_times"] >= 0 and data[str(user_id)]['buff2'] == 'lucky':
            data[str(user_id)]["lucky_times"] += 1
        if data[str(user_id)]["lucky_times"] == 0  and data[str(user_id)]['buff2'] == 'lucky':
            data[str(user_id)]['buff2'] == 'normal'
        
        #如果不在森林被困名单里
        if(user_id in stuckdata):
            
            if(current_time >= next_time_r):
                data[user_id]["buff"] = "normal"
                del stuckdata[user_id]
                if data[str(user_id)]["lucky_times"] >= 0 and data[str(user_id)]['buff2'] == 'lucky':
                    data[str(user_id)]["lucky_times"] -= 1
                if data[str(user_id)]["lucky_times"] == 0  and data[str(user_id)]['buff2'] == 'lucky':
                    data[str(user_id)]['buff2'] == 'normal'
                #写入主数据表
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                #写入森林被困名单
                with open(forest_path, 'w', encoding='utf-8') as f:
                    json.dump(stuckdata, f, indent=4)

                await message.finish("恭喜你成功脱险....", at_sender=True)

            else:
                #写入主数据表
                if data[str(user_id)]["lucky_times"] >= 0 and data[str(user_id)]['buff2'] == 'lucky':
                    data[str(user_id)]["lucky_times"] -= 1
                if data[str(user_id)]["lucky_times"] == 0  and data[str(user_id)]['buff2'] == 'lucky':
                    data[str(user_id)]['buff2'] == 'normal'
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                await message.finish("你还处在危险之中...", at_sender=True)
        elif(user_id in crystalStuckdata):
            if(current_time >= next_time_r):
                data[user_id]["buff"] = "normal"
                del crystalStuckdata[user_id]
                if data[str(user_id)]["lucky_times"] >= 0 and data[str(user_id)]['buff2'] == 'lucky':
                    data[str(user_id)]["lucky_times"] -= 1
                if data[str(user_id)]["lucky_times"] == 0  and data[str(user_id)]['buff2'] == 'lucky':
                    data[str(user_id)]['buff2'] == 'normal'
                #写入主数据表
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                #写入山洞被困名单
                with open(crystal_path, 'w', encoding='utf-8') as f:
                    json.dump(crystalStuckdata, f, indent=4)

                await message.finish("恭喜你成功脱险....", at_sender=True)

            else:
                #写入主数据表
                if data[str(user_id)]["lucky_times"] >= 0 and data[str(user_id)]['buff2'] == 'lucky':
                    data[str(user_id)]["lucky_times"] -= 1
                if data[str(user_id)]["lucky_times"] == 0  and data[str(user_id)]['buff2'] == 'lucky':
                    data[str(user_id)]['buff2'] == 'normal'
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                await message.finish("你还处在危险之中...", at_sender=True)

        else:
            data[user_id]["buff"] = "normal"
            data[user_id]['next_time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
            if data[str(user_id)]["lucky_times"] == 0  and data[str(user_id)]['buff2'] == 'lucky':
                data[str(user_id)]['buff2'] == 'normal'
            #写入主数据表
            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            await message.finish("恭喜你成功脱险....", at_sender=True)
    elif (data[user_id].get("buff")=="confuse"):
        #打开森林被困名单
        stuckdata = {}
        with open(forest_path, 'r', encoding='utf-8') as f:
            stuckdata = json.load(f)
        
                
        #如果不在森林被困名单里
        if(user_id in stuckdata):
            if(current_time >= next_time_r):
                data[user_id]["buff"] = "normal"
                if data[str(user_id)]["lucky_times"] == 0  and data[str(user_id)]['buff2'] == 'lucky':
                    data[str(user_id)]['buff2'] == 'normal'
                del stuckdata[user_id]
                #写入主数据表
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                #写入森林被困名单
                with open(forest_path, 'w', encoding='utf-8') as f:
                    json.dump(stuckdata, f, indent=4)

                await message.finish("看了半天你还是没想明白这是什么东西，但你意识到不能再在原地停留了", at_sender=True)

            else:
                #写入主数据表
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)   
                await message.finish("你还是感到很困惑", at_sender=True)
            
        else:
            data[user_id]["buff"] = "normal"
            data[user_id]['next_time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
            if data[str(user_id)]["lucky_times"] == 0  and data[str(user_id)]['buff2'] == 'lucky':
                data[str(user_id)]['buff2'] == 'normal'
            #写入主数据表
            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            await message.finish("看了半天你还是没想明白这是什么东西，但你意识到不能再在原地停留了", at_sender=True)

#参数列表(用户数据信息，猎场编号,，发送消息的句柄)
async def event_happen(user_data, user_id, message):

    #读取猎场编号
    liechang_number = user_data[user_id].get('lc','1')

    #一号猎场
    if(liechang_number=='1'): 
        await PlainStuck(user_data,user_id,message)

    #二号猎场
    if(liechang_number=='2'):
        await ForestStuck(user_data,user_id,message)
    
    #三号猎场
    if(liechang_number=='3'):
        await CrystalStuck(user_data,user_id,message)

#一号猎场事件
async def PlainStuck(user_data, user_id, message):
    ######其他事件#####
    rnd = random.randint(1,1000)
    
    '''
    #测试用的模拟代码
    rnd_times = 0
    fragments=0
    items=0
    while rnd_times<10000:
        rnd = random.randint(1,1000)
        if 20<rnd<=30:
            fragments+=1
        if 30<rnd<=40:
            items+=1
        rnd_times+=1
    t1=str(fragments)
    t2=str(items)
    await message.finish(f"10000次模拟成功，一共获得了{t1}次碎片，{t2}次幸运药水", at_sender=True)
    '''
    #遇到金矿
    if(rnd <= 20):
        #奖励刺儿
        spike = random.randint(100,200)
        user_data[user_id]['spike'] += spike
        #写入主数据表
        with open(user_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=4)
        #发送消息
        await message.finish(f"呀，你在森林里发现了一个小金矿，本次奖励{spike}刺儿！", at_sender=True)
    
    if(rnd<=30):#30
        #判断是否开辟道具栏
        if(not 'item' in user_data[str(user_id)]):
            user_data[str(user_id)]['item'] = {}

        #判断是否有开辟该道具
        if(not '神秘碎片' in user_data[str(user_id)]['item']):
            user_data[str(user_id)]['item']['神秘碎片'] = 0

        if (user_data[user_id]['item']['神秘碎片'] < 7):
            current_time = datetime.datetime.now()
            next_time = current_time + datetime.timedelta(minutes=60)
            user_data[user_id]['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
            user_data[user_id]['item']['神秘碎片'] += 1  #给碎片

            #写入主数据表
            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4)
            #发送消息
            await message.finish("你在一个人迹罕至的地方捡到了一个泛着蓝光的神秘碎片，出于好奇和困惑你在此观察了一个小时\n", at_sender=True)
        else:
            return
    
    if(rnd<=40):#40
        #判断是否开辟道具栏
        if(not 'item' in user_data[str(user_id)]):
            user_data[str(user_id)]['item'] = {}

        #判断是否有开辟该道具
        if(not '幸运药水' in user_data[str(user_id)]['item']):
            user_data[str(user_id)]['item']['幸运药水'] = 0

        user_data[user_id]['item']['幸运药水'] += 1
        #写入主数据表
        with open(user_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=4)
        #发送消息
        await message.finish("你捡到了一瓶奇怪的药水，似乎是别人遗留下来的？\n", at_sender=True)
    else:
        return
#二号猎场事件
async def ForestStuck(user_data, user_id, message):

    #打开森林被困名单
    stuckdata = {}
    with open(forest_path, 'r', encoding='utf-8') as f:
        stuckdata = json.load(f)

    #迷路
    lost = 1

    #是否拥有指南针道具
    if('item' in user_data[user_id]):
        if(user_data[user_id]['item'].get('指南针',0) > 0):
            lost = 0
    
    #迷路事件
    if(lost==1):
        rnd = random.randint(1,10)
        if(rnd <= 2):
            return
        else:
            #困在森林里八小时，在此期间什么都干不了
            current_time = datetime.datetime.now()
            next_time = current_time + datetime.timedelta(minutes=480)
            user_data[user_id]['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
            user_data[user_id]['buff'] = 'lost'
            #加入森林被困名单
            stuckdata[user_id] = '2'
            #正面buff检测逻辑
            #没有就先加上
            if(not 'buff2' in user_data[str(user_id)]):
                user_data[str(user_id)]['buff2'] = 'normal'
            if(not 'lucky_times' in user_data[str(user_id)]):
                user_data[str(user_id)]['lucky_times'] = 0
            #幸运
            if user_data[str(user_id)]["lucky_times"] >= 0  and user_data[str(user_id)]['buff2'] == 'lucky':
                user_data[str(user_id)]["lucky_times"] += 1
            #写入主数据表
            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4)
            #写入森林被困名单
            with open(forest_path, 'w', encoding='utf-8') as f:
                json.dump(stuckdata, f, indent=4)      
            #发送消息
            await message.finish("你在森林里迷路了，不知道何时才能走出去.....(请在你觉得可能找到路的时候使用zhuakid指令)", at_sender=True)

    else:
        ######其他事件#####
        rnd = random.randint(1,1000)
        
        #遇到金矿
        if(rnd <= 25):#25
            #奖励刺儿
            spike = random.randint(100,200)
            user_data[user_id]['spike'] += spike
            #写入主数据表
            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4)
            #发送消息
            await message.finish(f"呀，你在森林里发现了一个小金矿，本次奖励{spike}刺儿！", at_sender=True)
        
        #遇到被困人员
        if(rnd <= 150): #150
            if(len(stuckdata) >= 1):
                save_id = random.choice(list(stuckdata.keys()))
                if(stuckdata[save_id]!='2'): return
                user_data[user_id]['spike'] += 50
                user_data[save_id]['next_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")   #将下次的时间重置成当前
                del stuckdata[save_id]
                #正面buff检测逻辑
                #没有就先加上
                if(not 'buff2' in user_data[str(user_id)]):
                    user_data[str(user_id)]['buff2'] = 'normal'
                if(not 'lucky_times' in user_data[str(user_id)]):
                    user_data[str(user_id)]['lucky_times'] = 0
                #幸运
                if user_data[str(user_id)]["lucky_times"] >= 0  and user_data[str(user_id)]['buff2'] == 'lucky':
                    user_data[str(user_id)]["lucky_times"] += 1
                #写入主数据表
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=4)
                #写入森林被困名单
                with open(forest_path, 'w', encoding='utf-8') as f:
                    json.dump(stuckdata, f, indent=4)

                #发送消息
                await message.finish("恭喜你救出了森林里的"+MessageSegment.at(save_id)+"\n本次奖励50刺儿", at_sender=True)
            else:

                #没有需要救的人就结束事件，正常抓kid
                return
        #受伤事件
        if(rnd<=250):#250
            #受伤一小时，在此期间什么都干不了
            current_time = datetime.datetime.now()
            next_time = current_time + datetime.timedelta(minutes=60)
            user_data[user_id]['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
            user_data[user_id]['buff'] = 'lost'
            #加入森林被困名单
            stuckdata[user_id] = '2'
            #正面buff检测逻辑
            #没有就先加上
            if(not 'buff2' in user_data[str(user_id)]):
                user_data[str(user_id)]['buff2'] = 'normal'
            if(not 'lucky_times' in user_data[str(user_id)]):
                user_data[str(user_id)]['lucky_times'] = 0
            #幸运
            if user_data[str(user_id)]["lucky_times"] >= 0  and user_data[str(user_id)]['buff2'] == 'lucky':
                user_data[str(user_id)]["lucky_times"] += 1
            #写入主数据表
            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4)
            #写入森林被困名单
            with open(forest_path, 'w', encoding='utf-8') as f:
                json.dump(stuckdata, f, indent=4)

            #随机事件文本
            text = [
                "你被路边的荆棘刺到了！",
                "抓kid的途中，你掉进了莫名奇妙塌陷的大坑里，",
                "走着走着，树上的苹果落下来把你砸晕了！",
                "你走进一个山洞，可此地暗得你完全找不着北！"
            ]

            #发送消息
            await message.finish(random.choice(text)+"你需要原地等待一个小时", at_sender=True)
        if(rnd<=260):
            #判断是否开辟道具栏
            if(not 'item' in user_data[str(user_id)]):
                user_data[str(user_id)]['item'] = {}

            #判断是否有开辟该道具
            if(not '神秘碎片' in user_data[str(user_id)]['item']):
                user_data[str(user_id)]['item']['神秘碎片'] = 0

            if (user_data[user_id]['item']['神秘碎片'] < 7):
                current_time = datetime.datetime.now()
                next_time = current_time + datetime.timedelta(minutes=60)
                user_data[user_id]['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
                user_data[user_id]['buff'] = 'confuse'
                user_data[user_id]['item']['神秘碎片'] += 1  #给碎片

                #加入森林被困名单
                stuckdata[user_id] = '2'
                #写入主数据表
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=4)
                #写入森林被困名单
                with open(forest_path, 'w', encoding='utf-8') as f:
                    json.dump(stuckdata, f, indent=4)
                #发送消息
                await message.finish("你捡到了一个泛着蓝光的神秘碎片，出于好奇和困惑你在此观察了一个小时\n或许有人发现你的时候...你才会停止观察", at_sender=True)
            else:
                return


#三号猎场事件

async def CrystalStuck(user_data, user_id, message):
    #打开矿洞被困名单
    crystalStuckdata = {}
    with open(crystal_path, 'r', encoding='utf-8') as f:
        crystalStuckdata = json.load(f)
    #是否拥有7个碎片
    if('item' in user_data[user_id]):
        if(user_data[user_id]['item'].get('神秘碎片',0) < 7):
            await message.finish("在远古的水晶矿洞前，风轻轻吹过，岩石间传来阵阵低语。眼前的巨大门扉上镶嵌着神秘的符文，发出幽幽的光辉。你注意到面前门上的部分符文与你手上的碎片相契合\n或许......收集足够的碎片就可以打开这扇门？", at_sender=True)
    

    data2 = {}
    with open(user_liste2, 'r', encoding='utf-8') as f:
        data2 = json.load(f)
    
    if(str(user_id) in data2):
        num_of_level5 = 0
        for k in data2[str(user_id)].keys():
            level = k[0]
            if int(level)==5:
                num_of_level5 += 1
        
        #一号猎场进度
        for k, v in kid_name_list.items():
            #收集数
            for name in v:
                for j in user_data[str(user_id)]:
                    if(name.lower()==j.lower()):
                        if int(k)==5:
                            num_of_level5 += 1
        
        if num_of_level5 < 15:
            await message.finish("水晶矿洞内传来了强大的灵力，这股力量使你无法前进。或许......多带几个猎场的高等级kid可以抵御这股力量？", at_sender=True)
    
    ######其他事件#####
    rnd = random.randint(1,100)
    if user_data[user_id]['debuff'] == 'illusory':
        rnd = random.randint(16,70)
    if user_data[user_id]['buff2'] == 'lucky':
        while True:
            rnd_value = random.randint(1, 100)
            if 1 <= rnd_value <= 35 or 51 <= rnd_value <= 100:
                break
        rnd = rnd_value
    #抓到了特殊的道具
    if(rnd <= 10):#10
        current_time = datetime.datetime.now()
        next_time = current_time + datetime.timedelta(minutes=30)
        user_data[user_id]['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
        rnd_tool = random.randint(1,100)
        #判断是否开辟道具栏
        if(not 'item' in user_data[str(user_id)]):
            user_data[str(user_id)]['item'] = {}

                    
        #奖励道具
        if rnd_tool>=1 and rnd_tool<=33:
            #如果没有，则开辟道具
            if(not '弹弓' in user_data[str(user_id)]['item']):
                user_data[str(user_id)]['item']['弹弓'] = 0

            user_data[user_id]['item']['弹弓'] += 1
            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4)
            await message.finish(f"你发现了其他探险者在此遗落的一个弹弓", at_sender=True)
            
        elif rnd_tool>=34 and rnd_tool<=68:
            #如果没有，则开辟道具
            if(not '一次性小手枪' in user_data[str(user_id)]['item']):
                user_data[str(user_id)]['item']['一次性小手枪'] = 0
            user_data[user_id]['item']['一次性小手枪'] += 1
            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4)
            await message.finish(f"你发现了其他探险者在此遗落的一个一次性小手枪", at_sender=True)
           
        elif rnd_tool>=69 and rnd_tool<=84:
            #如果没有，则开辟道具
            if(not '胡萝卜' in user_data[str(user_id)]['item']):
                user_data[str(user_id)]['item']['胡萝卜'] = 0


            carrot_rnd=random.randint(1,10)
            if carrot_rnd>3:
                user_data[user_id]['item']['胡萝卜'] += 1
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=4)
                await message.finish(f"你发现了其他探险者在此遗落的一个胡萝卜，看起来还很新鲜，还能用。", at_sender=True)
            else:
                await message.finish(f"你发现了其他探险者在此遗落的一个胡萝卜，但是看起来变质用不了了", at_sender=True)
        
        elif rnd_tool>=85 and rnd_tool<=86:
            #如果没有，则开辟道具
            if(not 'kid提取器' in user_data[str(user_id)]['item']):
                user_data[str(user_id)]['item']['kid提取器'] = 0

            user_data[user_id]['item']['kid提取器'] += 1
            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4)
            await message.finish(f"你发现了其他探险者在此遗落的一个kid提取器", at_sender=True)
            
        elif rnd_tool>=87 and rnd_tool<=88:
            #如果没有，则开辟道具
            if(not '时间秒表' in user_data[str(user_id)]['item']):
                user_data[str(user_id)]['item']['时间秒表'] = 0

            if(user_data[user_id]['item'].get('时间秒表',0) < 20):
                user_data[user_id]['item']['时间秒表'] += 1
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=4)
                await message.finish(f"你发现了其他探险者在此遗落的一个时间秒表", at_sender=True)
            else:
                await message.finish(f"你发现了其他探险者在此遗落的一个时间秒表，但是你的背包放不下了，你无奈地丢弃了这个道具", at_sender=True)
        elif rnd_tool>=89 and rnd_tool<=100:
            #如果没有，则开辟道具
            if(not '万能解药' in user_data[str(user_id)]['item']):
                user_data[str(user_id)]['item']['万能解药'] = 0

            user_data[user_id]['item']['万能解药'] += 1
            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4)
            await message.finish(f"你发现了其他探险者在此遗落的一个万能解药", at_sender=True)
    #受伤事件
    if(rnd<=25):#25
        #受伤一小时，在此期间什么都干不了
        current_time = datetime.datetime.now()
        next_time = current_time + datetime.timedelta(minutes=90)
        user_data[user_id]['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
        user_data[user_id]['buff'] = 'lost'
        #加入山洞被困名单
        crystalStuckdata[user_id] = '3'
        #正面buff检测逻辑
        #没有就先加上
        if(not 'buff2' in user_data[str(user_id)]):
            user_data[str(user_id)]['buff2'] = 'normal'
        if(not 'lucky_times' in user_data[str(user_id)]):
            user_data[str(user_id)]['lucky_times'] = 0
        #幸运
        if user_data[str(user_id)]["lucky_times"] >= 0 and user_data[str(user_id)]['buff2'] == 'lucky':
            user_data[str(user_id)]["lucky_times"] += 1
        #写入主数据表
        with open(user_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=4)
        #写入山洞被困名单
        with open(crystal_path, 'w', encoding='utf-8') as f:
            json.dump(crystalStuckdata, f, indent=4)

        #随机事件文本
        text = [
            "你被两侧的小水晶划伤了腿！",
            "抓kid的途中，你掉进了莫名奇妙塌陷的大坑里，",
            "走着走着，矿洞上方的石头落下来把你砸晕了！"
        ]
        #发送消息
        await message.finish(random.choice(text)+"你需要原地等待90分钟", at_sender=True)
        
    #挖矿事件
    if(rnd<=35): #35
        #首先玩家没有buff/debuff时才会随机触发
        if user_data[user_id]['buff'] != 'unlucky':
            #遇到水晶矿
            rnd_crystal = random.randint(1,100)
            if(rnd_crystal <= 50):
                #奖励刺儿
                spike = 100
                user_data[user_id]['spike'] += spike
                #写入主数据表
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=4)
                #发送消息
                await message.finish(f"呀，你在矿洞里发现了一个小型水晶矿。\n这种是较为常见的黄色水晶，不过作为水晶来讲也是很值钱了。\n本次奖励{spike}刺儿！", at_sender=True)
            elif(rnd_crystal <= 90):
                #奖励刺儿
                spike = 200
                user_data[user_id]['spike'] += spike
                #写入主数据表
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=4)
                #发送消息
                await message.finish(f"呀，你在矿洞里发现了一个小型水晶矿。\n这种是不太常见的蓝色水晶，是较为珍贵的水晶之一。\n本次奖励{spike}刺儿！", at_sender=True)
            elif(rnd_crystal <= 100):
                #奖励刺儿
                spike = 500
                user_data[user_id]['spike'] += spike
                #写入主数据表
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=4)
                #发送消息
                await message.finish(f"呀，你在矿洞里发现了一个小型水晶矿。\n这种是相当稀有的紫色水晶，是极为珍贵的水晶之一。\n本次奖励{spike}刺儿！", at_sender=True)
        else:
            return
    #debuff事件
    if(rnd<=50): #50
        #首先玩家没有buff/debuff时才会随机触发
        if user_data[user_id]['debuff'] == 'normal':
            #判断是否开辟恢复时间栏
            current_time = datetime.datetime.now()
            if(not 'next_recover_time' in user_data[str(user_id)]):
                user_data[str(user_id)]['next_recover_time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
            rnd_debuff = random.randint(1,3)
            if rnd_debuff==1:
                #设定恢复时长为4小时后
                next_recover_time = current_time + datetime.timedelta(hours=4)
                user_data[user_id]['next_recover_time'] = next_recover_time.strftime("%Y-%m-%d %H:%M:%S")
                user_data[user_id]['debuff'] = 'illusory'
                with open(user_path, 'w', encoding='utf-8') as f:
                        json.dump(user_data, f, indent=4)
                await message.finish("你不小心走到了矿洞中氧气稀薄的地方，你感觉很难受，似乎4小时内无法再在本猎场抓到道具了。\n不过幸运地，这4小时内你应该不会获得其他debuff了。", at_sender=True)

            if rnd_debuff==2:
                #设定恢复时长为4小时后
                next_recover_time = current_time + datetime.timedelta(hours=4)
                user_data[user_id]['next_recover_time'] = next_recover_time.strftime("%Y-%m-%d %H:%M:%S")
                user_data[user_id]['debuff'] = 'poisoned'
                #虽说让幸运buff消失是不可能事件，但我还是想写上
                user_data[str(user_id)]["buff2"]='normal'
                user_data[str(user_id)]["lucky_times"] = 0
                with open(user_path, 'w', encoding='utf-8') as f:
                        json.dump(user_data, f, indent=4)
                await message.finish("矿洞的墙壁上的植物似乎在释放有毒气体，你中毒了，抓kid能力只剩1成，接下来4小时内在抓到kid时不会获得刺儿了。\n不过幸运地，这4小时内你应该不会获得其他debuff了。", at_sender=True)
            
            if rnd_debuff==3:
                #设定恢复时长为4小时后
                next_recover_time = current_time + datetime.timedelta(hours=4)
                user_data[user_id]['next_recover_time'] = next_recover_time.strftime("%Y-%m-%d %H:%M:%S")
                user_data[user_id]['debuff'] = 'unlucky'
                with open(user_path, 'w', encoding='utf-8') as f:
                        json.dump(user_data, f, indent=4)
                await message.finish("你不知道怎么回事，感觉像是被矿洞内的脏东西附身了，似乎有点不幸，接下来4小时内你不会再在此猎场内挖到宝石矿了。\n不过幸运地，这4小时内你应该不会获得其他debuff了。", at_sender=True)
        #否则就正常抓一次
        else:
            return
    return

#kid竞技场有关机制
async def kid_pvp_event(user_data, user_id, nickname, message, bot):
    # bot_owner_id = ["2153454883", "1047392286", "121096913", "2946244126"]
    # if str(user_id) not in bot_owner_id:
    #     await message.finish("0猎升级中，暂时封闭，仅管理员可抓~", at_sender=True)
    #正面buff检测逻辑
    #没有就先加上
    if(not 'buff2' in user_data[str(user_id)]):
        user_data[str(user_id)]['buff2'] = 'normal'
    if(not 'lucky_times' in user_data[str(user_id)]):
        user_data[str(user_id)]['lucky_times'] = 0
    #幸运
    if user_data[str(user_id)]["lucky_times"] >= 0 and user_data[str(user_id)]['buff2'] == 'lucky':
        user_data[str(user_id)]["lucky_times"] += 1
    # 获取当前时间
    current_time = datetime.datetime.now()
    # 当前时间戳
    timestamp = int(current_time.timestamp())

    # 获取用户的 pvp_next_time，如果不存在则设置为一个过去的时间
    pvp_next_time_str = user_data[user_id].get('pvp_next_time', '1970-01-01 00:00:00')
    pvp_next_time = datetime.datetime.strptime(pvp_next_time_str, "%Y-%m-%d %H:%M:%S")

    # 检查冷却时间
    if current_time < pvp_next_time:
        remaining_time = (pvp_next_time - current_time).total_seconds()
        await message.finish(f"请冷静一下，不能连续抓！还需等待 {remaining_time:.1f} 秒。", at_sender=True)

    # 更新冷却时间
    new_pvp_next_time = current_time + datetime.timedelta(seconds=5)
    user_data[user_id]['pvp_next_time'] = new_pvp_next_time.strftime("%Y-%m-%d %H:%M:%S")
    user_data[user_id]['next_time'] = time_decode(datetime.datetime.now()+datetime.timedelta(minutes=5))
    save_data(user_path, user_data)
    kc_data = {}
    kc_data = open_data(user_liste2)
    kc_data3 = open_data(user_liste3)
    ranliechangnum = random.randint(1, 3)
    #提前设置rana和status
    rana = 0
    lie3 = 0
    #如果没有注册二号猎场
    if(not user_id in kc_data):
        await message.finish("你还没有注册二号猎场哦~", at_sender=True)
    #若解锁三猎，将3猎加入可选池，并且初始概率+5
    liechang_number = "2"
    if (user_id in kc_data3):
        if (ranliechangnum <=1):
            liechang_number = "3"
            rana += 5
            lie3 += 5 #如果是3猎max和min都加5
    #打开竞技场文件
    pvp_data = {}
    pvp_data = open_data(pvp_path)
    #若本次竞技场还没有任何信息，先初始化一下
    if(pvp_data=={}):
        pvp_data['startTime'] = timestamp
        pvp_data['totalCount'] = random.randint(30, 100)
        pvp_data['count'] = 0
        pvp_data['list'] = []
    #从库存中随机抓出一个kid，概率均匀
    if (liechang_number == "2"):
        kid = random.choice(list(kc_data[user_id].keys()))
    #随机到3猎就从3猎抓
    if (liechang_number == "3"):
        kid = random.choice(list(kc_data3[user_id].keys()))
    #在猎场文件中找到位置
    list_current = pvp_data['list']
    stat = 0        #0是依次排队进入，1、2是替换，3、4是赢了，5是输了
    kida = kid.split('_')     #将字符串转为信息列表
    levela = int(kida[0])          #我的等级
    numa = int(kida[1])            #我的编号
    levelb = 0                     #对面等级
    numb = 0                       #对面编号
    rana += random.randint(levela*10, levela*10+50)  #战力系统，1级kid10-60，2级20-70以此类推
    if(len(list_current) < 10):
        #还没满十个不发生PK，依次排队进入
        list_current.append([user_id,kid,nickname,rana,lie3])
        stat = 0
    else:
        #满十个的情况下进入PK逻辑
        #随机选择十个位置中一个
        pos = random.randint(0,9)
        #PVP
        if(list_current[pos][0]==user_id):
            #如果选到的位置被自己占用了通过以下公式计算：战力 + 10*等级，高者留下
            kidb = list_current[pos][1].split('_')
            levelb = int(kidb[0])
            numb = int(kidb[1])
            ranb = list_current[pos][3]
            tihuana = rana + 10*levela
            tihuanb = ranb + 10*levelb
            # list_current[pos][1] = kid
            # stat = 1
            if(tihuana >= tihuanb):
                list_current[pos] = [user_id,kid,nickname,rana,lie3]
                stat = 1
            else:
                stat = 2
        else:
            #如果选到的位置被别人占用了发生PK，比较战力，战力高的人获胜，如果战力相同挑战者获胜
            nicknameb = list_current[pos][2]
            kidb = list_current[pos][1].split('_')
            levelb = int(kidb[0])
            numb = int(kidb[1])
            ranb = list_current[pos][3]
            lie3b = list_current[pos][4]
            #设置最大战力和最小战力
            minrankb = levelb * 10
            maxrankb = levelb * 10 + 50
            ranbrank = random.randint(ranb-15, ranb+15)
            if (ranbrank < minrankb):
                ranbrank = minrankb + lie3b
            if (ranbrank > maxrankb):
                ranbrank = maxrankb + lie3b
            if(rana > ranbrank):
                list_current[pos] = [user_id,kid,nickname,rana,lie3]
                stat = 3
            else:
                if(rana == ranbrank):
                    list_current[pos] = [user_id,kid,nickname,rana,lie3]
                    stat = 4
                else:
                    stat = 5
    #增加回合次数
    pvp_data['count'] += 1
    #更新pvp文件
    pvp_data['list'] = list_current
    save_data(pvp_path,pvp_data)
    ####通告PK结果####
    pk_text = ""
    #自己kid的信息(查等级，查名字，查描述，查图片)
    information = print_zhua(levela,numa,liechang_number)
    kidnamea = information[1]
    # img = information[2]
    # description = information[3]
    #根据不同状态添加额外反馈信息
    if(stat==5):
        kidnameb = print_zhua(levelb,numb,'2')
        pk_text = f"\n你抽出了 [{levela}级的{kidnamea}]，这个kid的战力为 [{rana}]\n\n你遇到了 [擂台{pos+1}] 的擂主 [{nicknameb}] 的 [{levelb}级{kidnameb[1]}]，对方的常驻战力为 [{ranb}]\n\n你的 [{levela}级的{kidnamea}] 的战力为 [{rana}] (lose)\n\n[{nicknameb}] 的 [{levelb}级的{kidnameb[1]}] 的本次战力为 [{ranbrank}] (win)\n\n你的kid被打败了！>_<"
    if(stat==3):
        kidnameb = print_zhua(levelb,numb,'2')
        pk_text = f"\n你抽出了 [{levela}级的{kidnamea}]，这个kid的战力为 [{rana}]\n\n你遇到了 [擂台{pos+1}] 的擂主 [{nicknameb}] 的 [{levelb}级{kidnameb[1]}]，对方的常驻战力为 [{ranb}]\n\n你的 [{levela}级的{kidnamea}] 的战力为 [{rana}] (draw/win)\n\n[{nicknameb}] 的 [{levelb}级的{kidnameb[1]}] 的本次战力为 [{ranbrank}] (draw/lose)\n\n你的kid的战力和擂主的本次战力相等，但是由于你是挑战者所以你赢了！ヽ(o^ ^o)ﾉ"
    if(stat==3):
        kidnameb = print_zhua(levelb,numb,'2')
        pk_text = f"\n你抽出了 [{levela}级的{kidnamea}]，这个kid的战力为 [{rana}]\n\n你遇到了 [擂台{pos+1}] 的擂主 [{nicknameb}] 的 [{levelb}级{kidnameb[1]}]，对方的常驻战力为 [{ranb}]\n\n你的 [{levela}级的{kidnamea}] 的战力为 [{rana}] (win)\n\n[{nicknameb}] 的 [{levelb}级的{kidnameb[1]}] 的本次战力为 [{ranbrank}] (lose)\n\n你的kid获胜了！ヽ(o^ ^o)ﾉ"
    if(stat==2):
        kidnameb = print_zhua(levelb,numb,'2')
        pk_text = f"\n你抽出了 [{levela}级的{kidnamea}]，该kid的常驻战力为 [{rana}]。\n你想替换你放的 [擂台{pos+1}] 的常驻战力为 [{ranb}] 的 [{levelb}级{kidnameb[1]}]，但是综合公式计算不如本擂台的kid，所以没能替换成功！"
    if(stat==1):
        kidnameb = print_zhua(levelb,numb,'2')
        pk_text = f"\n你抽出了 [{levela}级的{kidnamea}]，该kid的常驻战力为 [{rana}]。\n你成功替换了你放的 [擂台{pos+1}] 的常驻战力为 [{ranb}] 的 [{levelb}级{kidnameb[1]}]！"
    if(stat==0):
        pk_text = f"\n你抽出了 [{levela}级的{kidnamea}]，该kid的常驻战力为 [{rana}]。\n你成功占用了一个空擂台，该kid占用的擂台为 [擂台{len(list_current)}]"
    #发送信息
    await message.send(pk_text,at_sender=True)

    #公布结果(回合数达到totalCount决出胜负)
    list_final = []
    for v in list_current:
        list_final.append(v[0])
    if(pvp_data.get('count',0) >= pvp_data.get('totalCount', 70)):
        set_final = set(list_final)
        text = "恭喜"

        current_time_2 = datetime.datetime.now()
        # 当前时间戳
        timestamp_2= int(current_time_2.timestamp())
        start_time = pvp_data.get('startTime')
        end_time = timestamp_2
        time_diff = (end_time - start_time)/3600
        # 根据回合数分配奖励
        totalCount = pvp_data.get('totalCount', 0)
        if totalCount < 40:
            reward = 50
        elif totalCount < 60:
            reward  = 100
        elif totalCount < 80:
            reward  = 150
        elif totalCount <= 100:
            reward  = 200
        # 根据时间差分配奖励
        if time_diff <= 1:
            timeReward = 25
        elif time_diff <= 2:
            timeReward = 50
        else:
            timeReward = 100

        total = reward + timeReward

        for v in set_final:
            text += MessageSegment.at(v)
            user_data[v]['spike'] += total 
        text += f"在这场角逐中取得胜利,全员获得{reward}+{timeReward}={total}刺儿奖励！"
        pvp_data['startTime'] = timestamp
        pvp_data['totalCount'] = random.randint(30, 100)
        pvp_data['count'] = 0
        pvp_data['list'] = []
        await bot.call_api("send_group_msg",group_id=2159014275, message=text)
    #保存pvp文件
    user_data[user_id]['next_time'] = time_decode(datetime.datetime.now()+datetime.timedelta(minutes=5))
    save_data(user_path,user_data)
    save_data(pvp_path,pvp_data)