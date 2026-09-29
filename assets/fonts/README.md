# Paper-matched typography

The manuscript uses URW Palladio (the Palatino family). The website self-hosts P052, the current URW distribution of that family, in regular, bold, italic, and bold italic. No external font service is required.

The original OpenType files are in `source/`; the WOFF2 files are format conversions with unchanged glyphs and metrics. Copyright and the applicable font license are retained in `LICENSE.txt`.

Upstream: <https://github.com/ArtifexSoftware/urw-base35-fonts>

To regenerate a webfont, install FontTools and Brotli, then set `font.flavor = "woff2"` on a `fontTools.ttLib.TTFont` loaded from the corresponding OpenType file and save it.
