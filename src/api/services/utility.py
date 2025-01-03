import os
import zipfile

from ..core import config

download_path = config.DOWNLOAD_PATH


class FileMedia:
    def clearFile(Self, file):
        if os.path.exists(file):
            os.remove(file)

    def zipPlaylistDir(Self, filename: str, filesDir: str):
        with zipfile.ZipFile(f"{filename}.zip", "w") as zip:
            zip.write(filesDir, arcname=f"playlist_{filename}")

        return f"{filename}.zip"

    def zipPlaylistFiles(Self, filename: str, files: list):
        zip_path = f"{download_path}/{filename}.zip"

        with zipfile.ZipFile(zip_path, "w") as zip:
            for file in files:
                zip.write(file)

        for file in files:
            Self.clearFile(file=file)

        return zip_path
