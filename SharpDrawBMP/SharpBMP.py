from PIL import Image
from PIL import ImageFilter
import math

##################
#    by SharpQ   #
#     Arduino    #
#  QQ：907546989 #    
################## 
# 适用于u8glib、u8g2
# 取模 drawBitmapP 生成 txt

##################
#     参数定义    #
##################
###############################################################################################################
url = "aa.png"       #图片url地址
size = 128,64          #屏幕大小
name = "face"          #保存文件名称
file_format = "txt"    #文件格式
mode = 3               #模式及过滤选择：0：纯灰度、 1：边缘提取、 2:模糊、 3:轮廓 4:边缘增强 5:浮雕 6:锐化 7:光滑 
invert = 1             #像素颜色反选
threshold = 0        #二值化阈值 0-255，单色屏幕中灰度大于此阈值的则被显示
center = 1             #左右居中显示，0:关闭|1:开启 默认开启
center_up = 1          #上下居中显示，0:关闭|1:开启 默认开启
Img_MakeUp = 0         #图像补齐，如果出现最右侧出现缺少可开启补0
###############################################################################################################
#                       控制台显示内容开关 0:关闭|1:开启                                                         
show_wh = 1            #显示宽高
show_pixel = 0         #二进制图像打印显示
###############################################################################################################
file_path = name + '.' + file_format
txt_file = open(file_path,'w')
im = Image.open(url)  
im.thumbnail(size)
if(mode == 1):
    ipx = im.convert('L').filter(ImageFilter.FIND_EDGES)   
elif(mode == 2):
    ipx = im.convert('L').filter(ImageFilter.BLUR)
elif(mode == 3):
    ipx = im.convert('L').filter(ImageFilter.CONTOUR)
elif(mode == 4):
    ipx = im.convert('L').filter(ImageFilter.EDGE_ENHANCE)
elif(mode == 5):
    ipx = im.convert('L').filter(ImageFilter.EMBOSS)
elif(mode == 6):
    ipx = im.convert('L').filter(ImageFilter.SHARPEN)
elif(mode == 7):
    ipx = im.convert('L').filter(ImageFilter.SMOOTH)
else:
    ipx = im.convert('L')                     
w,h = ipx.size
if(show_wh == 1):
    print(w,h)
ima = ipx.load()
row = []
col = []
hexStr = ""
txt_file.write('const uint8_t rook_bitmap[] U8G_PROGMEM = {')
cnt_MaxNum = math.ceil(w/8)
hexRowStr = ""
row_count = 0
for x in range(h):
    if(row != []):
        #print(row)
        for z in row:
            row_count = row_count + 1 
            hexStr = str(hexStr + str(z))
            hexRowStr = str(hexRowStr + str(z))
            if(len(hexStr) == w and w%8 != 0 and Img_MakeUp == 1):
                for x in range(8*cnt_MaxNum-w):
                    hexStr = str(hexStr + str(0))
            if (len(hexStr) == 8 or row_count == w):
                col.append(hexStr)
                xbb = hex(int(hexStr,2))
                txt_file.write(xbb+',')
                hexStr = ""
    #print(col)
    row_count = 0            
    if(show_pixel == 1):
        print(hexRowStr)            
    txt_file.write('\n')
    hexStr = ""
    hexRowStr = ""
    col.clear()        
    #col.append(row)
    row.clear()
    for y in range(w):
        if(invert == 0):
            if(ima[y,x] > threshold):
                row.append(1)
            else:
               row.append(0)
        if(invert == 1):
            if(ima[y,x] > threshold):
                row.append(0)
            else:
                row.append(1)

txt_file.write('};')
txt_file.write('\n\n')
u8g_x = 0
if(size[0] != w):
    u8g_x = math.floor((size[0]-w)/2)
u8g_y = 0
if(size[1] != h and center):
    u8g_y = math.floor((size[1]-h)/2)
cnt = math.ceil(w/8)            
txt_file.write('u8g.drawBitmapP(' + str(u8g_x) + ','+ str(u8g_y) +',' + str(cnt) + ','+ str(h) + ', rook_bitmap);')                
txt_file.close()
print('已生成:'+ file_path)
    