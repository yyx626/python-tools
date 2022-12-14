# 天地图 底图 与 注记 叠加
from PIL import Image
import os


def img_overlay(vec_jpg_path, cva_jpg_path, output_jpg_path, x, y):
    try:
        vec_jpg = Image.open(vec_jpg_path)  # 传入底图jpg或png
        vec_jpg = vec_jpg.convert("RGBA")  # 转换成带透明通道的模式
        cva_jpg = Image.open(cva_jpg_path)  # 传入png透明图片路径
        cva_jpg = cva_jpg.convert("RGBA")  # png图片可以不用转换

        vec_jpg.paste(cva_jpg, (0, 0), cva_jpg)
        # 将透明背景图片 粘贴到jpg图片上的0, 0 坐标位置
        vec_jpg = vec_jpg.convert("RGB")  # 将图片转换回为RGB模式

        # vec_jpg.show()  # 将该图片显示出来
        vec_jpg.save(output_jpg_path)  # 保存为jpg / png
        print(str(x) + '_' + str(y) + '叠加成功')
    except Exception:
        print(str(x) + '_' + str(y) + '叠加失败,重试')
        img_overlay(vec_jpg_path, cva_jpg_path, output_jpg_path, x, y)


zoom = 7  # 下载切片的zoom

# 下载全球影像数据lefttop=[0,0],rightbottom=[2**zoom,2**zoom]
# lefttop[0]~rightbottom[0]为x范围
lefttop = [0, 0]
# lefttop[1]~rightbottom[1]为y范围
rightbottom = [2 ** zoom, 2 ** zoom]

print("开始叠加第", zoom, "级别的影像数据...")
print(str(lefttop[0]))
print(str(rightbottom[0]))
print(str(lefttop[1]))
print(str(rightbottom[1]))
print("共" + str(lefttop[0] - rightbottom[0]))
print("共" + str(lefttop[1] - rightbottom[1]))

vec_base_dir = "D:\\environment\\apache-tomcat-8.5.84\\webapps\\map\\tdt_vec\\"
cva_base_dir = "D:\\environment\\apache-tomcat-8.5.84\\webapps\\map\\tdt_cva\\"
out_base_dir = "D:\\environment\\apache-tomcat-8.5.84\\webapps\\map\\tdt_tile\\"
for x in range(lefttop[0], rightbottom[0]):
    for y in range(lefttop[1], rightbottom[1]):
        vec_path = vec_base_dir + str(zoom) + "\\" + str(x) + "\\" + str(y) + ".jpg"
        cva_path = cva_base_dir + str(zoom) + "\\" + str(x) + "\\" + str(y) + ".jpg"
        out_path = out_base_dir + str(zoom) + "\\" + str(x)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        img_overlay(vec_path, cva_path, os.path.join(out_path, str(y) + ".jpg"), x, y)
print('完成')
