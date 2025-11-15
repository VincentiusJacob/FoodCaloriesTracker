import streamlit as st
import cv2, pandas as pd, numpy as np
from pathlib import Path
from datetime import datetime
from ultralytics import YOLO
import supervision as sv
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration

MODEL_PATH   = "./model/final_model_nano.pt"
HISTORY_DIR  = Path("history")
HISTORY_DIR.mkdir(exist_ok=True)
CALORIE = {0:260, 1:67, 2:129, 3:36, 4:98, 5:22,
           6:80, 7:93, 8:110, 9:78, 10:225, 11:65, 12:0}

@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH).to("cpu")

model = load_model()
cls_names = model.names

def save_history(df: pd.DataFrame):
    csv_path = HISTORY_DIR / "history.csv"
    if csv_path.exists():
        df_old = pd.read_csv(csv_path)
        df_final = pd.concat([df_old, df], ignore_index=True)
    else:
        df_final = df
    df_final.to_csv(csv_path, index=False)


class VideoTransformer(VideoTransformerBase):
    _cnt = 0
    def __init__(self):
        self.last_cal = 0
        self.last_detections = None

    def recv(self, frame):
        self._cnt += 1
        img = frame.to_ndarray(format="bgr24")

        if self._cnt % 3 == 0:
            img_resized = cv2.resize(img, (416, 416))
            detections = model(img_resized, conf=0.25, verbose=False)[0]
            detections = sv.Detections.from_ultralytics(detections)

            h0, w0 = img.shape[:2]
            detections.xyxy[:, [0, 2]] *= w0 / 416
            detections.xyxy[:, [1, 3]] *= h0 / 416

            self.last_detections = detections
            cls_ids = detections.class_id
            counts = np.bincount(cls_ids, minlength=13)
            self.last_cal = sum(counts[i] * CALORIE[i] for i in range(13))

        if self.last_detections is not None:
            box_ann   = sv.BoxAnnotator(thickness=2)
            label_ann = sv.LabelAnnotator(text_scale=0.45)
            labels = [f"{cls_names[c]} {conf:.2f}" for c, conf in zip(self.last_detections.class_id, self.last_detections.confidence)]
            annotated = box_ann.annotate(img, self.last_detections)
            annotated = label_ann.annotate(annotated, self.last_detections, labels)
        else:
            annotated = img

        from av import VideoFrame
        return VideoFrame.from_ndarray(annotated, format="bgr24")


st.header("📹 Real-Time Calories Detector")

webrtc_ctx = webrtc_streamer(
    key="detection",
    rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}),
    video_processor_factory=VideoTransformer,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,   # non-blocking
)

if webrtc_ctx.video_processor:
    cal = webrtc_ctx.video_processor.last_cal
    st.metric("Current frame calories", f"{cal} kcal")

    if cal > 0:
        if st.button("Save this frame"):
            cls_ids = webrtc_ctx.video_processor.last_detections.class_id
            counts  = np.bincount(cls_ids, minlength=13)
            df_new = pd.DataFrame([{
                "datetime": datetime.now(),
                "total_cal": cal,
                **{cls_names[i]: counts[i] for i in range(13)}
            }])
            save_history(df_new)
            st.success("Frame saved!")
else:
    st.info("Please allow camera access and click START.")