import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Prediksi Omzet Bulanan", layout="centered")
st.title("📈 Prediksi Omzet Bulanan dengan XGBoost")

model = joblib.load("model.pkl")

st.sidebar.header("📥 Upload File Penjualan Anda")
uploaded_file = st.sidebar.file_uploader("Upload file Excel (.xlsx) dari laporan e-commerce", type=["xlsx"])

if uploaded_file is not None:
    try:
        df_user = pd.read_excel(uploaded_file)
        required_cols = {'Order Date', 'Order ID', 'Unit Price', 'Quantity'}
        if not required_cols.issubset(df_user.columns):
            st.error("❌ Format file salah. Pastikan ada kolom: Order Date, Order ID, Unit Price, Quantity")
            st.stop()

        df_user['Order Date'] = pd.to_datetime(df_user['Order Date'], errors='coerce')
        df_user = df_user.dropna(subset=['Order Date'])
        df_user['Subtotal'] = df_user['Unit Price'] * df_user['Quantity']
        df_user['Bulan'] = df_user['Order Date'].dt.to_period('M').astype(str)

        omzet = df_user.groupby('Bulan')['Subtotal'].sum().reset_index(name='Total_Penjualan')
        trx = df_user.groupby('Bulan')['Order ID'].nunique().reset_index(name='Jumlah_Transaksi')
        df_proc = pd.merge(omzet, trx, on='Bulan')

        if len(df_proc) < 3:
            st.warning("⚠️ Minimal 3 bulan data penjualan dibutuhkan untuk prediksi yang akurat.")
            st.stop()

        df_proc['Rata2_Omzet_per_Transaksi'] = df_proc['Total_Penjualan'] / df_proc['Jumlah_Transaksi']
        df_proc['Bulan_Index'] = range(1, len(df_proc)+1)

        st.success("✅ File berhasil diproses dan disederhanakan otomatis!")

        st.subheader("📊 Rekap Data Penjualan Bulanan")
        st.dataframe(df_proc.style.format({
            "Total_Penjualan": "Rp {:,.0f}",
            "Rata2_Omzet_per_Transaksi": "Rp {:,.0f}"
        }))

        st.markdown("### 📈 Visualisasi Omzet dan Transaksi")
        fig, ax1 = plt.subplots(figsize=(8,4))
        ax1.bar(df_proc['Bulan'], df_proc['Total_Penjualan'], color='skyblue')
        ax1.set_ylabel("Omzet (Rp)", color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.set_xticklabels(df_proc['Bulan'], rotation=45)

        ax2 = ax1.twinx()
        ax2.plot(df_proc['Bulan'], df_proc['Jumlah_Transaksi'], color='red', marker='o')
        ax2.set_ylabel("Transaksi", color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        st.pyplot(fig)

        st.subheader("🔮 Prediksi Omzet Bulan Depan")

        last_row = df_proc.iloc[-1]
        fitur = [[
            last_row['Jumlah_Transaksi'],
            last_row['Rata2_Omzet_per_Transaksi'],
            last_row['Bulan_Index'] + 1
        ]]

        pred = model.predict(fitur)[0]
        st.info(f"Prediksi omzet bulan depan berdasarkan {int(last_row['Jumlah_Transaksi'])} transaksi: **Rp {round(pred):,}**")

        df_proc['Prediksi_Omzet_Bulan_Depan'] = ""
        df_proc.at[len(df_proc)-1, 'Prediksi_Omzet_Bulan_Depan'] = round(pred)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_proc.to_excel(writer, index=False, sheet_name="Prediksi")
        st.download_button("💾 Download Hasil Prediksi", output.getvalue(), file_name="hasil_prediksi_omzet.xlsx")

    except Exception as e:
        st.error(f"Terjadi error saat memproses file: {e}")

else:
    st.warning("⬅ Silakan upload file Excel penjualan Anda untuk diproses.")