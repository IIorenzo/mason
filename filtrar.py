import sys

CATEGORIAS = {
    "movistar deportes playready",
    "dazn",
}

def grupo_de(bloque):
    """Devuelve el group-title (o #EXTGRP) de un bloque de canal."""
    for linea in bloque:
        if linea.startswith("#EXTINF"):
            marca = 'group-title="'
            i = linea.find(marca)
            if i != -1:
                resto = linea[i + len(marca):]
                return resto.split('"', 1)[0].strip().lower()
        if linea.startswith("#EXTGRP:"):
            return linea.split(":", 1)[1].strip().lower()
    return ""

def main(entrada, salida):
    with open(entrada, encoding="utf-8", errors="ignore") as f:
        lineas = [l.rstrip("\r\n") for l in f]

    resultado = ["#EXTM3U"]
    bloque = []
    for linea in lineas:
        if linea.startswith("#EXTM3U") or not linea.strip():
            continue
        bloque.append(linea)
        if not linea.startswith("#"):  # es la URL, cierra el canal
            if grupo_de(bloque) in CATEGORIAS:
                resultado.extend(bloque)
            bloque = []

    with open(salida, "w", encoding="utf-8") as f:
        f.write("\n".join(resultado) + "\n")

    canales = sum(1 for l in resultado if l.startswith("#EXTINF"))
    print(f"Canales conservados: {canales}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
