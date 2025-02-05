import os
from tkinter import Tk, Button, Label, Entry, END, messagebox, Menu, Text, Canvas, simpledialog, Frame, Scrollbar, \
    StringVar
from PIL import Image, ImageTk
from color_utils import hex_to_rgb
from file_utils import load_image
from menu_bar import MenuBar
from palette_manager import PaletteManager

class UIManager:
    def __init__(self, root):
        self.root = root
        self.input_image = None
        self.color_mapping = {}
        self.palette_manager = PaletteManager()

        # Initialisation de la barre de menu
        self.menu_bar = MenuBar(root)

        # Initialisation de l'interface
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Remplacement de Couleurs d'Image")
        self.root.geometry("1200x800")

        # Étiquette pour afficher le fichier sélectionné
        self.label_image = Label(self.root, text="Aucune image sélectionnée", wraplength=400)
        self.label_image.pack(pady=10)

        # Bouton pour sélectionner une image
        self.button_load = Button(self.root, text="Sélectionner une image", command=self.select_image)
        self.button_load.pack(pady=10)

        # Prévisualisation de l'image
        self.label_image_preview = Label(self.root, bg="white", width=200, height=200)
        self.label_image_preview.pack(pady=10)

        # Champs pour ajouter une correspondance de couleur
        Label(self.root, text="Couleur à remplacer (ex: #cd8580)").pack()
        self.entry_old_color = Entry(self.root, width=20)
        self.entry_old_color.pack()

        Label(self.root, text="Nouvelle couleur (ex: #776466)").pack()
        self.entry_new_color = Entry(self.root, width=20)
        self.entry_new_color.pack()

        self.button_add_color = Button(self.root, text="[+] Ajouter une couleur", command=self.add_color, state="disabled")
        self.button_add_color.pack(pady=10)

        # Widget Text pour afficher les correspondances de couleurs avec prévisualisation
        self.text_colors = Text(self.root, width=60, height=10, wrap="none")
        self.text_colors.pack(pady=10)

        # Gestion des palettes
        Label(self.root, text="Nom de la palette").pack()
        self.entry_palette_name = Entry(self.root, width=20)
        self.entry_palette_name.pack()

        self.button_save_palette = Button(self.root, text="Enregistrer la palette", command=self.save_palette)
        self.button_save_palette.pack(pady=5)

        self.button_load_palette = Button(self.root, text="Charger la palette", command=lambda: self.load_palette_by_name(self.entry_palette_name.get().strip()))
        self.button_load_palette.pack(pady=5)

        # Prévisualisation des palettes avec défilement
        self.frame_palette = Frame(self.root)
        self.frame_palette.pack(side="right", padx=20, pady=10)

        self.canvas_palette = Canvas(self.frame_palette, width=400, height=300, bg="white")
        self.scrollbar_palette = Scrollbar(self.frame_palette, orient="vertical", command=self.canvas_palette.yview)
        self.canvas_palette.configure(yscrollcommand=self.scrollbar_palette.set)

        self.scrollbar_palette.pack(side="right", fill="y")
        self.canvas_palette.pack(side="left", fill="both", expand=True)

        # Activer le défilement avec la molette de la souris
        self.canvas_palette.bind_all("<MouseWheel>", self.on_mousewheel)

        # Menu contextuel pour les actions sur les palettes
        self.selected_palette = StringVar()
        self.palette_context_menu = Menu(self.root, tearoff=0)
        self.palette_context_menu.add_command(label="Charger la palette", command=lambda: self.load_palette_by_name(self.selected_palette.get()))
        self.palette_context_menu.add_command(label="Renommer", command=self.rename_palette)
        self.palette_context_menu.add_command(label="[x] Supprimer", command=self.delete_palette)

        self.canvas_palette.bind("<Button-3>", self.show_palette_context_menu)
        self.canvas_palette.bind("<Button-1>", self.hide_palette_context_menu)
        self.canvas_palette.bind("<Double-Button-1>", self.handle_double_click)

        # Bouton pour appliquer les changements de couleurs (centré)
        self.frame_buttons = Frame(self.root)
        self.frame_buttons.pack(pady=20)
        self.button_apply = Button(self.frame_buttons, text="Appliquer les changements de couleurs", command=self.apply_changes, state="disabled")
        self.button_apply.pack()

        # Lancer l'interface graphique
        self.update_palette_preview()

    def select_image(self):
        try:
            self.input_image = load_image()
            if self.input_image:
                self.label_image.config(text=f"Image sélectionnée : {os.path.basename(self.input_image)}")
                self.button_add_color.config(state="normal")
                self.button_apply.config(state="normal")
                self.display_image_preview(self.input_image)  # Afficher la prévisualisation de l'image
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def display_image_preview(self, image_path):
        try:
            img = Image.open(image_path)
            img.thumbnail((200, 200))  # Redimensionner l'image pour la prévisualisation
            img_tk = ImageTk.PhotoImage(img)
            self.label_image_preview.config(image=img_tk)
            self.label_image_preview.image = img_tk  # Garder une référence pour éviter le garbage collection
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger l'image : {e}")

    def add_color(self):
        old_hex = self.entry_old_color.get().strip()
        new_hex = self.entry_new_color.get().strip()

        if not old_hex or not new_hex:
            messagebox.showerror("Erreur", "Veuillez remplir les deux champs de couleur.")
            return

        try:
            old_rgb = hex_to_rgb(old_hex)
            new_rgb = hex_to_rgb(new_hex)
        except ValueError:
            messagebox.showerror("Erreur", "Code hexadécimal invalide. Utilisez le format #RRGGBB ou RRGGBB.")
            return

        self.color_mapping[old_rgb] = new_rgb
        old_hex = self.ensure_hash(old_hex)
        new_hex = self.ensure_hash(new_hex)

        self.text_colors.insert(END, " ")
        self.text_colors.insert(END, " ", f"old_{len(self.color_mapping)}")
        self.text_colors.tag_configure(f"old_{len(self.color_mapping)}", background=old_hex)
        self.text_colors.insert(END, f" {old_hex} -> ")

        self.text_colors.insert(END, " ")
        self.text_colors.insert(END, " ", f"new_{len(self.color_mapping)}")
        self.text_colors.tag_configure(f"new_{len(self.color_mapping)}", background=new_hex)
        self.text_colors.insert(END, f" {new_hex}\n")

        self.entry_old_color.delete(0, END)
        self.entry_new_color.delete(0, END)

    def save_palette(self):
        palette_name = self.entry_palette_name.get().strip()
        if not palette_name:
            messagebox.showerror("Erreur", "Veuillez entrer un nom pour la palette.")
            return

        hex_mapping = {self.ensure_hash("#{:02x}{:02x}{:02x}".format(*k)): self.ensure_hash("#{:02x}{:02x}{:02x}".format(*v)) for k, v in self.color_mapping.items()}
        self.palette_manager.save_palette(palette_name, hex_mapping)
        self.update_palette_preview()

    def load_palette_by_name(self, palette_name):
        try:
            loaded_mapping = self.palette_manager.load_palette(palette_name)
            self.color_mapping.clear()
            self.text_colors.delete("1.0", END)

            for old_hex, new_hex in loaded_mapping.items():
                old_rgb = hex_to_rgb(old_hex)
                new_rgb = hex_to_rgb(new_hex)
                self.color_mapping[old_rgb] = new_rgb

                self.text_colors.insert(END, " ")
                self.text_colors.insert(END, " ", f"old_{len(self.color_mapping)}")
                self.text_colors.tag_configure(f"old_{len(self.color_mapping)}", background=old_hex)
                self.text_colors.insert(END, f" {old_hex} -> ")

                self.text_colors.insert(END, " ")
                self.text_colors.insert(END, " ", f"new_{len(self.color_mapping)}")
                self.text_colors.tag_configure(f"new_{len(self.color_mapping)}", background=new_hex)
                self.text_colors.insert(END, f" {new_hex}\n")

            messagebox.showinfo("Succès", f"Palette '{palette_name}' chargée.")
        except FileNotFoundError:
            messagebox.showerror("Erreur", f"La palette '{palette_name}' n'existe pas.")

    def delete_palette(self):
        palette_name = self.selected_palette.get()
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
        old_name = self.selected_palette.get()
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

    def update_palette_preview(self):
        self.canvas_palette.delete("all")
        palettes = self.palette_manager.list_palettes()
        y_offset = 10

        for i, palette_name in enumerate(palettes):
            self.canvas_palette.create_text(10, y_offset, text=palette_name, anchor="w", font=("Arial", 10, "bold"))

            try:
                palette_data = self.palette_manager.load_palette(palette_name)
                for j, (old_hex, new_hex) in enumerate(palette_data.items()):
                    self.canvas_palette.create_rectangle(10 + j * 30, y_offset + 20, 20 + j * 30, y_offset + 30, fill=old_hex, outline="")
                    self.canvas_palette.create_rectangle(10 + j * 30, y_offset + 35, 20 + j * 30, y_offset + 45, fill=new_hex, outline="")
            except Exception as e:
                print(f"Erreur lors de la prévisualisation de la palette '{palette_name}': {e}")

            self.canvas_palette.create_line(0, y_offset + 55, 400, y_offset + 55, fill="gray", width=1)
            y_offset += 60

        self.canvas_palette.config(scrollregion=self.canvas_palette.bbox("all"))

    def apply_changes(self):
        if not self.color_mapping:
            messagebox.showerror("Erreur", "Aucune correspondance de couleur définie.")
            return

        self.replace_colors_with_gui(self.input_image, self.color_mapping)

    def replace_colors_with_gui(self, image_path, color_mapping):
        try:
            from PIL import Image
            image = Image.open(image_path).convert("RGBA")
            pixels = image.load()

            width, height = image.size

            for x in range(width):
                for y in range(height):
                    r, g, b, a = pixels[x, y]

                    if a == 0:
                        continue

                    if (r, g, b) in color_mapping:
                        new_r, new_g, new_b = color_mapping[(r, g, b)]
                        pixels[x, y] = (new_r, new_g, new_b, a)

            base_name, ext = os.path.splitext(image_path)
            output_image = f"{base_name}_recolored{ext}"
            image.save(output_image, "PNG")
            messagebox.showinfo("Succès", f"Image sauvegardée sous : {output_image}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def ensure_hash(self, hex_color):
        if not hex_color.startswith("#"):
            hex_color = "#" + hex_color
        return hex_color

    def on_mousewheel(self, event):
        self.canvas_palette.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def show_palette_context_menu(self, event):
        try:
            palette_index = self.canvas_palette.canvasy(event.y) // 60
            palettes = self.palette_manager.list_palettes()
            if 0 <= palette_index < len(palettes):
                self.selected_palette.set(palettes[int(palette_index)])
                self.palette_context_menu.post(event.x_root, event.y_root)
        except Exception:
            pass

    def hide_palette_context_menu(self, event):
        self.palette_context_menu.unpost()

    def handle_double_click(self, event):
        try:
            palette_index = self.canvas_palette.canvasy(event.y) // 60
            palettes = self.palette_manager.list_palettes()
            if 0 <= palette_index < len(palettes):
                palette_name = palettes[int(palette_index)]
                self.load_palette_by_name(palette_name)
        except Exception as e:
            print(f"Erreur lors du double-clic : {e}")