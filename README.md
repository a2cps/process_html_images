# Process HTML Images

Python Script that goes through the a HTML file and replaces the relative links to images with embedded data URLs.

## Get Started

```bash
python embed_html_images.py -o sub-10615.html tests/data/fmriprep/sub-10615.html 
python embed_html_images.py -o sub-10624.html tests/data/qsiprep/sub-10624.html
```

## Docker

```bash
docker run --rm -v $(pwd):/in psadil/process_html_images:main -o sub-10624.html /in/tests/data/qsiprep/sub-10624.html
```
