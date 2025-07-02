from abc import ABC, abstractmethod

from PIL import Image


class BaseOptimizationStrategy(ABC):
    def __init__(self, img: Image.Image, target_bytes: int, wild_mode: bool):
        self.img = img
        self.target_bytes = target_bytes
        self.wild_mode = wild_mode

    @abstractmethod
    def optimize(self) -> dict:
        """
        Executes the optimization strategy for a given format.

        Returns:
            A dictionary containing the results, e.g.,
            {
                "best_result_data": bytes | None,
                "best_params": dict,
                ...
            }
        """
        pass
