import tkinter as tk
from tkinter import filedialog, Label, Button
from deepface import DeepFace
import os

def analyze_emotion():
    # Image select karo
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if not file_path:
        return

    # Absolute path
    img_path = os.path.abspath(file_path)

    result_label.config(text="Analyzing...")
    root.update()

    try:
        # DeepFace analyze
        result = DeepFace.analyze(
            img_path=img_path,
            actions=['emotion'],
            enforce_detection=False
        )

        # List/dict handle
        if isinstance(result, list):
            result = result[0]

        emotion = result['dominant_emotion']
        result_label.config(text=f"Detected Emotion: {emotion}")

    except Exception as e:
        print("Real Error:", str(e))
        result_label.config(text="Error detecting emotion")

# GUI Setup
root = tk.Tk()
root.title("AI Emotion Detection App")
root.geometry("400x300")
root.resizable(False, False)

title = Label(root, text="AI Emotion Detector", font=("Arial", 16))
title.pack(pady=20)

btn = Button(root, text="Select Image", command=analyze_emotion, width=20, height=2, bg="#4CAF50", fg="white")
btn.pack(pady=10)

result_label = Label(root, text="", font=("Arial", 14))
result_label.pack(pady=20)

root.mainloop()