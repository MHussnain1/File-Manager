import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from module import Copy_File


class CopyFileTests(unittest.TestCase):
    def test_get_source_file_retries_invalid_paths(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_file = root / "source.txt"
            source_file.write_text("content", encoding="utf-8")
            directory = root / "directory"
            directory.mkdir()

            with (
                patch(
                    "builtins.input",
                    side_effect=[
                        " ",
                        str(root / "missing.txt"),
                        str(directory),
                        str(source_file),
                    ],
                ),
                patch("builtins.print") as print_mock,
            ):
                result = Copy_File.get_source_file()

            self.assertEqual(result, source_file)
            self.assertEqual(print_mock.call_count, 3)

    def test_get_destination_directory_retries_invalid_paths(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            file_path = root / "file.txt"
            file_path.write_text("content", encoding="utf-8")
            destination = root / "destination"
            destination.mkdir()

            with (
                patch(
                    "builtins.input",
                    side_effect=[
                        "",
                        str(root / "missing"),
                        str(file_path),
                        str(destination),
                    ],
                ),
                patch("builtins.print") as print_mock,
            ):
                result = Copy_File.get_destination_directory()

            self.assertEqual(result, destination)
            self.assertEqual(print_mock.call_count, 3)

    def test_get_destination_path_uses_source_filename(self):
        source_file = Path("source.txt")
        destination_directory = Path("target")

        result = Copy_File.get_destination_path(source_file, destination_directory)

        self.assertEqual(result, destination_directory / "source.txt")

    def test_destination_exists_checks_path(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            destination_path = Path(temporary_directory) / "copy.txt"

            self.assertFalse(Copy_File.destination_exists(destination_path))
            destination_path.touch()
            self.assertTrue(Copy_File.destination_exists(destination_path))

    def test_user_confirmation_retries_invalid_response(self):
        with patch("builtins.input", side_effect=["maybe", " YES "]), patch(
            "builtins.print"
        ) as print_mock:
            result = Copy_File.user_confirmation(Path("copy.txt"))

        self.assertTrue(result)
        print_mock.assert_called_once_with(
            "Invalid response. Please enter 'y' or 'n'."
        )

    def test_user_confirmation_accepts_no(self):
        with patch("builtins.input", return_value="n"):
            self.assertFalse(Copy_File.user_confirmation(Path("copy.txt")))

    def test_copy_file_copies_contents_and_returns_destination(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_file = root / "source.txt"
            source_file.write_text("content", encoding="utf-8")
            destination_path = root / "destination.txt"

            result = Copy_File.copy_file(source_file, destination_path)

            self.assertEqual(result, destination_path)
            self.assertEqual(
                destination_path.read_text(encoding="utf-8"), "content"
            )

    def test_copy_file_wraps_os_errors(self):
        with patch("module.Copy_File.shutil.copy2", side_effect=OSError("disk full")):
            with self.assertRaisesRegex(RuntimeError, "Failed to copy file: disk full"):
                Copy_File.copy_file(Path("source.txt"), Path("destination.txt"))

    def test_display_result_reports_success_and_failure(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            destination_path = Path(temporary_directory) / "copy.txt"
            destination_path.write_text("content", encoding="utf-8")

            with patch("builtins.print") as print_mock:
                Copy_File.display_result(destination_path)

            print_mock.assert_called_once_with(
                f"File copied successfully to: {destination_path}"
            )

            destination_path.unlink()
            with patch("builtins.print") as print_mock:
                Copy_File.display_result(destination_path)

            print_mock.assert_called_once_with("File was not copied.")

    def test_controller_copies_file_to_destination_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_file = root / "source.txt"
            source_file.write_text("content", encoding="utf-8")
            destination_directory = root / "destination"
            destination_directory.mkdir()
            destination_path = destination_directory / source_file.name

            with (
                patch(
                    "module.Copy_File.get_source_file", return_value=source_file
                ),
                patch(
                    "module.Copy_File.get_destination_directory",
                    return_value=destination_directory,
                ),
                patch("module.Copy_File.display_result") as display_result,
            ):
                Copy_File.controller()

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
                    "module.Copy_File.get_source_file", return_value=source_file
                ),
                patch(
                    "module.Copy_File.get_destination_directory",
                    return_value=destination_directory,
                ),
                patch("module.Copy_File.user_confirmation", return_value=False),
                patch("module.Copy_File.copy_file") as copy_file,
                patch("builtins.print") as print_mock,
            ):
                Copy_File.controller()

            copy_file.assert_not_called()
            self.assertEqual(
                destination_path.read_text(encoding="utf-8"), "existing"
            )
            print_mock.assert_any_call(
                "\nOperation cancelled. File was not copied."
            )

    def test_controller_does_not_copy_file_onto_itself(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            source_file = Path(temporary_directory) / "source.txt"
            source_file.write_text("content", encoding="utf-8")

            with (
                patch(
                    "module.Copy_File.get_source_file", return_value=source_file
                ),
                patch(
                    "module.Copy_File.get_destination_directory",
                    return_value=source_file.parent,
                ),
                patch("module.Copy_File.user_confirmation") as confirmation,
                patch("module.Copy_File.copy_file") as copy_file,
                patch("builtins.print") as print_mock,
            ):
                Copy_File.controller()

            confirmation.assert_not_called()
            copy_file.assert_not_called()
            print_mock.assert_any_call(
                "\nSource and destination are the same file. No copy was made."
            )


if __name__ == "__main__":
    unittest.main()
