import os
from tkinter import Frame, Label, Button, Entry, Text, messagebox, END
from PIL import Image, ImageTk
from color_utils import hex_to_rgb
from file_utils import load_image

class LeftPanel:
    def __init__(self, root, parent):
        self.parent = parent  # Instance de UIManager
        self.root = root  # Widget parent Tkinter (Tk ou Frame)
        self.input_image = None
        self.color_mapping = {}

        # Initialisation du panneau gauche
        self.setup_left_panel()

    def setup_left_panel(self):
        # Conteneur principal pour le panneau gauche
        self.left_frame = Frame(self.root, width=850, bg="white")  # Utiliser self.root ici
        self.left_frame.pack(side="left", fill="both", padx=20, pady=20)

        # Étiquette pour afficher le fichier sélectionné
        self.label_image = Label(self.left_frame, text="Aucune image sélectionnée", wraplength=400)
        self.label_image.pack(pady=10)

        # Bouton pour sélectionner une image
        self.button_load = Button(self.left_frame, text="Sélectionner une image", command=self.select_image)
        self.button_load.pack(pady=10)

        # Prévisualisation de l'image
        self.label_image_preview = Label(self.left_frame, bg="white", width=200, height=200)
        self.label_image_preview.pack(pady=10)

        # Champs pour ajouter une correspondance de couleur
        Label(self.left_frame, text="Couleur à remplacer (ex: #cd8580)").pack()
        self.entry_old_color = Entry(self.left_frame, width=20)
        self.entry_old_color.pack()

        Label(self.left_frame, text="Nouvelle couleur (ex: #776466)").pack()
        self.entry_new_color = Entry(self.left_frame, width=20)
        self.entry_new_color.pack()

        self.button_add_color = Button(self.left_frame, text="[+] Ajouter une couleur", command=self.add_color, state="disabled")
        self.button_add_color.pack(pady=10)

        # Widget Text pour afficher les correspondances de couleurs avec prévisualisation
        self.text_colors = Text(self.left_frame, width=60, height=10, wrap="none")
        self.text_colors.pack(pady=10)

        # Gestion des palettes
        Label(self.left_frame, text="Nom de la palette").pack()
        self.entry_palette_name = Entry(self.left_frame, width=20)
        self.entry_palette_name.pack()

        self.button_save_palette = Button(self.left_frame, text="Enregistrer la palette", command=self.save_palette)
        self.button_save_palette.pack(pady=5)

        self.button_load_palette = Button(self.left_frame, text="Charger la palette", command=lambda: self.load_palette_by_name(self.entry_palette_name.get().strip()))
        self.button_load_palette.pack(pady=5)

        # Bouton pour appliquer les changements de couleurs
        self.frame_buttons = Frame(self.left_frame)
        self.frame_buttons.pack(pady=20)
        self.button_apply = Button(self.frame_buttons, text="Appliquer les changements de couleurs", command=self.apply_changes, state="disabled")
        self.button_apply.pack()

    def select_image(self):
        try:
            self.input_image = load_image()  # Utiliser directement la fonction load_image
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
        self.parent.palette_manager.save_palette(palette_name, hex_mapping)
        self.parent.update_palette_preview()

    def load_palette_by_name(self, palette_name):
        try:
            loaded_mapping = self.parent.palette_manager.load_palette(palette_name)
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

    def apply_changes(self):
        if not self.color_mapping:
            messagebox.showerror("Erreur", "Aucune correspondance de couleur définie.")
            return

        self.parent.replace_colors_with_gui(self.input_image, self.color_mapping)  # Appel via self.parent

    def ensure_hash(self, hex_color):
        if not hex_color.startswith("#"):
            hex_color = "#" + hex_color
        return hex_color