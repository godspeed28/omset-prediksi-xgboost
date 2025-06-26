import pandas as pd
from xgboost import XGBRegressor
import pickle
import os

# Baca dataset yang berisi kolom harga_rata_rata dan omset
df = pd.read_csv('data_omset_dengan_harga.csv')

# Pilih fitur dan target
X = df[['bulan', 'jumlah_transaksi', 'total_produk_terjual', 'harga_rata_rata']]
y = df['omset']

# Buat dan latih model
model = XGBRegressor()
model.fit(X, y)

# Simpan model ke file
model_dir = os.path.join(os.getcwd(), 'model')
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, 'xgb_model.pkl')

with open(model_path, 'wb') as f:
    pickle.dump(model, f)

print(f"✅ Model berhasil disimpan ke: {model_path}")
