import os
import shutil
import asyncio
import aiofiles
import logging
from pathlib import Path
from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_arguments():
    parser = ArgumentParser(
        description="Sort files by extension asynchronously.")
    parser.add_argument('source_folder', type=str,
                        help='Path to the source folder containing files.')
    parser.add_argument('output_folder', type=str,
                        help='Path to the output folder for sorted files.')
    return parser.parse_args()


async def copy_file(file_path: Path, output_folder: Path):
    try:
        file_extension = file_path.suffix.lstrip('.').lower() or 'unknown'

        dest_folder = output_folder / file_extension
        dest_folder.mkdir(parents=True, exist_ok=True)

        dest_file_path = dest_folder / file_path.name
        shutil.copy2(file_path, dest_file_path)
        logging.info(f"Copied: {file_path} to {dest_file_path}")
    except Exception as e:
        logging.error(f"Error copying file {file_path}: {e}")


async def read_folder(source_folder: Path, output_folder: Path):
    tasks = []

    for root, _, files in os.walk(source_folder):
        for file in files:
            tasks.append(copy_file(Path(root) / file, output_folder))

    await asyncio.gather(*tasks)


async def main():
    args = parse_arguments()
    source_folder = Path(args.source_folder)
    output_folder = Path(args.output_folder)

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error(f"Source folder '{
                      source_folder}' does not exist or is not a directory.")
        return

    output_folder.mkdir(parents=True, exist_ok=True)

    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    asyncio.run(main())
