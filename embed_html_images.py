import argparse
import base64
import bs4
import os


def embed_image_urls(html_file):
    '''
    Convert Image to Text Equivalent From HTML File
    '''

    try:
        with open(html_file) as fp:
            soup = bs4.BeautifulSoup(fp, "html.parser")
    except IOError as e:
        print("Couldn't open file (%s)." % e)

    # grab the img tags
    images = soup.findAll("img")

    # convert images to text with base64
    for img in images:
        if img.has_attr("src"):
            path_to_image = img['src']
            with open(path_to_image, 'rb') as image_to_text:
                text = base64.b64encode(image_to_text.read())
                converted_text = text.decode('utf-8')
                data_url = "data:image/jpg;base64,"
                path_to_image = path_to_image.replace(path_to_image,
                                                      data_url +
                                                      converted_text)
                img['src'] = path_to_image

    # write contents back to the html file
    try:
        with open(html_file, "wb") as fo:
            fo.write(soup.prettify("utf-8"))
    except IOError as e:
        print("Couldn't open or write to file (%s)." % e)


def main():
    parser = argparse.ArgumentParser(description='Read in HTML \
                                                 file to embed image',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file_path', help='Path of html file to process')
    args = parser.parse_args()
    path = os.path.join(os.getcwd(), args.file_path)
    embed_image_urls(path)


if __name__ == "__main__":
    main()
