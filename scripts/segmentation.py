# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from PIL import Image
import PIL
import traceback
from scripts import pixel_analyzer as pa
from scripts import deeplab_model, runTilles
import os

domain = 'tree_trunk'

MODEL = deeplab_model.MODEL # load from deeplab_script

def getTreeDBH(filename, tag_width, measured_dbh):
    '''
    Run some images as tiles if no tag was detected with running the full image
    '''
    try:
        # load image
        im = Image.open(filename)

        file = filename.split("/")[-1].split(".")[0]
        #print(file)
        
        # check image orientation and rotate if needed
        width, height = im.size
        if width > height:
          im = im.rotate(270, PIL.Image.NEAREST, expand = 1)
          im.save(filename)

        # run model 
        resized_img , seg_map = MODEL.run(im)
        seg_image = deeplab_model.label_to_color_image(seg_map, domain).astype(np.uint8)

        # move to background later -- saved mask
        new_seg_iamge = Image.fromarray(np.uint8(seg_image)).convert('RGB')
        new_seg_iamge.save('data/outputs/seg_image_original.png')
        resized_img.save('data/outputs/resized_original_img.png')
        #print(resized_img.size)

        # get pixel width of tree around the tag and generate visualization
        pixels_width = pa.getTreePixelWidth(seg_image, file, measured_dbh, tag_width) 

        # if pixel_width is None then no tag was detected try tilling the image
        if pixels_width == None:
          print("Running Tilles")
          seg_image = runTilles.runTilles(filename)

          # move to background later -- saved mask
          new_seg_iamge = Image.fromarray(np.uint8(seg_image)).convert('RGB')
          new_seg_iamge.save('data/outputs/seg_image_original.png')

          # get tree/tag pixel ration
          pixels_width = pa.getTreePixelWidth(seg_image, file, measured_dbh, tag_width) 

        # if no tag is detected return the message
        if pixels_width == None:
          return "No tag detected"
        
        # ESTIMATE DBH !!!
        dbh = pixels_width * tag_width

        return dbh

    except Exception:
        print(traceback.format_exc())
        return "Execution failed"


def getTreeDBH1(filename, tag_width, measured_dbh):

    '''
    Runs all incoming images as tilles 
    '''
    try:
        # load image
        im = Image.open(filename)

        file = filename.split("/")[-1].split(".")[0]
        #print(file)
        
        # check image orientation and rotate if needed
        width, height = im.size
        if width > height:
          im = im.rotate(270, PIL.Image.NEAREST, expand = 1)
          im.save(filename)

        # run model 
        resized_img , seg_map = MODEL.run(im)
        seg_image = deeplab_model.label_to_color_image(seg_map, domain).astype(np.uint8)

        # move to background later -- saved mask
        new_seg_iamge = Image.fromarray(np.uint8(seg_image)).convert('RGB')
        new_seg_iamge.save('data/outputs/seg_image_original.png')
        resized_img.save('data/outputs/resized_original_img.png')


        # get pixel width of tree around the tag and generate visualization
        pixels_width = None 

        if pixels_width == None:
          print("Running Tilles")
          seg_image = runTilles.runTilles(filename)

          # move to background later -- saved mask
          new_seg_iamge = Image.fromarray(np.uint8(seg_image)).convert('RGB')
          new_seg_iamge.save('data/outputs/seg_image_original.png')

          # get tree/tag pixel ration
          pixels_width = pa.getTreePixelWidth(seg_image, file, measured_dbh, tag_width) 

        # if no tag is detected return the message
        if pixels_width == None:
          return "No tag detected"
        
        # ESTIMATE DBH !!!
        dbh = pixels_width * tag_width

        return dbh

    except Exception:
        print(traceback.format_exc())
        return "Execution failed"


def getTreeDBH2(filename, tag_width, measured_dbh):
  try:
    # load image
    im = Image.open(filename)

    # filename
    file = filename.split("/")[-1].split(".")[0]

    # check the orientation
    width, height = im.size
    if width > height:
      im = im.rotate(270, PIL.Image.NEAREST, expand = 1)
      im.save(filename)

    # run model as tilled
    #resized_im, seg_map = MODEL.run(im)
    resized_img, seg_image = runTilles.runTilles(filename)
    new_seg_iamge = Image.fromarray(np.uint8(seg_image)).convert('RGB')
    new_seg_iamge.save('data/outputs/seg_image_original_1.png')
    resized_img.save('data/outputs/resized_original_img_1.png')

    
    # get zoom coordinates on tag
    left,top,right,bottom = pa.getZoomCordinates(seg_image, 100)  

    # Zoom into resized image
    zoomed_img = resized_img.crop((left,top,right,bottom))
    zoomed_img.save(f'data/outputs/zoomed_img_{file}.png') 

    # get dbh on zoomed image
    dbh = getTreeDBH(f'data/outputs/zoomed_img_{file}.png', tag_width, measured_dbh)

    return dbh
  except:
    print(traceback.format_exc())
    return None