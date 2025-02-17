from tkinter import Frame, Label, Button, Entry, Text, Canvas, Scrollbar, Menu

def apply_dark_theme(root):
    """
    Applique un thème sombre à une application Tkinter.
    :param root: La fenêtre principale (Tk ou Toplevel).
    """
    # Palette de couleurs pour le thème sombre
    dark_bg = "#2d2d2d"  # Fond
    dark_fg = "#ffffff"  # Texte
    dark_button = "#4a4a4a"  # Boutons
    dark_highlight = "#5c5c5c"  # Bordures

    # Appliquer le thème à la fenêtre principale
    root.configure(bg=dark_bg)

    # Fonction récursive pour appliquer le style à tous les widgets
    def apply_style(widget):
        try:
            if isinstance(widget, (Label, Button, Entry, Text)):
                widget.config(bg=dark_bg, fg=dark_fg)
            elif isinstance(widget, Frame):
                widget.config(bg=dark_bg)
            elif isinstance(widget, Canvas):
                widget.config(bg=dark_bg, highlightbackground=dark_highlight)
            elif isinstance(widget, Scrollbar):
                widget.config(bg=dark_bg, troughcolor=dark_bg, activebackground=dark_highlight)
            elif isinstance(widget, Menu):
                widget.config(bg=dark_bg, fg=dark_fg)

            # Propager aux sous-widgets
            for sub_widget in widget.winfo_children():
                apply_style(sub_widget)
        except Exception as e:
            # Ignorer les erreurs pour les widgets qui ne supportent pas certaines options
            pass

    # Appliquer le style à la fenêtre principale et à tous ses enfants
    apply_style(root)