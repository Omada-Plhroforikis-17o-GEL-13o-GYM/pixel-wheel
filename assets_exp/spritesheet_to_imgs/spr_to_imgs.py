from PIL import Image
import os

def extract_sprites(spritesheet_path, sprite_width, sprite_height, output_folder="output_sprites"):
    # Load the spritesheet
    try:
        spritesheet = Image.open(spritesheet_path)
    except FileNotFoundError:
        print(f"File not found: {spritesheet_path}")
        return

    sheet_width, sheet_height = spritesheet.size
    print(f"Spritesheet size: {sheet_width}x{sheet_height}")

    # Calculate how many sprites fit horizontally and vertically
    cols = sheet_width // sprite_width
    rows = sheet_height // sprite_height

    # Create output directory
    os.makedirs(output_folder, exist_ok=True)

    count = 0
    # Reverse Y-axis: bottom to top
    for row in reversed(range(rows)):
        y = row * sprite_height
        for col in range(cols):
            x = col * sprite_width
            box = (x, y, x + sprite_width, y + sprite_height)
            sprite = spritesheet.crop(box)
            sprite.save(os.path.join(output_folder, f"sprite_{count+100}.png"))
            count += 1

    print(f"Extracted {count} sprites into '{output_folder}'")

# Example usage
if __name__ == "__main__":
    extract_sprites(
        spritesheet_path="kamara.png",   # ← Change to your file path
        sprite_width=40,
        sprite_height=40
    )
