"""Графический интерфейс эмулятора (tkinter). Одинаков для всех этапов."""
import tkinter as tk

from shell import ExitShell, ShellError

FONT = ("Courier New", 11)
BG = "#111111"


class App:
    def __init__(self, shell, title, banner=(), script=None):
        self.shell = shell
        self.banner = banner
        self.script = script
        self.history = []
        self.hist_pos = 0

        self.root = tk.Tk()
        self.root.title(title)  # заголовок окна содержит имя VFS
        self.root.geometry("880x540")

        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)
        self.out = tk.Text(frame, bg=BG, fg="#dddddd", font=FONT,
                           state="disabled", wrap="word")
        bar = tk.Scrollbar(frame, command=self.out.yview)
        self.out.config(yscrollcommand=bar.set)
        bar.pack(side="right", fill="y")
        self.out.pack(side="left", fill="both", expand=True)

        row = tk.Frame(self.root, bg=BG)
        row.pack(fill="x")
        self.prompt = tk.Label(row, bg=BG, fg="#77ff77", font=FONT)
        self.prompt.pack(side="left")
        self.entry = tk.Entry(row, bg=BG, fg="#ffffff", font=FONT,
                              insertbackground="#ffffff", relief="flat")
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.bind("<Up>", lambda e: self.browse_history(-1))
        self.entry.bind("<Down>", lambda e: self.browse_history(1))
        self.entry.focus_set()

        self.update_prompt()
        self.root.after(100, self.start)

    def write(self, text):
        self.out.config(state="normal")
        self.out.insert("end", text)
        self.out.see("end")
        self.out.config(state="disabled")

    def update_prompt(self):
        self.prompt.config(text=self.shell.prompt())

    def start(self):
        """Баннер и (если задан) стартовый скрипт."""
        for line in self.banner:
            self.write(line + "\n")
        if self.script:
            try:
                self.shell.run_script(self.script, self.write)
            except ExitShell:
                self.root.destroy()
                return
            except ShellError as e:
                self.write(f"error: {e}\n")
        self.update_prompt()

    def on_enter(self, _event):
        line = self.entry.get()
        self.entry.delete(0, "end")
        if line.strip():
            self.history.append(line)
        self.hist_pos = len(self.history)
        self.write(f"{self.shell.prompt()}{line}\n")
        try:
            out = self.shell.execute(line)
        except ExitShell:
            self.root.destroy()
            return
        except ShellError as e:
            self.write(f"error: {e}\n")
            out = ""
        if out:
            self.write(out + "\n")
        self.update_prompt()

    def browse_history(self, step):
        if not self.history:
            return
        self.hist_pos = max(0, min(len(self.history), self.hist_pos + step))
        self.entry.delete(0, "end")
        if self.hist_pos < len(self.history):
            self.entry.insert(0, self.history[self.hist_pos])

    def run(self):
        self.root.mainloop()
