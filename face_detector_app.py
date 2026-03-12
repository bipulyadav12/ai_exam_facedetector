import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from deepface import DeepFace
import threading
import time

# ---------------- COLOR MAP ----------------
emotion_colors = {
    "happy": "#00ff00",
    "sad": "#3498db",
    "angry": "#ff0000",
    "surprise": "#f1c40f",
    "fear": "#9b59b6",
    "neutral": "#ffffff",
    "disgust": "#e67e22"
}

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Ultimate Emotion - Developer Bipul Kumar")
root.state("zoomed")
root.configure(bg="#121212")

# ---------------- SPLASH SCREEN ----------------
splash = tk.Toplevel()
splash.state("zoomed")
splash.configure(bg="black")

label = tk.Label(
    splash,
    text="Ultimate Emotion App\n\nDeveloper - Bipul Kumar",
    font=("Arial", 40, "bold"),
    fg="white",
    bg="black"
)
label.pack(expand=True)

root.withdraw()
root.update()
time.sleep(2)

splash.destroy()
root.deiconify()

# ---------------- UI ----------------
video_label = tk.Label(root, bg="black")
video_label.pack(expand=True)

emotion_label = tk.Label(
    root,
    text="Emotion: ",
    font=("Arial", 25, "bold"),
    fg="white",
    bg="#121212"
)
emotion_label.pack()

# ---------------- VARIABLES ----------------
running = False
cap = None
frame_count = 0

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# ---------------- CAMERA ----------------
def start_camera():
    global running, cap, frame_count

    running = True
    cap = cv2.VideoCapture(0)

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        try:
            # Run AI every 5 frames (faster)
            if frame_count % 5 == 0:
                result = DeepFace.analyze(
                    frame,
                    actions=['emotion'],
                    enforce_detection=False
                )

                emotion = result[0]['dominant_emotion']
                color = emotion_colors.get(emotion, "#ffffff")

                emotion_label.config(
                    text=f"Emotion: {emotion}",
                    fg=color
                )

        except Exception as e:
            print("AI Error:", e)

        # Face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            1.3,
            5
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                3
            )

        # Convert to Tkinter format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = ImageTk.PhotoImage(Image.fromarray(frame))

        video_label.imgtk = img
        video_label.configure(image=img)

    if cap:
        cap.release()

# ---------------- STOP CAMERA ----------------
def stop_camera():
    global running, cap

    running = False

    if cap:
        cap.release()
        cap = None

# ---------------- PHOTO DETECTION ----------------
def open_photo():

    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    img = cv2.imread(file_path)

    try:
        result = DeepFace.analyze(
            img,
            actions=['emotion'],
            enforce_detection=False
        )

        emotion = result[0]['dominant_emotion']
        color = emotion_colors.get(emotion, "#ffffff")

        emotion_label.config(
            text=f"Emotion: {emotion}",
            fg=color
        )

    except Exception as e:
        print("Photo AI Error:", e)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        1.3,
        5
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(
            img,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = ImageTk.PhotoImage(Image.fromarray(img))

    video_label.imgtk = img
    video_label.configure(image=img)

# ---------------- MENU ----------------
menu = tk.Frame(root, bg="#1e1e1e")
menu.pack(fill="x")

start_btn = tk.Button(
    menu,
    text="Start Live Camera",
    command=lambda: threading.Thread(target=start_camera).start(),
    bg="#2c3e50",
    fg="white"
)
start_btn.pack(side="left", padx=10, pady=10)

stop_btn = tk.Button(
    menu,
    text="Stop Camera",
    command=stop_camera,
    bg="#c0392b",
    fg="white"
)
stop_btn.pack(side="left", padx=10, pady=10)

photo_btn = tk.Button(
    menu,
    text="Open Photo",
    command=open_photo,
    bg="#16a085",
    fg="white"
)
photo_btn.pack(side="left", padx=10, pady=10)

exit_btn = tk.Button(
    menu,
    text="Exit",
    command=root.destroy,
    bg="black",
    fg="white"
)
exit_btn.pack(side="right", padx=10, pady=10)

# ---------------- RUN ----------------
root.mainloop()
