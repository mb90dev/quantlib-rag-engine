import os
from pathlib import Path
from typing import Dict

import trafilatura
from ..config import *


# Mapping of logical document names to their source URLs
URLS: Dict[str, str] = {
    "basics": "https://quantlib-python-docs.readthedocs.io/en/latest/basics.html",
    "cashflows": "https://quantlib-python-docs.readthedocs.io/en/latest/cashflows.html",
    "dates": "https://quantlib-python-docs.readthedocs.io/en/latest/dates.html",
    "indexes": "https://quantlib-python-docs.readthedocs.io/en/latest/indexes.html",
    "instruments": "https://quantlib-python-docs.readthedocs.io/en/latest/instruments.html",
    "pricing_engines": "https://quantlib-python-docs.readthedocs.io/en/latest/pricing_engines.html",
    "termstructures": "https://quantlib-python-docs.readthedocs.io/en/latest/termstructures.html",
}


class QuantLibDocsDownloader:
    """
    Klasa odpowiedzialna za:
    - ustalenie katalogu wyjściowego (data/processed/quantlib_md)
    - pobranie stron z ReadTheDocs
    - konwersję do markdown (trafilatura)
    - zapis plików .md
    """

    def __init__(self, output_dir: Path | None = None, urls: Dict[str, str] | None = None) -> None:
        self.output_dir = output_dir or MD_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.urls = urls if urls is not None else URLS

    @staticmethod
    def download_and_convert(url: str) -> str | None:
        """
        Download a single URL and return its content as markdown (string),
        or None if something went wrong.
        """
        try:
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                print(f"[WARN] Could not fetch URL: {url}")
                return None

            md = trafilatura.extract(downloaded, output_format="markdown")
            if not md:
                print(f"[WARN] Could not extract main content from: {url}")
                return None

            return md
        except Exception as exc:
            print(f"[ERROR] Exception while processing {url}: {exc}")
            return None

    def run(self) -> None:
        """
        Główna metoda – iteruje po URLS, pobiera, konwertuje i zapisuje .md
        """
        print(f"[INFO] Output directory: {self.output_dir}")

        for name, url in self.urls.items():
            print(f"[INFO] Downloading '{name}' from {url} ...")
            md_content = self.download_and_convert(url)

            if md_content is None:
                print(f"[WARN] Skipping '{name}' due to previous errors.")
                continue

            out_path = self.output_dir / f"{name}.md"
            try:
                with out_path.open("w", encoding="utf-8") as f:
                    f.write(md_content)
                print(f"[INFO] Saved: {out_path}")
            except OSError as exc:
                print(f"[ERROR] Failed to write file {out_path}: {exc}")

        print("[INFO] Done.")


def main() -> None:
    downloader = QuantLibDocsDownloader()
    downloader.run()


if __name__ == "__main__":
    main()
