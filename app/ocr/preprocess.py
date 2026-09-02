import cv2
import numpy as np


def load_image(image_path: str):
    """
    Load an image from disk.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(
            f"Unable to read image: {image_path}"
        )

    return image


def convert_to_grayscale(image):
    """
    Convert BGR image to grayscale.
    """

    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


def upscale_image(
    image,
    scale: float = 2.0
):
    """
    Upscale image using cubic interpolation.
    """

    return cv2.resize(
        image,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC
    )


def enhance_contrast(image):
    """
    Improve local contrast using CLAHE.
    """

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    return clahe.apply(image)


def denoise_image(image):
    """
    Reduce small amounts of noise.
    """

    return cv2.GaussianBlur(
        image,
        (3, 3),
        0
    )


def deskew_image(image):
    """
    Correct small rotations/skew in a document.
    """

    _, binary = cv2.threshold(
        image,
        0,
        255,
        cv2.THRESH_BINARY_INV
        + cv2.THRESH_OTSU
    )

    coordinates = np.column_stack(
        np.where(binary > 0)
    )

    if len(coordinates) < 10:
        return image

    angle = cv2.minAreaRect(
        coordinates
    )[-1]

    if angle < -45:
        angle = -(90 + angle)

    else:
        angle = -angle

    if abs(angle) < 0.1:
        return image

    height, width = image.shape[:2]

    center = (
        width // 2,
        height // 2
    )

    rotation_matrix = cv2.getRotationMatrix2D(
        center,
        angle,
        1.0
    )

    rotated = cv2.warpAffine(
        image,
        rotation_matrix,
        (width, height),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )

    return rotated


def threshold_image(image):
    """
    Convert grayscale image into a binary document image.
    """

    return cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )


def morphological_cleanup(image):
    """
    Remove small noise and improve text structure.
    """

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (2, 2)
    )

    cleaned = cv2.morphologyEx(
        image,
        cv2.MORPH_OPEN,
        kernel
    )

    return cleaned


def preprocess_image(
    image_path: str,
    output_path: str = None
):
    """
    Complete document preprocessing pipeline.

    Returns the processed image.
    """

    image = load_image(image_path)

    gray = convert_to_grayscale(image)

    resized = upscale_image(
        gray,
        scale=2.0
    )

    enhanced = enhance_contrast(
        resized
    )

    denoised = denoise_image(
        enhanced
    )

    deskewed = deskew_image(
        denoised
    )

    thresholded = threshold_image(
        deskewed
    )

    cleaned = morphological_cleanup(
        thresholded
    )

    if output_path:
        cv2.imwrite(
            output_path,
            cleaned
        )

    return cleaned