from nonebot.log import logger
from pathlib import Path
from .config import kid_name_list, kid_data
from .list2 import kid_name_list2, kid_data2
from .shop import item
import random
import re

__all__ = [
    'kid_path_lc1',
    'kid_path_lc2',
    'current_liechang',
    'kid_level1',
    'kid_level2',
    'kid_level3',
    'kid_level4',
    'kid_level5',
    'kid_filename',
    'give_spike',
    'print_zhua',
    'zhua_random',
    'shop_list',
    'decode_buy_text',
    'find_kid',
    'find_kid_single_lc',
    'time_text'
]

#Kid图鉴
kid_path_lc1 = Path() / "data" / "KidLc1"   #一号猎场
kid_path_lc2 = Path() / "data" / "KidLc2"   #二号猎场

kid_level1 = "Kid1"
kid_level2 = "Kid2"
kid_level3 = "Kid3"
kid_level4 = "Kid4"
kid_level5 = "Kid5"

#kid名字
kid_filename = "Kid{index}"

#确定猎场路径
def current_liechang(command):
    if(command=='1'):
        return kid_path_lc1
    if(command=='2'):
        return kid_path_lc2

#奖励刺儿
def give_spike(level):
    if(level==1): spike_give = 5
    if(level==2): spike_give = 10
    if(level==3): spike_give = 15
    if(level==4): spike_give = 20
    if(level==5): spike_give = 25   
    return spike_give

#给定Kid的文件坐标，输出该Kid相关的信息 [等级，名字，图像路径，描述，编号，猎场编号]
def print_zhua(level, num, liechang_number):
    kid_path = current_liechang(liechang_number)
    #锁定kid档案
    current_data = kid_data
    if(liechang_number=='1'):
        current_data = kid_data
    if(liechang_number=='2'):
        current_data = kid_data2
    #根据猎场确定路径
    kid_level1_path = kid_path / kid_level1
    kid_level2_path = kid_path / kid_level2
    kid_level3_path = kid_path / kid_level3
    kid_level4_path = kid_path / kid_level4
    kid_level5_path = kid_path / kid_level5
    #根据等级确定坐标
    if(level == 1): zhua_path = kid_level1_path
    if(level == 2): zhua_path = kid_level2_path
    if(level == 3): zhua_path = kid_level3_path
    if(level == 4): zhua_path = kid_level4_path
    if(level == 5): zhua_path = kid_level5_path
    #名字信息
    name = current_data.get(str(level)).get(str(num)).get('name')
    #图片信息
    houzhui = '.png'
    if(current_data.get(str(level)).get(str(num)).get('gif',False)): houzhui = '.gif' #自动加后缀名
    kid_file_name = kid_filename.format(index=str(num)) + houzhui
    img = zhua_path / kid_file_name
    #描述信息
    description = current_data.get(str(level)).get(str(num)).get('description')
    #确定该KID的打印信息
    kid = [level, name, img, description, num, liechang_number]
    return kid

#Kid的抓取函数
def zhua_random(a=10, b=50, c=200, d=500, liechang_number='1'):
    #随机选择一个等级
    rnd = random.randint(1,1000)
    level = 1
    if(rnd <= a): level = 5
    if(rnd > a and rnd <= b): level = 4
    if(rnd > b and rnd <= c): level = 3
    if(rnd > c and rnd <= d): level = 2
    if(rnd > d and rnd <= 1000): level = 1
    #根据猎场确定路径
    kid_path = current_liechang(liechang_number)
    #各等级路径
    kid_level1_path = kid_path / kid_level1
    kid_level2_path = kid_path / kid_level2
    kid_level3_path = kid_path / kid_level3
    kid_level4_path = kid_path / kid_level4
    kid_level5_path = kid_path / kid_level5
    #锁定kid档案
    current_name_list = kid_name_list
    current_data = kid_data
    if(liechang_number=='1'):
        current_name_list - kid_name_list
        current_data = kid_data
    if(liechang_number=='2'):
        current_name_list - kid_name_list2
        current_data = kid_data2
    #根据等级确定坐标
    if(level == 1): zhua_path = kid_level1_path
    if(level == 2): zhua_path = kid_level2_path
    if(level == 3): zhua_path = kid_level3_path
    if(level == 4): zhua_path = kid_level4_path
    if(level == 5): zhua_path = kid_level5_path
    #选好等级后在该等级中随机抓取
    length = len(current_name_list[str(level)])
    num = random.randint(1,length)
    logger.info(f"{level}级Kid，该级共{length}个，选择了{num}号")
    #名字信息
    name = current_data.get(str(level)).get(str(num)).get('name')
    #图片信息
    houzhui = '.png'
    if(current_data.get(str(level)).get(str(num)).get('gif',False)): houzhui = '.gif' #自动加后缀名
    kid_file_name = kid_filename.format(index=str(num)) + houzhui
    img = zhua_path / kid_file_name
    #描述信息
    description = current_data.get(str(level)).get(str(num)).get('description')
    #确定该KID的打印信息
    kid = [level, name, img, description, num]
    return kid

######打印商品信息######
def shop_list(item_list):
    level_to_str = {0:"一", 1:"二", 2:"三", 3:"四", 4:"五"}
    text = "\n今日商品\n"
    level_str = ["", "", "", "", ""]
    for i in range(4, -1, -1):
        for k, v in item.items():
            if(v[1]==i+1 and k in item_list):
                if(level_str[i]==""): level_str[i] = f"{level_to_str[i]}级：\n"
                level_str[i] += f"{k} x {str(item_list[k])}     单价：{str(v[0])}刺儿\n"
        text += level_str[i]
        if(level_str[i]!="" and i > 0): text += "--------------\n"
    
    return text

#解析玩家的购买指令(物品名称集合，购买指令)
def decode_buy_text(item_name_list, text):
    a = text.split(" ")
    if(len(a)==2):
        if(a[1] in item_name_list):
            return a
        else:
            return None
    else:
        if(len(a)==1):
            if(a[0] in item_name_list):
                return ["1", a[0]]
            else:
                return None
        else:
            return None

#在特定猎场里查找kid
def find_kid_single_lc(value, liechang_number):
    current_data =kid_data
    #确定档案信息
    if(liechang_number=='1'):
        current_data = kid_data
    if(liechang_number=='2'):
        current_data = kid_data2
    #一号猎场查询，由于一号猎场为内测时期产物，没有经过良好维护，现在已经成石山，所以特别查询
    for k, v in current_data.items():
        for i, j in v.items():
            if(j['name'].lower()==value):
                return [k, i]   #返回等级与编号

    return 0

#根据名字查找kid的所在的猎场和等级和位置[等级，编号，几号猎场]
def find_kid(value):
    #一号猎场查询，由于一号猎场为内测时期产物，没有经过良好维护，现在已经成石山，所以特别查询
    for k, v in kid_data.items():
        for i, j in v.items():
            if(j['name'].lower()==value):
                return [k, i, '1']   #返回等级与编号

    #二号猎场查询
    for k, v in kid_data2.items():
        for i, j in v.items():
            if(j['name'].lower()==value):
                return [k, i, '2']   #返回等级与编号

    return 0

#将日期间隔转化成想要表达的形式
def time_text(delta_time):
    a = re.findall(r'\d+', str(delta_time))
    logger.info(f"{a[-4]}小时{a[-3]}分钟{a[-2]}秒：f{delta_time}")
    text = ""
    if(int(a[-4])!=0):
        text += f"{a[-4]}小时"
    if(int(a[-3])!=0):
        text += f"{a[-3]}分钟"
    text += f"{a[-2]}秒"
    
    return text
