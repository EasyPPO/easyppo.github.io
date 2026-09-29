#!/usr/bin/env python3
"""Render equations with the manuscript's mathpazo fonts as standalone SVG.

Requires LaTeX with standalone, amsmath, amssymb, mathpazo, xcolor, and dvisvgm.
The website needs no math runtime or remote font download.
"""
import html
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
MATH = ROOT / 'assets' / 'math'
PREAMBLE = r'''\documentclass[border=2pt]{standalone}
\usepackage{amsmath,amssymb,mathpazo,xcolor}
\definecolor{accent}{HTML}{B53146}
\definecolor{ink}{HTML}{202124}
\begin{document}
\color{ink}$\displaystyle
'''


def render(name, tex, font_size, inline=False):
    with tempfile.TemporaryDirectory(prefix='easyppo-math-') as temporary:
        directory = Path(temporary)
        source = directory / 'equation.tex'
        preamble = PREAMBLE.replace('border=2pt', 'border=0.5pt').replace(r'\displaystyle', r'\textstyle') if inline else PREAMBLE
        source.write_text(preamble + tex + '\n$\n\\end{document}\n')
        for command in (
            ['latex', '-interaction=batchmode', '-halt-on-error', source.name],
            ['dvisvgm', '--no-fonts', '--exact', '--output=equation.svg', 'equation.dvi'],
        ):
            result = subprocess.run(command, cwd=directory, capture_output=True, text=True)
            if result.returncode:
                log = directory / 'equation.log'
                raise RuntimeError(result.stdout + result.stderr + (log.read_text() if log.exists() else ''))
        svg = (directory / 'equation.svg').read_text()
    # Scale 10 TeX points to the chosen CSS font size. Outlined glyphs preserve
    # the paper's fonts on every device, and the viewBox preserves their shape.
    element = ET.fromstring(svg)
    _, _, width, height = map(float, element.attrib['viewBox'].split())
    scale = font_size / (10 * 72 / 72.27)
    dimensions = (math.ceil(width * scale), math.ceil(height * scale))
    svg = re.sub(r"(<svg\b[^>]*?)\bwidth='[^']*'", rf"\g<1>width='{dimensions[0]}'", svg, count=1)
    svg = re.sub(r"(<svg\b[^>]*?)\bheight='[^']*'", rf"\g<1>height='{dimensions[1]}'", svg, count=1)
    (MATH / f'{name}.svg').write_text(svg)
    return dimensions


def main():
    equations = json.loads((MATH / 'equations.json').read_text())
    page = (ROOT / 'index.html').read_text()
    for name, equation in equations.items():
        if equation.get('inline'):
            width, height = render(name, equation['tex'], 16, inline=True)
            image = f'<img src="assets/math/{name}.svg" width="{width}" height="{height}" style="width: {width / 16}em; height: {height / 16}em" alt="{html.escape(equation["alt"], quote=True)}">'
            marker = rf'(<span class="math-inline" data-equation="{name}">)[\s\S]*?(</span>)'
            page, count = re.subn(marker, lambda match: match[1] + image + match[2], page)
            if count != 1:
                raise ValueError(f'Expected one placeholder for {name}, found {count}')
            print(f'{name}: inline {width}×{height}')
            continue
        width, height = render(name, equation['tex'], 22)
        compact_width, compact_height = render(name + '-compact', equation.get('compact', equation['tex']), 20)
        picture = f'''<picture style="--math-width: {width}px; --math-compact-width: {compact_width}px">
        <source media="(max-width: 760px)" srcset="assets/math/{name}-compact.svg" width="{compact_width}" height="{compact_height}">
        <img src="assets/math/{name}.svg" width="{width}" height="{height}" alt="{html.escape(equation['alt'], quote=True)}" loading="lazy">
      </picture>'''
        marker = rf'(<div class="math-display" data-equation="{name}">)[\s\S]*?(</div>)'
        page, count = re.subn(marker, lambda match: match[1] + '\n      ' + picture + '\n    ' + match[2], page)
        if count != 1:
            raise ValueError(f'Expected one placeholder for {name}, found {count}')
        print(f'{name}: {width}×{height}; compact {compact_width}×{compact_height}')
    (ROOT / 'index.html').write_text(page)


if __name__ == '__main__':
    main()
