import json
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import os
import joblib

def getJsonData(folderPath):
    # 導入數據
    json_data = []
    num = 0
    for filename in os.listdir(folderPath):
        if filename.endswith('.json'):
            filePath = os.path.join(folderPath, filename)
            try:
                with open(filePath, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if isinstance(data, list):
                        json_data.extend(data)
                        # print(num)
                        num += 1
            except Exception as e:
                print(f'{e} {data}')
    print(type(json_data))
    return json_data

def knnModelTrain(data,labels):
    # 特徵縮放
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    # 將數據分為訓練集和測試集
    X_train, X_test, y_train, y_test = train_test_split(scaled_data, labels, test_size=0.2, random_state=42)

    # 訓練和保存不同K值的KNN模型
    k_values = range(1, 21)
    best_k = 1
    best_accuracy = 0
    results = []

    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        accuracy = knn.score(X_test, y_test)
        results.append((k, accuracy))
        if accuracy > best_accuracy:
            best_k = k
            best_accuracy = accuracy
        print(f"K值: {k}, 準確率: {accuracy * 100:.2f}%")

    # 儲存最佳K值的模型和特徵縮放器
    knn_best = KNeighborsClassifier(n_neighbors=best_k)
    knn_best.fit(X_train, y_train)
    joblib.dump(scaler, 'scaler_model0619_1P.pkl')
    joblib.dump(knn_best, 'knn_model_0619_1P.pkl')

    print(f"最佳K值: {best_k}, 準確率: {best_accuracy * 100:.2f}%")

json_data = getJsonData(r"C:\Users\gslab\AppData\Local\paia_desktop\app-2.6.0\resources\app.asar.unpacked\games\TankMan\LOG_P1")

# 展平嵌套數據結構並提取特徵和標籤
features = []
labels = []
for item in json_data:
    if len(item) == 4:  # 確保數據結構符合預期
        feature = item[0] + item[1] + [item[2]]  # 展平特徵
        label = item[3]  # 提取標籤
        features.append(feature)
        labels.append(label)

# 將特徵和標籤轉換為NumPy數組
data = np.array(features)
labels = np.array(labels)
print(type(data))
print(type(labels))

#訓練模型
knnModelTrain(data,labels)

# 加載已保存的特徵縮放器和最佳模型
scaler = joblib.load('scaler_model0619_1P.pkl')
knn_best = joblib.load('knn_model_0619_1P.pkl')

# 導入測試數據
test_json_data = getJsonData(r"C:\Users\gslab\AppData\Local\paia_desktop\app-2.6.0\resources\app.asar.unpacked\games\TankMan\測試用")

# 展平嵌套數據結構並提取特徵和標籤
test_features = []
test_labels = []
for item in test_json_data:
    if len(item) == 4:  # 確保數據結構符合預期
        feature = item[0] + item[1] + [item[2]]  # 展平特徵
        label = item[3]  # 提取標籤
        test_features.append(feature)
        test_labels.append(label)

# 將特徵和標籤轉換為NumPy數組
X_test = np.array(test_features)
y_test = np.array(test_labels)

# 特徵縮放
X_test_scaled = scaler.transform(X_test)

# 使用最佳模型進行預測
y_pred = knn_best.predict(X_test_scaled)

# 計算模型的準確性
test_accuracy = np.mean(y_pred == y_test)
print(f"最佳模型在測試集上的準確性: {test_accuracy * 100:.2f}%")