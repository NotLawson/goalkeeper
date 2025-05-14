# File manager module
# This module controls the server's use of the file system, including file uploads, downloads, and deletions.
import os, sys
class FileManager:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def save_file(self, file, filename):
        """
        Save a file to the server.
        :param file: The file object to save.
        :param filename: The name to save the file as.
        :return: The path to the saved file.
        """
        file_path = os.path.join(self.upload_folder, filename)
        file.save(file_path)
        return file_path

    def delete_file(self, filename):
        """
        Delete a file from the server.
        :param filename: The name of the file to delete.
        :return: True if the file was deleted, False otherwise.
        """
        file_path = os.path.join(self.upload_folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False