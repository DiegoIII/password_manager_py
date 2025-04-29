import customtkinter as ctk
from tkinter import simpledialog
from utils.storage import cargar_datos, guardar_datos
from ui.user_view import abrir_vista_usuario

def launch_main_menu(app):
    for widget in app.winfo_children():
        widget.destroy()

    datos = cargar_datos()

    def abrir_usuario(nombre):
        abrir_vista_usuario(app, nombre)

    def agregar_usuario():
        nombre = simpledialog.askstring("Nuevo usuario", "Ingresa un nombre:")
        if nombre:
            if any(p["nombre"] == nombre for p in datos):
                return
            datos.append({"nombre": nombre, "sitios": []})
            guardar_datos(datos)
            launch_main_menu(app)

    title = ctk.CTkLabel(app, text="Usuarios", font=("Arial", 24))
    title.pack(pady=20)

    for persona in datos:
        btn = ctk.CTkButton(app, text=persona["nombre"], command=lambda n=persona["nombre"]: abrir_usuario(n))
        btn.pack(pady=5, padx=20, fill="x")

    add_btn = ctk.CTkButton(app, text="➕ Agregar Usuario", command=agregar_usuario)
    add_btn.pack(pady=20)
