import streamlit as st
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from ultralytics import YOLO
import supervision as sv

REPO_ROOT   = Path(__file__).parent
MODEL_PATH  = REPO_ROOT / "model" / "final_model_detr.pt"
HISTORY_DIR = REPO_ROOT / "history"
EXPORTS_DIR = REPO_ROOT / "exports"

HISTORY_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)
CSV_PATH    = HISTORY_DIR / "history.csv"

CALORIE = {0:260, 1:67, 2:129, 3:36, 4:98, 5:22, 6:80, 7:93, 8:110, 9:78, 10:225, 11:65, 12:0}

@st.cache_resource
def load_model():
    model = YOLO(MODEL_PATH)
    return model

model = load_model()
cls_names = model.names

def predict(image):
    result = model(image, conf=0.30)[0]
    return sv.Detections.from_ultralytics(result)

def load_history() -> pd.DataFrame:
    """Load history from CSV with error handling"""
    if not CSV_PATH.exists():
        return pd.DataFrame()
    try:
        df = pd.read_csv(CSV_PATH)
        if 'datetime' in df.columns:
            df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading history: {e}")
        return pd.DataFrame()

def save_history(new_row: dict):
    """Save a single row to history CSV"""
    df_old = load_history()
    df_new = pd.DataFrame([new_row])
    
    df_final = pd.concat([df_old, df_new], ignore_index=True)
    
    try:
        df_final.to_csv(CSV_PATH, index=False)
        st.success("Data saved successfully!")
    except Exception as e:
        st.error(f"Failed to save data: {e}")

st.header("📷 Upload Image & Track Calories")

uploaded = st.file_uploader("Choose Image", type=["png", "jpg", "jpeg"])
if uploaded:
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    detections = predict(img_rgb)
    cls_ids  = detections.class_id
    counts   = np.bincount(cls_ids, minlength=13)
    total_cal = sum(counts[i] * CALORIE[i] for i in range(13))

    box_ann   = sv.BoxAnnotator(thickness=2)
    label_ann = sv.LabelAnnotator(text_scale=0.4)
    labels = [f"{cls_names[c]} {conf:.2f}" for c, conf in zip(detections.class_id, detections.confidence)]
    annotated = label_ann.annotate(box_ann.annotate(img_rgb.copy(), detections), detections, labels)
    st.image(annotated, use_container_width=True)

    detail = [
        {"Food": cls_names[i], "Count": counts[i],
         "Cal/item": CALORIE[i], "Total": counts[i] * CALORIE[i]}
        for i in range(13) if counts[i]
    ]
    df_show = pd.DataFrame(detail)
    st.dataframe(df_show, use_container_width=True)
    st.metric("Total Calories", f"{total_cal} kcal")

    if total_cal > 0 and st.button("Are you going to eat this?"):
        row = {
            "datetime": datetime.now(),
            "total_cal": total_cal
        }

        for i in range(13):
            row[cls_names[i]] = counts[i]

        save_history(row)
        # st.rerun()  
