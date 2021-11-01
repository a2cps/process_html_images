import argparse
import base64
import bs4
import os


def embed_in_elem(elem: bs4.element.Tag, attr_name: str):
    assert elem.get(attr_name), "element has no HTML attribute " + attr_name
    path_to_image = elem[attr_name]

    if str(path_to_image).endswith('.svg'):
        data_url = "data:image/svg+xml;base64,"
    elif str(path_to_image).endswith(('.png', '.jpg')):
        data_url = "data:image/jpg;base64,"
    else:
        raise Exception("extension not supported")

    with open(path_to_image, 'rb') as image_to_text:
        text = base64.b64encode(image_to_text.read())
        converted_text = text.decode('utf-8')
        path_to_image = path_to_image.replace(path_to_image,
                                                data_url +
                                                converted_text)
        elem[attr_name] = path_to_image


def embed_image_urls(html_file, out_path=None):
    '''
    Convert Image to Text Equivalent From HTML File
    '''

    if not out_path:
        out_path = html_file
        
    try:
        with open(html_file) as fp:
            soup = bs4.BeautifulSoup(fp, "html.parser")
    except IOError as e:
        print("Couldn't open file (%s)." % e)
        raise

    # embed img elements with base64
    for elem in soup.findAll("img"):
        if elem.get('src'):
            embed_in_elem(elem, 'src')

    # embed object elements with base64
    for elem in soup.findAll("object"):
        if elem.get('data'):
            embed_in_elem(elem, 'data')

    # write contents back to the html file
    try:
        with open(out_path, "wb") as fo:
            fo.write(soup.prettify("utf-8"))
    except IOError as e:
        print("Couldn't open or write to file (%s)." % e)
        raise


def main():
    parser = argparse.ArgumentParser(description='Read in HTML \
                                                 file to embed image',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--file_path', required=True, help='Path of html file to process')
    parser.add_argument('--out_path', required=False, default=None, help='Path of html file to process')
    args = parser.parse_args()
    path = os.path.join(os.getcwd(), args.file_path)
    embed_image_urls(html_file=path, out_path=args.out_path)


if __name__ == "__main__":
    main()
