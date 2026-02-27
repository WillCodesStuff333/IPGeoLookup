import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from IPGeoLocation import GEO_API_Request
from inputValidation import is_valid_ipv4


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IP Lookup")
        self.geometry("700x420")

        bg = "#0f1115"
        panel = "#151924"
        fg = "#e6e6e6"
        border = "#2a3245"
        btn = "#232a3a"
        btn_hover = "#2a3245"

        self.configure(bg=bg)

        frame = tk.Frame(self, bg=panel, bd=1,
                         highlightthickness=1,
                         highlightbackground=border)
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        tk.Label(frame, text="IP Lookup",
                 bg=panel, fg=fg,
                 font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=14, pady=(14, 10))

        row = tk.Frame(frame, bg=panel)
        row.pack(fill="x", padx=14)

        tk.Label(row, text="IP Address:",
                 bg=panel, fg=fg).pack(side="left")

        self.ip_var = tk.StringVar()

        self.entry = tk.Entry(
            row,
            textvariable=self.ip_var,
            bg="#0b0d12",
            fg=fg,
            insertbackground=fg,
            relief="solid",
            bd=1
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(10, 10))
        self.entry.bind("<Return>", lambda e: self.lookup())

        tk.Button(
            row,
            text="Lookup",
            command=self.lookup,
            bg=btn,
            fg=fg,
            activebackground=btn_hover,
            relief="flat",
            padx=12,
            pady=6
        ).pack(side="left")

        self.output = ScrolledText(
            frame,
            wrap="none",  # important for clean centering
            bg="#0b0d12",
            fg=fg,
            insertbackground=fg,
            relief="solid",
            bd=1
        )
        self.output.pack(fill="both", expand=True, padx=14, pady=14)

        # Configure tags
        self.output.tag_configure("center", justify="center")
        self.output.tag_configure("green", foreground="#00ff88")
        self.output.tag_raise("green")

        self.entry.focus_set()

    def lookup(self):
        self.output.delete("1.0", "end")

        ip = self.ip_var.get().strip()

        if not is_valid_ipv4(ip):
            self._insert_line("Invalid IPv4 address")
            return

        try:
            result = GEO_API_Request(ip)

            if isinstance(result, dict):
                for k, v in result.items():
                    self._insert_line(f"{k}: {v}", key_length=len(k))
            else:
                self._insert_line(str(result))

        except Exception as e:
            self._insert_line(f"Error: {e}", key_length=5)

    def _insert_line(self, text, key_length=None):
        # Get concrete start index
        start = self.output.index("end-1c")

        # Insert line
        self.output.insert("end", text + "\n")

        # Get concrete end index
        end = self.output.index("end-1c")

        # Center entire line
        self.output.tag_add("center", start, end)

        # Color key portion if provided
        if key_length:
            key_end = f"{start}+{key_length}c"
            self.output.tag_add("green", start, key_end)


if __name__ == "__main__":
    App().mainloop()