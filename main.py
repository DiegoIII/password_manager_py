import customtkinter as ctk
from ui.main_menu import launch_main_menu

FONT_SIZE = 14  
FONT_FAMILY = "Roboto"

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Gestor de Contraseñas")
    app.geometry("600x500")
    app.font_settings = {"family": FONT_FAMILY, "size": FONT_SIZE}
    launch_main_menu(app)
    app.mainloop()