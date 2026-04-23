import sounddevice as sd
import numpy as np
import tkinter as tk
import time

# ===== Tkinter ウィンドウ設定 =====
root = tk.Tk()
root.title("Mic Level")
root.geometry("60x300")
root.attributes("-topmost", True)
root.resizable(False, False)

BG = "#222222"
FG = "#00ff00"

root.configure(bg=BG)

canvas = tk.Canvas(root, width=40, height=260, bg=BG, highlightthickness=0)
canvas.pack(padx=10, pady=10)

# ===== マイクレベル更新 =====
def update_meter(indata, frames, time_info, status):
    volume = np.sqrt(np.mean(indata**2))
    level = min(int(volume * 260 * 20), 260)

    canvas.delete("all")
    canvas.create_rectangle(0, 260 - level, 40, 260, fill=FG, width=0)

# ===== マイクストリーム管理 =====
stream = None

def start_stream():
    global stream
    while True:
        try:
            stream = sd.InputStream(callback=update_meter, channels=1, samplerate=44100)
            stream.start()
            break  # 成功したら抜ける
        except Exception:
            # マイク未接続など → 1秒後に再試行
            canvas.delete("all")
            canvas.create_text(20, 130, text="No Mic", fill="red")
            root.update()
            time.sleep(1)

# ===== 別スレッドでストリーム開始 =====
import threading
threading.Thread(target=start_stream, daemon=True).start()

root.mainloop()
