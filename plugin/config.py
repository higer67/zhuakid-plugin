from pathlib import Path

__all__ = [
    "group_img",
    "other",
    "kid_level0",
    "kid_level0_path",
    "shop_database",
    "shop_open_img",
    "shop_work_img",
    "update_text",
    "bot_owner_id",
    "user_path",
    "file_name",
    "duchang_list",
    "duchang_open_img",
]

########数据信息#######

#抓kid专用群
group_img = Path() / "data" / "group.jpg"

#除了Kid名字以外的其他key值
other = ["next_time", "next_recover_time", "spike", "date", "buff", "item", "lc"]

#Kid图鉴存放目录
kid_path_lc1 = Path() / "data" / "KidLc1"   #一号猎场
kid_path_lc2 = Path() / "data" / "KidLc2"   #二号猎场
kid_path_lc3 = Path() / "data" / "KidLc3"   #三号猎场

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