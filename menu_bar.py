from tkinter import Menu, Toplevel, Label

class MenuBar:
    def __init__(self, root):
        self.root = root
        self.menu_bar = Menu(root)
        self.setup_menu()

    def setup_menu(self):
        # Créer le menu "Fichier"
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Quitter", command=self.root.quit)
        self.menu_bar.add_cascade(label="Fichier", menu=file_menu)

        # Créer le menu "Info"
        info_menu = Menu(self.menu_bar, tearoff=0)
        info_menu.add_command(label="Instructions", command=self.show_instructions)
        self.menu_bar.add_cascade(label="Info", menu=info_menu)

        # Configurer la barre de menu
        self.root.config(menu=self.menu_bar)

    def show_instructions(self):
        """
        Affiche une fenêtre modale avec les instructions du logiciel.
        """
        instructions_window = Toplevel(self.root)
        instructions_window.title("Instructions")
        instructions_window.geometry("600x400")
        instructions_window.resizable(False, False)

        # Contenu des instructions
        instructions_text = """
        Bienvenue dans notre outil de remplacement de couleurs !

        Instructions :
        1. Sélectionnez une image en cliquant sur "Sélectionner une image".
        2. Ajoutez des correspondances de couleurs :
           - Entrez la couleur à remplacer (ex: #cd8580).
           - Entrez la nouvelle couleur (ex: #776466).
           - Cliquez sur "[+] Ajouter une couleur".
        3. Enregistrez votre palette de couleurs en entrant un nom et en cliquant sur "Enregistrer la palette".
        4. Chargez une palette existante en entrant son nom et en cliquant sur "Charger la palette".
        5. Appliquez les changements de couleurs en cliquant sur "Appliquer les changements de couleurs".

        Autres fonctionnalités :
        - Renommez ou supprimez une palette via le menu contextuel (clic droit) dans la prévisualisation des palettes.
        - Double-cliquez sur une palette pour la charger directement.

        Merci d'utiliser notre logiciel !
        """

        label_instructions = Label(instructions_window, text=instructions_text, justify="left", wraplength=580, padx=10, pady=10)
        label_instructions.pack(expand=True, fill="both")