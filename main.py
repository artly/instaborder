from PIL import Image, ImageOps, UnidentifiedImageError, TiffImagePlugin
from os import walk, path, mkdir
from tkinter import filedialog
from sys import argv
from tqdm import tqdm

def pic_resize(pic_orig, desired_size):
    pic_resized = pic_orig
    if (pic_orig.size[0] > desired_size[0] or pic_orig.size[1] > desired_size[1]):
        if (pic_orig.size[0] / pic_orig.size[1] < desired_size[0] / desired_size[1]):
            #  pick resizing coeff by y axis
            y = desired_size[1]
            coeff = desired_size[1] / pic_orig.size[1]
            x = min([round(coeff * pic_orig.size[0]), desired_size[0]])
        else:
            #  pick resizing coeff by x axis
            x = desired_size[0]
            coeff = desired_size[0] / pic_orig.size[0]
            y = min([round(coeff * pic_orig.size[1]), desired_size[1]])
        pic_resized = pic_orig.resize((x, y), Image.LANCZOS)
    return pic_resized

def process_images(dirn):
    for root, dir, filenames in walk(dirn):
        print(root, dir, filenames)
        if root == dirn:
            for f in tqdm(filenames):
                try:
                    pic_orig = Image.open(path.join(root, f))
                except UnidentifiedImageError:
                    continue
                # print(pic_orig.size)
                #  resizing
                pic_resized = pic_resize(pic_orig, (1080, 1350))
                box = tuple((new - old) // 2 for new, old in zip([1080, 1350], pic_resized.size))
                filler_pixel = tuple(map(lambda x: x % 2, pic_resized.size))
                pic_adj = ImageOps.expand(pic_resized, border=(box[0],
                                                               box[1],
                                                               box[0] + filler_pixel[0],
                                                               box[1] + filler_pixel[1]))
                if not path.isdir(path.join(root, "insta")):
                    mkdir(path.join(root, "insta"))
                if not path.isdir(path.join(root, "high_res")):
                    mkdir(path.join(root, "high_res"))
                exif = pic_orig.getexif()
                del exif[TiffImagePlugin.STRIPOFFSETS]
                #  saving for instagram
                pic_adj.save(path.join(root, "insta", ".".join(f.split(".")[:-1]) + "_insta_feed.jpg"),
                             quality=100,
                             subsampling=0,
                             exif=exif)
                #  saving the highres original
                pic_orig.save(path.join(root, "high_res", ".".join(f.split(".")[:-1]) + ".jpg"),
                             quality=100,
                             subsampling=0,
                             exif=exif)

if __name__ == '__main__':
    dirn = ""
    if not argv[1:2]:
        dirn = filedialog.askdirectory(initialdir="~/Documents/Photos/")
        print(dirn)
    else:
        dirn = argv[1]
    if dirn:
        process_images(dirn)
