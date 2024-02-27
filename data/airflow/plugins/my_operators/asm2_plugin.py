from airflow.plugins_manager import AirflowPlugin
from airflow.models import BaseOperator
import logging as log
from airflow.utils.decorators import apply_defaults

import requests
import zipfile
import warnings
from sys import stdout
from os import makedirs
from os.path import dirname
from os.path import exists


class GoogleDriveDownloader(BaseOperator):
    """
    Minimal class to download shared files from Google Drive.
    """
    @apply_defaults
    def __init__(self, file_id, dest_path, overwrite, unzip, showsize, *args, **kwargs):
        self.file_id = file_id
        self.dest_path = dest_path
        self.overwrite = overwrite
        self.unzip = unzip
        self.showsize = showsize
        super().__init__(*args, **kwargs)

    CHUNK_SIZE = 32768
    DOWNLOAD_URL = 'https://docs.google.com/uc?export=download'

    
    def execute(self, context):

        dest_path = self.dest_path
        log.info(f"Destination set to: {dest_path}")
        file_id = self.file_id
        log.info(f"File ID input as: {file_id}")
        overwrite = self.overwrite
        log.info(f"Overwirte mode set to: {overwrite}")
        unzip = self.unzip
        log.info(f"Unzip mode set to: {unzip}")
        showsize = self.showsize
        log.info(f"Showsize mode set to: {showsize}")

        destination_directory = dirname(dest_path)
        if not exists(destination_directory):
            makedirs(destination_directory)

        if not exists(dest_path) or overwrite:

            session = requests.Session()

            log.info('Downloading {} into {}... '.format(file_id, dest_path), end='')
            stdout.flush()

            response = session.post(GoogleDriveDownloader.DOWNLOAD_URL, params={'id': file_id, 'confirm': 't'}, stream=True)

            if showsize:
                print()  # Skip to the next line

            current_download_size = [0]
            GoogleDriveDownloader._save_response_content(response, dest_path, showsize, current_download_size)
            log.info('Done.')

            if unzip:
                try:
                    print('Unzipping...', end='')
                    stdout.flush()
                    with zipfile.ZipFile(dest_path, 'r') as z:
                        z.extractall(destination_directory)
                    print('Done.')
                except zipfile.BadZipfile:
                    warnings.warn('Ignoring `unzip` since "{}" does not look like a valid zip file'.format(file_id))

    @staticmethod
    def _save_response_content(response, destination, showsize, current_size):
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(GoogleDriveDownloader.CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    if showsize:
                        log.info('\r' + GoogleDriveDownloader.sizeof_fmt(current_size[0]), end=' ')
                        stdout.flush()
                        current_size[0] += GoogleDriveDownloader.CHUNK_SIZE

    # From https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    @staticmethod
    def sizeof_fmt(num, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return '{:.1f} {}{}'.format(num, unit, suffix)
            num /= 1024.0
        return '{:.1f} {}{}'.format(num, 'Yi', suffix)


class AsmPlugin (AirflowPlugin):
    name = "asm2_plugin"
    operators = [GoogleDriveDownloader]
    sensors = []