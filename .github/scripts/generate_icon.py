#!/usr/bin/env python3

import struct, zlib, os, json

def create_png(width, height, pixels):
    """Create a minimal PNG from raw RGBA pixel data"""
    def chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    raw = b''
    for y in range(height):
        raw += b'\x00'
        for x in range(width):
            idx = (y * width + x) * 4
            raw += bytes(pixels[idx:idx + 4])
    idat = zlib.compress(raw)

    return (b'\x89PNG\r\n\x1a\n' +
            chunk(b'IHDR', ihdr) +
            chunk(b'IDAT', idat) +
            chunk(b'IEND', b''))

def generate_icon(size):
    w, h = size, size
    pixels = []
    cx, cy = w // 2, h // 2
    r = w // 2

    # Colors
    dark_green = (8, 45, 35)
    med_green = (18, 85, 65)
    gold = (180, 140, 50)
    white = (255, 255, 255)

    for y in range(h):
        for x in range(w):
            dx, dy = x - cx, y - cy
            dist = (dx*dx + dy*dy) ** 0.5

            if dist > r:
                pixels.extend([0, 0, 0, 0])
                continue

            # Gradient background
            t = dist / r
            rr = int(dark_green[0] + (med_green[0] - dark_green[0]) * t)
            gg = int(dark_green[1] + (med_green[1] - dark_green[1]) * t)
            bb = int(dark_green[2] + (med_green[2] - dark_green[2]) * t)

            # Islamic 8-pointed star overlay
            angle = (__import__('math').atan2(dy, dx) + __import__('math').pi) % (2 * __import__('math').pi)
            star_angle = angle % (__import__('math').pi / 4)
            star_dist = dist / r

            # Draw star lines
            star_width = 0.03
            in_star = False
            for i in range(8):
                a1 = i * __import__('math').pi / 4 - __import__('math').pi / 8
                a2 = a1 + __import__('math').pi / 4
                if a1 <= angle <= a2:
                    mid = (a1 + a2) / 2
                    ang_dist = abs(angle - mid)
                    if ang_dist < star_width * 2 and star_dist > 0.15 and star_dist < 0.85:
                        in_star = True

            # Decorative circle
            if 0.82 < star_dist < 0.88:
                in_star = True
                rr, gg, bb = gold
            elif 0.88 < star_dist < 0.95:
                rr = int(rr * 0.85)
                gg = int(gg * 0.85)
                bb = int(bb * 0.85)

            if in_star:
                rr = int(rr * 0.7 + gold[0] * 0.3)
                gg = int(gg * 0.7 + gold[1] * 0.3)
                bb = int(bb * 0.7 + gold[2] * 0.3)

            # Crescent near top (subtle)
            if dy < -r * 0.35 and abs(dx) < r * 0.3 and dist > r * 0.6:
                rr = int(rr * 0.9)
                gg = int(gg * 0.9)
                bb = int(bb * 0.9)

            # Inner glow
            if star_dist < 0.15:
                glow = 1 - star_dist / 0.15
                rr = int(rr + (gold[0] - rr) * glow * 0.3)
                gg = int(gg + (gold[1] - gg) * glow * 0.3)

            pixels.extend([
                max(0, min(255, rr)),
                max(0, min(255, gg)),
                max(0, min(255, bb)),
                255
            ])

    return create_png(w, h, pixels)

def main():
    base = "AdhkarWidget/Resources/Assets.xcassets/AppIcon.appiconset"
    os.makedirs(base, exist_ok=True)

    icon_sizes = [
        (20, "20x20@1x", "iphone", "20"),
        (40, "20x20@2x", "iphone", "20"),
        (60, "20x20@3x", "iphone", "20"),
        (29, "29x29@1x", "iphone", "29"),
        (58, "29x29@2x", "iphone", "29"),
        (87, "29x29@3x", "iphone", "29"),
        (40, "40x40@1x", "iphone", "40"),
        (80, "40x40@2x", "iphone", "40"),
        (120, "40x40@3x", "iphone", "40"),
        (57, "57x57@1x", "iphone", "57"),
        (114, "57x57@2x", "iphone", "57"),
        (60, "60x60@1x", "iphone", "60"),
        (120, "60x60@2x", "iphone", "60"),
        (180, "60x60@3x", "iphone", "60"),
        (1024, "1024x1024@1x", "ios-marketing", "1024"),
    ]

    images = []
    for size, idiom_key, idiom, scale_info in icon_sizes:
        filename = f"AppIcon-{idiom_key}.png"
        print(f"Generating {filename} ({size}x{size})...")
        png_data = generate_icon(size)
        filepath = os.path.join(base, filename)
        with open(filepath, "wb") as f:
            f.write(png_data)

        scale = "1x" if "@1x" in idiom_key else ("2x" if "@2x" in idiom_key else "3x")
        images.append({
            "filename": filename,
            "idiom": idiom,
            "scale": scale,
            "size": f"{scale_info}x{scale_info}"
        })

    contents = {
        "images": images,
        "info": {
            "author": "xcode",
            "version": 1
        }
    }

    with open(os.path.join(base, "Contents.json"), "w") as f:
        json.dump(contents, f, indent=2)

    print(f"Done! Generated {len(images)} icons.")

if __name__ == "__main__":
    main()
