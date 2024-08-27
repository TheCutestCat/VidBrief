import numpy as np
import cv2
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from pathlib import Path
from collections import defaultdict

# 提取图像特征的函数（示例中为简单的展平特征）
def extract_features(image_path):
    image = cv2.imread(image_path)
    if image is None:
         raise FileNotFoundError(f"Image at path {image_path} not found or unable to load.")
    image = cv2.resize(image, (224, 224))  # 调整图像大小
    image = image / 255.0  # 归一化
    features = image.flatten()  # 展平图像特征
    return features

def cluster_images(image_paths, n_clusters):
    features = np.array([extract_features(path) for path in image_paths])

    # 标准化特征
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    # PCA降维
    pca = PCA(n_components=50)
    features = pca.fit_transform(features)

    # K-means聚类
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(features)

    return labels, kmeans.cluster_centers_

def get_representative_images(image_paths, labels, n_clusters):
    cluster_info = defaultdict(list)

    # 将图像分配到对应的聚类
    for i, label in enumerate(labels):
        cluster_info[label].append(image_paths[i])

    # 选择每个聚类的代表图像，并统计每个聚类的图片数量
    representative_images = []
    cluster_sizes = {}
    for i in range(n_clusters):
        if i in cluster_info:
            images = cluster_info[i]
            representative_images.append(images[0])  # 选择第一个图像作为代表
            cluster_sizes[i] = len(images)  # 统计图片数量
    
    return representative_images, cluster_sizes


def get_representative_images_path(image_paths, n_clusters= 10 ):

    # 聚类
    labels, cluster_centers = cluster_images(image_paths, n_clusters)

    # 获取代表图像
    representative_images, _ = get_representative_images(image_paths, labels, n_clusters)
    print(representative_images)
    return representative_images

import os

    # Assuming frame output folder contains files like frame_0.jpg, frame_1.jpg, ..., frame_n.jpg
def group_and_process_frames(frame_output_folder):
    # List all files in the directory
    files = [os.path.join(frame_output_folder, f) for f in os.listdir(frame_output_folder)]

    key_frames_info = get_representative_images_path(files,n_clusters= 10)
    return key_frames_info

if __name__ == "__main__":
    image_folder = './cache/test_video_kmeans'
    image_paths = [str(Path(image_folder) / f'frame_{i}.jpg') for i in range(60)]
    get_representative_images_path(image_paths)


