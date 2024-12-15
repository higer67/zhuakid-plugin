#roris的渲染模块，给roris提高颜值
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

__all__ = ["draw_qd"]

#保存目录
save_dir = Path()/"Data"/"Image"

#素材和字体
font_path = Path()/"Data"/"Image"/"ZhanKu.ttf"
zhenxun = Path()/"Data"/"Image"/"zhenxun.png"
background_qd = Path()/"Data"/"Image"/"background_qd.png"

#将图片渲染到绘制对象上
def texture_render(image: Image, file: str, x: int, y: int, scale: int=1):
    texture = Image.open(file)
    new_size = (int(texture.size[0]*scale), int(texture.size[1]*scale))
    texture = texture.resize(new_size)
    image.paste(texture, (x, y), texture)

#渲染带边缘的作文本
def draw_text_outline(draw: ImageDraw, x: int, y: int, text: str, font: ImageFont, color: str, outline_color: str):
    draw.text((x-1, y-1), text, fill=outline_color, font=font, align="center")
    draw.text((x+1, y-1), text, fill=outline_color, font=font, align="center")
    draw.text((x-1, y+1), text, fill=outline_color, font=font, align="center")
    draw.text((x+1, y+1), text, fill=outline_color, font=font, align="center")
    draw.text((x, y), text, fill=color, font=font, align="center")

#输入用户昵称和刺儿数量，输出签到页面
def draw_qd(nickname: str, spike: int, extra_spike: int=0):
    # 创建一个白色背景的图像
    width, height = 960, 608
    image = Image.new("RGB", (width, height), "white")

    # 创建一个可以在上面绘制的对象
    draw = ImageDraw.Draw(image)

    #绘制背景图
    texture_render(image, background_qd, 0, 0)
    #把真寻图片贴到背景图上
    texture_render(image, zhenxun, -32, 160, 0.5)

    # 设置字体和颜色
    font = ImageFont.truetype(font_path, 48)
    if extra_spike==0:
        text = f"签到成功，奖励你{spike}刺儿"
    else:
        text = f"签到成功，奖励你{spike}+{extra_spike}刺儿"
    text_color = "black"
    outline_color = "white"

    #文本位置
    x = 300
    y = 304

    # 在图片上绘制文本
    draw_text_outline(draw, x, y-64, f"用户 {nickname}:", font, text_color, outline_color)  #绘制用户名称
    draw_text_outline(draw, x, y, text, font, text_color, outline_color)  #绘制奖励多少刺儿

    # 保存图像为 PNG 文件
    image.save(save_dir/"output.png")

    #输出文件路径
    return save_dir/"output.png"