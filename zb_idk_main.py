import os
import tkinter as tk

class ZmansiEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("ZB_IDK_MAIN - Zmansi Color Scanner")

        # Path for your local data on breathearn
        self.save_path = os.path.expanduser("~/zmansi_notes.txt")

        # The Zmansi 6-Sign Scheme (RE-ADDED)
        self.scheme = {
            '0': {'bg': 'black', 'fg': 'white', 'desc': 'IDK/Meditation'},
            '.': {'bg': 'red', 'fg': 'white', 'desc': 'Silence'},
            ',': {'bg': 'yellow', 'fg': 'black', 'desc': 'Breath'},
            ';': {'bg': 'green', 'fg': 'white', 'desc': 'Simple'},
            '"': {'bg': 'blue', 'fg': 'white', 'desc': 'Complex'},
            '@': {'bg': 'white', 'fg': 'black', 'desc': 'Zmansi/Camel'}
        }

        # Frame to hold Text + Scrollbar
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill='both')

        self.scrollbar = tk.Scrollbar(frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text = tk.Text(frame, font=("Monospace", 14),
                            bg="#1e1e1e", fg="#888",
                            insertbackground="white", padx=10, pady=10,
                            yscrollcommand=self.scrollbar.set)
        self.text.pack(expand=True, fill='both')
        self.scrollbar.config(command=self.text.yview)

        # Initialize the styles
        for sign, style in self.scheme.items():
            self.text.tag_configure(f"z_{sign}", background=style['bg'], foreground=style['fg'])

        # Load existing notes if they exist
        self.load_on_startup()

        self.text.bind("<KeyRelease>", self.auto_save_and_scan)

    def load_on_startup(self):
        if os.path.exists(self.save_path):
            with open(self.save_path, "r") as f:
                self.text.insert("1.0", f.read())
            self.scan_for_master_sign()  # Color it immediately

    def auto_save_and_scan(self, event=None):
        self.scan_for_master_sign()
        # Silent background save
        with open(self.save_path, "w") as f:
            f.write(self.text.get("1.0", tk.END + "-1c"))

    def scan_for_master_sign(self, event=None):
        # 1. Clear previous tags
        for sign in self.scheme:
            self.text.tag_remove(f"z_{sign}", "1.0", tk.END)

        # 2. Get content
        content = self.text.get("1.0", tk.END + "-1c")
        lines = content.split('\n')

        for i, line_content in enumerate(lines, start=1):
            if not line_content:
                continue

            # Find ALL signs and their positions in this line
            line_triggers = []
            for sign in self.scheme:
                start_search = 0
                while True:
                    idx = line_content.find(sign, start_search)
                    if idx == -1: break
                    line_triggers.append((idx, sign))
                    start_search = idx + 1

            # Sort triggers by their position in the line
            line_triggers.sort()

            last_idx = 0
            for idx, sign in line_triggers:
                # Color from the end of the last segment up to (and including) this sign
                # This matches your image where "silence." is red, but "breath" is not yet
                start_pos = f"{i}.{last_idx}"
                end_pos = f"{i}.{idx + 1}"

                self.text.tag_add(f"z_{sign}", start_pos, end_pos)

                # Move the marker to the character after this sign
                last_idx = idx + 1
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    app = ZmansiEditor(root)
    root.mainloop()