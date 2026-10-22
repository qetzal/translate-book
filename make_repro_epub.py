#!/usr/bin/env python3
"""Builds a minimal EPUB exhibiting the markup patterns common in real
publisher EPUBs: empty page anchors, <sup>-marked footnotes with per-chapter
numbering restarts, internal cross-references, heading/span attributes,
em/en dashes and a bibliography 3-em dash."""
import zipfile, os

CH1 = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Ch1</title></head><body>
<a id="page_1"/>
<h2 class="ch_title" id="ch1-title"><a id="ch1-anchor"/>Chapter One</h2>
<p>A paragraph with a page anchor<a id="page_2"/> in the middle, an
internal <a href="bib.xhtml#b1">cross-reference</a>, a
<span lang="lat">sic erat scriptum</span> span, an em dash—like this,
an en dash (pp. 12–34), and a footnote ref.<a href="ch1.xhtml#fn1" id="fr1"><sup>1</sup></a></p>
<p class="note2" id="fn1"><a href="ch1.xhtml#fr1"><sup>1</sup></a> First chapter note.</p>
</body></html>"""

CH2 = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Ch2</title></head><body>
<a id="page_3"/>
<h2 class="ch_title" id="ch2-title">Chapter Two</h2>
<p>Another chapter, whose footnote numbering restarts at one.<a href="ch2.xhtml#fn1" id="fr2"><sup>1</sup></a></p>
<p class="note2" id="fn1"><a href="ch2.xhtml#fr2"><sup>1</sup></a> Second chapter note.</p>
</body></html>"""

BIB = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Bib</title></head><body>
<p class="bibitem" id="b1">Doe, J. <em>Some Book</em>. Press, 2001.</p>
<p class="bibitem">——— <em>Another Book</em>. Press, 2005.</p>
</body></html>"""

OPF = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" version="2.0">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>Repro</dc:title><dc:language>en</dc:language><dc:identifier id="id">repro-1</dc:identifier>
</metadata>
<manifest>
<item id="ch1" href="ch1.xhtml" media-type="application/xhtml+xml"/>
<item id="ch2" href="ch2.xhtml" media-type="application/xhtml+xml"/>
<item id="bib" href="bib.xhtml" media-type="application/xhtml+xml"/>
<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
</manifest>
<spine toc="ncx"><itemref idref="ch1"/><itemref idref="ch2"/><itemref idref="bib"/></spine>
</package>"""

NCX = """<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="repro-1"/></head><docTitle><text>Repro</text></docTitle>
<navMap>
<navPoint id="n1"><navLabel><text>Chapter One</text></navLabel><content src="ch1.xhtml"/></navPoint>
<navPoint id="n2"><navLabel><text>Chapter Two</text></navLabel><content src="ch2.xhtml"/></navPoint>
</navMap></ncx>"""

CONTAINER = """<?xml version="1.0" encoding="utf-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>"""

out = "repro-markup.epub"
if os.path.exists(out):
    os.remove(out)
with zipfile.ZipFile(out, "w") as z:
    z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip")  # first, stored
    z.writestr("META-INF/container.xml", CONTAINER, zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/content.opf", OPF, zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/toc.ncx", NCX, zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/ch1.xhtml", CH1, zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/ch2.xhtml", CH2, zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/bib.xhtml", BIB, zipfile.ZIP_DEFLATED)
print("written:", out, os.path.getsize(out), "bytes")
