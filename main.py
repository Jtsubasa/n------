import tkinter as tk
from tkinter import ttk, messagebox

class CountUpTimer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("n進数タイマー")
        self.window.config(padx=20, pady=20, bg="#87cefa")
        self.window.geometry("1000x400+0+0")

        self.bases = [10, 10, 10]  # 3つのタイマーの進数
        self.timers_running = False  # 開始、停止を区別するフラグ
        self.timer_values = [0, 0, 0]  # 3つのタイマー初期値
        self.timer_labels = []
        self.settings_window_open = False  # 設定ウィンドウを余分に開かないためのフラグ
        self.setup_ui()

    def setup_ui(self):
        # フォント
        TITLE_FONT = ("Helvetica", 28, "bold")
        TIMER_FONT = ("Helvetica", 64, "bold")
        BUTTON_FONT = ("Helvetica", 14, "bold")
        MAIN_COLOR = "#4169e1"
        SECONDARY_COLOR = "#7fffd4"
        ACCENT_COLOR = "#ff7f50"
        
        self.title_label = tk.Label(text="n進数タイマー", fg=MAIN_COLOR, bg="#87cefa", font=TITLE_FONT)
        self.title_label.pack()

        # タイマーフレームのコンテナ
        self.timer_frame_container = tk.Frame(self.window, bg="#87cefa")
        self.timer_frame_container.pack(pady=20)

        # タイマーフレームのラベル
        for i in range(3):
            frame = tk.Frame(self.timer_frame_container, bg="#0000cd", bd=2, relief="raised")
            frame.pack(side=tk.LEFT, padx=10)
            label = tk.Label(frame, text="000", fg=MAIN_COLOR, bg="#0000cd", font=TIMER_FONT, width=5)  # Fixed width
            label.pack(pady=20)
            self.timer_labels.append(label)

        # ボタン群
        self.button_frame = tk.Frame(self.window, bg="#87cefa")
        self.button_frame.pack(pady=20)

        # ボタンたち
        self.start_button = tk.Button(self.button_frame, text="開始", padx=30, pady=10, command=self.start_timers, font=BUTTON_FONT, bg=SECONDARY_COLOR, width=10)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="停止", padx=30, pady=10, command=self.stop_timers, font=BUTTON_FONT, bg=SECONDARY_COLOR, width=10)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(self.button_frame, text="リセット", padx=30, pady=10, command=self.reset_timers, font=BUTTON_FONT, bg=SECONDARY_COLOR, width=10)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.option_button = tk.Button(self.button_frame, text="設定", padx=30, pady=10, command=self.option_setup, font=BUTTON_FONT, bg=ACCENT_COLOR, width=10)
        self.option_button.pack(side=tk.LEFT, padx=5)

    def start_timers(self):
        if not self.timers_running:
            self.timers_running = True
            self.start_button.config(state=tk.DISABLED) 
            self.update_timers()

    def stop_timers(self):
        self.timers_running = False
        self.start_button.config(state=tk.NORMAL)

    def reset_timers(self):
        self.timers_running = False
        self.timer_values = [0, 0, 0]
        self.update_timer_labels()
        self.start_button.config(state=tk.NORMAL)

    def update_timers(self):
        if self.timers_running:
            for i in range(3):
                self.timer_values[i] += 1
                if self.timer_values[i] >= self.bases[i] ** 3:
                    self.timer_values[i] = 0
            self.update_timer_labels()
            self.window.after(1000, self.update_timers)

    def update_timer_labels(self):
        for i, label in enumerate(self.timer_labels):
            value = self.timer_values[i]
            label.config(text=self.convert_to_base(value, self.bases[i]))

    def convert_to_base(self, value, base):
        chars = "0123456789ABCDEF"
        result = ""
        for _ in range(3):
            result = chars[value % base] + result
            value //= base
        return result.zfill(3)

    def option_setup(self):
        if self.settings_window_open:
            return

        self.settings_window_open = True

        settings_window = tk.Toplevel(self.window)
        settings_window.title("設定")
        settings_window.config(bg="#87cefa")
        settings_window.geometry("450x300+0+400")

        settings_window.protocol("WM_DELETE_WINDOW", lambda: self.close_settings_window(settings_window))

        LABEL_FONT = ("Helvetica", 18)
        BUTTON_FONT = ("Helvetica", 14, "bold")
        ACCENT_COLOR = "#ff7f50"

        label = tk.Label(settings_window, text="各タイマーの進数を設定してください。", font=LABEL_FONT, bg="#87cefa")
        label.grid(row=0, column=0, columnspan=3, pady=10)

        base_selectors = []
        for i in range(3):
            timer_label = tk.Label(settings_window, text=f"タイマー {i+1} の進数: ", font=LABEL_FONT, bg="#87cefa")
            timer_label.grid(row=i + 1, column=0, padx=10, pady=10)

            base_options = [str(n) for n in range(2, 17)] 
            base_selector = ttk.Combobox(settings_window, values=base_options, font=("Helvetica", 14), width=5)
            base_selector.set(str(self.bases[i]))
            base_selector.grid(row=i + 1, column=1, padx=10, pady=10)
            base_selectors.append(base_selector)

        apply_button = tk.Button(settings_window, text="決定", command=lambda: self.apply_settings(base_selectors, settings_window), font=BUTTON_FONT, bg=ACCENT_COLOR)
        apply_button.grid(row=4, column=0, columnspan=3, pady=20)

    def close_settings_window(self, window):
        self.settings_window_open = False 
        window.destroy()
    
    def apply_settings(self, selectors, window):
        try:
            for i, selector in enumerate(selectors):
                base = int(selector.get())
                if base < 2 or base > 16:
                    raise ValueError
                self.bases[i] = base
            self.close_settings_window(window)
        except ValueError:
            messagebox.showerror("入力エラー", "2から16の間の数値を入力してください。")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    timer = CountUpTimer()
    timer.run()