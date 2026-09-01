import cv2
import numpy as np
import pytesseract
from PIL import Image
import os

class ImageProcessor:
    def __init__(self):
        self.min_font_size = 4  # Minimum font size in points
        self.min_contrast = 50  # Minimum contrast ratio
    
    def process_image(self, image_path):
        """
        Process product label image and extract text and metadata
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return {'error': 'Could not read image'}
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Extract text using OCR
            extracted_text = pytesseract.image_to_string(image)
            
            # Get detailed OCR data
            ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            # Process extracted data
            declarations = self._process_ocr_data(ocr_data, extracted_text, image)
            
            # Analyze image quality
            image_quality = self._analyze_image_quality(gray)
            
            return {
                'raw_text': extracted_text,
                'declarations': declarations,
                'image_quality': image_quality,
                'image_dimensions': {
                    'width': image.shape[1],
                    'height': image.shape[0]
                },
                'manufacturer_name': self._extract_manufacturer_name(extracted_text)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _process_ocr_data(self, ocr_data, extracted_text, image):
        """
        Process OCR data to identify declarations
        """
        declarations = {}
        
        # Extract individual words with confidence
        words = ocr_data['text']
        confidences = ocr_data['conf']
        left = ocr_data['left']
        top = ocr_data['top']
        width = ocr_data['width']
        height = ocr_data['height']
        
        for i, word in enumerate(words):
            if word.strip():
                # Calculate font size approximation
                font_size = self._estimate_font_size(height[i])
                
                declarations[f'word_{i}'] = {
                    'text': word,
                    'confidence': float(confidences[i]) / 100,
                    'font_size': font_size,
                    'position': {
                        'x': int(left[i]),
                        'y': int(top[i]),
                        'width': int(width[i]),
                        'height': int(height[i])
                    },
                    'is_readable': float(confidences[i]) > 50
                }
        
        return declarations
    
    def _estimate_font_size(self, height_pixels):
        """
        Estimate font size from pixel height
        """
        # Rough approximation: 1 point ≈ 1.33 pixels at 96 DPI
        return round(height_pixels / 1.33, 1)
    
    def _analyze_image_quality(self, gray_image):
        """
        Analyze image quality metrics
        """
        # Calculate contrast
        contrast = gray_image.std()
        
        # Calculate brightness
        brightness = gray_image.mean()
        
        # Detect edges for sharpness
        edges = cv2.Canny(gray_image, 100, 200)
        edge_ratio = np.sum(edges > 0) / edges.size
        
        return {
            'contrast': float(contrast),
            'brightness': float(brightness),
            'sharpness': float(edge_ratio),
            'quality_score': self._calculate_quality_score(contrast, brightness, edge_ratio)
        }
    
    def _calculate_quality_score(self, contrast, brightness, edge_ratio):
        """
        Calculate overall image quality score (0-100)
        """
        score = 0
        
        # Contrast score (ideal: 50-100)
        if 30 < contrast < 120:
            score += 30
        elif 50 < contrast < 100:
            score += 40
        else:
            score += max(0, 30 - abs(contrast - 65) / 10)
        
        # Brightness score (ideal: 50-200)
        if 50 < brightness < 200:
            score += 30
        else:
            score += max(0, 30 - abs(brightness - 125) / 20)
        
        # Sharpness score
        if edge_ratio > 0.05:
            score += 40
        elif edge_ratio > 0.02:
            score += 20
        
        return min(100, max(0, score))
    
    def _extract_manufacturer_name(self, text):
        """
        Extract manufacturer name from text
        """
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if 'manufacturer' in line.lower() or 'mfg' in line.lower() or 'made by' in line.lower():
                if i + 1 < len(lines):
                    return lines[i + 1].strip()
        
        return None
