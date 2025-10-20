from tkinter import Tk, messagebox, simpledialog, END

from color_utils import hex_to_rgb
from menu_bar import MenuBar
from left_panel import LeftPanel
from right_panel import RightPanel
from palette_manager import PaletteManager
from PIL import Image
import os

class UIManager:
    def __init__(self, root):
        self.root = root
        self.palette_manager = PaletteManager()

        # Initialisation de la barre de menu
        self.menu_bar = MenuBar(root)

        # Initialisation des panneaux gauche et droit
        self.left_panel = LeftPanel(root, self)  # Passer root comme parent
        self.right_panel = RightPanel(root, self)  # Passer root comme parent

        # Mettre à jour la prévisualisation des palettes après l'initialisation complète
        self.update_palette_preview()

    def update_palette_preview(self):
        self.right_panel.canvas_palette.delete("all")
        palettes = self.palette_manager.list_palettes()
        y_offset = 10

        for i, palette_name in enumerate(palettes):
            self.right_panel.canvas_palette.create_text(10, y_offset, text=palette_name, anchor="w", font=("Arial", 10, "bold"))

            try:
                palette_data = self.palette_manager.load_palette(palette_name)
                for j, (old_hex, new_hex) in enumerate(palette_data.items()):
                    self.right_panel.canvas_palette.create_rectangle(10 + j * 30, y_offset + 20, 20 + j * 30, y_offset + 30, fill=old_hex, outline="")
                    self.right_panel.canvas_palette.create_rectangle(10 + j * 30, y_offset + 35, 20 + j * 30, y_offset + 45, fill=new_hex, outline="")
            except Exception as e:
                print(f"Erreur lors de la prévisualisation de la palette '{palette_name}': {e}")

            self.right_panel.canvas_palette.create_line(0, y_offset + 55, 400, y_offset + 55, fill="gray", width=1)
            y_offset += 60

        self.right_panel.canvas_palette.config(scrollregion=self.right_panel.canvas_palette.bbox("all"))

    def replace_colors_with_gui(self, image_path, color_mapping):
        try:
            image = Image.open(image_path).convert("RGBA")
            pixels = image.load()
            width, height = image.size

            # Paramètre de tolérance (ajustable de 0 à 255)
            tolerance = 30  # Augmentez si trop strict, diminuez si trop permissif

            def is_similar(color1, color2, tol):
                """Vérifie si deux couleurs RGB sont similaires selon la tolérance"""
                r1, g1, b1 = color1
                r2, g2, b2 = color2
                return (abs(r1 - r2) <= tol and
                        abs(g1 - g2) <= tol and
                        abs(b1 - b2) <= tol)

            for x in range(width):
                for y in range(height):
                    r, g, b, a = pixels[x, y]

                    # Ignorer les pixels transparents
                    if a == 0:
                        continue

                    # Chercher une correspondance avec tolérance
                    for original_color, new_color in color_mapping.items():
                        if is_similar((r, g, b), original_color, tolerance):
                            new_r, new_g, new_b = new_color
                            pixels[x, y] = (new_r, new_g, new_b, a)
                            break

            base_name, ext = os.path.splitext(image_path)
            output_image = f"{base_name}_recolored{ext}"
            image.save(output_image, "PNG")
            messagebox.showinfo("Succès", f"Image sauvegardée sous : {output_image}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def load_palette_by_name(self, palette_name):
        try:
            loaded_mapping = self.palette_manager.load_palette(palette_name)
            self.left_panel.color_mapping.clear()
            self.left_panel.text_colors.delete("1.0", END)

            for old_hex, new_hex in loaded_mapping.items():
                old_rgb = hex_to_rgb(old_hex)
                new_rgb = hex_to_rgb(new_hex)
                self.left_panel.color_mapping[old_rgb] = new_rgb

                self.left_panel.text_colors.insert(END, " ")
                self.left_panel.text_colors.insert(END, " ", f"old_{len(self.left_panel.color_mapping)}")
                self.left_panel.text_colors.tag_configure(f"old_{len(self.left_panel.color_mapping)}", background=old_hex)
                self.left_panel.text_colors.insert(END, f" {old_hex} -> ")

                self.left_panel.text_colors.insert(END, " ")
                self.left_panel.text_colors.insert(END, " ", f"new_{len(self.left_panel.color_mapping)}")
                self.left_panel.text_colors.tag_configure(f"new_{len(self.left_panel.color_mapping)}", background=new_hex)
                self.left_panel.text_colors.insert(END, f" {new_hex}\n")

            messagebox.showinfo("Succès", f"Palette '{palette_name}' chargée.")
        except FileNotFoundError:
            messagebox.showerror("Erreur", f"La palette '{palette_name}' n'existe pas.")

    def delete_palette(self):
        palette_name = self.right_panel.selected_palette.get()
        if not palette_name:
            messagebox.showerror("Erreur", "Aucune palette sélectionnée.")
            return

        try:
            os.remove(os.path.join(self.palette_manager.palette_dir, f"{palette_name}.json"))
            self.update_palette_preview()
            messagebox.showinfo("Succès", f"Palette '{palette_name}' supprimée.")
        except FileNotFoundError:
            messagebox.showerror("Erreur", f"La palette '{palette_name}' n'existe pas.")

    def rename_palette(self):
        old_name = self.right_panel.selected_palette.get()
        if not old_name:
            messagebox.showerror("Erreur", "Aucune palette sélectionnée.")
            return

        new_name = simpledialog.askstring("Renommer la palette", "Nouveau nom de la palette :", initialvalue=old_name)
        if not new_name:
            return

        try:
            old_path = os.path.join(self.palette_manager.palette_dir, f"{old_name}.json")
            new_path = os.path.join(self.palette_manager.palette_dir, f"{new_name}.json")
            os.rename(old_path, new_path)
            self.update_palette_preview()
            messagebox.showinfo("Succès", f"Palette renommée de '{old_name}' à '{new_name}'.")
        except FileNotFoundError:
            messagebox.showerror("Erreur", f"La palette '{old_name}' n'existe pas.")
        except FileExistsError:
            messagebox.showerror("Erreur", f"Une palette avec le nom '{new_name}' existe déjà.")