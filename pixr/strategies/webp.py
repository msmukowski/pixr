import io

from .base import BaseOptimizationStrategy


class WebPStrategy(BaseOptimizationStrategy):
    def optimize(self) -> dict:
        """
        Placeholder for WebP optimization strategy.
        Currently, it just saves the image with default quality.
        """
        with io.BytesIO() as buffer:
            self.img.save(buffer, format='WEBP', quality=80)
            data = buffer.getvalue()
            size = buffer.tell()

        return {
            "best_result_data": data,
            "best_params": {"info": "WebP optimization not yet implemented"},
            "smallest_size": size,
            "quality_floor_hit": False,
        }
