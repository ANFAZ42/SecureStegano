import cv2
import numpy as np

def calculate_mse(img1_path: str, img2_path: str) -> float:
    """
    Calculates the Mean Squared Error (MSE) between two images.
    """
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    if img1 is None or img2 is None:
        raise ValueError("Could not read one or both images.")
        
    if img1.shape != img2.shape:
        raise ValueError("Images must have the same dimensions to calculate MSE.")
        
    err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
    err /= float(img1.shape[0] * img1.shape[1] * img1.shape[2])
    return err

def calculate_psnr(img1_path: str, img2_path: str) -> float:
    """
    Calculates the Peak Signal-to-Noise Ratio (PSNR) between two images.
    Values > 30dB indicate minimal to no visual distortion.
    """
    mse = calculate_mse(img1_path, img2_path)
    if mse == 0:
        return float('inf')
    pixel_max = 255.0
    return 20 * np.log10(pixel_max / np.sqrt(mse))
