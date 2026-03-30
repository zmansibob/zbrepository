import tkinter as tk


class ZmansiEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("ZB_IDK_MAIN - Zmansi Color Scanner")

        # UI Setup: Dark Terminal Style
        self.text = tk.Text(self.root, font=("Monospace", 14),
                            bg="#1e1e1e", fg="#888",
                            insertbackground="white", padx=10, pady=10)
        self.text.pack(expand=True, fill='both')

        # The Zmansi 6-Sign Scheme
        # 0=Black, 1=Red, 2=Yellow, 3=Green, 4=Blue, 5=White
        self.scheme = {
            '0': {'bg': 'black', 'fg': 'white', 'desc': 'IDK/Meditation'},
            '.': {'bg': 'red', 'fg': 'white', 'desc': 'Silence'},
            ',': {'bg': 'yellow', 'fg': 'black', 'desc': 'Breath'},
            ';': {'bg': 'green', 'fg': 'white', 'desc': 'Simple'},
            '"': {'bg': 'blue', 'fg': 'white', 'desc': 'Complex'},
            '@': {'bg': 'white', 'fg': 'black', 'desc': 'Zmansi/Camel'}
        }

        # Initialize the styles
        for sign, style in self.scheme.items():
            self.text.tag_configure(f"z_{sign}", background=style['bg'], foreground=style['fg'])

        self.text.bind("<KeyRelease>", self.scan_for_master_sign)

    def scan_for_master_sign(self, event=None):
        # Clear existing color tags
        for sign in self.scheme:
            self.text.tag_remove(f"z_{sign}", "1.0", tk.END)

        lines = self.text.get("1.0", tk.END).splitlines()

        for i, line_content in enumerate(lines, start=1):
            # Find the absolute FIRST sign in this line
            triggers = []
            for sign in self.scheme:
                idx = line_content.find(sign)
                if idx != -1:
                    triggers.append((idx, sign))

            if triggers:
                # Sort by index to find the 'First' sign
                triggers.sort()
                first_idx, master_char = triggers[0]

                # Apply the theme from that sign to the end of the line
                self.text.tag_add(f"z_{master_char}", f"{i}.{first_idx}", f"{i}.end")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    app = ZmansiEditor(root)
    root.mainloop()