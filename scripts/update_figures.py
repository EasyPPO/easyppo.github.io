#!/usr/bin/env python3
"""Render the manuscript's figures for the site; never publish the manuscript PDF.

Requires Pillow and Poppler's pdftoppm/pdftocairo commands.
Usage: python3 scripts/update_figures.py /path/to/manuscript
"""

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image


FIGURES = {
    "teaser": "teaser",
    "filtering": "frontiercs_overlong_filtering",
    "return-noise": "fcs_critic_gradient_combined",
    "main-results": "main_results",
    "critic-learning": "fcs_critic_diagnostics_wrap",
    "normalization": "fcs_normalization_ablation",
    "mini-batches": "fcs_minibatch_ablation",
    "seeds": "fcs_seed_comparison",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    args = parser.parse_args()
    source = args.manuscript.resolve()
    site = Path(__file__).resolve().parents[1]
    assets = site / "assets"
    for stem in FIGURES.values():
        if not (source / "figures" / f"{stem}.pdf").is_file():
            parser.error(f"Missing figure: {stem}.pdf")

    manifest = {}
    with tempfile.TemporaryDirectory(prefix="easyppo-figures-") as temp:
        for name, stem in FIGURES.items():
            pdf = source / "figures" / f"{stem}.pdf"
            prefix = Path(temp) / name
            subprocess.run([
                "pdftoppm", "-scale-to", "2400", "-png", "-singlefile",
                str(pdf), str(prefix),
            ], check=True)
            with Image.open(prefix.with_suffix(".png")) as image:
                image.convert("RGB").save(
                    assets / "figures" / f"{name}.webp",
                    format="WEBP", lossless=True, method=6,
                )
                manifest[name] = {
                    "source": pdf.name,
                    "width": image.width,
                    "height": image.height,
                    "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
                }

    for name in ("berkeley", "princeton"):
        subprocess.run([
            "pdftocairo", "-svg", str(source / "figures" / "logos" / f"{name}.pdf"),
            str(assets / "logos" / f"{name}.svg"),
        ], check=True)
    manifest["paper_commit"] = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=source, text=True,
    ).strip()
    (assets / "figure-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("Figures refreshed. Check image dimensions, captions, scores, and the social preview before publishing.")


if __name__ == "__main__":
    main()
