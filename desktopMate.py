"""Show the chatbot and handle voice conversations in a desktop window."""

from collections.abc import Callable
from pathlib import Path
import queue
import threading
import time
import tkinter as tk


IMAGE_PATH = Path(__file__).resolve().with_name("chatbot.png")
TRANSPARENT_COLOR = "#01ff01"
IMAGE_SCALE = 3
GREETING = "Hello! I am Lin. আমি বাংলা ও ইংরেজিতে কথা বলতে পারি।"


class DesktopMate:
    def __init__(
        self,
        *,
        listen: Callable[[], str | None],
        respond: Callable[[str], tuple[str, bool]],
        speak: Callable[[str], None],
        shutdown_voice: Callable[[], None],
    ) -> None:
        if not IMAGE_PATH.is_file():
            raise FileNotFoundError(f"Desktop mate image not found: {IMAGE_PATH}")

        self.listen = listen
        self.respond = respond
        self.speak = speak
        self.shutdown_voice = shutdown_voice
        self.messages: queue.Queue[tuple[str, str]] = queue.Queue()
        self.stop_event = threading.Event()
        self.listening_event = threading.Event()
        self.listening_event.set()

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
        self.canvas = tk.Canvas(
            self.root,
            bg=TRANSPARENT_COLOR,
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            width=max(230, self.image.width()),
            height=self.image.height() + 115,
        )
        self.canvas.pack()
        self.canvas.create_image(
            self.canvas.winfo_reqwidth() // 2,
            self.image.height() // 2,
            image=self.image,
        )
        self.status_item = self.canvas.create_text(
            self.canvas.winfo_reqwidth() // 2,
            self.image.height() + 10,
            text="Starting...",
            fill="#102840",
            font=("Segoe UI", 10, "bold"),
            width=self.canvas.winfo_reqwidth() - 12,
            anchor="n",
            justify="center",
        )

        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<Button-3>", self.show_menu)

        self.menu = tk.Menu(self.root, tearoff=False)
        self.menu.add_command(
            label="Pause listening",
            command=self.toggle_listening,
        )
        self.menu.add_command(label="Exit", command=self.root.destroy)
        self.root.protocol("WM_DELETE_WINDOW", self.stop)

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
            self.menu.entryconfigure(
                0,
                label=(
                    "Resume listening"
                    if self.listening_event.is_set()
                    else "Pause listening"
                ),
            )
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def toggle_listening(self) -> None:
        if self.listening_event.is_set():
            self.listening_event.clear()
            self.set_status("Listening paused. Right-click to resume.")
        else:
            self.listening_event.set()
            self.set_status("Listening...")

    def set_status(self, message: str) -> None:
        self.canvas.itemconfigure(self.status_item, text=message[:300])

    def stop(self) -> None:
        self.stop_event.set()
        self.listening_event.set()
        self.root.destroy()

    def process_messages(self) -> None:
        try:
            while True:
                kind, message = self.messages.get_nowait()
                if kind == "status":
                    self.set_status(message[:100])
                elif kind == "exit":
                    self.root.destroy()
                    return
        except queue.Empty:
            pass

        if self.root.winfo_exists():
            self.root.after(100, self.process_messages)

    def voice_loop(self) -> None:
        try:
            self.speak(GREETING)
            while not self.stop_event.is_set():
                if not self.listening_event.wait(timeout=0.2):
                    continue

                self.messages.put(("status", "Listening..."))
                try:
                    user_text = self.listen()
                    if self.stop_event.is_set():
                        break
                    if not user_text:
                        continue

                    self.messages.put(("status", f"You: {user_text}"))
                    answer, should_exit = self.respond(user_text)
                    self.messages.put(("status", f"Lin: {answer}"))
                    self.speak(answer)

                    if should_exit:
                        self.messages.put(("exit", ""))
                        break
                except Exception as exc:
                    print(f"Voice assistant error: {exc}")
                    self.messages.put(
                        ("status", f"Assistant error: {exc}")
                    )
                    time.sleep(1)
        finally:
            self.shutdown_voice()

    def run(self) -> None:
        worker = threading.Thread(target=self.voice_loop, daemon=True)
        worker.start()
        self.root.after(100, self.process_messages)
        self.root.mainloop()
        self.stop_event.set()
        self.listening_event.set()


if __name__ == "__main__":
    from assistant import main

    main()