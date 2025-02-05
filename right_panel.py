from tkinter import Frame, Canvas, Scrollbar, Menu, StringVar

class RightPanel:
    def __init__(self, root, parent):
        self.parent = parent  # Instance de UIManager
        self.root = root  # Widget parent Tkinter (Tk ou Frame)

        # Initialisation du panneau droit
        self.setup_right_panel()

    def setup_right_panel(self):
        # Conteneur principal pour le panneau droit
        self.right_frame = Frame(self.root, width=350, bg="white")  # Utiliser self.root ici
        self.right_frame.pack(side="right", fill="both", padx=20, pady=20)

        # Prévisualisation des palettes
        self.canvas_palette = Canvas(self.right_frame, width=330, height=600, bg="white")
        self.scrollbar_palette = Scrollbar(self.right_frame, orient="vertical", command=self.canvas_palette.yview)
        self.canvas_palette.configure(yscrollcommand=self.scrollbar_palette.set)

        self.scrollbar_palette.pack(side="right", fill="y")
        self.canvas_palette.pack(side="left", fill="both", expand=True)

        # Activer le défilement avec la molette de la souris
        self.canvas_palette.bind_all("<MouseWheel>", self.on_mousewheel)

        # Menu contextuel pour les actions sur les palettes
        self.selected_palette = StringVar()
        self.palette_context_menu = Menu(self.root, tearoff=0)  # Utiliser self.root ici
        self.palette_context_menu.add_command(label="Charger la palette", command=lambda: self.parent.load_palette_by_name(self.selected_palette.get()))
        self.palette_context_menu.add_command(label="Renommer", command=self.parent.rename_palette)  # Appel via self.parent
        self.palette_context_menu.add_command(label="[x] Supprimer", command=self.parent.delete_palette)  # Appel via self.parent

        self.canvas_palette.bind("<Button-3>", self.show_palette_context_menu)
        self.canvas_palette.bind("<Button-1>", self.hide_palette_context_menu)
        self.canvas_palette.bind("<Double-Button-1>", self.handle_double_click)

        # NE PAS APPELER update_palette_preview ICI
        # Laisser UIManager gérer cet appel après l'initialisation complète

    def on_mousewheel(self, event):
        self.canvas_palette.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def show_palette_context_menu(self, event):
        try:
            palette_index = self.canvas_palette.canvasy(event.y) // 60
            palettes = self.parent.palette_manager.list_palettes()
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
            palettes = self.parent.palette_manager.list_palettes()
            if 0 <= palette_index < len(palettes):
                palette_name = palettes[int(palette_index)]
                self.parent.load_palette_by_name(palette_name)
        except Exception as e:
            print(f"Erreur lors du double-clic : {e}")