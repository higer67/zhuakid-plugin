import datetime
#事件系统
#在道具使用和普通的抓kid中会触发

#参数列表(用户数据信息，猎场编号,，发送消息的句柄)
async def event_happen(user_data, liechang_number, message):

    #一号猎场：啥事件没有
    if(liechang_number=='1'): return

    #二号猎场
    if(liechang_number=='2'):
        await ForestStuck(user_data,message)


#二号猎场事件
async def ForestStuck(user_data, message):

    #迷路
    lost = 1

    #是否拥有指南针道具
    if('item' in user_data):
        if(user_data['item'].get('指南针',0) > 0):
            lost = 0
    
    #迷路事件
    if(lost==1):
        #困在森林里八小时，在此期间什么都干不了
        current_time = datetime.datetime.now()
        next_time = current_time + datetime.timedelta(minutes=480)
        user_data['next_time'] = next_time.strftime("%Y-%m-%d %H:%M:%S")
        user_data['buff'] = 'lost'
        #发送消息
        await message.finish("你在森林里迷路了，不知道何时才能走出去.....", at_sender=True)

