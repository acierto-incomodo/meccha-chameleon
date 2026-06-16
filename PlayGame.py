import tkinter as tk
from tkinter import messagebox
import json
import os
import subprocess
import sys

def get_base_path():
    """
    Obtiene la ruta del directorio base. 
    Funciona tanto ejecutando el .py directamente como tras convertirlo en .exe con PyInstaller.
    """
    if getattr(sys, 'frozen', False):
        # Si es un ejecutable de PyInstaller, el .exe está en el directorio sys.executable
        return os.path.dirname(sys.executable)
    # Si es un script .py, usamos el archivo actual
    return os.path.dirname(os.path.abspath(__file__))

def is_dark_mode():
    """
    Detecta si el sistema operativo (Windows) está en modo oscuro.
    """
    try:
        if sys.platform == "win32":
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
    except:
        pass
    return False

def launch_exe(relative_path):
    """
    Construye la ruta completa y ejecuta el programa.
    """
    base_dir = get_base_path()
    
    # Limpiamos la ruta del JSON (quitamos el '/' inicial si existe para unir correctamente)
    clean_rel_path = relative_path.lstrip('/')
    full_path = os.path.normpath(os.path.join(base_dir, clean_rel_path))

    if not os.path.exists(full_path):
        messagebox.showerror("Error", f"No se pudo encontrar el ejecutable en:\n{full_path}")
        return

    try:
        # Establecer el directorio de trabajo (cwd) es fundamental para que el juego 
        # cargue sus dependencias y recursos correctamente.
        subprocess.Popen(full_path, cwd=os.path.dirname(full_path))
    except Exception as e:
        messagebox.showerror("Error de ejecución", f"Ocurrió un error al intentar abrir el juego:\n{e}")

def main():
    base_dir = get_base_path()
    dark_mode = is_dark_mode()

    # Configuración de colores
    if dark_mode:
        bg_color = "#1e1e1e"
        fg_color = "#ffffff"
        button_bg = "#333333"
        secondary_fg = "#aaaaaa"
    else:
        bg_color = "#f0f0f0"
        fg_color = "#000000"
        button_bg = "#e0e0e0"
        secondary_fg = "#555555"

    root = tk.Tk()
    root.title("Lanzador de Plague Inc")
    root.geometry("450x600")
    root.resizable(False, False)
    root.configure(bg=bg_color)

    # Intentar cargar icono con el mismo nombre que el programa (PlayGame)
    icon_name = "PlayGame"
    for ext in [".ico", ".png"]:
        icon_path = os.path.join(base_dir, icon_name + ext)
        if os.path.exists(icon_path):
            try:
                if ext == ".ico":
                    root.iconbitmap(icon_path)
                else:
                    icon_img = tk.PhotoImage(file=icon_path)
                    root.iconphoto(True, icon_img)
                break
            except Exception:
                pass

    json_path = os.path.join(base_dir, "PlayGame.json")

    # Carga de configuración
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            game_modes = json.load(f)
            
        # Usar el campo "id" del primer objeto como título de la ventana y removerlo de la lista de modos
        if game_modes and "id" in game_modes[0]:
            root.title(game_modes[0]["id"])
            game_modes = game_modes[1:]

    except Exception as e:
        messagebox.showerror("Error de Configuración", f"No se pudo cargar PlayGame.json:\n{e}")
        return

    # Título de la GUI
    tk.Label(root, text="Plague Inc: Evolved Launcher", font=("Segoe UI", 16, "bold"), bg=bg_color, fg=fg_color).pack(pady=20)
    tk.Label(root, text="Selecciona un modo para iniciar:", font=("Segoe UI", 10), bg=bg_color, fg=fg_color).pack(pady=5)

    # Lista para mantener referencia de las imágenes y evitar que el recolector de basura las borre
    root.images = []

    # Generación dinámica de botones basada en el JSON
    for mode in game_modes:
        name = mode.get("name", "Modo")
        desc = mode.get("description", "")
        path = mode.get("path", "")
        img_path = mode.get("image", "")

        # Contenedor para cada opción
        frame = tk.Frame(root, bg=bg_color)
        frame.pack(pady=15, fill="x", padx=50)

        # Cargar imagen si existe
        if img_path:
            full_img_path = os.path.normpath(os.path.join(base_dir, img_path.lstrip('/')))
            if os.path.exists(full_img_path):
                try:
                    # Nota: PhotoImage soporta PNG en versiones modernas de Python/Tkinter
                    img = tk.PhotoImage(file=full_img_path)
                    # Redimensionar si es necesario (opcional, ej: img = img.subsample(2, 2))
                    img_label = tk.Label(frame, image=img, bg=bg_color)
                    img_label.pack(pady=5)
                    root.images.append(img) # Guardar referencia
                except Exception:
                    pass

        btn = tk.Button(
            frame, 
            text=f"Iniciar {name}", 
            font=("Segoe UI", 11, "bold"),
            command=lambda p=path: launch_exe(p),
            bg=button_bg,
            fg=fg_color,
            activebackground=fg_color,
            activeforeground=bg_color,
            relief="flat",
            cursor="hand2"
        )
        btn.pack(fill="x")
        tk.Label(frame, text=desc, font=("Segoe UI", 9), bg=bg_color, fg=secondary_fg).pack(pady=2)

    # Centrar ventana
    root.update_idletasks()
    root.eval('tk::PlaceWindow . center')
    root.mainloop()

if __name__ == "__main__":
    main()