import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from pathlib import Path

from app import export_pdf


REPO_ROOT   = Path(__file__).parent
HISTORY_FILE   = REPO_ROOT / "history" / "history.csv"




@st.cache_data(show_spinner=False)
def load_history():
    if not HISTORY_FILE.exists():
        return pd.DataFrame()
    df = pd.read_csv(HISTORY_FILE)
    df["datetime"] = pd.to_datetime(df["datetime"])  
    return df

def save_history(df):
    df.to_csv(HISTORY_FILE, index=False)

df_hist = load_history()


st.header("📊 Daily & Weekly Reports")

if df_hist.empty:
    st.info("No data yet. Start detecting food from the Upload or Real-time page.")
    st.stop()


today = datetime.now().date()
today_df = df_hist[df_hist["datetime"].dt.date == today]
today_total = today_df["total_cal"].sum()
today_avg   = today_df["total_cal"].mean()

col1, col2 = st.columns(2)
col1.metric("Total Calories Today", f"{today_total:.0f} kcal")
col2.metric("Average per Meal",     f"{today_avg:.0f}  kcal")


st.subheader("Last 7 Days Trend")
seven_days = pd.date_range(today - timedelta(days=6), today, freq='D')
daily_tot = (
    df_hist[df_hist["datetime"].dt.date >= (today - timedelta(days=6))]
    .groupby(df_hist["datetime"].dt.date)["total_cal"]
    .sum()
    .reindex(seven_days.date, fill_value=0)
)

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x=daily_tot.index.astype(str), y=daily_tot.values, palette="Blues_d", ax=ax)
ax.set_ylabel("Calories")
ax.set_xlabel("Date")
plt.xticks(rotation=45)
st.pyplot(fig)


st.subheader("Detailed History")
display_df = df_hist.copy()
display_df["date"] = display_df["datetime"].dt.date
display_df["time"] = display_df["datetime"].dt.strftime("%H:%M")
st.dataframe(display_df[["date", "time", "total_cal"] + [c for c in display_df.columns if c.startswith("Telur") or c.startswith("Sayur") or c in {"Capcay", "Tahu", "Tempe", "Tumisbuncis"}]])


st.subheader("Delete a Record")
idx_to_del = st.selectbox("Select row to delete", display_df.index, format_func=lambda x: f"{display_df.loc[x, 'date']} {display_df.loc[x, 'time']} – {display_df.loc[x, 'total_cal']} kcal")
if st.button("Delete", type="secondary"):
    df_hist = df_hist.drop(index=idx_to_del).reset_index(drop=True)
    save_history(df_hist)
    st.success("Deleted!")
    st.rerun()

if st.button("📄 Export PDF Report", type="primary"):
    pdf_path = export_pdf(df_hist)
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="⬇️ Download PDF",
            data=f,
            file_name=Path(pdf_path).name,
            mime="application/pdf"
        )
