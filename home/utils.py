from PIL import Image as pil
import os

def rescale(image, width=1920, max_file_size=5 * 1024 * 1024):
    img=pil.open(image)
    src_width, src_height = img.size
    
    # 원본 파일 크기 확인
    if hasattr(image, 'size'):
        file_size = image.size  # Django InMemoryUploadedFile
    else:
        file_size = os.path.getsize(image.name)  # 일반 파일

    if file_size > max_file_size or src_width > width:
        src_ratio = float(src_height) / float(src_width)  # 원본 비율 계산
        dst_height = round(src_ratio * width)  # 비율 유지한 높이 계산

        # 리사이즈 수행
        size = (width, dst_height)
        img.thumbnail(size, pil.LANCZOS)
        img = img.convert("RGB")
     # 임시 파일 저장
    temp_dir = "./home/temp"
    temp_file_path = os.path.join(temp_dir, image.name if hasattr(image, 'name') else "temp_image.jpg")

    img.save(temp_file_path, format="JPEG")
    return temp_file_path

