import io

from .base import BaseOptimizationStrategy


class JpegStrategy(BaseOptimizationStrategy):
    def optimize(self) -> dict:
        """
        Performs a binary search on JPEG quality to meet the target size.
        """
        low = 1
        high = 100
        min_quality = 1 if self.wild_mode else 50
        best_result_data = None
        best_quality = -1
        smallest_size_so_far = float('inf')
        smallest_size_data = None
        smallest_size_quality = -1
        quality_floor_hit = False

        img = self.img
        if img.mode != 'RGB':
            img = img.convert('RGB')

        iterations = 0
        max_iterations = 10  # Safety break

        while low <= high and iterations < max_iterations:
            iterations += 1
            mid_quality = (low + high) // 2

            if mid_quality < min_quality:
                quality_floor_hit = True
                break

            with io.BytesIO() as buffer:
                img.save(buffer, format='JPEG', quality=mid_quality, optimize=True)
                current_size = buffer.tell()

                if current_size < smallest_size_so_far:
                    smallest_size_so_far = current_size
                    smallest_size_data = buffer.getvalue()
                    smallest_size_quality = mid_quality

                if current_size <= self.target_bytes:
                    best_result_data = buffer.getvalue()
                    best_quality = mid_quality
                    low = mid_quality + 1
                else:
                    high = mid_quality - 1

        if not best_result_data and smallest_size_data:
            best_result_data = smallest_size_data
            best_quality = smallest_size_quality

        return {
            "best_result_data": best_result_data,
            "best_params": {"quality": best_quality},
            "smallest_size": smallest_size_so_far,
            "quality_floor_hit": quality_floor_hit,
        }
