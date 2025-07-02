import io

from .base import BaseOptimizationStrategy


class PngStrategy(BaseOptimizationStrategy):
    def optimize(self) -> dict:
        """
        Placeholder for PNG optimization strategy.
        Currently, it just saves the image without changes.
        """
        with io.BytesIO() as buffer:
            self.img.save(buffer, format='PNG', optimize=True)
            data = buffer.getvalue()
            size = buffer.tell()

        return {
            "best_result_data": data,
            "best_params": {"info": "PNG optimization not yet implemented"},
            "smallest_size": size,
            "quality_floor_hit": False,
        }
