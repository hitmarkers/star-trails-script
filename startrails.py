#modules(you need to download some of them)
import rawpy
import imageio
import cv2 
import glob
import numpy
from blend_modes import lighten_only
from tqdm import tqdm 


#globals

#plug in your raw photos(keep the *. change the filetype depending on you camera)
files = glob.glob("directory*.nef")

#functions

def read_image(file):  #reading any image
    
    with rawpy.imread(file) as raw:
        image_array = raw.postprocess()  #add any argument you like such temperature etc(serach documentation)
    image_float = image_array.astype(numpy.float32) 
    image_float = cv2.cvtColor(image_float, cv2.COLOR_RGB2BGR)
    return image_float
 

def add_alpha(image_float): #adding alpha channel dependency of blend modes
    r_channel, g_channel, b_channel = cv2.split(image_float)
    alpha_channel = numpy.ones(b_channel.shape, b_channel.dtype)*255.0
    RGBA_image_float = cv2.merge((r_channel, g_channel, b_channel, alpha_channel))
    return RGBA_image_float 


def blend(image1, image2):
    blended_float = lighten_only(image1, image2, opacity = 0.75) #change opacity to your liking just like ps
    return blended_float                                         #note: 0 to 1


#main
def main():
    #reading and blending first 2 images
    file = files.pop(0)
    image_float1 = read_image(file)
    RGBA_image_float1 = add_alpha(image_float1)

    file = files.pop(0)
    image_float2 = read_image(file)
    RGBA_image_float2 = add_alpha(image_float2)

    first_blend = blend(RGBA_image_float1, RGBA_image_float2)


    #blending rest of the files
    for img_file in tqdm(files):
        image_array_float = read_image(img_file)
        RGBA_image_array_float = add_alpha(image_array_float)
        first_blend= blend(first_blend, RGBA_image_array_float)

    #saving final product
    r_channel, g_channel, b_channel, alpha_channel = cv2.split(first_blend)
    RGB_image = cv2.merge((r_channel, g_channel, b_channel)) 
    RGB_image = cv2.cvtColor(RGB_image, cv2.COLOR_BGR2RGB)
    #save directory
    cv2.imwrite('save_directory', RGB_image)
    
    
main()