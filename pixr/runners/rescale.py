from PIL import Image, ImageSequence

from pixr.runners import BaseRunner


class RescaleRunner(BaseRunner):
    def run(self) -> None:
        """Rescale image by percentage."""
        input_path = self._validate_input_file()
        output_path = self._determine_output_path(suffix=f"_rescaled_{self.command.options.percentage}pct")

        with Image.open(input_path) as img:
            original_dims = f"{img.width}x{img.height}"
            scale = self.command.options.percentage / 100.0
            new_width = int(img.width * scale)
            new_height = int(img.height * scale)
            new_dims = f"{new_width}x{new_height}"

            if getattr(img, "is_animated", False):
                frames = []
                for frame in ImageSequence.Iterator(img):
                    resized_frame = frame.convert("RGBA").resize((new_width, new_height), Image.Resampling.LANCZOS)
                    frames.append(resized_frame)

                if frames:
                    frames[0].save(
                        output_path,
                        save_all=True,
                        append_images=frames[1:],
                        duration=img.info.get("duration", 100),
                        loop=img.info.get("loop", 0),
                        disposal=2,
                    )
            else:
                new_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                new_img.save(output_path)

            print(f"Rescaled {input_path} ({original_dims}) to {new_dims} and saved to {output_path}")
