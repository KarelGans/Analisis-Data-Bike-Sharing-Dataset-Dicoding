import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

#styling
st.markdown(
    """
    <style>
        body {
            background-color: white;
            color: black;
        }
        .stApp {
            background-color: white;
            color: black;
        }
        h1, h2, h3, h4, h5, h6, p, div {
            color: black !important;
        }
        [data-testid="stHeader"] {
            background-color: #A0C4FF !important; /* Pastel Blue */
        }
        div[data-baseweb="select"] > div {
        background-color: white !important;
        border: 2px solid black !important;
        border-radius: 5px !important;
    }
    ul {
        background-color: white !important; /* Background color */
        border: 2px solid black !important; /* Black border */
    }
    ul li:hover {
        background-color: lightgray !important; /* Light gray on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Streamlit App Title
st.title("Data Analysis - Bike Sharing Dataset (2011-2012)")

# Load data

df = pd.read_csv("day.csv", delimiter=",")
df['dteday'] = pd.to_datetime(df['dteday'])
df.loc[:, 'year'] = df['dteday'].dt.year
df.loc[:, 'month'] = df['dteday'].dt.month

year_options = df.loc[:, 'year'].unique()
getYearSelection = st.selectbox("Select Year:", year_options, index=0)

df_byYear = df[df['year'] == getYearSelection].copy()
monthly_summary = df_byYear.groupby('month').agg(
    total_cnt=('cnt', 'sum'),  
    count_hours=('cnt', 'count'), 
    windspeed =('windspeed','mean'),
    season=('season', lambda x: x.mode().iloc[0] if not x.mode().empty else None)
).reset_index()
monthly_summary['count_per_hour'] = monthly_summary['total_cnt'] / (monthly_summary['count_hours'])


df2 = pd.read_csv("df2.csv", delimiter=",")
daily_summary = pd.read_csv("daily_summary.csv", delimiter=",")



# Plot 1: Bike Rentals over the Months (2011)
st.subheader("Figure 1 : Bike Rentals over the Months "+"("+str(getYearSelection)+")")
season_colors = {1: "#A0E7E5", 2: "#B4F8C8", 3: "#FFAEBC", 4: "#FBE7C6"}
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_summary['month'], monthly_summary['total_cnt'], marker='o', linestyle='-', color='b', label="Total Rentals")
for i in range(12):
    ax.axvspan(i + 0.5, i + 1.5, color=season_colors[monthly_summary['season'][i]], alpha=0.3)
ax.set_xlabel("Month")
ax.set_ylabel("Total Count")
ax.set_title("Bike Rentals Per Month "+"("+str(getYearSelection)+")")
ax.legend()
ax.grid(True)
fig.text(0.5, -0.05, 
    "Background colors represent seasonal changes:\n"
    "Spring (Light Blue) | Summer (Light Green) | Fall (Pink) | Winter (Peach)",
    wrap=True, horizontalalignment='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))
st.pyplot(fig)


# Plot 2: Correlation Heatmap
st.subheader("Figure 2 : Correlation Heatmap Analysis")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df2.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
ax.set_title("Correlation Heatmap")
st.pyplot(fig)

st.write(
    """
    - Karena data yang digunakan pada dataset ini menyangkut ke kebiasaan, maka saya menggunakan Jacob Cohen's Effect Size Guidelines (1988). Saya ingin mencari kolerasi yang moderate (0.3) dan large (0.5).
    - Dari heatmap ini, saya ingin melihat faktor yang membuat musim memiliki perubahan pada jumlah pengguna. Setelah melihat heatmap, saya menyimpulkan bahwa suhu memiliki kolerasi besar terhadap banyak pengguna.
    """
)

# Plot 3: Scatter Plot 
st.subheader("Figure 3 : Bike Usage Group By Month With Temperature "+"("+str(getYearSelection)+")")
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(df_byYear['mnth'], df_byYear['cnt'], c=df_byYear['temp'], cmap='coolwarm', alpha=0.75)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Normalized Temperature 0-1')
ax.set_xlabel("Month")
ax.set_ylabel("Total Bike Rentals (cnt)")
ax.set_title("Bike Rentals per Month with Temperature Indication "+"("+str(getYearSelection)+")")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
st.pyplot(fig)


# Plot 4: Bar Chart - Casual vs Registered Users by Weekday
st.subheader("Figure 4 : Casual vs Registered Users by Weekday (2011-2022)")
daily_summary = daily_summary.sort_values("weekday").reset_index(drop=True)
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.4
index = np.arange(len(daily_summary['weekday']))
ax.bar(index - bar_width/2, daily_summary['total_casual'], bar_width, label='Casual', color='skyblue')
ax.bar(index + bar_width/2, daily_summary['total_registered'], bar_width, label='Registered', color='salmon')
ax.plot(index, daily_summary['total_cnt'], marker='o', linestyle='-', color='black', label='Total Count')
ax.set_xlabel("Weekday")
ax.set_ylabel("Total Bike Rentals")
ax.set_title("Total Casual vs Registered Bike Rentals by Weekday (2011-2012)")
ax.set_xticks(index)
ax.set_xticklabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.write(
    """
    - Grafik Bike Rentals per Month menunjukan adanya perubahan setiap pergantian musim. Pergantian musim ini memengaruhi suhu, dilihat dari heatmap yang menandakan kolerasi di angka 0.33. Validasi dilakukan ketika membuat grafik Total Rental terhadap bulan dengan menggunakan scatter plot untuk melihat suhu. Alhasil, dapat disimpulkan bahwa jumlah rental sepeda mengalami peningkatan pengguna ketika digunakan pada season dengan suhu lebih hangat.
    - Menurut grafik total casual vs total registered by weekday yang diperoleh, pengguna pada umumnya menggunakan sepeda untuk commute saat bekerja dibandingkan untuk casual. Setelah melihat trend dari grafik, bisa disimpulkan bahwa hari senin dan minggu menjadi hari dimana pengguna tidak menggunakan sepeda untuk bekerja melainkan untuk aktivitas kasual. Namun, penggunaan keseluruhan untuk sepeda mencapai angka 400.000-500.000 sehingga tidak memiliki banyak perubahan secara total untuk perbedaan hari.
    """
    )

st.subheader("Conclusion")
st.write(
    """
    - Kenaikan rental dimulai pada akhir Q1 hingga pertengahan Q3. Hal ini terjadi akibat perubahan musim. Setelah ditinjau lebih lanjut, sepertinya perubahan suhu ketika pergantian musim memiliki dampak yang besar pada penggunaan sepeda.
    - Pada hari jumat, bisnis memiliki rental terbesar dibandingkan hari-hari lainnya. Sepeda sepertinya digunakan untuk bekerja dilihat dari penggunaan yang lebih tinggi di weekdays dibandingkan weekends. Hal ini memberikan analisa bagaimana langkah untuk dapat meningkatkan penggunaan sepeda di hari minggu, sebagai hari yang paling sedikit jumlah pengguna registered bike, namun dengan penggunaan tertinggi untuk casual.
    """
    )
