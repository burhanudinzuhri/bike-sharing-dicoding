import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Menyiapkan data_day
data_day = pd.read_csv(f"https://drive.google.com/uc?export=download&id=1lIEVro2Cb98C2gYfAbm6qj8JPSU3nFGY")
data_day.head()

# Menghapus kolom yang tidak diperlukan
drop_col = ['windspeed']

for i in data_day.columns:
  if i in drop_col:
    data_day.drop(labels=i, axis=1, inplace=True)

# Mengubah nama kolom
data_day.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Mengubah angka menjadi keterangan
data_day['month'] = data_day['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
data_day['season'] = data_day['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
data_day['weekday'] = data_day['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
data_day['weather_cond'] = data_day['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Membuat Dashboard secara lengkap

# Membuat judul
st.header('Halaman Bike Sharing')

# Tren penyewaan sepeda 2011-2012
st.subheader('Tren Penyewaan Sepeda 2011-2012')
fig, ax = plt.subplots(figsize=(24, 8))
data_day['month'] = pd.Categorical(data_day['month'], categories=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], ordered=True)
monthly_counts = data_day.groupby(by=["month","year"]).agg({
    "count":"sum"
}).reset_index()
sns.lineplot(
    data=monthly_counts,
    x="month",
    y="count",
    hue="year",
    palette="Paired",
    marker="o")
plt.title("Total Penyewaan Sepeda")
plt.xlabel(None)
plt.ylabel(None)
plt.legend(title="Tahun", loc="upper right")
plt.tight_layout()
st.pyplot(fig)

# Penyewaan sepeda serdasarkan temp dan atemp, dan humidity
st.subheader('Pengaruh Temp dan Atemp, dan Humidity Terhadap Penyewaan Sepeda')
fig, ax = plt.subplots(figsize=(16, 8))
plt.subplot(1, 3, 1)
sns.scatterplot(
    x='temp',
    y='count',
    color='red',
    data=data_day,
    alpha=0.5
)
plt.title('Temperature dengan Count')
plt.subplot(1, 3, 2)
sns.scatterplot(
    x='atemp',
    y='count',
    color='green',
    data=data_day,
    alpha=0.5
)
plt.title('Feels Like Temperature dengan Count')
plt.subplot(1, 3, 3)
sns.scatterplot(
    x='hum',
    y='count',
    color='blue',
    data=data_day,
    alpha=0.5
)
plt.title('Humidity dengan Count')
st.pyplot(fig)

# Kondisi penyewaan sepeda pada weekday, working day, dan holiday
st.subheader('Kondisi Penyewaan Sepeda pada Weekday, Working Day, dan Holiday')
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15,10))
sns.barplot(
    x='weekday',
    y='count',
    palette='Paired',
    data=data_day,
    ax=axes[0])
axes[0].set_title('Jumlah Penyewaan Sepeda berdasarkan Hari dalam Seminggu')
axes[0].set_xlabel('Hari dalam Seminggu')
axes[0].set_ylabel('Jumlah Penyewaan')
sns.barplot(
    x='workingday',
    y='count',
    palette='Paired',
    data=data_day,
    ax=axes[1])
axes[1].set_title('Jumlah Penyewaan Sepeda berdasarkan Hari Kerja')
axes[1].set_xlabel('Hari Kerja')
axes[1].set_ylabel('Jumlah Penyewaan')
sns.barplot(
    x='holiday',
    y='count',
    palette='Paired',
    data=data_day,
    ax=axes[2])
axes[2].set_title('Jumlah Penyewaan Sepeda berdasarkan Hari Libur')
axes[2].set_xlabel('Hari Libur')
axes[2].set_ylabel('Jumlah Penyewaan')
plt.tight_layout()
st.pyplot(fig)

# Pengaruh musim terhadap penyewa sepeda 
st.subheader('Pengaruh Musim Terhadap Penyewaan Sepeda')
seasonal_rental = data_day.groupby('season')[['registered', 'casual']].sum().reset_index()
fig = plt.figure(figsize=(12, 6))
plt.bar(
    seasonal_rental['season'],
    seasonal_rental['registered'],
    label='Registered',
    color='green',
)
plt.bar(
    seasonal_rental['season'],
    seasonal_rental['casual'],
    label='Casual',
   color='blue',
)
plt.xlabel(None)
plt.ylabel(None)
plt.title('Jumlah Penyewaan Sepeda Berdasarkan Musim')
plt.legend()
st.pyplot(fig)

# Keterkaitan antara kondisi cuaca dan jumlah pengguna sepeda
st.subheader('Keterkaitan Antara Kondisi Cuaca dan Jumlah Pengguna Sepeda')
fig = plt.figure(figsize=(12,6))
sns.barplot(
    x='weather_cond',
    y='count',
    data=data_day,
    palette='Paired')
plt.title('Jumlah Penyewaan Sepeda berdasarkan Kondisi Cuaca')
plt.xlabel('Cuaca')
plt.ylabel('Jumlah Penyewaan Sepeda')
st.pyplot(fig)