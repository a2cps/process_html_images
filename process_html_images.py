import base64
from pathlib import Path

import bs4
import click

ELEMS = {"img": "src", "object": "data"}


def embed_all_elem(
    soup: bs4.BeautifulSoup, root: Path, elem_name: str, url_attr: str = "src"
):
    for elem in soup.find_all(elem_name):
        if elem.get("type") == "image/gif":
            with open(root / elem.get(url_attr), "rb") as f:
                text = base64.b64encode(f.read()).decode("utf-8")
                elem[url_attr] = f"data:image/gif;base64,{text}"
        else:
            with open(root / elem.get(url_attr)) as f:
                if "carpetplot" in elem.get(url_attr):
                    s = bs4.BeautifulSoup(f, features="xml")
                    tag = s.svg
                    tag["width"] = "100%"
                    del tag["height"]
                else:
                    tag = bs4.BeautifulSoup(f, features="html.parser")
                elem.replace_with(tag)


@click.command()
@click.argument("in-path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "-o",
    "--out-path",
    required=False,
    default=None,
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    help="path to output file. Omit if same as in-path",
)
def embed_in_html(in_path: Path, out_path: Path = None):
    """Convert external links to images in `in_path` to embedded images."""
    if not out_path:
        out_path = in_path
    with open(in_path) as f:
        soup = bs4.BeautifulSoup(f, "html.parser")

    # embed all img and object elements
    for elem_name, url_attr in ELEMS.items():
        embed_all_elem(
            soup, root=in_path.parent, elem_name=elem_name, url_attr=url_attr
        )

    with open(out_path, "wb") as f:
        f.write(soup.encode(formatter="html5"))


if __name__ == "__main__":
    embed_in_html()
