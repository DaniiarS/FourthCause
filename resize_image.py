import os
from PIL import Image

WIDTH, HEIGHT = 448, 320



cwd = os.getcwd() + '/myapp/static/images'

img_dirs = os.listdir(cwd)
print(img_dirs)
for dir in img_dirs:
    dest_directory = os.getcwd() + f'/myapp/static/resized_images/{dir}/'
    current_dir = cwd + '/' + dir
    # if iterable is directory, then print the files inside
    if os.path.isdir(current_dir):
        img_files = os.listdir(current_dir)

        for file_name in img_files:
            # print("Files:", file_name)

            name, ext = os.path.splitext(file_name)

            if ext == ".jpeg" or ext == ".png":
                image = Image.open(current_dir+f'/{file_name}')
                
                resized_image = image.resize((WIDTH, HEIGHT), Image.LANCZOS)
                os.makedirs(dest_directory, exist_ok=True)
                resized_image.save(dest_directory + name + ext)

    
