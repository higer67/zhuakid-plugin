import datetime
import json
import random
from pathlib import Path
from nonebot.adapters.onebot.v11 import MessageSegment
#事件系统
#在道具使用和普通的抓kid中会触发

user_path = Path() / "data" / "UserList" / "UserData.json"
forest_path = Path() / "data" / "UserList" / "Forest.json"

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

#参数列表(用户数据信息，猎场编号,，发送消息的句柄)
async def event_happen(user_data, user_id, message):

    #读取猎场编号
    liechang_number = user_data[user_id].get('lc','1')

    #一号猎场：啥事件没有
    if(liechang_number=='1'): return

    #二号猎场
    if(liechang_number=='2'):
        await ForestStuck(user_data,user_id,message)


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
        #遇到被困人员
        if(rnd <= 20):
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

        if(rnd<=30):
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


        




