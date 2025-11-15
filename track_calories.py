import streamlit as st
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from ultralytics import YOLO
import supervision as sv


MODEL_PATH = "./model/final_model_detr.pt"
HISTORY_DIR = Path("history")
EXPORTS_DIR = Path("exports")
HISTORY_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)

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

def save_history(df:pd.DataFrame):
    csv_path = HISTORY_DIR / "history.csv"
    if csv_path.exists():
        df_old = pd.read_csv(csv_path)
        df_final = pd.concat([df_old, df], ignore_index=True)
    else:
        df_final = df
    df_final.to_csv(csv_path, index=False)


st.header("Upload Image & Track Calories")

uploaded = st.file_uploader("Choose Image", type=['png', 'jpg', 'jpeg'])
if uploaded:
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    detections = predict(img_rgb)
    cls_ids = detections.class_id
    counts = np.bincount(cls_ids, minlength=13)
    total_cal = sum(counts[i] * CALORIE[i] for i in range(13))

    box_ann = sv.BoxAnnotator(thickness=2)
    label_ann = sv.LabelAnnotator(text_scale=0.4)
    labels = [f"{cls_names[c]} {conf:.2f}" for c, conf in zip(detections.class_id, detections.confidence)]
    annotated = box_ann.annotate(img_rgb.copy(), detections)
    annotated = label_ann.annotate(annotated, detections, labels)
    st.image(annotated, use_container_width=True, width=100)

    detail = [{"Food": cls_names[i], "Count": counts[i], "Cal/item": CALORIE[i], "Total": counts[i]*CALORIE[i]} for i in range(13) if counts[i]]
    df_show = pd.DataFrame(detail)
    st.dataframe(df_show)
    st.metric("Total Calories", f"{total_cal} kcal")

    if total_cal > 0:
        if st.button("Are you going to eat this?"):
            df_new = pd.DataFrame([{
                "datetime": datetime.now(),
                "total_cal": total_cal,
                **{cls_names[i]: counts[i] for i in range(13)}
            }])
            save_history(df_new)
            st.success("Data Saved!")
    else:
        st.info("No food detected.")

