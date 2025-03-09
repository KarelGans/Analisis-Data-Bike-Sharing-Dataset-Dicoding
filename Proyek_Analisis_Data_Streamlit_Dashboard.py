import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

# Custom CSS to set background to white and text to black
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
    </style>
    """,
    unsafe_allow_html=True
)

# Load data
daily_summary = pd.read_csv("daily_summary.csv", delimiter=",")
monthly_summary_2011 = pd.read_csv("monthly_summary_2011.csv", delimiter=",")
monthly_summary_2012 = pd.read_csv("monthly_summary_2012.csv", delimiter=",")
df2 = pd.read_csv("df2.csv", delimiter=",")
df_byYear2011 = pd.read_csv("df_byYear2011.csv", delimiter=",")
df_byYear2012 = pd.read_csv("df_byYear2012.csv", delimiter=",")

# Streamlit App Title
st.title("Data Analysis - Bike Sharing Dataset (2011-2012)")

# Plot 1: Bike Rentals over the Months (2011)
st.subheader("Figure 1 : Bike Rentals over the Months (2011)")
season_colors = {1: "#A0E7E5", 2: "#B4F8C8", 3: "#FFAEBC", 4: "#FBE7C6"}
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_summary_2011['month'], monthly_summary_2011['total_cnt'], marker='o', linestyle='-', color='b', label="Total Rentals")
for i in range(12):
    ax.axvspan(i + 0.5, i + 1.5, color=season_colors[monthly_summary_2011['season'][i]], alpha=0.3)
ax.set_xlabel("Month")
ax.set_ylabel("Total Count")
ax.set_title("Bike Rentals Per Month (2011)")
ax.legend()
ax.grid(True)
fig.text(0.5, -0.05, 
    "Background colors represent seasonal changes:\n"
    "Spring (Light Blue) | Summer (Light Green) | Fall (Pink) | Winter (Peach)",
    wrap=True, horizontalalignment='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))
st.pyplot(fig)

# Plot 2: Bike Rentals per Month (2012)
st.subheader("Figure 2 : Bike Rentals over the Months (2012)")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_summary_2012['month'], monthly_summary_2012['total_cnt'], marker='o', linestyle='-', color='b', label="Total Rentals")
for i in range(12):
    ax.axvspan(i + 0.5, i + 1.5, color=season_colors[monthly_summary_2012['season'][i]], alpha=0.3)
ax.set_xlabel("Month")
ax.set_ylabel("Total Count")
ax.set_title("Bike Rentals Over The Months (2012)")
ax.legend()
ax.grid(True)
fig.text(0.5, -0.05, 
    "Background colors represent seasonal changes:\n"
    "Spring (Light Blue) | Summer (Light Green) | Fall (Pink) | Winter (Peach)",
    wrap=True, horizontalalignment='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))
st.pyplot(fig)


# Plot 3: Correlation Heatmap
st.subheader("Figure 3 : Correlation Heatmap Analysis")
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

# Plot 4: Scatter Plot 1
st.subheader("Figure 4 : Bike Usage Group By Month With Temperature (2011)")
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(df_byYear2011['mnth'], df_byYear2011['cnt'], c=df_byYear2011['temp'], cmap='coolwarm', alpha=0.75)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Normalized Temperature 0-1')
ax.set_xlabel("Month")
ax.set_ylabel("Total Bike Rentals (cnt)")
ax.set_title("Bike Rentals per Month with Temperature Indication (2011)")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
st.pyplot(fig)

# Plot 5: Scatter Plot - Bike Rentals vs. Temperature (2012)
st.subheader("Figure 5 : Bike Usage Group By Month With Temperature (2012)")
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(df_byYear2012['mnth'], df_byYear2012['cnt'], c=df_byYear2012['temp'], cmap='coolwarm', alpha=0.75)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Normalized Temperature 0-1')
ax.set_xlabel("Month")
ax.set_ylabel("Total Bike Rentals (cnt)")
ax.set_title("Bike Rentals per Month with Temperature Indication (2012)")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
st.pyplot(fig)

# Plot 6: Bar Chart - Casual vs Registered Users by Weekday
st.subheader("Figure 6 : Casual vs Registered Users by Weekday (2011-2022)")
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
