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

def detect_steganography_lsb(image_path: str) -> float:
    """
    Analyzes an image using the Pairs of Values (PoV) Chi-Square statistical attack 
    to determine the probability that it contains LSB steganography.
    Returns a probability (0.0 to 1.0) where 1.0 means highly likely to contain hidden data.
    """
    import scipy.stats as stats
    
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image for analysis.")
        
    flat_img = img.flatten()
    # Calculate histogram
    counts, _ = np.histogram(flat_img, bins=256, range=(0, 255))
    
    expected = []
    observed = []
    
    # Analyze pairs of values (2k, 2k+1)
    for i in range(128):
        v_2k = counts[2*i]
        v_2k_plus_1 = counts[2*i + 1]
        
        # We only consider pairs containing at least some data
        if v_2k + v_2k_plus_1 > 0:
            avg = (v_2k + v_2k_plus_1) / 2.0
            expected.append(avg)
            expected.append(avg)
            observed.append(v_2k)
            observed.append(v_2k_plus_1)
            
    if not expected:
        return 0.0
        
    expected = np.array(expected)
    observed = np.array(observed)
    
    # Calculate Chi-Square statistic
    chi_sq = np.sum((observed - expected)**2 / np.maximum(expected, 1e-10))
    degrees_of_freedom = len(expected) // 2 - 1
    
    if degrees_of_freedom <= 0:
        return 0.0
        
    # The P-value indicates the probability that the observed distribution Matches the expected distribution.
    # In a normal image, they don't match -> P-value is close to 0.
    # In a stego image, they do match (due to LSB randomization) -> P-value is close to 1.
    p_value = stats.chi2.sf(chi_sq, degrees_of_freedom)
    
    return p_value
