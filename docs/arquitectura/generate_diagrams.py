from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "imagenes"
OUT.mkdir(exist_ok=True)

BG = (245, 247, 250)
PRIMARY = (25, 118, 210)
ACCENT = (76, 175, 80)
DARK = (33, 37, 41)
MUTED = (92, 98, 112)
LIGHT = (255, 255, 255)
ALERT = (244, 143, 66)
PURPLE = (123, 88, 255)
RED = (220, 53, 69)


def load_font(size=22):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()


def rounded_box(draw, x1, y1, x2, y2, fill, outline, radius=18, text=None, text_color=DARK, font_size=22, align="center"):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=2)
    if text:
        font = load_font(font_size)
        lines = text.split("\n")
        total_h = len(lines) * (font_size + 8)
        start_y = y1 + (y2 - y1 - total_h) / 2
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            x = x1 + (x2 - x1 - tw) / 2 if align == "center" else x1 + 20
            y = start_y + i * (font_size + 8)
            draw.text((x, y), line, font=font, fill=text_color)


def arrow(draw, x1, y1, x2, y2, color=PRIMARY, width=3):
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    angle = __import__("math").atan2(y2 - y1, x2 - x1)
    size = 16
    x3 = x2 - size * __import__("math").cos(angle - 0.5)
    y3 = y2 - size * __import__("math").sin(angle - 0.5)
    x4 = x2 - size * __import__("math").cos(angle + 0.5)
    y4 = y2 - size * __import__("math").sin(angle + 0.5)
    draw.polygon([(x2, y2), (x3, y3), (x4, y4)], fill=color)


def save_png(filename, width, height, renderer):
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)
    renderer(draw, width, height)
    img.save(OUT / filename, format="PNG")


def draw_architecture(draw, w, h):
    title = "Arquitectura del sistema"
    draw.text((40, 20), title, fill=DARK, font=load_font(32))

    boxes = {
        "usuario": (50, 140, 250, 260),
        "frontend": (330, 120, 690, 300),
        "api": (790, 120, 1150, 300),
        "usecases": (790, 380, 1150, 560),
        "repo": (790, 640, 1150, 820),
        "model": (360, 640, 720, 820),
        "sqlite": (40, 640, 300, 820),
    }

    rounded_box(draw, *boxes["usuario"], fill=LIGHT, outline=PRIMARY, text="Usuario\nNavegador", font_size=24)
    rounded_box(draw, *boxes["frontend"], fill=(230, 240, 255), outline=PRIMARY, text="Frontend\nHTML + CSS + JavaScript\nThree.js + controles 3D", font_size=22)
    rounded_box(draw, *boxes["api"], fill=(230, 255, 235), outline=ACCENT, text="Backend\nFastAPI\n/health + /api/v1/items", font_size=22)
    rounded_box(draw, *boxes["usecases"], fill=(245, 235, 255), outline=PURPLE, text="ItemUseCases\ncreate_item\nlist_items_by_space\nupdate_item + remove_item", font_size=20)
    rounded_box(draw, *boxes["repo"], fill=(255, 240, 230), outline=ALERT, text="ItemRepository\nCRUD async\nSQLAlchemy AsyncSession", font_size=21)
    rounded_box(draw, *boxes["model"], fill=(235, 245, 255), outline=PRIMARY, text="ItemModel / spatial_items\nid, name, space_id, color\nx, y, z, width, height, depth", font_size=19)
    rounded_box(draw, *boxes["sqlite"], fill=(255, 230, 230), outline=RED, text="SQLite\nspatial_inventory.db", font_size=23)

    arrow(draw, 260, 200, 360, 200)
    arrow(draw, 690, 210, 790, 210)
    arrow(draw, 970, 300, 970, 380)
    arrow(draw, 970, 560, 970, 640)
    arrow(draw, 790, 730, 720, 730)
    arrow(draw, 360, 730, 300, 730)

    draw.text((40, 835), "FastAPI tambien sirve frontend/ como archivos estaticos.", fill=MUTED, font=load_font(16))
    draw.text((40, 860), "La conexion SQLite se configura en database/connection.py y admite DATABASE_URL.", fill=MUTED, font=load_font(16))


