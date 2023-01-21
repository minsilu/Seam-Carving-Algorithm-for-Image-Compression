import argparse
import cv2
import numpy as np
import time as time
import os


def calc_disrupt(image):
    G_x = cv2.Sobel(image, -1, 1, 0)
    G_y = cv2.Sobel(image, -1, 0, 1)
    G = np.sum(np.absolute(G_x) + np.absolute(G_y), axis=-1)
    return G


def find_seam(image):
    dis_map = calc_disrupt(image)   #破坏度标示矩阵
    m = dis_map.shape[0]  # m为行数
    n = dis_map.shape[1]  # n为列数
    acc = np.zeros_like(dis_map)  #累积破坏度计算
    store = np.zeros_like(dis_map)  #记录最优路径

    acc[0] = dis_map[0]
    for i in range(1, m):
        for j in range(0, n):
            if j == 0:
                acc[i, j] = np.min([acc[i - 1, j], acc[i - 1, j + 1]]) + dis_map[i, j]
                store[i, j] = np.argmin([acc[i - 1, j], acc[i - 1, j + 1]]) + j
            elif j == n - 1:
                acc[i, j] = np.min([acc[i - 1, j - 1], acc[i - 1, j]]) + dis_map[i, j]
                store[i, j] = np.argmin([acc[i - 1, j - 1], acc[i - 1, j]]) + j - 1
            else:
                acc[i, j] = np.min([acc[i - 1, j - 1], acc[i - 1, j], acc[i - 1, j + 1]]) + dis_map[i, j]
                store[i, j] = np.argmin([acc[i - 1, j - 1], acc[i - 1, j], acc[i - 1, j + 1]]) + j - 1

    result = [np.argmin(acc[-1])]
    for i in range(m - 1, -1, -1):
        result.append(store[i, result[-1]])
    result = result[::-1]
    return result


def delete_seam(image, seam):
    m = image.shape[0]  # m为行数
    n = image.shape[1]  # n为列数
    mask = np.ones((m, n)).astype(np.bool)
    for i in range(m):
        mask[i, seam[i]] = False
    return image[mask].reshape((m, n - 1, 3))


def compress(image, compression_ratio):
    compress = image.copy()
    n = image.shape[1]  # n为列数
    for i in range(int(n * (1 - compression_ratio))):
        seam = find_seam(compress)
        compress = delete_seam(compress, seam)
    return compress


def read_img():
    data = argparse.ArgumentParser(description='seam_carving')
    data.add_argument('--image', '-i', type=str, required=True)
    data.add_argument('--compress_m', '-m', type=float, default=0.5)   #高度压缩率
    data.add_argument('--compress_n', '-n', type=float, default=0.5)   #宽度压缩率
    return data.parse_args()


if __name__ == '__main__':

    # 通过命令行读取图片数据
    data = read_img()
    print("成功读取图片！")
    image = cv2.imread(data.image)
    print("原始图片的大小（高，宽，通道）=", image.shape)

    # 图片压缩程序计时开始
    tic = time.perf_counter()
    # 压缩宽度
    print('压缩宽度中...')
    com_w = compress(image, data.compress_n)
    # 压缩高度
    print('压缩高度中...')
    com_h = np.rot90(com_w)
    com_h = compress(com_h, data.compress_m)
    com_h = np.rot90(com_h)
    com_h = np.rot90(com_h)
    com_h = np.rot90(com_h)
    # 图片压缩程序计时结束
    toc = time.perf_counter()

    # 输出
    name, extent = os.path.splitext(data.image)
    path = name + '_result' + extent
    cv2.imwrite(path, com_h)
    print('===============压缩成功！===============')
    print('压缩过程耗时:%s秒' % (toc - tic))
    print("压缩后图片的大小（高，宽，通道）=", com_h.shape)
    print("图片保存路径为", path)
