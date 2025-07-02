from PIL import Image

from pixr.strategies import BaseOptimizationStrategy, JpegStrategy, PngStrategy, WebPStrategy


class StrategyFactory:
    @staticmethod
    def get_strategy(img: Image.Image, target_bytes: int, wild_mode: bool) -> BaseOptimizationStrategy:
        format = img.format.upper()
        if format == 'JPEG':
            return JpegStrategy(img, target_bytes, wild_mode)
        elif format == 'PNG':
            return PngStrategy(img, target_bytes, wild_mode)
        elif format == 'WEBP':
            return WebPStrategy(img, target_bytes, wild_mode)
        elif format == 'GIF':
            return PngStrategy(img, target_bytes, wild_mode)
        else:
            return JpegStrategy(img, target_bytes, wild_mode)
