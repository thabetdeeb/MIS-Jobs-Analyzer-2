import customtkinter as ctk
from tkinter import messagebox
import os
import main


EXCEL_FILE = "north_is_jobs_analysis.xlsx"


def run_program():
    try:
        status_label.configure(text="Status: Running...")
        result_label.configure(text="Searching jobs from Drushim and JobMaster...")
        app.update()

        main.main()

        status_label.configure(text="Status: Finished successfully")
        result_label.configure(text="Excel file created successfully from multiple sources")
        open_button.configure(state="normal")

        messagebox.showinfo("Success", "Search finished and Excel file was created")

    except Exception as e:
        status_label.configure(text="Status: Error")
        result_label.configure(text="There was an error while running the search")
        messagebox.showerror("Error", str(e))


def open_excel():
    if os.path.exists(EXCEL_FILE):
        os.startfile(EXCEL_FILE)
    else:
        messagebox.showwarning("Error", "Excel file was not found")


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("MIS Opportunity Hub")
app.geometry("700x450")

title = ctk.CTkLabel(
    app,
    text="MIS Opportunity Hub",
    font=("Arial", 26, "bold")
)
title.pack(pady=25)

subtitle = ctk.CTkLabel(
    app,
    text="Job Search System for Information Systems Graduates in Northern Israel",
    font=("Arial", 15)
)
subtitle.pack(pady=5)

sources_label = ctk.CTkLabel(
    app,
    text="Sources: Drushim + JobMaster",
    font=("Arial", 14)
)
sources_label.pack(pady=5)

run_button = ctk.CTkButton(
    app,
    text="Start Job Search",
    font=("Arial", 16, "bold"),
    width=230,
    height=45,
    command=run_program
)
run_button.pack(pady=25)

status_label = ctk.CTkLabel(
    app,
    text="Status: Ready",
    font=("Arial", 15)
)
status_label.pack(pady=10)

result_label = ctk.CTkLabel(
    app,
    text="",
    font=("Arial", 14)
)
result_label.pack(pady=5)

open_button = ctk.CTkButton(
    app,
    text="Open Excel File",
    font=("Arial", 15),
    width=210,
    height=40,
    command=open_excel,
    state="disabled"
)
open_button.pack(pady=20)

footer = ctk.CTkLabel(
    app,
    text="Final Project - Information Systems",
    font=("Arial", 12)
)
footer.pack(side="bottom", pady=15)

app.mainloop()