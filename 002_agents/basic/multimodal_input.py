import io, os
from PIL import Image
from strands import Agent
from my_env import model_id

MAX_BYTES = 5 * 1024 * 1024  # 5MB

def compress_image_to_limit(path: str, prefer: str = "jpeg") -> tuple[str, bytes]:
    """
    Returns (bedrock_format, image_bytes) <= 5MB.
    prefer: 'jpeg' (best for photos) or 'webp' (keeps alpha, great compression).
    """
    img = Image.open(path)
    # Decide format & handle alpha
    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
    if prefer == "jpeg" and not has_alpha:
        bedrock_fmt, pil_fmt = "jpeg", "JPEG"
        img = img.convert("RGB")
    elif prefer == "webp":
        bedrock_fmt, pil_fmt = "webp", "WEBP"
    else:
        # fallback for graphics/alpha
        bedrock_fmt, pil_fmt = "png", "PNG"

    # Helper to encode with params
    def encode(quality=85):
        buf = io.BytesIO()
        save_kwargs = {"format": pil_fmt}
        if pil_fmt in ("JPEG", "WEBP"):
            save_kwargs.update(dict(quality=quality, optimize=True))
            if pil_fmt == "WEBP":
                save_kwargs["method"] = 6
        elif pil_fmt == "PNG":
            save_kwargs.update(dict(optimize=True, compress_level=9))
        img.save(buf, **save_kwargs)
        return buf.getvalue()

    # Try multiple passes: quality → downscale loop
    quality = 85
    data = encode(quality)
    # If still too big, progressively downscale shortest side by 85% until it fits
    while len(data) > MAX_BYTES:
        if pil_fmt in ("JPEG", "WEBP") and quality > 50:
            quality -= 5
        else:
            # scale down
            w, h = img.size
            new_w, new_h = int(w * 0.85), int(h * 0.85)
            if min(new_w, new_h) < 400:
                break  # don't destroy it; accept slightly over limit
            img = img.resize((new_w, new_h), Image.LANCZOS)
        data = encode(quality)
    return bedrock_fmt, data

agent = Agent(model=model_id)

# Path relative to this script's directory
script_dir = os.path.dirname(__file__)
image_path = os.path.join(script_dir, "test_small.jpg")
fmt, image_bytes = compress_image_to_limit(image_path, prefer="jpeg")  # try "webp" for best size

with open(image_path, "rb") as fp:
    image_bytes = fp.read()

response = agent([
    {"text": "What can you see in this image?"},
    {
        "image": {
            "format": "png",
            "source": {
                "bytes": image_bytes,
            },
        },
    },
])

print(response)