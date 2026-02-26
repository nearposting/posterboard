import argparse
import random
import os
import math
from PIL import Image, ImageDraw, ImageFont

def get_random_color():
    """Generates a random RGB tuple."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def get_aspect_ratio(width, height):
    """Calculates the simplified aspect ratio string using GCD."""
    gcd = math.gcd(width, height)
    return f"{width//gcd}to{height//gcd}"

def create_image(width, height, count, output_folder, img_format):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    # 1. Colors & Setup
    color1 = get_random_color()
    color2 = get_random_color()
    square_size = max(1, width // 5)
    
    img = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(img)

    # 2. Draw Checkerboard
    for y in range(0, height, square_size):
        for x in range(0, width, square_size):
            if (x // square_size + y // square_size) % 2 == 1:
                draw.rectangle([x, y, x + square_size, y + square_size], fill=color2)

    # 3. Add Number
    font_size = int(height * 0.3)
    font = ImageFont.load_default(size = font_size)

    text = str(count)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    draw.text(((width - text_w) // 2, (height - text_h) // 2), 
              text, fill="white", font=font, stroke_width=2, stroke_fill="black")

    # 4. Save with chosen format
    ext = img_format.lower()
    filename = f"image_{count}.{ext}"
    save_path = os.path.join(output_folder, filename)
    
    if ext in ["jpg", "jpeg"]:
        img.save(save_path, "JPEG", quality=95)
    else:
        img.save(save_path, "PNG")

def main():
    parser = argparse.ArgumentParser(description="Generate checkerboard images.")
    parser.add_argument("width", type=int, help="Width of the image")
    parser.add_argument("height", type=int, help="Height of the image")
    parser.add_argument("num_images", type=int, help="Number of images to generate")
    
    parser.add_argument("-o", "--out", type=str, help="Override default output directory")
    parser.add_argument("-f", "--format", type=str, default="png", choices=["png", "jpg", "jpeg"], 
                        help="Image format: png or jpg (default: png)")
    
    args = parser.parse_args()

    # Default directory naming: AtoB_XbyY
    if args.out:
        target_dir = args.out
    else:
        ratio = get_aspect_ratio(args.width, args.height)
        target_dir = f"{ratio}_{args.width}by{args.height}"

    print(f"Generating {args.num_images} {args.format.upper()}s in: {target_dir}")

    for i in range(args.num_images):
        create_image(args.width, args.height, i, target_dir, args.format)
    
    print("Finished successfully.")

if __name__ == "__main__":
    main()