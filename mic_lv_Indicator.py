import sounddevice as sd
import numpy as np
import tkinter as tk
import threading
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
    try:
        volume = np.sqrt(np.mean(indata**2))
        level = min(int(volume * 260 * 20), 260)

        canvas.delete("all")
        canvas.create_rectangle(0, 260 - level, 40, 260, fill=FG, width=0)

    except Exception:
        # callback 内で例外が出てもアプリを落とさない
        pass

# ===== マイクストリーム管理 =====
def mic_loop():
    while True:
        try:
            stream = sd.InputStream(callback=update_meter, channels=1, samplerate=44100)
            stream.start()

            # ストリームが動いている間は待機
            while stream.active:
                time.sleep(0.1)

        except Exception:
            # マイク未接続時の表示
            canvas.delete("all")
            canvas.create_text(20, 130, text="No Mic", fill="red")
            root.update()
            time.sleep(1)  # 1秒後に再接続

# ===== 別スレッドでストリーム開始 =====
threading.Thread(target=mic_loop, daemon=True).start()

root.mainloop()
