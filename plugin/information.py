from nonebot import on_command, on_fullmatch
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GROUP
from .config import update_text
from nonebot.adapters.onebot.v11 import Message
from .story import npc_da

__all__ = ['help', 'gong_gao', 'npc', 'cklc', 'pvpck']

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

#猎场信息
cklc = on_fullmatch('cklc', permission=GROUP, priority=1, block=True)
@cklc.handle()
async def cklc_handle():
    text = "#######猎场信息######\n1号猎场：田园\n危险等级：0\n\n2号猎场：迷雾森林\n危险等级：2\n\n3号猎场：水晶矿洞\n危险等级：3\n\n？号猎场：虚数空间\n危险等级：5"
    await cklc.finish(text)

#竞技场细则
pvpck = on_fullmatch('0场细则', permission=GROUP, priority=1, block=True)
@pvpck.handle()
async def pvpck_handle():
    text = "有关0号猎场细则：\n\n在本猎场，zhuakid将会从自己的2猎收集池里抓取。竞技场内共十个擂台，抓取完后系统会自动放上十个擂台中的某一个。但是如果该擂台被占用了，就会发生一次PK来决定谁使用这个擂台，一段时间后十个擂台上留下的人将会发放200刺儿的奖励，并重新开始。目前处于试用阶段，但没任何的debuff，可大胆测试！"
    await pvpck.finish(text)