def draw_usecase(draw, w, h):
    draw.text((40, 20), "Diagrama de caso de uso", fill=DARK, font=load_font(32))

    rounded_box(draw, 80, 120, 250, 220, fill=LIGHT, outline=PRIMARY, text="Usuario", font_size=26)

    rounded_box(draw, 420, 80, 700, 180, fill=(225, 245, 254), outline=PRIMARY, text="Crear objeto 3D", font_size=23)
    rounded_box(draw, 420, 230, 700, 330, fill=(232, 245, 233), outline=ACCENT, text="Seleccionar objeto", font_size=23)
    rounded_box(draw, 420, 380, 700, 480, fill=(255, 243, 224), outline=ALERT, text="Mover / rotar / escalar", font_size=23)
    rounded_box(draw, 420, 530, 700, 630, fill=(248, 243, 255), outline=PURPLE, text="Eliminar objeto", font_size=23)
    rounded_box(draw, 420, 680, 700, 780, fill=(255, 235, 238), outline=RED, text="Ver escena 3D", font_size=23)

    rounded_box(draw, 850, 150, 1260, 250, fill=(235, 245, 255), outline=PRIMARY, text="POST /api/v1/items/", font_size=22)
    rounded_box(draw, 850, 310, 1260, 410, fill=(233, 255, 242), outline=ACCENT, text="TransformControls", font_size=22)
    rounded_box(draw, 850, 470, 1260, 570, fill=(255, 242, 230), outline=ALERT, text="PUT /api/v1/items/{id}", font_size=22)
    rounded_box(draw, 850, 630, 1260, 730, fill=(246, 235, 255), outline=PURPLE, text="DELETE /api/v1/items/{id}", font_size=22)

    for x1, y1, x2, y2 in [(250, 170, 420, 130), (250, 280, 420, 280), (250, 430, 420, 430), (250, 580, 420, 580), (250, 730, 420, 730)]:
        arrow(draw, x1, y1, x2, y2)

    arrow(draw, 700, 130, 850, 200)
    arrow(draw, 700, 280, 850, 360)
    arrow(draw, 700, 430, 850, 520)
    arrow(draw, 700, 580, 850, 680)
    arrow(draw, 700, 730, 850, 360)


def draw_erd(draw, w, h):
    draw.text((40, 20), "Entidad principal: ItemModel", fill=DARK, font=load_font(32))
    draw.rounded_rectangle([360, 100, 1180, 780], radius=18, fill=LIGHT, outline=PRIMARY, width=2)
    draw.text((640, 125), "Tabla: spatial_items", fill=DARK, font=load_font(28))
    fields = [
        "id: UUID PK",
        "name: string",
        "space_id: string",
        "color: string",
        "x: float",
        "y: float",
        "z: float",
        "width: float",
        "height: float",
        "depth: float",
    ]

    y = 200
    for field in fields:
        draw.rounded_rectangle([420, y, 1120, y + 42], radius=10, fill=(240, 245, 255), outline=PRIMARY, width=1)
        draw.text((440, y + 10), field, fill=DARK, font=load_font(20))
        y += 52

    draw.text((360, 820), "space_id agrupa registros; actualmente no existe una tabla Space ni una FK.", fill=MUTED, font=load_font(20))


