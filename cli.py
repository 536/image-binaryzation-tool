import os
import sys

from PIL import Image

from lib import binaryzation

if __name__ == '__main__':
    threshold = 100
    alpha = True
    if len(sys.argv) >= 2:
        for file_path in sys.argv[1:]:
            if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    input_file = os.path.realpath(file_path)
                    img = Image.open(input_file)
                    img = binaryzation(img, threshold=threshold, alpha=alpha)
                    if alpha:
                        output_dir, output_file_ext = os.path.split(input_file)
                        output_file_no_ext = os.path.splitext(output_file_ext)[0]
                        img.save(os.path.join(output_dir, output_file_no_ext + '.png'))
                    else:
                        img.save(input_file)
                except Exception as e:
                    print(e)
    else:
        print('Just drag image files onto this script.')
