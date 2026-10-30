"""Display chatbot.png as a small, draggable desktop companion."""

from pathlib import Path
import tkinter as tk


IMAGE_PATH = Path(__file__).resolve().with_name("chatbot.png")
TRANSPARENT_COLOR = "#01ff01"
IMAGE_SCALE = 3


class DesktopMate:
    def __init__(self) -> None:
        if not IMAGE_PATH.is_file():
            raise FileNotFoundError(f"Desktop mate image not found: {IMAGE_PATH}")

        self.root = tk.Tk()
        self.root.title("Desktop Mate")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
        self.root.configure(bg=TRANSPARENT_COLOR)
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.image = tk.PhotoImage(file=str(IMAGE_PATH)).subsample(
            IMAGE_SCALE, IMAGE_SCALE
        )
        self.mate = tk.Label(
            self.root,
            image=self.image,
            bg=TRANSPARENT_COLOR,
            bd=0,
            highlightthickness=0,
            cursor="hand2",
        )
        self.mate.pack()

        self.mate.bind("<ButtonPress-1>", self.start_drag)
        self.mate.bind("<B1-Motion>", self.drag)
        self.mate.bind("<Button-3>", self.show_menu)

        self.menu = tk.Menu(self.root, tearoff=False)
        self.menu.add_command(label="Exit", command=self.root.destroy)

        self.root.update_idletasks()
        x = self.root.winfo_screenwidth() - self.root.winfo_width() - 24
        y = self.root.winfo_screenheight() - self.root.winfo_height() - 80
        self.root.geometry(f"+{max(0, x)}+{max(0, y)}")

    def start_drag(self, event: tk.Event) -> None:
        self.drag_offset_x = event.x
        self.drag_offset_y = event.y

    def drag(self, event: tk.Event) -> None:
        x = event.x_root - self.drag_offset_x
        y = event.y_root - self.drag_offset_y
        max_x = max(0, self.root.winfo_screenwidth() - self.root.winfo_width())
        max_y = max(0, self.root.winfo_screenheight() - self.root.winfo_height())
        self.root.geometry(f"+{min(max(0, x), max_x)}+{min(max(0, y), max_y)}")

    def show_menu(self, event: tk.Event) -> None:
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    DesktopMate().run()