from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pathlib import Path


STATIC_DIR = Path(__file__).parent.parent.parent / "static"
FONTS_DIR = STATIC_DIR / "fonts"
FLAGS_DIR = STATIC_DIR / "flags"
IMG_DIR = STATIC_DIR / "img"
TEMPLATES_DIR = STATIC_DIR / "templates"


def break_string(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines = []
    current_line = ""
    for char in text:
        test_line = current_line + char
        bbox = font.getbbox(test_line)
        if bbox[2] - bbox[0] > max_width:
            if current_line:
                lines.append(current_line)
            current_line = char
        else:
            current_line = test_line
    if current_line:
        lines.append(current_line)
    return lines


def load_font(font_name: str, size: int) -> ImageFont.FreeTypeFont:
    font_path = FONTS_DIR / font_name
    if font_path.exists():
        return ImageFont.truetype(str(font_path), size)
    return ImageFont.load_default()


def load_image(image_path: str) -> Image.Image:
    path = STATIC_DIR / image_path
    if path.exists():
        return Image.open(path).convert("RGBA")
    return Image.new("RGBA", (100, 100), (200, 200, 200, 255))


def render_text_on_image(
    base: Image.Image,
    text: str,
    position: tuple[int, int],
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, ...] = (0, 0, 0, 255),
    max_width: int | None = None,
) -> Image.Image:
    draw = ImageDraw.Draw(base)
    if max_width:
        lines = break_string(text, font, max_width)
        y = position[1]
        for line in lines:
            draw.text((position[0], y), line, font=font, fill=fill)
            bbox = font.getbbox(line)
            y += bbox[3] - bbox[1] + 4
    else:
        draw.text(position, text, font=font, fill=fill)
    return base


def image_to_bytes(img: Image.Image, format: str = "PNG") -> BytesIO:
    buf = BytesIO()
    img.save(buf, format=format)
    buf.seek(0)
    return buf


def make_rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), size], radius=radius, fill=255)
    return mask


def apply_rounded_corners(img: Image.Image, radius: int) -> Image.Image:
    mask = make_rounded_mask(img.size, radius)
    output = Image.new("RGBA", img.size, (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)
    return output


def load_flag(country_code: str) -> Image.Image:
    path = FLAGS_DIR / f"{country_code}.png"
    if path.exists():
        return Image.open(path).convert("RGBA")
    return Image.new("RGBA", (30, 20), (200, 200, 200, 255))
