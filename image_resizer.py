import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import os

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🖼️ Image Resizer by RS")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        window_width = 500
        window_height = 700
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.img_path = None
        self.original_img = None
        self.resized_img = None

        self.setup_scrollable_frame()
        self.build_ui()

    def setup_scrollable_frame(self):
        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, width=500, height=700, highlightthickness=0, borderwidth=0, bg="#f9f9f9")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ttk.Frame(self.canvas, width=500)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=500)

    def build_ui(self):
        f = self.scrollable_frame

        tk.Label(f, text="Image Resizer", font=("Helvetica", 13)).pack(pady=10)

        self.drop_frame = tk.Label(f, bg="white", width=55, height=8, relief="solid", bd=2)
        self.drop_frame.pack(pady=5)
        self.drop_label = tk.Label(self.drop_frame, text="📂 Drag & Drop Image Here \n Or \n Click Here to Upload Image",
                                   font=("Arial", 12), fg="gray", bg="white")
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")
        self.drop_label = tk.Label(self.drop_frame, text="Drag & Drop Image Here",
                                   font=("Arial", 12), fg="gray", bg="white")
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")
        self.drop_label.place_forget()  # hide drop text once image is loaded
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.drop_file)
        self.drop_frame.bind("<Button-1>", lambda e: self.upload_image())

        # Centered image preview area
        self.image_container = tk.Frame(f, bg="#f9f9f9")
        self.image_container.pack(pady=10)
        self.image_preview_label = tk.Label(self.image_container, bg="#f9f9f9")
        self.image_preview_label.pack(anchor="center")

        # Resize by scale
        tk.Label(f, text="Resize by Scale (e.g. 0.5 = 50%)", font=("Arial", 10)).pack(pady=5)
        self.scale_entry = tk.Entry(f, font=("Arial", 11), justify="center")
        self.scale_entry.insert(0, "0.5")
        self.scale_entry.pack(pady=5)

        tk.Button(f, text="💾 Resize and Save", font=("Arial", 12),
                  bg="#28a745", fg="white", command=self.resize_and_save).pack(pady=15)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp")])
        if file_path:
            self.load_image(file_path)

    def drop_file(self, event):
        file_path = event.data.strip().replace("{", "").replace("}", "")
        if os.path.isfile(file_path):
            self.load_image(file_path)

    def load_image(self, path):
        try:
            self.original_img = Image.open(path)
            self.img_path = path
            self.preview_image(self.original_img)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{e}")

    def preview_image(self, img):
        preview = img.copy()
        preview.thumbnail((450, 300))
        tk_img = ImageTk.PhotoImage(preview)
        self.image_preview_label.configure(image=tk_img)
        self.image_preview_label.image = tk_img

    def resize_and_save(self):
        if not self.original_img:
            messagebox.showerror("No Image", "Please upload an image first.")
            return

        try:
            scale = float(self.scale_entry.get())
            if not 0 < scale < 1:
                raise ValueError
            w, h = self.original_img.size
            new_size = (int(w * scale), int(h * scale))
            img = self.original_img.resize(new_size, Image.ANTIALIAS)

            save_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                     filetypes=[("JPEG", "*.jpg"),
                                                                ("PNG", "*.png"),
                                                                ("All files", "*.*")])
            if save_path:
                img.save(save_path)
                messagebox.showinfo("Saved", f"Image saved to:\n{save_path}")
        except:
            messagebox.showerror("Invalid Input", "Enter a valid scale (e.g. 0.5)")

# Launch the app
if __name__ == "__main__":
    try:
        from tkinterdnd2 import TkinterDnD
    except ImportError:
        print("Install tkinterdnd2: pip install tkinterdnd2")
        exit()

    app = TkinterDnD.Tk()
    ImageResizerApp(app)
    app.mainloop()
