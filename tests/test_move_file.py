import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from module import Move_File


class MoveFileTests(unittest.TestCase):
    def test_move_file_moves_contents_and_returns_destination(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_file = root / "source.txt"
            source_file.write_text("content", encoding="utf-8")
            destination_path = root / "destination.txt"

            result = Move_File.move_file(source_file, destination_path)

            self.assertEqual(result, destination_path)
            self.assertFalse(source_file.exists())
            self.assertEqual(
                destination_path.read_text(encoding="utf-8"), "content"
            )

    def test_move_file_wraps_os_errors(self):
        with patch(
            "module.Move_File.shutil.move", side_effect=OSError("disk full")
        ):
            with self.assertRaisesRegex(
                RuntimeError, "Failed to move file: disk full"
            ):
                Move_File.move_file(
                    Path("source.txt"), Path("destination.txt")
                )

    def test_controller_moves_file_to_destination_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_file = root / "source.txt"
            source_file.write_text("content", encoding="utf-8")
            destination_directory = root / "destination"
            destination_directory.mkdir()
            destination_path = destination_directory / source_file.name

            with (
                patch(
                    "module.Move_File.get_source_file", return_value=source_file
                ),
                patch(
                    "module.Move_File.get_destination_directory",
                    return_value=destination_directory,
                ),
                patch("module.Move_File.display_result") as display_result,
            ):
                Move_File.controller()

            self.assertFalse(source_file.exists())
            self.assertEqual(
                destination_path.read_text(encoding="utf-8"), "content"
            )
            display_result.assert_called_once_with(destination_path)

    def test_controller_cancels_overwrite_when_user_declines(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_file = root / "source.txt"
            source_file.write_text("source", encoding="utf-8")
            destination_directory = root / "destination"
            destination_directory.mkdir()
            destination_path = destination_directory / source_file.name
            destination_path.write_text("existing", encoding="utf-8")

            with (
                patch(
                    "module.Move_File.get_source_file", return_value=source_file
                ),
                patch(
                    "module.Move_File.get_destination_directory",
                    return_value=destination_directory,
                ),
                patch("module.Move_File.user_confirmation", return_value=False),
                patch("module.Move_File.move_file") as move_file,
            ):
                Move_File.controller()

            move_file.assert_not_called()
            self.assertEqual(
                source_file.read_text(encoding="utf-8"), "source"
            )
            self.assertEqual(
                destination_path.read_text(encoding="utf-8"), "existing"
            )

    def test_controller_does_not_move_file_onto_itself(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            source_file = Path(temporary_directory) / "source.txt"
            source_file.write_text("content", encoding="utf-8")

            with (
                patch(
                    "module.Move_File.get_source_file", return_value=source_file
                ),
                patch(
                    "module.Move_File.get_destination_directory",
                    return_value=source_file.parent,
                ),
                patch("module.Move_File.move_file") as move_file,
            ):
                Move_File.controller()

            move_file.assert_not_called()
            self.assertEqual(
                source_file.read_text(encoding="utf-8"), "content"
            )


if __name__ == "__main__":
    unittest.main()
