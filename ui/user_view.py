import customtkinter as ctk
from tkinter import simpledialog, messagebox
from utils.storage import cargar_datos, guardar_datos

# Configuración de colores
PRIMARY_COLOR = "#2b2d42"
SECONDARY_COLOR = "#8d99ae"
ACCENT_COLOR = "#3a86ff"
HOVER_COLOR = "#457b9d"
DARK_BG = "#1a1a2e"
CARD_BG = "#16213e"
ERROR_COLOR = "#e63946"

def get_font(app, size_multiplier=1.0, weight="normal"):
    """Función para generar fuentes consistentes basadas en la configuración de la app"""
    size = int(app.font_settings["size"] * size_multiplier)
    weight_map = {
        "normal": "",
        "medium": " Medium",
        "bold": " Bold"
    }
    return (app.font_settings["family"] + weight_map.get(weight, ""), size)

def abrir_vista_usuario(app, nombre_usuario):
    for widget in app.winfo_children():
        widget.destroy()

    app.configure(fg_color=DARK_BG)
    datos = cargar_datos()
    persona = next((p for p in datos if p["nombre"] == nombre_usuario), None)

    if not persona:
        messagebox.showerror("Error", "Usuario no encontrado")
        from_menu(app)
        return

    # Frame principal
    main_frame = ctk.CTkFrame(app, fg_color="transparent")
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Encabezado
    header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    header_frame.pack(fill="x")

    # Título
    titulo = ctk.CTkLabel(
        header_frame,
        text=f"🔐 {nombre_usuario}",
        font=get_font(app, 1.6, "medium"),
        text_color=ACCENT_COLOR
    )
    titulo.pack(side="left", padx=10)

    # Controles de la derecha
    controls_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
    controls_frame.pack(side="right")

    # Selector de tamaño de texto
    font_control_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
    font_control_frame.pack(side="left", padx=10)

    ctk.CTkLabel(
        font_control_frame, 
        text="Tamaño:", 
        font=get_font(app, 0.9)
    ).pack(side="left", padx=(0, 5))

    def change_font_size(new_size):
        """Actualiza el tamaño de fuente y recarga la vista"""
        app.font_settings["size"] = new_size
        abrir_vista_usuario(app, nombre_usuario)

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

    # Botón de volver
    back_btn = ctk.CTkButton(
        controls_frame,
        text="⬅️ Volver",
        font=get_font(app, 1.0),
        command=lambda: from_menu(app),
        fg_color="transparent",
        hover_color=PRIMARY_COLOR,
        border_color=SECONDARY_COLOR,
        border_width=1,
        width=80,
        height=30
    )
    back_btn.pack(side="right", padx=10)

    # Subtítulo
    subtitle = ctk.CTkLabel(
        main_frame,
        text="Tus credenciales guardadas",
        font=get_font(app, 1.2),
        text_color=SECONDARY_COLOR
    )
    subtitle.pack(pady=(0, 15))

    # Frame de sitios (scrollable)
    sitios_frame = ctk.CTkScrollableFrame(
        main_frame,
        fg_color=PRIMARY_COLOR,
        scrollbar_button_color=ACCENT_COLOR,
        scrollbar_button_hover_color=HOVER_COLOR,
        corner_radius=10
    )
    sitios_frame.pack(fill="both", expand=True, pady=5)

    def crear_label(parent, text, size_mult=1.0, color="white", weight="normal"):
        """Función helper para crear labels consistentes"""
        return ctk.CTkLabel(
            parent,
            text=text,
            font=get_font(app, size_mult, weight),
            text_color=color,
            anchor="w",
            justify="left"
        )

    def mostrar_sitios():
        """Muestra todas las credenciales guardadas"""
        for widget in sitios_frame.winfo_children():
            widget.destroy()

        if not persona["sitios"]:
            empty_msg = ctk.CTkLabel(
                sitios_frame,
                text="No hay sitios guardados aún.\nHaz clic en 'Agregar sitio' para comenzar.",
                font=get_font(app, 1.1),
                text_color=SECONDARY_COLOR
            )
            empty_msg.pack(pady=40)
            return

        for idx, sitio in enumerate(persona["sitios"]):
            # Tarjeta de sitio
            card_frame = ctk.CTkFrame(
                sitios_frame,
                fg_color=CARD_BG,
                border_color=ACCENT_COLOR,
                border_width=1,
                corner_radius=8
            )
            card_frame.pack(pady=8, padx=5, fill="x")

            # Contenido de la tarjeta
            content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            # Mostrar información del sitio
            sitio_label = crear_label(content_frame, f"🌐 {sitio['sitio']}", 1.2, ACCENT_COLOR, "medium")
            sitio_label.pack(anchor="w")

            usuario_label = crear_label(content_frame, f"👤 {sitio['usuario']}", 1.0)
            usuario_label.pack(anchor="w", pady=(5, 0))

            password_label = crear_label(content_frame, f"🔒 {'•' * 12}", 1.0)
            password_label.pack(anchor="w", pady=(5, 0))

            # Botón para mostrar/ocultar contraseña
            def toggle_password(label, password, btn, index=idx):
                if label.cget("text").endswith(password):
                    label.configure(text=f"🔒 {'•' * 12}")
                    btn.configure(text="👁️ Mostrar")
                else:
                    label.configure(text=f"🔒 {password}")
                    btn.configure(text="👁️ Ocultar")

            show_pass_btn = ctk.CTkButton(
                content_frame,
                text="👁️ Mostrar",
                font=get_font(app, 0.9),
                width=80,
                height=20,
                fg_color="transparent",
                hover_color=PRIMARY_COLOR,
                border_color=SECONDARY_COLOR,
                border_width=1,
                command=lambda l=password_label, p=sitio['password'], b=None, i=idx: toggle_password(l, p, b, i)
            )
            show_pass_btn.pack(anchor="w", pady=(5, 0))

            # Botones de acciones
            btn_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            btn_frame.pack(side="right", padx=5, pady=5)

            def editar_sitio(index=idx):
                sitio_actual = persona["sitios"][index]
                
                # Diálogo para editar usuario
                dialog = ctk.CTkInputDialog(
                    text=f"Editar usuario para {sitio_actual['sitio']}:",
                    title="Editar credencial",
                    font=get_font(app, 1.0)
                )
                nuevo_usuario = dialog.get_input()
                
                if nuevo_usuario is None: return
                
                # Diálogo para editar contraseña
                dialog = ctk.CTkInputDialog(
                    text=f"Nueva contraseña para {sitio_actual['sitio']}:",
                    title="Editar credencial",
                    font=get_font(app, 1.0)
                )
                nueva_contraseña = dialog.get_input()
                
                if nueva_contraseña is None: return
                
                sitio_actual["usuario"] = nuevo_usuario
                sitio_actual["password"] = nueva_contraseña
                guardar_datos(datos)
                mostrar_sitios()

            def eliminar_sitio(index=idx):
                sitio_nombre = persona["sitios"][index]['sitio']
                confirm = messagebox.askyesno(
                    "Confirmar eliminación",
                    f"¿Estás seguro de eliminar '{sitio_nombre}'?",
                    parent=app
                )
                if confirm:
                    persona["sitios"].pop(index)
                    guardar_datos(datos)
                    mostrar_sitios()

            edit_btn = ctk.CTkButton(
                btn_frame,
                text="✏️ Editar",
                font=get_font(app, 1.0),
                width=80,
                height=30,
                fg_color=PRIMARY_COLOR,
                hover_color=HOVER_COLOR
            )
            edit_btn.configure(command=editar_sitio)
            edit_btn.pack(pady=5)

            delete_btn = ctk.CTkButton(
                btn_frame,
                text="🗑️ Eliminar",
                font=get_font(app, 1.0),
                width=80,
                height=30,
                fg_color=ERROR_COLOR,
                hover_color="#d90429",
                text_color="white"
            )
            delete_btn.configure(command=eliminar_sitio)
            delete_btn.pack(pady=5)

    def agregar_sitio():
        """Función para agregar un nuevo sitio"""
        # Diálogo para nombre del sitio
        dialog = ctk.CTkInputDialog(
            text="Nombre del sitio web/app:",
            title="Agregar nueva credencial",
            font=get_font(app, 1.0)
        )
        sitio = dialog.get_input()
        if not sitio: return
        
        # Diálogo para usuario/email
        dialog = ctk.CTkInputDialog(
            text="Correo electrónico o nombre de usuario:",
            title="Agregar nueva credencial",
            font=get_font(app, 1.0)
        )
        usuario = dialog.get_input()
        if not usuario: return
        
        # Diálogo para contraseña
        dialog = ctk.CTkInputDialog(
            text="Contraseña:",
            title="Agregar nueva credencial",
            font=get_font(app, 1.0)
        )
        password = dialog.get_input()
        if not password: return
        
        persona["sitios"].append({
            "sitio": sitio, 
            "usuario": usuario, 
            "password": password
        })
        guardar_datos(datos)
        mostrar_sitios()

    # Mostrar sitios inicialmente
    mostrar_sitios()

    # Botón para agregar sitio
    add_btn = ctk.CTkButton(
        main_frame,
        text="➕ Agregar sitio",
        font=get_font(app, 1.1),
        command=agregar_sitio,
        fg_color=ACCENT_COLOR,
        hover_color=HOVER_COLOR,
        height=40,
        corner_radius=8
    )
    add_btn.pack(pady=20, fill="x", padx=50)

def from_menu(app):
    """Regresa al menú principal"""
    from ui.main_menu import launch_main_menu
    launch_main_menu(app)