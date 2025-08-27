import customtkinter as ctk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader
import ttkbootstrap as tb
from ttkbootstrap.dialogs.dialogs import FontDialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# ---------------- App Setup ----------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("NoteS Lite")
app.geometry("1000x900")

# ttkbootstrap root (needed for FontDialog)
style = tb.Style()

# ---------------- UI Layout ----------------
frame = ctk.CTkFrame(app, corner_radius=10, height=50)
frame.pack(fill="x", padx=10, pady=10)
frame.pack_propagate(False)

# Buttons
new_btn = ctk.CTkButton(frame, text="New txt File")
new_btn.pack(side="left", padx=5)

open_txt_btn = ctk.CTkButton(frame, text="Open txt File")
open_txt_btn.pack(side="left", padx=5)

save_txt_btn = ctk.CTkButton(frame, text="Save Text")
save_txt_btn.pack(side="left", padx=5)

export_pdf_btn = ctk.CTkButton(frame, text="Export PDF")
export_pdf_btn.pack(side="left", padx=5)

font_btn = ctk.CTkButton(frame, text="Change Font")
font_btn.pack(side="left", padx=5)

import_pdf_btn = ctk.CTkButton(frame, text="Import PDF")
import_pdf_btn.pack(side="left", padx=5)

exit_btn = ctk.CTkButton(frame, text="Exit")
exit_btn.pack(side="right", padx=5)

# Main text area
text_box = ctk.CTkTextbox(app, wrap="word")
text_box.pack(expand=True, fill="both", padx=10, pady=10)

# ---------------- Functions ----------------
def new_file():
    text_box.delete("1.0", ctk.END)

def open_txt_file():
    file = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file:
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                text_box.delete("1.0", ctk.END)
                text_box.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

def save_txt_file():
    file = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text File", "*.txt"), ("All Files", "*.*")]
    )
    if file:
        try:
            data = text_box.get("1.0", "end-1c")
            with open(file, "w", encoding="utf-8") as f:
                f.write(data)
            messagebox.showinfo("Saved", f"Data saved to {file}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

def export_to_pdf():
    file = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF File", "*.pdf"), ("All Files", "*.*")]
    )
    if file:
        try:
            data = text_box.get("1.0", "end-1c")
            c = canvas.Canvas(file, pagesize=A4)
            width, height = A4
            y = height - 50
            for line in data.split("\n"):
                c.drawString(50, y, line)
                y -= 15
                if y < 50:
                    c.showPage()
                    y = height - 50
            c.save()
            messagebox.showinfo("Saved", f"PDF saved to {file}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save PDF: {e}")

def import_pdf_file():
    file = filedialog.askopenfilename(
        title="Select PDF file",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
    )
    if file:
        try:
            pdf_frame = ctk.CTkFrame(app, corner_radius=10)
            pdf_frame.pack(fill="both", expand=True, padx=10, pady=10)

            global pdf_textbox
            pdf_textbox = ctk.CTkTextbox(pdf_frame, wrap="word")
            pdf_textbox.pack(expand=True, fill="both", padx=10, pady=10)

            reader = PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pdf_textbox.insert("end", text + "\n")

            save_pdf_btn = ctk.CTkButton(pdf_frame, text="Save PDF", command=lambda: save_pdf_from_pdfbox(pdf_textbox))
            save_pdf_btn.pack(side="left", padx=5)

        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

def save_pdf_from_pdfbox(pdf_textbox):
    file = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF File", "*.pdf"), ("All Files", "*.*")]
    )
    if file:
        try:
            data = pdf_textbox.get("1.0", "end-1c")
            c = canvas.Canvas(file, pagesize=A4)
            width, height = A4
            y = height - 50
            for line in data.split("\n"):
                c.drawString(50, y, line)
                y -= 15
                if y < 50:
                    c.showPage()
                    y = height - 50
            c.save()
            messagebox.showinfo("Saved", f"PDF saved to {file}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save PDF: {e}")

def change_font():
    dialog = FontDialog()
    dialog.show()
    if dialog.result:
        text_box._textbox.configure(font=dialog.result)

def close_app():
    app.destroy()

# ---------------- Bind Buttons ----------------
new_btn.configure(command=new_file)
open_txt_btn.configure(command=open_txt_file)
save_txt_btn.configure(command=save_txt_file)
export_pdf_btn.configure(command=export_to_pdf)
font_btn.configure(command=change_font)
import_pdf_btn.configure(command=import_pdf_file)
exit_btn.configure(command=close_app)

# ---------------- Run ----------------
app.mainloop()
