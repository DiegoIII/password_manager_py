import customtkinter as ctk
from tkinter import simpledialog, messagebox
from utils.storage import cargar_datos, guardar_datos

def abrir_vista_usuario(app, nombre_usuario):
    for widget in app.winfo_children():
        widget.destroy()

    datos = cargar_datos()
    persona = next((p for p in datos if p["nombre"] == nombre_usuario), None)

    frame = ctk.CTkFrame(app)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    titulo = ctk.CTkLabel(frame, text=f"Sitios de {nombre_usuario}", font=("Arial", 20))
    titulo.pack(pady=10)

    global sitios_frame
    sitios_frame = ctk.CTkScrollableFrame(frame, height=350)
    sitios_frame.pack(pady=10, fill="both", expand=True)

    def crear_label(parent, text, size=14):
        return ctk.CTkLabel(parent, text=text, font=("Arial", size))

    def mostrar_sitios():
        for widget in sitios_frame.winfo_children():
            widget.destroy()

        if not persona["sitios"]:
            crear_label(sitios_frame, "No hay sitios aún.").pack()
            return

        for idx, sitio in enumerate(persona["sitios"]):
            frame_sitio = ctk.CTkFrame(sitios_frame)
            frame_sitio.pack(pady=5, padx=10, fill="x")

            texto = f"🌐 {sitio['sitio']}\n👤 {sitio['usuario']}\n🔒 {sitio['password']}"
            label = crear_label(frame_sitio, texto, size=13)
            label.configure(anchor="w", justify="left")
            label.pack(side="left", fill="x", expand=True, padx=5)

            def editar_sitio(index=idx):
                sitio_actual = persona["sitios"][index]
                nuevo_usuario = simpledialog.askstring("Editar usuario", "Correo o usuario:", initialvalue=sitio_actual["usuario"])
                if nuevo_usuario is None: return
                nueva_contraseña = simpledialog.askstring("Editar contraseña", "Nueva contraseña:", initialvalue=sitio_actual["password"])
                if nueva_contraseña is None: return
                sitio_actual["usuario"] = nuevo_usuario
                sitio_actual["password"] = nueva_contraseña
                guardar_datos(datos)
                mostrar_sitios()

            def eliminar_sitio(index=idx):
                confirm = messagebox.askyesno("Eliminar sitio", f"¿Eliminar '{persona['sitios'][index]['sitio']}'?")
                if confirm:
                    persona["sitios"].pop(index)
                    guardar_datos(datos)
                    mostrar_sitios()

            btn_frame = ctk.CTkFrame(frame_sitio, fg_color="transparent")
            btn_frame.pack(side="right", padx=5)

            editar_btn = ctk.CTkButton(btn_frame, text="✏️ Editar", width=70, height=30, command=editar_sitio)
            editar_btn.pack(pady=2)

            eliminar_btn = ctk.CTkButton(btn_frame, text="🗑️ Eliminar", width=70, height=30, fg_color="red", hover_color="#cc0000", command=eliminar_sitio)
            eliminar_btn.pack(pady=2)

    def agregar_sitio():
        sitio = simpledialog.askstring("Sitio", "Nombre del sitio web:")
        if not sitio: return
        usuario = simpledialog.askstring("Usuario", "Correo o usuario:")
        if not usuario: return
        password = simpledialog.askstring("Contraseña", "Contraseña del sitio:")
        if not password: return
        persona["sitios"].append({"sitio": sitio, "usuario": usuario, "password": password})
        guardar_datos(datos)
        mostrar_sitios()

    mostrar_sitios()

    ctk.CTkButton(frame, text="➕ Agregar sitio", command=agregar_sitio).pack(pady=10)
    ctk.CTkButton(frame, text="⬅️ Volver", command=lambda: from_menu(app)).pack(pady=5)

def from_menu(app):
    from ui.main_menu import launch_main_menu
    launch_main_menu(app)