def draw_flow(draw, w, h):
    draw.text((40, 20), "Flujos principales del sistema", fill=DARK, font=load_font(32))

    boxes = [
        (40, 110, 300, 220, "Formulario\ncrear objeto"),
        (360, 110, 630, 220, "Frontend\nvalida y envia"),
        (690, 110, 960, 220, "POST /api/v1/items/"),
        (1020, 110, 1310, 220, "FastAPI +\nItemUseCases"),
        (1370, 110, 1640, 220, "Repository ->\nSQLite commit"),
        (1370, 330, 1640, 440, "Respuesta JSON\ncon id"),
        (1020, 330, 1310, 440, "Three.js crea\ny selecciona cubo"),
        (690, 330, 960, 440, "sessionStorage\nrestaura la sesion"),
        (40, 580, 420, 720, "TransformControls\nmover / rotar / escalar"),
        (520, 580, 850, 720, "PUT /api/v1/items/{id}"),
        (950, 580, 1310, 720, "Actualiza nombre, posicion,\ncolor y space_id"),
        (1370, 580, 1640, 720, "Rotacion, escala y\ndimensiones no se guardan"),
        (40, 850, 420, 970, "Eliminar seleccion\nZ / Delete / boton"),
        (520, 850, 850, 970, "DELETE /api/v1/items/{id}"),
        (950, 850, 1250, 970, "Repository borra\nregistro en SQLite"),
        (1370, 850, 1640, 970, "Quita cubo y registro\nde sessionStorage"),
    ]

    for x1, y1, x2, y2, label in boxes:
        rounded_box(draw, x1, y1, x2, y2, fill=LIGHT, outline=PRIMARY, text=label, font_size=18)

    arrows = [
        (300, 165, 360, 165), (630, 165, 690, 165),
        (960, 165, 1020, 165), (1310, 165, 1370, 165),
        (1505, 220, 1505, 330), (1370, 385, 1310, 385),
        (1020, 385, 960, 385),
        (420, 650, 520, 650), (850, 650, 950, 650), (1310, 650, 1370, 650),
        (420, 910, 520, 910), (850, 910, 950, 910), (1250, 910, 1370, 910),
    ]
    for x1, y1, x2, y2 in arrows:
        arrow(draw, x1, y1, x2, y2, color=ACCENT, width=3)


def uml_class(draw, x, y, width, title, attributes, methods, height):
    draw.rounded_rectangle([x, y, x + width, y + height], radius=12, fill=LIGHT, outline=PRIMARY, width=3)
    draw.text((x + 16, y + 12), title, fill=DARK, font=load_font(21))
    divider_y = y + 48
    draw.line((x, divider_y, x + width, divider_y), fill=PRIMARY, width=2)
    font = load_font(16)
    line_y = divider_y + 10
    for attribute in attributes:
        draw.text((x + 16, line_y), attribute, fill=DARK, font=font)
        line_y += 24
    if methods:
        method_divider_y = line_y + 4
        draw.line((x, method_divider_y, x + width, method_divider_y), fill=PRIMARY, width=1)
        line_y = method_divider_y + 10
        for method in methods:
            draw.text((x + 16, line_y), method, fill=MUTED, font=font)
            line_y += 24


