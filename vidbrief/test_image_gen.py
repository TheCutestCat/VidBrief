from PIL import Image, ImageDraw, ImageFont

def create_movie_layout(items, canvas_size=(1920, 1080), margin=10, font_path='./font/times-roman/OPTITimes-Roman.otf'):
    # Calculate the number of columns and rows
    num_items = len(items)
    num_columns = min(5, max(1, (num_items + 2) // 3))
    num_rows = (num_items + num_columns - 1) // num_columns
    
    # Calculate cell size
    cell_width = (canvas_size[0] - margin * (num_columns + 1)) // num_columns
    cell_height = (canvas_size[1] - margin * (num_rows + 1)) // num_rows
    
    # Create canvas
    canvas = Image.new('RGB', canvas_size, (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    # Determine initial font size based on cell size
    font_size = int(cell_width * 0.1)
    font = ImageFont.truetype(font_path, font_size)
    
    # Place each item
    for idx, (text, img_path) in enumerate(items):
        row = idx // num_columns
        col = idx % num_columns
        
        # Load and resize image
        with Image.open(img_path) as img:
            img.thumbnail((cell_width, int(cell_height * 0.8)))
        
        # Calculate position
        x = margin + col * (cell_width + margin)
        y = margin + row * (cell_height + margin)
        
        # Paste image
        img_x = x + (cell_width - img.width) // 2
        img_y = y
        canvas.paste(img, (img_x, img_y))
        
        # Adjust font size based on available space beneath the image
        max_text_width = cell_width
        max_text_lines = 2
        for size in range(14, 7, -1):  # Try sizes 14 down to 8
            font = ImageFont.truetype(font_path, size)
            lines = text.split('\n')
            wrapped_text = []
            for line in lines:
                while line:
                    fragment = line
                    while draw.textlength(fragment, font=font) > max_text_width and len(fragment) > 0:
                        fragment = fragment.rsplit(' ', 1)[0]  # Try removing last word
                    wrapped_text.append(fragment)
                    line = line[len(fragment):].strip()
            if len(wrapped_text) <= max_text_lines:
                break
        
        # Align text centrally within the cell width
        text_y = y + img.height + 5
        for line in wrapped_text:
            text_width = draw.textlength(line, font=font)
            text_x = x + (cell_width - text_width) // 2
            draw.text((text_x, text_y), line, fill="black", font=font)
            text_y += font.getbbox(line)[3]  # Adjust line height calculation using getbbox to avoid errors
    return canvas

if __name__ == "__main__":
    # Example usage
    items = [
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        ("Movie 1", "./cache/video_frames/akeytNVcIy4/frame_781.jpg"),
        
    ]

    output_image = create_movie_layout(items)
    output_image.save('movie_layout.png')