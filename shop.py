#商店货物系统，结构为：{物品名称：[价格，等级]}
item = {
    #一次性自动抓捕类道具
    '捕Kid夹': 
    [
        100, 
        1,
        '放下kid夹后，过一段时间可以来查看哪个倒霉kid被捕kid夹抓到了'
    ],
    '假存档': 
    [
        200, 
        2,
        '假存档可以诱惑一些kid前来，也就低级一点的kid能被坑到了吧'
    ],
    #额外次数抓捕类道具
    '弹弓': 
    [
        50, 
        1,
        '半小时内忍不住想抓kid的心？没关系，弹弓能让你额外抓取一次！'
    ],
    '一次性小手枪': 
    [
        100, 
        2,
        '和弹弓一样满足你半小时内想抓kid的心，但是因为是枪械，能额外提高概率，应该吧......'
    ],
    '胡萝卜': 
    [
        200, 
        4,
        '胡萝卜，感觉像是能诱惑兔子的道具啊，难道kid里面也有兔子吗？'
    ],
    'kid提取器': 
    [
        150, 
        3,
        '/use kid提取器使用条例\n1. 输入“/use kid提取器/kid名称”来使用\n2. 只能提取当下的确存在的kid\n3. 提取失败会产生巨大爆炸，请做好防护措施\n4. 严禁递归'
    ],
    #BUFF道具
    '大力药水': 
    [
        100, 
        2,
        '一天之内增强你的力量！提高你抓kid的频率！'
    ],
    '捕Kid网': 
    [
        1200, 
        5,
        '给与你每次正常抓都能提高概率的永久性buff'
    ]
}

#今日物品，前期道具较少，采用固定商品固定数量
today_item = {'弹弓': 20, '一次性小手枪': 20, '胡萝卜': 20, 'kid提取器': 20}