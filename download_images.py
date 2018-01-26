import argparse
import urllib.request
import os
import time

parser = argparse.ArgumentParser(description="Download a range of images from a url")
parser.add_argument("url")
parser.add_argument("directory")
parser.add_argument("--from_page", type=int, default=1)
parser.add_argument("--to_page", type=int)
parser.add_argument("--pad_to", type=int, default=4)
parser.add_argument("--delay_seconds", type=int, default=5)
args = parser.parse_args()

url = args.url
directory = args.directory
from_page = args.from_page
to_page = args.to_page
pad_to = args.pad_to
delay_seconds = args.delay_seconds

if not os.path.exists(directory):
    os.makedirs(directory)

for page in range(from_page, to_page):
    page_padded = str(page).rjust(pad_to, '0')
    full_url = url.format(page_padded) 
    output = os.path.join(directory, "{}.jpg".format(page_padded)) 
    print("Downloading {} to {}".format(full_url, output))
    urllib.request.urlretrieve(full_url, output)
    time.sleep(delay_seconds)

