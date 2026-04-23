import sounddevice as sd
import numpy as np
import tkinter as tk
import threading
import time
import textwrap

# ===== Tkinter ウィンドウ設定 =====
root = tk.Tk()
root.title("Mic Level")
root.geometry("60x300")
root.attributes("-topmost", True)

# 画面サイズを完全固定
root.resizable(False, False)
root.minsize(60, 300)
root.maxsize(60, 300)

BG = "#222222"
FG = "#00ff00"

root.configure(bg=BG)

# メインキャンバス（ゲージ + マイク名）
canvas = tk.Canvas(root, width=60, height=260, bg=BG, highlightthickness=0)
canvas.pack(padx=0, pady=20)

# ===== マイク名を縦向きで描画（長い場合は2段） =====
def draw_mic_name(name):
    canvas.delete("mic_text")

    # 長い場合は2段に分割（最大 8 文字 × 2 行）
    if len(name) > 8:
        lines = textwrap.wrap(name, 8)[:2]
    else:
        lines = [name]

    y_positions = {1: [130], 2: [110, 150]}

    for i, line in enumerate(lines):
        canvas.create_text(
            55, y_positions[len(lines)][i],
            text=line,
            fill="white",
            angle=90,
            font=("Arial", 8),
            anchor="e",
            tags="mic_text"
        )

# ===== マイクレベル更新 =====
def update_meter(indata, frames, time_info, status):
    try:
        volume = np.sqrt(np.mean(indata**2))
        level = min(int(volume * 260 * 20), 260)

        # ゲージだけ削除
        canvas.delete("meter")

        # ゲージ描画
        canvas.create_rectangle(
            0, 260 - level, 40, 260,
            fill=FG, width=0, tags="meter"
        )

    except Exception:
        pass

# ===== マイクストリーム管理 =====
def mic_loop():
    while True:
        try:
            # 再接続時に No Mic を消す
            canvas.delete("no_mic")

            # マイク名取得
            dev = sd.query_devices(kind='input')
            mic_name = dev["name"]
            draw_mic_name(mic_name)

            stream = sd.InputStream(callback=update_meter, channels=1, samplerate=44100)
            stream.start()

            while stream.active:
                time.sleep(0.1)

        except Exception:
            # No Mic を表示（タグ付き）
            canvas.delete("meter")
            canvas.delete("mic_text")
            canvas.delete("no_mic")
            canvas.create_text(20, 130, text="No Mic", fill="red", tags="no_mic")
            root.update()
            time.sleep(1)

# ===== 別スレッドでストリーム開始 =====
threading.Thread(target=mic_loop, daemon=True).start()

root.mainloop()
