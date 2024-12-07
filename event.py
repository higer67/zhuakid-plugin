import datetime
import json
import random
from pathlib import Path
from nonebot.adapters.onebot.v11 import MessageSegment
from .function import open_data, save_data, print_zhua, time_decode
#事件系统
#在道具使用和普通的抓kid中会触发

pvp_path = Path() / "data" / "UserList" / "pvp.json"
user_path = Path() / "data" / "UserList" / "UserData.json"
user_liste2 = Path() / "data" / "UserList" / "UserList2.json"
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

        #如果不在森林被困名单里
        if(user_id in stuckdata):
            if(current_time >= next_time_r):
                data[user_id]["buff"] = "normal"
                del stuckdata[user_id]
                #写入主数据表
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                #写入森林被困名单
                with open(forest_path, 'w', encoding='utf-8') as f:
                    json.dump(stuckdata, f, indent=4)

                await message.finish("恭喜你成功脱险....", at_sender=True)

            else:

                await message.finish("你还处在危险之中...", at_sender=True)
            
        else:
            data[user_id]["buff"] = "normal"
            data[user_id]['next_time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
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
                del stuckdata[user_id]
                #写入主数据表
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                #写入森林被困名单
                with open(forest_path, 'w', encoding='utf-8') as f:
                    json.dump(stuckdata, f, indent=4)

                await message.finish("看了半天你还是没想明白这是什么东西，但你意识到不能再在原地停留了", at_sender=True)

            else:

                await message.finish("你还是感到很困惑", at_sender=True)
            
        else:
            data[user_id]["buff"] = "normal"
            data[user_id]['next_time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
            #写入主数据表
            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            await message.finish("看了半天你还是没想明白这是什么东西，但你意识到不能再在原地停留了", at_sender=True)

#参数列表(用户数据信息，猎场编号,，发送消息的句柄)
async def event_happen(user_data, user_id, message):

    #读取猎场编号
    liechang_number = user_data[user_id].get('lc','1')

    #一号猎场：啥事件没有
    if(liechang_number=='1'): return

    #二号猎场
    if(liechang_number=='2'):
        await ForestStuck(user_data,user_id,message)
    
    #三号猎场
    if(liechang_number=='3'):
        await CrystalStuck(user_data,user_id,message)


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
        rnd = random.randint(1,100)
        #遇到金矿
        if(rnd <= 3):
            #奖励刺儿
            spike = random.randint(400,800)
            user_data[user_id]['spike'] += spike
            #写入主数据表
            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4)
            #发送消息
            await message.finish(f"呀，你在森林里发现了一个小金矿，本次奖励{spike}刺儿！", at_sender=True)
        #遇到被困人员
        if(rnd <= 15):
            if(len(stuckdata) >= 1):
                save_id = random.choice(list(stuckdata.keys()))
                if(stuckdata[save_id]!='2'): return
                user_data[user_id]['spike'] += 25
                user_data[save_id]['next_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")   #将下次的时间重置成当前
                del stuckdata[save_id]
                #写入主数据表
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=4)
                #写入森林被困名单
                with open(forest_path, 'w', encoding='utf-8') as f:
                    json.dump(stuckdata, f, indent=4)

                #发送消息
                await message.finish("恭喜你救出了森林里的"+MessageSegment.at(save_id)+"\n本次奖励25刺儿", at_sender=True)
            else:

                #没有需要救的人就结束事件，正常抓kid
                return
        #受伤事件
        if(rnd<=25):
            #受伤一小时，在此期间什么都干不了
            current_time = datetime.datetime.now()
            next_time = current_time + datetime.timedelta(minutes=60)
            user_data[user_id]['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
            user_data[user_id]['buff'] = 'lost'
            #加入森林被困名单
            stuckdata[user_id] = '2'
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
        if(rnd<=27):
            #判断是否开辟道具栏
            if(not 'item' in user_data[str(user_id)]):
                user_data[str(user_id)]['item'] = {}

            #判断是否有开辟该道具
            if(not '神秘碎片' in user_data[str(user_id)]['item']):
                user_data[str(user_id)]['item']['神秘碎片'] = 0

            if(user_data[user_id]['item']['神秘碎片'] < 10):
                current_time = datetime.datetime.now()
                next_time = current_time + datetime.timedelta(minutes=60)
                user_data[user_id]['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
                user_data[user_id]['buff'] = 'confuse'
                user_data[user_id]['item']['神秘碎片'] += 1  #给碎片

                #写入主数据表
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=4)
                #发送消息
                await message.finish("你捡到了一个泛着蓝光的神秘碎片，出于好奇和困惑你在此观察了一个小时\n或许有人发现你的时候...你才会停止观察", at_sender=True)
            else:
                return


#三号猎场事件

async def CrystalStuck(user_data, user_id, message):
    #打开矿洞被困名单(还没想好写点什么)
    crystalStuckdata = {}
    with open(forest_path, 'r', encoding='utf-8') as f:
        crystalStuckdata = json.load(f)
    #是否拥有10个碎片
    if('item' in user_data[user_id]):
        if(user_data[user_id]['item'].get('神秘碎片',0) < 10):
            await message.finish("在远古的水晶矿洞前，风轻轻吹过，岩石间传来阵阵低语。眼前的巨大门扉上镶嵌着神秘的符文，发出幽幽的光辉。你注意到面前门上的部分符文与你手上的碎片相契合\n或许......收集足够的碎片就可以打开这扇门？", at_sender=True)
    
    data2 = {}
    with open(user_liste2, 'r', encoding='utf-8') as f:
        data2 = json.load(f)
    
    if(str(user_id) in data2):
        num_of_lc2_level5 = 0
        for k in data2[str(user_id)].keys():
            level = k[0]
            if int(level)==5:
                num_of_lc2_level5 += 1
        
        if num_of_lc2_level5 < 5:
            await message.finish("水晶矿洞内传来了强大的灵力，这股力量使你无法前进。或许......多带几个第二猎场的高等级kid可以抵御这股力量？", at_sender=True)
    
    ######其他事件#####
    rnd = random.randint(1,100)
    if user_data[user_id]['buff'] == 'illusory':
         rnd = random.randint(16,75)
    #抓到了特殊的道具
    if(rnd <= 15):
        current_time = datetime.datetime.now()
        next_time = current_time + datetime.timedelta(minutes=30)
        user_data[user_id]['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
        rnd_tool = random.randint(1,60)
        #判断是否开辟道具栏
        if(not 'item' in user_data[str(user_id)]):
            user_data[str(user_id)]['item'] = {}

                    
        #奖励道具
        if rnd_tool>=1 and rnd_tool<=25:
            #如果没有，则开辟道具
            if(not '弹弓' in user_data[str(user_id)]['item']):
                user_data[str(user_id)]['item']['弹弓'] = 0

            if(user_data[user_id]['item'].get('弹弓',0) < 20):
                user_data[user_id]['item']['弹弓'] += 1
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=4)
                await message.finish(f"你发现了其他探险者在此遗落的一个弹弓", at_sender=True)
            else:
                await message.finish(f"你发现了其他探险者在此遗落的一个弹弓，但是你的背包放不下了，你无奈地丢弃了这个道具", at_sender=True)
        elif rnd_tool>=26 and rnd_tool<=45:
            #如果没有，则开辟道具
            if(not '一次性小手枪' in user_data[str(user_id)]['item']):
                user_data[str(user_id)]['item']['一次性小手枪'] = 0

            if(user_data[user_id]['item'].get('一次性小手枪',0) < 20):
                user_data[user_id]['item']['一次性小手枪'] += 1
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=4)
                await message.finish(f"你发现了其他探险者在此遗落的一个一次性小手枪", at_sender=True)
            else:
                await message.finish(f"你发现了其他探险者在此遗落的一个一次性小手枪，但是你的背包放不下了，你无奈地丢弃了这个道具", at_sender=True)
        elif rnd_tool>=46 and rnd_tool<=55:
            #如果没有，则开辟道具
            if(not '胡萝卜' in user_data[str(user_id)]['item']):
                user_data[str(user_id)]['item']['胡萝卜'] = 0

            if(user_data[user_id]['item'].get('胡萝卜',0) < 20):
                carrot_rnd=random.randint(1,10)
                if carrot_rnd>3:
                    user_data[user_id]['item']['胡萝卜'] += 1
                    with open(user_path, 'w', encoding='utf-8') as f:
                        json.dump(user_data, f, indent=4)
                    await message.finish(f"你发现了其他探险者在此遗落的一个胡萝卜，看起来还很新鲜，还能用。", at_sender=True)
                else:
                    await message.finish(f"你发现了其他探险者在此遗落的一个胡萝卜，但是看起来变质用不了了，你无奈地丢弃了这个道具", at_sender=True)
            else:
                await message.finish(f"你发现了其他探险者在此遗落的一个胡萝卜，但是你的背包放不下了，你无奈地丢弃了这个道具", at_sender=True)
        elif rnd_tool>=56 and rnd_tool<=58:
            #如果没有，则开辟道具
            if(not 'kid提取器' in user_data[str(user_id)]['item']):
                user_data[str(user_id)]['item']['kid提取器'] = 0

            if(user_data[user_id]['item'].get('kid提取器',0) < 20):
                user_data[user_id]['item']['kid提取器'] += 1
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=4)
                await message.finish(f"你发现了其他探险者在此遗落的一个kid提取器", at_sender=True)
            else:
                await message.finish(f"你发现了其他探险者在此遗落的一个kid提取器，但是你的背包放不下了，你无奈地丢弃了这个道具", at_sender=True)
        elif rnd_tool>=59 and rnd_tool<=60:
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
        elif rnd_tool>=61 and rnd_tool<=70:
            #如果没有，则开辟道具
            if(not '万能解药' in user_data[str(user_id)]['item']):
                user_data[str(user_id)]['item']['万能解药'] = 0

            if(user_data[user_id]['item'].get('万能解药',0) < 20):
                user_data[user_id]['item']['万能解药'] += 1
                with open(user_path, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=4)
                await message.finish(f"你发现了其他探险者在此遗落的一个万能解药", at_sender=True)
            else:
                await message.finish(f"你发现了其他探险者在此遗落的一个万能解药，但是你的背包放不下了，你无奈地丢弃了这个道具", at_sender=True)
    #受伤事件
    if(rnd<=35):
        #受伤一小时，在此期间什么都干不了
        current_time = datetime.datetime.now()
        next_time = current_time + datetime.timedelta(minutes=90)
        user_data[user_id]['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
        user_data[user_id]['buff'] = 'lost'
        #加入森林被困名单
        crystalStuckdata[user_id] = '3'
        #写入主数据表
        with open(user_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=4)
        #写入森林被困名单
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
    
    #debuff事件
    if(rnd<=50):
        #首先玩家没有buff/debuff时才会随机触发
        if user_data[user_id]['buff'] == 'normal':
            #判断是否开辟恢复时间栏
            current_time = datetime.datetime.now()
            if(not 'next_recover_time' in user_data[str(user_id)]):
                user_data[str(user_id)]['next_recover_time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
            rnd_debuff = random.randint(1,2)
            if rnd_debuff==1:
                #设定恢复时长为4小时后
                next_recover_time = current_time + datetime.timedelta(hours=4)
                user_data[user_id]['next_recover_time'] = next_recover_time.strftime("%Y-%m-%d %H:%M:%S")
                user_data[user_id]['buff'] = 'illusory'
                with open(user_path, 'w', encoding='utf-8') as f:
                        json.dump(user_data, f, indent=4)
                await message.finish("你不小心走到了矿洞中氧气稀薄的地方，你感觉很难受，似乎4小时内无法再在本猎场抓到道具了。\n不过幸运地，这4小时内你应该不会获得其他debuff了。", at_sender=True)

            if rnd_debuff==2:
                #设定恢复时长为4小时后
                next_recover_time = current_time + datetime.timedelta(hours=4)
                user_data[user_id]['next_recover_time'] = next_recover_time.strftime("%Y-%m-%d %H:%M:%S")
                user_data[user_id]['buff'] = 'poisoned'
                with open(user_path, 'w', encoding='utf-8') as f:
                        json.dump(user_data, f, indent=4)
                await message.finish("矿洞的墙壁上的植物似乎在释放有毒气体，你中毒了，抓kid能力只剩1成，接下来4小时内在抓到kid时不会获得刺儿了。\n不过幸运地，这4小时内你应该不会获得其他debuff了。", at_sender=True)
        #否则就正常抓一次
        else:
            return
    return

#kid竞技场有关机制
async def kid_pvp_event(user_data, user_id, nickname, message, bot):
    #打开二号猎场库存
    kc_data = {}
    kc_data = open_data(user_liste2)
    #如果没有注册二号猎场
    if(not user_id in kc_data):
        await message.finish("你还没有注册二号猎场哦~", at_sender=True)
    #打开竞技场文件
    pvp_data = {}
    pvp_data = open_data(pvp_path)
    #若本次竞技场还没有任何信息，先初始化一下
    if(pvp_data=={}):
        pvp_data['count'] = 0
        pvp_data['list'] = []
    #从库存中随机抓出一个kid，概率均匀
    kid = random.choice(list(kc_data[user_id].keys()))
    #在猎场文件中找到位置
    list_current = pvp_data['list']
    stat = 0        #0是依次排队进入，1是替换，2是赢了，3是输了
    kida = kid.split('_')     #将字符串转为信息列表
    levela = int(kida[0])          #我的等级
    numa = int(kida[1])            #我的编号
    levelb = 0                     #对面等级
    numb = 0                       #对面编号
    if(len(list_current) < 10):
        #还没满十个不发生PK，依次排队进入
        list_current.append([user_id,kid,nickname])
        stat = 0
    else:
        #满十个的情况下进入PK逻辑
        #随机选择十个位置中一个
        pos = random.randint(0,9)
        #PVP
        if(list_current[pos][0]==user_id):
            #如果选到的位置被自己占用了直接替换即可
            kidb = list_current[pos][1].split('_')
            levelb = int(kidb[0])
            numb = int(kidb[1])
            list_current[pos][1] = kid
            stat = 1
        else:
            #如果选到的位置被别人占用了发生PK，暂时先试用高等级直接打败低等级的逻辑，等级相同就抛硬币
            kidb = list_current[pos][1].split('_')
            levelb = int(kidb[0])
            numb = int(kidb[1])
            if(levela > levelb):
                list_current[pos] = [user_id,kid,nickname]
                stat = 2
            else:
                if(levela==levelb):
                    rnd = random.randint(0,1)
                    if(rnd==0):
                        list_current[pos] = [user_id,kid,nickname]
                        stat = 2
                    else:
                        stat = 3
                else:
                    stat = 3
    #增加回合次数
    pvp_data['count'] += 1
    #更新pvp文件
    pvp_data['list'] = list_current
    save_data(pvp_path,pvp_data)
    ####通告PK结果####
    pk_text = ""
    #自己kid的信息(查等级，查名字，查描述，查图片)
    information = print_zhua(levela,numa,'2')
    img = information[2]
    description = information[3]
    #根据不同状态添加额外反馈信息
    if(stat==2):
        oppo = print_zhua(levelb,numb,'2')
        pk_text = f"\n\n打败了{levelb}级的{oppo[1]}！"
    if(stat==3):
        oppo = print_zhua(levelb,numb,'2')
        pk_text = f"\n\n但是被{levelb}级的{oppo[1]}打败了！>_<"
    if(stat==1):
        oppo = print_zhua(levelb,numb,'2')
        pk_text = f"\n\n替换了你放的{levelb}级的{oppo[1]}！"
    if(stat==0):
        pk_text = "\n\n你占用了一个空位置"
    #发送信息
    await message.send(f"\n等级：{levela}\n"+MessageSegment.image(img)+f"\n{description}"+pk_text,at_sender=True)
    #公布结果(回合数达到200决出胜负)
    list_final = []
    for v in list_current:
        list_final.append(v[0])
    if(pvp_data.get('count',0)>=200):
        set_final = set(list_final)
        text = "恭喜"
        for v in set_final:
            text += MessageSegment.at(v)
            user_data[v]['spike'] += 500
        text += "在这场角逐中取得胜利,全员获得500刺儿奖励！"
        #重置pvp文件并发信息
        pvp_data.clear()
        await bot.call_api("send_group_msg",group_id=2159014275, message=text)
    #保存pvp文件
    user_data[user_id]['next_time'] = time_decode(datetime.datetime.now()+datetime.timedelta(minutes=5))
    save_data(user_path,user_data)
    save_data(pvp_path,pvp_data)


        




