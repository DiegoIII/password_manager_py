import customtkinter as ctk
from tkinter import simpledialog
from utils.storage import cargar_datos, guardar_datos
from ui.user_view import abrir_vista_usuario

# Configuración de estilo (ahora dinámica basada en app.font_settings)
PRIMARY_COLOR = "#2b2d42"
SECONDARY_COLOR = "#8d99ae"
ACCENT_COLOR = "#3a86ff"
HOVER_COLOR = "#457b9d"
DARK_BG = "#1a1a2e"

def get_font(app, size_multiplier=1.0, weight="normal"):
    size = int(app.font_settings["size"] * size_multiplier)
    weight_map = {
        "normal": "",
        "medium": " Medium",
        "bold": " Bold"
    }
    return (app.font_settings["family"] + weight_map.get(weight, ""), size)

def launch_main_menu(app):
    for widget in app.winfo_children():
        widget.destroy()

    app.configure(fg_color=DARK_BG)
    datos = cargar_datos()

    def abrir_usuario(nombre):
        abrir_vista_usuario(app, nombre)

    def agregar_usuario():
        nombre = simpledialog.askstring("Nuevo usuario", "Ingresa un nombre:", parent=app)
        if nombre:
            if any(p["nombre"] == nombre for p in datos):
                ctk.CTkLabel(app, text="⚠️ Usuario ya existe", text_color="orange").pack()
                return
            datos.append({"nombre": nombre, "sitios": []})
            guardar_datos(datos)
            launch_main_menu(app)

    def change_font_size(new_size):
        app.font_settings["size"] = new_size
        launch_main_menu(app)

    # Frame principal
    main_frame = ctk.CTkFrame(app, fg_color="transparent")
    main_frame.pack(pady=40, padx=40, fill="both", expand=True)

    # Barra superior con título y controles
    header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    header_frame.pack(fill="x", pady=(0, 20))

    # Título
    title = ctk.CTkLabel(
        header_frame, 
        text="Gestor de Contraseñas", 
        font=get_font(app, 1.7, "medium"),
        text_color=ACCENT_COLOR
    )
    title.pack(side="left", padx=10)

    # Selector de tamaño de texto
    font_control_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
    font_control_frame.pack(side="right", padx=10)

    ctk.CTkLabel(
        font_control_frame, 
        text="Tamaño texto:", 
        font=get_font(app, 0.9)
    ).pack(side="left", padx=(0, 5))

    font_size = ctk.CTkOptionMenu(
        font_control_frame,
        values=["Pequeño", "Normal", "Grande", "Extra Grande"],
        command=lambda x: change_font_size({
            "Pequeño": 12,
            "Normal": 14,
            "Grande": 16,
            "Extra Grande": 18
        }[x]),
        font=get_font(app, 0.9),
        dropdown_font=get_font(app, 0.9),
        width=20
    )
    font_size.pack(side="left")
    font_size.set({
        12: "Pequeño",
        14: "Normal",
        16: "Grande",
        18: "Extra Grande"
    }.get(app.font_settings["size"], "Normal"))

    # Subtítulo
    subtitle = ctk.CTkLabel(
        main_frame,
        text="Selecciona un usuario o crea uno nuevo",
        font=get_font(app, 1.1),
        text_color=SECONDARY_COLOR
    )
    subtitle.pack(pady=(0, 20))

    # Frame de usuarios
    users_frame = ctk.CTkScrollableFrame(
        main_frame, 
        fg_color=PRIMARY_COLOR,
        scrollbar_button_color=ACCENT_COLOR,
        scrollbar_button_hover_color=HOVER_COLOR,
        corner_radius=10
    )
    users_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Botones de usuarios
    for persona in datos:
        btn = ctk.CTkButton(
            users_frame,
            text=persona["nombre"],
            font=get_font(app, 1.1),
            command=lambda n=persona["nombre"]: abrir_usuario(n),
            fg_color=PRIMARY_COLOR,
            hover_color=HOVER_COLOR,
            border_color=ACCENT_COLOR,
            border_width=1,
            corner_radius=8
        )
        btn.pack(pady=8, padx=10, fill="x")

    # Botón para agregar usuario
    add_btn = ctk.CTkButton(
        main_frame,
        text="➕ Agregar Usuario",
        font=get_font(app, 1.1),
        command=agregar_usuario,
        fg_color=ACCENT_COLOR,
        hover_color=HOVER_COLOR,
        corner_radius=8,
        height=40
    )
    add_btn.pack(pady=20, fill="x", padx=50)