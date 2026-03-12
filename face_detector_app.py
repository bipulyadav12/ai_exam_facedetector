import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from deepface import DeepFace
import threading
import time

# ------------------ COLOR MAP ------------------
emotion_colors = {
    "happy": "#00ff00",
    "sad": "#3498db",
    "angry": "#ff0000",
    "surprise": "#f1c40f",
    "fear": "#9b59b6",
    "neutral": "#ffffff",
    "disgust": "#e67e22"
}

# ------------------ MAIN WINDOW ------------------
root = tk.Tk()
root.title("Ultimate Emotion - Developer Bipul Kumar")
root.state("zoomed")  # Full screen maximize
root.configure(bg="#121212")

# ------------------ SPLASH SCREEN ------------------
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

# ------------------ UI ELEMENTS ------------------
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

# ------------------ CAMERA FUNCTION ------------------
running = False

def start_camera():
    global running
    running = True
    cap = cv2.VideoCapture(0)

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
            color = emotion_colors.get(emotion, "#ffffff")

            emotion_label.config(text=f"Emotion: {emotion}", fg=color)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            ).detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)

        except:
            pass

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        video_label.imgtk = img
        video_label.configure(image=img)

    cap.release()

def stop_camera():
    global running
    running = False

# ------------------ PHOTO FUNCTION ------------------
def open_photo():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    img = cv2.imread(file_path)

    result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
    emotion = result[0]['dominant_emotion']
    color = emotion_colors.get(emotion, "#ffffff")

    emotion_label.config(text=f"Emotion: {emotion}", fg=color)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    ).detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 3)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(img))
    video_label.imgtk = img
    video_label.configure(image=img)

# ------------------ MENU ------------------
menu_frame = tk.Frame(root, bg="#1e1e1e")
menu_frame.pack(fill="x")

btn1 = tk.Button(menu_frame, text="Start Live Camera", command=lambda: threading.Thread(target=start_camera).start(), bg="#2c3e50", fg="white")
btn1.pack(side="left", padx=10, pady=10)

btn2 = tk.Button(menu_frame, text="Stop Camera", command=stop_camera, bg="#c0392b", fg="white")
btn2.pack(side="left", padx=10, pady=10)

btn3 = tk.Button(menu_frame, text="Open Photo", command=open_photo, bg="#16a085", fg="white")
btn3.pack(side="left", padx=10, pady=10)

btn4 = tk.Button(menu_frame, text="Exit", command=root.destroy, bg="black", fg="white")
btn4.pack(side="right", padx=10, pady=10)

# ------------------ RUN ------------------
root.mainloop()
