import os
import json
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import joblib
import time

def get_json_data(folder_path):
    """
    讀取指定資料夾中的所有 JSON 文件，並將資料合併成一個陣列。
    """
    all_data = []

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            # 构建完整的文件路径
            file_path = os.path.join(folder_path, file_name)
            # 打开 JSON 文件并加载数据
            with open(file_path, "r", encoding='utf-8') as json_file:
                data = json.load(json_file)
                all_data.extend(data)

    # 将所有数据合并成一个数组
    merged_data = [item for sublist in all_data for item in sublist]
    data_array = np.array(merged_data)
    return data_array

def train_knn_classifier(data_array, n_neighbors=3):
    """
    使用 KNN 模型訓練數據，並傳回訓練好的模型。
    """
    first_three = data_array[:, :4]
    last_one = data_array[:, 4]

    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(first_three, last_one)

    return knn

def save_model(model, file_path):
    """
    保存訓練好的模型到文件。
    """
    joblib.dump(model, file_path)

def load_model(file_path):
    """
    從檔案載入模型。
    """
    return joblib.load(file_path)

def predict_knn(knn, data_array):
    """
    使用訓練好的 KNN 模型預測新的資料。
    """
    predictions = []
    for i in range(len(data_array)):
        predicted_direction = knn.predict(data_array[:i+1])
        print(predicted_direction)
        time.sleep(1)
        # predictions.append(predicted_direction[len(predicted_direction) - 1])
    
    return predictions

def main():
    folder_path = r"C:\\Users\\gslab\\AppData\\Local\\paia_desktop\\app-2.6.0\\resources\\app.asar.unpacked\\games\\arkanoid\\log"
    model_path = 'knn_model.pkl'
    
    # 取得並處理訓練數據
    data_array = get_json_data(folder_path)
    
    # 訓練 KNN 模型
    knn = train_knn_classifier(data_array)
    
    # 保存模型
    save_model(knn, model_path)
    
    # 載入模型
    knn = load_model(model_path)
    
    # 取得並處理預測數據
    folder_path2 = r"C:\\Users\\gslab\\AppData\\Local\\paia_desktop\\app-2.6.0\\resources\\app.asar.unpacked\\games\\arkanoid\\log2"
    data_array2 = get_json_data(folder_path2)
    data_array2 = data_array2[:, :4]
    predict_knn(knn, data_array2)
    # 預測板子的移動方向
    # predictions = predict_knn(knn, data_array2)
    
    # for prediction in predictions:
    #     print(prediction)

if __name__ == "__main__":
    main()
