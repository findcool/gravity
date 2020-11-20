# coding=utf8
import hashlib
import os
from PIL import Image

flag_cut = {}
ven = {}
ven_key = {}
background = Image.new("RGB", (1500, 1500), (0, 0, 0))


def splitimage(src, rownum, colnum, dstpath):
    img = Image.open(src)
    w, h = img.size
    if rownum <= h and colnum <= w:
        print('Original image info: %sx%s, %s, %s' % (w, h, img.format, img.mode))
        print('开始处理图片切割, 请稍候...')
        s = os.path.split(src)
        if dstpath == '':
            dstpath = s[0]
        fn = s[1].split('.')
        basename = fn[0]
        ext = fn[-1]

        num = 0
        rowheight = h // rownum
        colwidth = w // colnum
        for r in range(rownum):
            for c in range(colnum):
                box = (c * colwidth, r * rowheight, (c + 1) * colwidth, (r + 1) * rowheight)
                img.crop(box).save(os.path.join(dstpath, str(num) + '.' + ext), ext)
                num = num + 1
        print('图片切割完毕，共生成 %s 张小图片。' % num)
    else:
        print('不合法的行列切割参数！')

# splitimage('venom_source.png', 100, 100, 'ven')

for i in os.listdir('flag_cut'):
    path = 'flag_cut/' + i
    value = hashlib.md5(open(path).read()).hexdigest()
    # flag_cut.setdefault(path, value)
    flag_cut.setdefault(value, path)

for i in os.listdir('ven'):
    path = 'ven/' + i
    value = hashlib.md5(open(path).read()).hexdigest()
    ven.setdefault(path, value)


def paste(image1, image2, box):
    image1.paste(image2, box)
    if count % 500 == 0:
        image1.show()


count = 0
for ven_path, ven_value in ven.items():
    try:
        flag_cut_path = flag_cut[ven_value]
        ven_key.setdefault(ven_path, flag_cut_path)
    except:
        continue

for ven_path, flag_cut_path in ven_key.items():
    count += 1
    pos = int(ven_path.split('/')[1].split('.')[0])
    flag_cut_image = Image.open(flag_cut_path)
    paste(background, flag_cut_image, ((pos % 100) * 15, (pos // 100) * 15))
    print(ven_path, flag_cut_path, ((pos % 100) * 15, (pos // 100) * 15), count)

background.save('res.png')
