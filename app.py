"""
app.py
------
GUI(클라이언트) 역할만 담당. 실제 치환 로직은 engine.py, 로그 기록은 logger.py에
완전히 위임한다 (LSP가 에디터와 언어 분석 서버를 분리하는 것과 같은 구조).

실행:
    python app.py
"""

import tkinter as tk
from tkinter import ttk, scrolledtext

from engine import AnonymizerEngine
from logger import RunLogger


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("델파이 코드 조각 익명화 도구")
        root.geometry("1050x720")

        self.engine = AnonymizerEngine()
        self.logger = RunLogger()

        warn = tk.Label(
            root,
            text=(
                "⚠ 결과(아래 '결과' 칸)만 공유하세요. 매핑표와 로그 파일(anonymize_log.txt)에는 "
                "실제 이름이 그대로 들어있으니 절대 외부로 보내지 마세요."
            ),
            fg="#8a6a22",
            wraplength=1000,
            justify="left",
        )
        warn.pack(fill="x", padx=10, pady=(10, 4))

        tk.Label(root, text="입력 (원본 코드 조각)").pack(anchor="w", padx=10)
        self.input_box = scrolledtext.ScrolledText(root, height=10, font=("Consolas", 10), wrap="none")
        self.input_box.pack(fill="x", padx=10, pady=(0, 6))

        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x", padx=10)
        ttk.Button(btn_frame, text="익명화하기", command=self.run).pack(side="left", padx=(0, 6))
        ttk.Button(btn_frame, text="전체 지우기", command=self.clear).pack(side="left")
        ttk.Button(btn_frame, text="로그 파일 보기", command=self.open_log).pack(side="left", padx=(6, 0))
        self.status_var = tk.StringVar()
        tk.Label(btn_frame, textvariable=self.status_var, fg="#6b7280").pack(side="left", padx=10)

        wl_frame = tk.Frame(root)
        wl_frame.pack(fill="x", padx=10, pady=(8, 0))
        tk.Label(wl_frame, text="가리지 않을 이름 (쉼표로 구분):").pack(side="left")
        self.whitelist_entry = tk.Entry(wl_frame)
        self.whitelist_entry.pack(side="left", fill="x", expand=True, padx=(6, 0))

        mid = tk.Frame(root)
        mid.pack(fill="both", expand=True, padx=10, pady=10)

        left = tk.Frame(mid)
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))
        tk.Label(left, text="결과 (공유해도 안전한 코드)").pack(anchor="w")
        self.output_box = scrolledtext.ScrolledText(left, font=("Consolas", 10), wrap="none")
        self.output_box.pack(fill="both", expand=True)
        ttk.Button(left, text="결과 복사", command=self.copy_output).pack(anchor="w", pady=(6, 0))

        right = tk.Frame(mid)
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))
        tk.Label(right, text="매핑표 (본인만 확인용 · 절대 공유 금지)").pack(anchor="w")
        columns = ("placeholder", "original")
        self.tree = ttk.Treeview(right, columns=columns, show="headings", height=18)
        self.tree.heading("placeholder", text="가명")
        self.tree.heading("original", text="원래 값")
        self.tree.column("placeholder", width=90)
        self.tree.column("original", width=280)
        self.tree.pack(fill="both", expand=True)

    def run(self):
        code = self.input_box.get("1.0", "end-1c")
        if not code.strip():
            self.status_var.set("입력이 비어있습니다.")
            return

        whitelist = self.whitelist_entry.get().split(",")
        output, mapping = self.engine.anonymize(code, whitelist)

        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", output)

        for row in self.tree.get_children():
            self.tree.delete(row)
        for placeholder, original in mapping.items():
            self.tree.insert("", "end", values=(placeholder, original))

        run_id = self.logger.log_run(len(code), output, mapping)
        self.status_var.set(f"완료 (run id: {run_id}) — anonymize_log.txt 에 기록됨")

    def clear(self):
        self.input_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.status_var.set("")

    def copy_output(self):
        text = self.output_box.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set("복사됨")

    def open_log(self):
        content = self.logger.read_all()
        win = tk.Toplevel(self.root)
        win.title("익명화 로그 (anonymize_log.txt)")
        win.geometry("750x520")
        box = scrolledtext.ScrolledText(win, font=("Consolas", 9))
        box.pack(fill="both", expand=True)
        box.insert("1.0", content if content else "(아직 로그가 없습니다. '익명화하기'를 먼저 실행해보세요.)")
        box.configure(state="disabled")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()