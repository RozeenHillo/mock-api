# באיזה מערכת הפעלה התמונה תרוץ
FROM python:3.11-slim

# התקנת ספריות OS בסיסיות
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# יצירת תיקייה לאפליקציה
WORKDIR /app

# העתקת כל הפרויקט לתוך התמונה
COPY . /app

# התקנת כל החבילות שמופיעות ב-requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# הפקודה שתורץ כשהקונטיינר יעלה
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
