from PIL import Image as pil
import os

def rescale(image,width):
    img=pil.open(image)
    src_width, src_height = img.size
    src_ratio = float(src_height) / float(src_width)
    dst_height = round(src_ratio * width)

    size = (width, dst_height)
    img.thumbnail(size, pil.LANCZOS)
    img = img.convert("RGB")

    # 임시 파일 
    temp_dir = "./home/temp"
    os.makedirs(temp_dir, exist_ok=True)  # 임시 폴더 생성
    temp_file_path = os.path.join(temp_dir, image.name)

    img.save(temp_file_path, format="JPEG")
    return temp_file_path