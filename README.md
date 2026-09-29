# EasyPPO project website

Static project page for **EasyPPO: Stabilizing the Critic Is Key**.

Published at <https://easyppo.github.io/>. The page, styles, and interactions are implemented without a framework.

## Preview

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000`. No build step or JavaScript dependency installation is required. Text, figures, and navigation also work without JavaScript. JavaScript adds figure previews and citation copying.

## Update

- Edit narrative, authors, links, and the score table in `index.html`.
- Edit styling in `assets/css/style.css`.
- The site uses self-hosted Palladio / Palatino-family fonts to match the manuscript. Font sources and license notices are in `assets/fonts/`.
- The site logo is the [EasyPPO GitHub organization avatar](https://github.com/EasyPPO), saved in `assets/logos/easyppo.png`. The favicon, Apple touch icon, and social preview use the same artwork.
- Equations use the manuscript’s `mathpazo` fonts, rendered as standalone SVGs. Edit the LaTeX in `assets/math/equations.json`, then run `python3 scripts/render_math.py` with LaTeX and dvisvgm installed. Desktop and mobile layouts are generated together; no browser-side math library is needed.
- Figures are rendered from the corresponding manuscript PDFs, without changing plotted data. `assets/figure-manifest.json` records their source filenames, dimensions, checksums, and the manuscript commit.
- The overview video is `assets/videos/easyppo_video.mp4`, with a poster in the same directory. It uses native playback controls and scales to the page width.
- To refresh those assets, run `python3 scripts/update_figures.py /path/to/manuscript` with Pillow and Poppler installed. Check the figures, HTML image dimensions, captions, score table, and social-preview image afterward.
- Code links to the [EasyPPO training repository](https://github.com/EasyPPO/EasyPPO). Paper remains a disabled gray button until its public URL is available. The manuscript PDF is not published in this repository. The footer’s Website source link is only this website’s source.
- Keep score gains and seed-study claims synchronized with the paper. Reported percentage gains compare best validation checkpoints; seed-study bands are min–max, not confidence intervals.

GitHub Pages serves the root of the `main` branch. `.nojekyll` keeps the site static.
