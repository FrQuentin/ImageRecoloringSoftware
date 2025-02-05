def hex_to_rgb(hex_color):
    """
    Convertit une couleur hexadécimale (#RRGGBB) en un tuple RGB (R, G, B).
    Si le # est manquant, il est ajouté automatiquement.
    """
    if not hex_color.startswith("#"):
        hex_color = "#" + hex_color
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))