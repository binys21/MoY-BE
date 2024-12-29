from PIL import Image as pil, ImageOps
import os

def rescale(image, width=1440, max_file_size=2 * 1024 * 1024):
    img = pil.open(image)
    img = ImageOps.exif_transpose(img)
    src_width, src_height = img.size
    
    # 원본 파일 크기 확인
    if hasattr(image, 'size'):
        file_size = image.size  # Django InMemoryUploadedFile
    else:
        file_size = os.path.getsize(image.name)  # 일반 파일

    # 파일 크기나 해상도 조건 확인
    if file_size > max_file_size or min(src_width, src_height) > width:
        # 비율 계산: 더 긴 축을 기준으로 맞추기
        if src_width > src_height:
            dst_width = width
            dst_height = int((src_height / src_width) * dst_width)  # 세로 비율 유지
        else:
            dst_height = width
            dst_width = int((src_width / src_height) * dst_height)  # 가로 비율 유지

        # 리사이즈 수행
        img = img.resize((dst_width, dst_height), pil.LANCZOS)  # 비율 유지하며 리사이즈
    img = img.convert("RGB")  # JPEG로 저장 가능하게 RGB로 변환

    # 임시 파일 저장
    temp_dir = "./home/temp"
    os.makedirs(temp_dir, exist_ok=True)  # 임시 폴더가 없으면 생성
    temp_file_path = os.path.join(temp_dir, image.name if hasattr(image, 'name') else "temp_image.jpg")

    img.save(temp_file_path, format="JPEG")
    return temp_file_path

def rescale_from_path(temp_file_path, width=1440, max_file_size=2 * 1024 * 1024):
    """
    저장된 임시 파일 경로를 기반으로 이미지를 리사이즈합니다.
    """
    # 이미지 열기
    img = pil.open(temp_file_path)
    img = ImageOps.exif_transpose(img)  # EXIF 정보 기준으로 회전 보정
    src_width, src_height = img.size

    # 파일 크기 확인
    file_size = os.path.getsize(temp_file_path)

    # 파일 크기나 해상도 조건 확인
    if file_size > max_file_size or min(src_width, src_height) > width:
        # 비율 계산: 더 긴 축을 기준으로 맞추기
        if src_width > src_height:
            dst_width = width
            dst_height = int((src_height / src_width) * dst_width)  # 세로 비율 유지
        else:
            dst_height = width
            dst_width = int((src_width / src_height) * dst_height)  # 가로 비율 유지

        # 리사이즈 수행
        img = img.resize((dst_width, dst_height), pil.LANCZOS)  # 비율 유지하며 리사이즈

    img = img.convert("RGB")  # JPEG로 저장 가능하게 RGB로 변환

    # 동일한 경로에 다시 저장
    img.save(temp_file_path, format="JPEG")
    return temp_file_path