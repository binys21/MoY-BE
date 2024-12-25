from PIL import Image as pil
import os

def rescale(image, width=1440, max_file_size=2 * 1024 * 1024):
    img = pil.open(image)
    src_width, src_height = img.size
    
    # 원본 파일 크기 확인
    if hasattr(image, 'size'):
        file_size = image.size  # Django InMemoryUploadedFile
    else:
        file_size = os.path.getsize(image.name)  # 일반 파일

    # 가로, 세로 중 더 짧은 쪽을 기준으로 리사이즈 조건 확인
    if file_size > max_file_size or min(src_width, src_height) > width:
        # 가로 세로 중 짧은 쪽을 기준으로 비율 계산
        if src_width > src_height:
            dst_width = width
            dst_height = int((src_height / src_width) * dst_width)  # 세로 비율 유지
        else:
            dst_height = width
            dst_width = int((src_width / src_height) * dst_height)  # 가로 비율 유지

        # 리사이즈 수행
        size = (dst_width, dst_height)
        img.thumbnail(size, pil.LANCZOS)
    img = img.convert("RGB")
        
    # 임시 파일 저장
    temp_dir = "./home/temp"
    # os.makedirs(temp_dir, exist_ok=True)  # 임시 폴더가 없으면 생성
    temp_file_path = os.path.join(temp_dir, image.name if hasattr(image, 'name') else "temp_image.jpg")

    img.save(temp_file_path, format="JPEG")
    return temp_file_path

