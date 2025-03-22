import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
def load_data():
    file_path = r"C:\Users\WORKPLUS\Downloads\Submission\submission\Data\day.csv"
    day_df = pd.read_csv(file_path, parse_dates=["dteday"])  # Pastikan kolom tanggal dalam format datetime
    
    # Kategori Hari
    day_df["day_type"] = day_df.apply(lambda row:
        "Holiday" if row["holiday"] == 1 else
        "Weekday" if row["workingday"] == 1 else
        "Weekend", axis=1)
    
    return day_df

# Load dataset
day_df = load_data()

# Dashboard Title
st.title("📊 Bike Sharing Dashboard 🚴‍♂️")
st.markdown("🚲 **Analisis Penyewaan Sepeda**")

# Sidebar Filtering
st.sidebar.header("⚙️ Pengaturan")

# Filter Tanggal
st.sidebar.subheader("📅 Filter Rentang Tanggal")
start_date = pd.to_datetime(st.sidebar.date_input("Tanggal Mulai", day_df["dteday"].min()))
end_date = pd.to_datetime(st.sidebar.date_input("Tanggal Akhir", day_df["dteday"].max()))

# Pastikan rentang tanggal valid
if start_date > end_date:
    st.sidebar.error("⚠️ Tanggal mulai tidak boleh lebih besar dari tanggal akhir!")

# Filter data berdasarkan tanggal
filtered_df = day_df[(day_df["dteday"] >= start_date) & (day_df["dteday"] <= end_date)]

# Pilih Visualisasi
chart_option = st.sidebar.radio(
    "Pilih grafik yang ingin ditampilkan:",
    ["Total Penyewaan Berdasarkan Hari", "Faktor yang Mempengaruhi Penyewaan"]
)

# Visualisasi 1: Berdasarkan Hari
if chart_option == "Total Penyewaan Berdasarkan Hari":
    st.subheader("🚴‍♂️ Total Penyewaan Sepeda Berdasarkan Hari")
    
    # Total penyewaan per kategori hari dalam rentang tanggal yang dipilih
    day_type_df = filtered_df.groupby("day_type")["cnt"].sum().reset_index()
    
    # Plot Bar Chart
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ["#FFA500", "#008000", "#0000FF"]
    sns.barplot(x="day_type", y="cnt", data=day_type_df, palette=colors, ax=ax)
    
    for index, row in enumerate(day_type_df.itertuples()):
        ax.text(index, row.cnt + 5000, f"{row.cnt:,}", ha="center", color="black", fontsize=12)
    
    ax.set_xlabel("Jenis Hari", fontsize=12)
    ax.set_xlabel("-", fontsize=0)
    ax.set_ylabel("Total Penyewaan Sepeda", fontsize=12)
    ax.set_title("Total Penyewaan Sepeda Berdasarkan Jenis Hari", fontsize=14)
    
    st.pyplot(fig)

# Visualisasi 2: Faktor yang Mempengaruhi Penyewaan
elif chart_option == "Faktor yang Mempengaruhi Penyewaan":
    st.subheader("📈 Faktor yang Mempengaruhi Penyewaan Sepeda")
    
    # Pilih faktor yang ingin dianalisis
    faktor = st.sidebar.selectbox(
        "Pilih faktor:", ["Suhu", "Kelembapan", "Kecepatan Angin"]
    )

    # Mapping faktor ke dataset
    faktor_mapping = {
        "Suhu": "temp",
        "Kelembapan": "hum",
        "Kecepatan Angin": "windspeed"
    }
    faktor_kolom = faktor_mapping[faktor]

    # Scatter Plot
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.regplot(data=filtered_df, x=faktor_kolom, y="cnt", ax=ax, color="blue")

    ax.set_xlabel(faktor, fontsize=12)
    ax.set_ylabel("Jumlah Sepeda Disewa", fontsize=12)
    ax.set_title(f"{faktor} vs Jumlah Penyewaan Sepeda", fontsize=14)

    st.pyplot(fig)

# ℹInformasi Tambahan
st.sidebar.header("ℹ️ Informasi Tambahan")

# Total Penyewaan Sepeda dalam Rentang Waktu yang Dipilih
total_rentals = filtered_df["cnt"].sum()
st.sidebar.metric(label="🚲 Total Penyewaan Sepeda", value=f"{total_rentals:,}")

# Hari dengan Penyewaan Tertinggi
if not filtered_df.empty:
    busiest_day = filtered_df.loc[filtered_df["cnt"].idxmax()]
    st.sidebar.write(f"📅 **Hari dengan penyewaan tertinggi:** {busiest_day['dteday']} ({busiest_day['cnt']} sepeda)")
else:
    st.sidebar.write("🚫 Tidak ada data dalam rentang tanggal yang dipilih!")

