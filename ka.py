from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import io
import os
import sys
import json
import urllib3
import multiprocessing

from PIL import Image
from tqdm import tqdm
from urllib3.util import Retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def download_image(fnames_and_urls):
    """
    download image and save its with 90% quality as JPG format
    skip image downloading if image already exists at given path
    :param fnames_and_urls: tuple containing absolute path and url of image
    """
    fname, url = fnames_and_urls
    if not os.path.exists(fname):
        http = urllib3.PoolManager(retries=Retry(connect=3, read=2, redirect=3))
        response = http.request("GET", url)
        image = Image.open(io.BytesIO(response.data))
        image_rgb = image.convert("RGB")
        image_rgb.save(fname, format='JPEG', quality=100)


def parse_dataset(dataset, outdir, _max=10000, label=False):
    """
    parse the dataset to create a list of tuple containing absolute path and url of image
    :param _dataset: dataset to parse
    :param _outdir: output directory where data will be saved
    :param _max: maximum images to download (change to download all dataset)
    :return: list of tuple containing absolute path and url of image
    """
    #if label == False:
    _fnames_urls = []
    with open(dataset, 'r') as f:
        data = json.load(f)
        for image in data["images"]:
            url = image["url"]
            fname = os.path.join(outdir, "{}.jpg".format(image["imageId"]))
            _fnames_urls.append((fname, url))
    #    return _fnames_urls[:_max]
    #else:
    #_fnames_urls = []
    #with open(dataset, 'r') as f:
    #    data = json.load(f)
    #    for image in data["annotations"]:
    #        url = ""
    #        for i in image["labelId"]:
    #            url = url+i+"\n"
    #        #url = image["labelId"]
    #        fname = os.path.join(outdir, "{}.jpg.txt".format(image["imageId"]))
    #        _fnames_urls.append((fname, url))
    return _fnames_urls[:_max]
def save_file(fnames_and_label):
    fname, label = fnames_and_label
    if not os.path.exists(fname):
        with open(fname, "w") as text_file:
            text_file.write(label)
 
if __name__ == '__main__':

    data_path = input("Data path: ")
    out_path = input("Output path: ")
    num_pic = input("Numbers: ")
    label = bool(input("Label: "))
    #quality = input("Quality: ")
    #if quality == "":
    #    quality = 90
    #else:
    #    quality = int(quality)
    # parse json dataset file
    #if label == "F":
    fnames_urls = parse_dataset(data_path, out_path, _max = int(num_pic))

    # download data
    pool = multiprocessing.Pool(processes=16)
    with tqdm(total=len(fnames_urls)) as progress_bar:
        for _ in pool.imap_unordered(download_image, fnames_urls):
            progress_bar.update(1)
    #else:
    #fnames_urls = parse_dataset(data_path, out_path, _max = int(num_pic), label=True)
    #pool = multiprocessing.Pool(processes=8)
    #with tqdm(total=len(fnames_urls)) as progress_bar:
    #    for _ in pool.imap_unordered(save_file, fnames_urls):
    #        progress_bar.update(1)    
    sys.exit(1)
    
    #if len(sys.argv) != 3:
    #    print("error: not enough arguments")
    #    sys.exit(0)
    #
    # get args and create output directory
    #dataset, outdir = sys.argv[1:]
    #if not os.path.exists(outdir):
    #    os.makedirs(outdir)
    #
    ## parse json dataset file
    #fnames_urls = parse_dataset(dataset, outdir)
    #
    ## download data
    #pool = multiprocessing.Pool(processes=12)
    #with tqdm(total=len(fnames_urls)) as progress_bar:
    #    for _ in pool.imap_unordered(download_image, fnames_urls):
    #        progress_bar.update(1)
    #
    #sys.exit(1)