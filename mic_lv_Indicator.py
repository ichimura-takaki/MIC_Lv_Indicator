import sounddevice as sd
import numpy as np
import tkinter as tk

# ===== Tkinter ウィンドウ設定 =====
root = tk.Tk()
root.title("Mic Level")
root.geometry("60x300")  # 縦長ウィンドウ
root.attributes("-topmost", True)  # 最前面
root.resizable(False, False)

BG = "#222222"
FG = "#00ff00"

root.configure(bg=BG)

canvas = tk.Canvas(root, width=40, height=260, bg=BG, highlightthickness=0)
canvas.pack(padx=10, pady=10)

# ===== マイクレベル更新 =====
def update_meter(indata, frames, time_info, status):
    volume = np.sqrt(np.mean(indata**2))  # RMS
    level = min(int(volume * 260 * 20), 260)  # バーの高さに変換

    canvas.delete("all")
    # 下から上に伸びる縦バー
    canvas.create_rectangle(0, 260 - level, 40, 260, fill=FG, width=0)

# ===== マイクストリーム開始 =====
stream = sd.InputStream(callback=update_meter, channels=1, samplerate=44100)
stream.start()

root.mainloop()
