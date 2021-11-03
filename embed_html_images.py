import argparse
import base64
import bs4
import os
import attr
import click


@attr.s
class ImgEmbedder:
    """Converts link to an image from HTML element to encoded data in 
    the element.
    """
    EXT_TO_TYPE_MAPPING = {
        'svg': 'image/svg+xml',
    }

    elem = attr.ib(type=bs4.element.Tag)
    url_attr = attr.ib(type=str)

    @property
    def img_url(self) -> str:
        """Returns the URL of the linked image"""
        url = self.elem.get(self.url_attr)
        if url:
            return url
        else:
            raise ValueError(f"could not find an HTML attribute {self.url_attr} "
                             f"in the element {self.elem}")

    @property
    def img_encoded(self) -> str:
        with open(self.img_url, 'rb') as f:
            text = base64.b64encode(f.read())
            return text.decode('utf-8')

    @property
    def img_ext(self) -> str:
        """Returns the extension of the image URL, without the dot prefix"""
        root, ext = os.path.splitext(self.img_url)
        return ext.lstrip('.')

    @property
    def dtype(self) -> str:
        """Get the `type` attribute of the HTML element. Guess the data type 
        based on file extension if `type` attribute does not exist or not
        defined in the `EXT_TO_TYPE_MAPPING`.
        """
        dtype = self.elem.get('type')
        if dtype:
            return dtype
        elif self.img_ext in self.EXT_TO_TYPE_MAPPING:
            return self.EXT_TO_TYPE_MAPPING[self.img_ext]
        else:
            return f"image/{self.img_ext}"
    
    @property
    def already_encoded(self) -> bool:
        return hasattr(self, '_og_attr')

    def embed_img(self):
        # save the original contents of the attribute
        if not self.already_encoded:
            self._og_attr = self.elem.get(self.url_attr)
        self.elem[self.url_attr] = f"data:{self.dtype};base64,{self.img_encoded}"


def embed_all_elem(soup: bs4.BeautifulSoup, elem_name: str, url_attr: str = 'src'):
    for elem in soup.findAll(elem_name):
        encoder = ImgEmbedder(elem=elem, url_attr=url_attr)
        encoder.embed_img()


@click.command()
@click.option('-i', '--in-path', required=True, type=click.Path(), 
              help='path to input HTML file')
@click.option('-o', '--out-path', required=False, default=None, type=click.Path(),
              help='path to output file. Omit if same as --in-path')
def embed_in_html(in_path: str, out_path: str = None):
    """Convert external links to images in `in_path` to embedded images.
    """
    if not out_path:
        out_path = in_path
    with open(in_path) as f:
        soup = bs4.BeautifulSoup(f, "html.parser")
    
    # embed all img and object elements
    embed_all_elem(soup, 'img', url_attr='src')
    embed_all_elem(soup, 'object', url_attr='data')

    with open(out_path, "wb") as f:
        f.write(soup.prettify("utf-8"))


if __name__ == "__main__":
    embed_in_html()
