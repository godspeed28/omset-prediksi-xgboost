import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from django.conf import settings
from django.shortcuts import render
from xgboost import XGBRegressor

def home(request):
    result = None
    error = None
    grafik_url = None

    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['data_file']

            # Simpan file sementara
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, 'wb+') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            # Baca file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Hanya file .csv atau .xlsx yang didukung.")

            # Validasi kolom wajib
            required = ['bulan', 'jumlah_transaksi', 'total_produk_terjual', 'harga_rata_rata']
            missing = [col for col in required if col not in df.columns]
            if missing:
                raise ValueError(f"Kolom wajib tidak ditemukan: {', '.join(missing)}")

            # ✅ Validasi & konversi 'bulan' (MM atau nama bulan)
            df['bulan_str'] = df['bulan'].astype(str).str.strip().str.lower()
            map_bulan = {
                '01': 1, '1': 1, 'januari': 1,
                '02': 2, '2': 2, 'februari': 2,
                '03': 3, '3': 3, 'maret': 3,
                '04': 4, '4': 4, 'april': 4,
                '05': 5, '5': 5, 'mei': 5,
                '06': 6, '6': 6, 'juni': 6,
                '07': 7, '7': 7, 'juli': 7,
                '08': 8, '8': 8, 'agustus': 8,
                '09': 9, '9': 9, 'september': 9,
                '10': 10, 'oktober': 10,
                '11': 11, 'november': 11,
                '12': 12, 'desember': 12
            }
            df['bulan_parsed'] = df['bulan_str'].map(map_bulan)
            if df['bulan_parsed'].isnull().any():
                raise ValueError("❌ Format kolom 'bulan' tidak valid. Gunakan MM (01–12) atau nama bulan Indonesia lengkap.")

            df['bulan'] = df['bulan_parsed'].astype(int)
            df.drop(columns=['bulan_str', 'bulan_parsed'], inplace=True)

            # Hitung omset jika belum ada
            if 'omset' not in df.columns:
                df['omset'] = df['total_produk_terjual'] * df['harga_rata_rata']

            # Pelatihan model
            X = df[['bulan', 'jumlah_transaksi', 'total_produk_terjual', 'harga_rata_rata']]
            y = df['omset']
            model = XGBRegressor(n_estimators=100, learning_rate=0.1)
            model.fit(X, y)

            # Simpan model
            model_dir = os.path.join(settings.BASE_DIR, 'model')
            os.makedirs(model_dir, exist_ok=True)
            model_path = os.path.join(model_dir, 'xgb_model.pkl')
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)

            # Prediksi
            df['prediksi_omset'] = model.predict(X)

            # Simpan grafik
            image_dir = os.path.join(settings.BASE_DIR, 'prediksi', 'static', 'prediksi', 'images')
            os.makedirs(image_dir, exist_ok=True)

            plt.figure(figsize=(10, 5))
            plt.plot(df['bulan'], y, label='Omset Asli', marker='o')
            plt.plot(df['bulan'], df['prediksi_omset'], label='Prediksi Omset', marker='o')
            plt.title('Grafik Prediksi Omset')
            plt.xlabel('Bulan')
            plt.ylabel('Omset')
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            image_path = os.path.join(image_dir, 'grafik_prediksi.png')
            plt.savefig(image_path)
            plt.close()
            grafik_url = '/static/prediksi/images/grafik_prediksi.png'

            # Format Rupiah
            df['prediksi_omset'] = df['prediksi_omset'].apply(lambda x: f"Rp {x:,.0f}".replace(',', '.'))
            df['harga_rata_rata'] = df['harga_rata_rata'].apply(lambda x: f"Rp {x:,.0f}".replace(',', '.'))

            result = df[['bulan', 'jumlah_transaksi', 'total_produk_terjual', 'harga_rata_rata', 'prediksi_omset']].to_html(
                classes='table table-bordered text-center', index=False)

        except Exception as e:
            error = str(e)

    return render(request, 'prediksi/index.html', {
        'result': result,
        'error': error,
        'grafik_url': grafik_url
    })
