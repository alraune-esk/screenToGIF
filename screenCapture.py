from PIL import ImageGrab
from PIL import Image
import time
import os
import glob
import win32gui
import ctypes
ctypes.windll.user32.SetProcessDPIAware() # for DPI scaling
import imageio
import pathlib
from pygifsicle import optimize


def capture(numShots=1,delaySec=0,qual=95):
    """
    Capture screenshots with a specified delay inbetween and save as bmps 
    Paste cursor to each image (otherwise wont show in gif)
    
    """
    imCursor = Image.open('cursor.png')
    
    for n in range(numShots):
        im=ImageGrab.grab()
        curX,curY=win32gui.GetCursorPos()
        im.paste(imCursor,box=(curX,curY),mask=imCursor)
        fname="output/{}.bmp".format(time.time())
        print("saving [{0}] ({1} of {2})".format(fname,n+1,numShots))
        #im.resize((600,800),Image.ANTIALIAS)
        im.save(fname, optimize=True, quality=qual)
        if delaySec:
            time.sleep(delaySec)


if __name__=="__main__":
    if not os.path.exists("output/"):
        os.mkdir("output")
    # remove images from previous gif making
    for fname in glob.glob("output/*.bmp"):
        os.remove(fname)
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("3")
    # get the screenshots
    capture(numShots=40,delaySec=1/5,qual=10)
    
    images = []
    filenames = os.listdir("output")
    cwd = os.path.dirname(os.path.realpath(__file__))
    img_save_loc = os.path.join(cwd, "output")
    gif_save_loc = os.path.join(cwd, "output_gif")
    
    for filename in filenames:
        images.append(imageio.imread(os.path.join(img_save_loc,filename)))
    output_filename = "output_{}.gif".format(time.time())
    # convert all the images into a single gif, also produce an optimised version to see if it reduces size
    imageio.mimsave(os.path.join(gif_save_loc, output_filename), images)
    optimize(os.path.join(gif_save_loc, output_filename), os.path.join(gif_save_loc, "optimised_" + output_filename))

    # for fname in glob.glob("output/*.bmp"):
    #     os.remove(fname)