def binaryzation(img, threshold=100, alpha=False):
    """图片二值化
    :param img: Image.open()
    :param threshold: 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    :param alpha: 是否将白色部分转为透明
    """
    # 模式L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
    img = img.convert('L')
    img = img.point([int(i >= threshold) for i in range(256)], '1')

    if alpha:
        # 白色部分转透明
        img = img.convert('RGBA')
        for w in range(img.width):
            for h in range(img.height):
                dot = (w, h,)
                color = img.getpixel(dot)
                if color[:3] == (255, 255, 255):
                    img.putpixel(dot, (255, 255, 255, 0))
    return img
