import json
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import os
import joblib
num = 0
# 導入數據
json_data = []
folder_path = r"C:\Users\gslab\AppData\Local\paia_desktop\app-2.6.0\resources\app.asar.unpacked\games\TankMan\LOG_P2"
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if isinstance(data, list):
                    json_data.extend(data)
                    print(num)
                    num= num+1
        except Exception as e:
            print(f'{e} {data}')

# 假設json_data是一個包含15萬筆資料的列表

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

# 特徵縮放
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# 將數據分為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(scaled_data, labels, test_size=0.2, random_state=42)

# 訓練KNN模型
k = 5
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X_train, y_train)

# 儲存特徵縮放器和模型
joblib.dump(scaler, 'scaler_model0619_2P.pkl')
joblib.dump(knn, 'knn_model_0619_2P.pkl')