def draw_uml_classes(draw, w, h):
    draw.text((40, 20), "UML de clases: capa de aplicacion y persistencia", fill=DARK, font=load_font(30))

    uml_class(draw, 60, 100, 500, "ItemUseCases", ["- repository: ItemRepository"], [
        "+ create_item(data): ItemResponseSchema",
        "+ list_items_by_space(space_id)",
        "+ update_item(id, data): ItemResponseSchema?",
        "+ remove_item(id): bool",
    ], 190)
    uml_class(draw, 700, 100, 500, "ItemRepository", ["- session: AsyncSession"], [
        "+ create(data): ItemModel",
        "+ get_all_by_space(space_id): List[ItemModel]",
        "+ get_by_id(id): ItemModel?",
        "+ update(id, data): ItemModel?",
        "+ delete(id): bool",
    ], 220)
    uml_class(draw, 1340, 100, 500, "ItemModel <<SQLModel, table>>", [
        "+ id: UUID (PK)", "+ name: str", "+ space_id: str", "+ color: str",
        "+ x, y, z: float", "+ width, height, depth: float",
    ], [], 240)

    uml_class(draw, 60, 500, 500, "ItemCreateSchema", [
        "+ name: str", "+ position: Position3DSchema", "+ dimensions: Dimensions3DSchema",
        "+ color: str", "+ space_id: str",
    ], [], 190)
    uml_class(draw, 700, 500, 500, "ItemUpdateSchema", [
        "+ name: str", "+ position: Position3DSchema", "+ color: str", "+ space_id: str",
    ], [], 165)
    uml_class(draw, 1340, 500, 500, "ItemResponseSchema", [
        "extends ItemCreateSchema", "+ id: UUID", "from_attributes = True",
    ], [], 145)

    uml_class(draw, 300, 900, 500, "Position3DSchema", [
        "+ x: float", "+ y: float", "+ z: float",
    ], [], 125)
    uml_class(draw, 1000, 900, 500, "Dimensions3DSchema", [
        "+ width: float (gt 0)", "+ height: float (gt 0)", "+ depth: float (gt 0)",
    ], [], 125)

    arrow(draw, 560, 195, 700, 195)
    arrow(draw, 1200, 195, 1340, 195)
    arrow(draw, 250, 290, 250, 500)
    arrow(draw, 500, 290, 850, 500)
    arrow(draw, 820, 320, 820, 500)
    arrow(draw, 310, 690, 500, 900)
    arrow(draw, 410, 690, 1100, 900)

    draw.text((60, 1120), "Las schemas exponen position/dimensions anidadas; ItemRepository las transforma a columnas x/y/z y width/height/depth.", fill=MUTED, font=load_font(18))
    draw.text((60, 1160), "La rotacion, la escala y las dimensiones no forman parte de ItemUpdateSchema ni se persisten en SQLite.", fill=MUTED, font=load_font(18))


def draw_endpoints(draw, w, h):
    draw.text((40, 20), "Endpoints principales", fill=DARK, font=load_font(32))
    title_fill = (245, 247, 250)
    draw.rounded_rectangle([50, 90, 1500, 780], radius=18, fill=LIGHT, outline=PRIMARY, width=2)

    rows = [
        ("GET", "/health", "Verifica que la API está activa"),
        ("POST", "/api/v1/items/", "Crea un objeto 3D"),
        ("GET", "/api/v1/items/space/{space_id}", "Lista objetos por espacio"),
        ("PUT", "/api/v1/items/{item_id}", "Actualiza un item existente"),
        ("DELETE", "/api/v1/items/{item_id}", "Elimina un item por UUID"),
    ]

    headers = ["Método", "Ruta", "Descripción"]
    x0 = 90
    widths = [170, 460, 670]
    y = 130
    for i, text in enumerate(headers):
        x = x0 + sum(widths[:i])
        rounded_box(draw, x, y, x + widths[i], y + 50, fill=PRIMARY, outline=PRIMARY, text=text, text_color=LIGHT, font_size=20)

    y += 70
    for method, route, desc in rows:
        x = x0
        for i, text in enumerate([method, route, desc]):
            xx = x + sum(widths[:i])
            draw.rounded_rectangle([xx, y, xx + widths[i], y + 70], radius=10, fill=(246, 248, 251), outline=(196, 203, 212), width=1)
            draw.text((xx + 20, y + 20), str(text), fill=DARK, font=load_font(20))
        y += 85


def main():
    save_png("arquitectura.png", 1600, 900, draw_architecture)
    save_png("casos_de_uso.png", 1600, 900, draw_usecase)
    save_png("erd.png", 1600, 900, draw_erd)
    save_png("flujo_de_trabajo.png", 1700, 1050, draw_flow)
    save_png("endpoints.png", 1600, 900, draw_endpoints)
    save_png("uml_clases.png", 1900, 1250, draw_uml_classes)
    print(f"Diagramas creados en: {OUT}")


if __name__ == "__main__":
    main()
