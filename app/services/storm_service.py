from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from app.utils.image import break_string, load_font, FONTS_DIR


class StormService:
    @staticmethod
    def text_to_image(text: str) -> BytesIO:
        img = Image.new("RGB", (1920, 1080), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype(str(FONTS_DIR / "MiSans-Bold.ttf"), 40)
        except Exception:
            font = ImageFont.load_default()
        lines = break_string(text, font, 1800)
        y = 540 - len(lines) * 25
        for line in lines:
            bbox = font.getbbox(line)
            x = (1920 - (bbox[2] - bbox[0])) // 2
            draw.text((x, y), line, fill=(0, 0, 0), font=font)
            y += bbox[3] - bbox[1] + 10
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf

    @staticmethod
    def generate_chaoshi(text: str) -> BytesIO:
        return StormService._generate_meme(text, "chaoshi.jpg", (0, 0, 0))

    @staticmethod
    def generate_happy(text: str) -> BytesIO:
        return StormService._generate_meme(text, "happy.jpg", (255, 0, 0))

    @staticmethod
    def generate_pw1(text: str) -> BytesIO:
        return StormService._generate_meme(text, "pw1.jpg", (0, 0, 0))

    @staticmethod
    def generate_yesno1(text_a: str, text_b: str) -> BytesIO:
        return StormService._generate_meme(text_a, "yesno1.jpg", (0, 0, 0))

    @staticmethod
    def _generate_meme(text: str, template: str, color: tuple) -> BytesIO:
        img = Image.new("RGB", (800, 600), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype(str(FONTS_DIR / "IPix-Chinese.ttf"), 30)
        except Exception:
            font = ImageFont.load_default()
        draw.text((50, 50), text, fill=color, font=font)
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf
