# Food-Calorie Tracker

Detect food, count calories, and track your daily intake in one place – powered by YOLOv8.

---

## 🌟 Demo

📸 Upload image → get instant calorie estimation  
📹 Real-time webcam detection  
📊 Daily & weekly calorie dashboard  
📄 Export clean PDF report

---

## 🚀 Quick Start (local)

1. Clone repo

   ```bash
   git clone https://github.com/VincentiusJacob/FoodCaloriesTracker.git
   cd FoodCaloriesTracker
   ```

2. Install dependencies

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run app
   ```bash
   streamlit run app.py
   ```

---

## 📁 Project Structure

```
FoodCaloriesTracker/
├── app.py
├── home.py                         # landing page
├── track_calories.py               # upload & detect
├── track_calories_realtime.py      # webcam live
├── reports.py                      # daily / weekly summary
├── pdf_report.py                   # export PDF
├── model/final_model_nano.pt       # YOLOv8n weights
├── history/                        # calorie logs
└── exports/                        # PDF output folder
```

---

## 🍽️ Supported Foods

Ayam Goreng, Capcay, Nasi, Sayur Bayam, Sayur Kangkung, Sayur Sop, Tahu, Telur Dadar, Telur Mata Sapi, Telur Rebus, Tempe, Tumis Buncis, food-z7P4

---

## 📝 Usage Flow

1. **Upload** or **real-time webcam**
2. Confirm _“Are you eating this?”_ → saved to history
3. View **daily & weekly** calorie trend
4. **Export PDF** for sharing / archiving

---

> Webcam only works on **HTTPS** domains – allow camera permission when prompted.

---
