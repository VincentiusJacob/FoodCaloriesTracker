import streamlit as st
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

EXPORTS_DIR = Path("exports")
EXPORTS_DIR.mkdir(exist_ok=True)

def export_pdf(df: pd.DataFrame):

    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = EXPORTS_DIR / filename

    doc = SimpleDocTemplate(str(filepath), pagesize=A4, topMargin=0.8*inch, bottomMargin=0.8*inch)
    story = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name="TitleCustom", fontSize=18, textColor=colors.HexColor("#2e3a59"), spaceAfter=12)
    normal = styles["Normal"]

    story.append(Paragraph("Food-Calorie Tracker Report", title_style))
    story.append(Spacer(1, 0.2*inch))

    today_total = df[df["datetime"].dt.date == datetime.now().date()]["total_cal"].sum()
    week_avg    = df[df["datetime"] >= (datetime.now() - pd.Timedelta(days=7))]["total_cal"].mean()
    story.append(Paragraph(f"Today: <b>{today_total:.0f} kcal</b>", normal))
    story.append(Paragraph(f"7-day average: <b>{week_avg:.0f} kcal</b>", normal))
    story.append(Spacer(1, 0.3*inch))

    fig, ax = plt.subplots(figsize=(6, 2.5))
    daily = (
        df[df["datetime"] >= (datetime.now() - pd.Timedelta(days=7))]
        .groupby(df["datetime"].dt.date)["total_cal"]
        .sum()
        .reindex(pd.date_range(datetime.now() - pd.Timedelta(days=6), datetime.now(), freq='D').date, fill_value=0)
    )
    sns.barplot(x=daily.index.astype(str), y=daily.values, ax=ax, color="#667eea")
    ax.set_ylabel("Calories"); ax.set_xlabel("")
    plt.xticks(rotation=45)
    plt.tight_layout()
    img_path = EXPORTS_DIR / "tmp_chart.png"
    plt.savefig(img_path, dpi=150, bbox_inches="tight")
    plt.close()

    story.append(RLImage(str(img_path), width=6*inch, height=2.2*inch))
    story.append(Spacer(1, 0.3*inch))

    recent = df.tail(10)[["datetime", "total_cal"]].copy()
    recent["datetime"] = recent["datetime"].dt.strftime("%d/%m %H:%M")
    data = [["Date-Time", "Calories (kcal)"]] + recent.values.tolist()
    table = Table(data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#667eea")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f7f9fc")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e1e5eb")),
    ]))
    story.append(table)

    doc.build(story)
    img_path.unlink(missing_ok=True)
    return str(filepath)



st.set_page_config(page_title="Food-Calorie Tracker", layout="wide")

pages = {
    "Home": [
        st.Page("home.py", title="Home")
    ],
    "Detection Pages": [
        st.Page("track_calories.py", title="Upload and Track Calories"),
        st.Page("track_calories_realtime.py", title="Real-time Calories Detector"),
    ],
    "Analysis Pages": [
        st.Page("reports.py", title="Reports"),
    ],
}

pg = st.navigation(pages)
pg.run()
