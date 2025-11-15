import pygame
from PIL import Image,ImageStat
import os


#currentImage = Image.open("src/scenes/Media/dogbarking.jpg") #Need to add image path here 


#SIZE = (img.height // 5, img.width // 5) #Pixel size
#ORIGINAL_SIZE = (img.width, img.height) #Original size
#NEW_SIZE = (300, 300) #Output size

def pixelizeImage(currentImage, SIZE):

#RESIZE IMAGE TO MAX HEIGHT OF 500 FOR PROCESSING
    ORIGINAL_SIZE = currentImage.size
    MAX_HEIGHT = 1500
    w, h = ORIGINAL_SIZE
    scale_factor = MAX_HEIGHT / h
    resized_width = int(w * scale_factor)
    resized_height = MAX_HEIGHT
    resized = currentImage.resize((resized_width, resized_height), Image.NEAREST)

#PIXELATE IMAGE
    downscaled = resized.resize(SIZE, Image.NEAREST)
    upscaledImage = downscaled.resize((resized_width, resized_height), Image.NEAREST)
    #resizedImage = currentImage.resize(SIZE, Image.NEAREST) #Image.LANCZOS for smoother
  #  upscaledImage = resizedImage.resize(ORIGINAL_SIZE, Image.NEAREST) #Image.FIXED for smoother

    return upscaledImage


photoList = [
    "axes1.jpg",
    "axes2.jpg",
    "ball1.jpg",
    "ball2.jpg",
    "bar1.jpg",
    "bar2.jpg",
    "bass1.jpg",
    "bass2.jpg",
    "bat1.jpg",
    "bat2.jpg",
    "bow1.jpg",
    "bow2.jpg",
    "broke1.jpg",
    "broke2.jpg",
    "chile1.jpg",
    "chile2.jpg",
    "china1.jpg",
    "china2.jpg",
    "converse1.jpg",
    "converse2.jpg",
    "cow1.jpg",
    "cow2.jpg",
    "crane1.jpg",
    "crane2.jpg",
    "flush1.jpg",
    "flush2.jpg",
    "fly1.jpg",
    "fly2.jpg",
    "gas1.jpg",
    "gas2.jpg",
    "grave1.jpg",
    "grave2.jpg",
    "jam1.jpg",
    "jam2.jpg",
    "land1.jpg",
    "land2.jpg",
    "lead1.jpg",
    "lead2.jpg",
    "leaves1.jpg",
    "leaves2.jpg",
    "light1.jpg",
    "light2.jpg",
    "mark1.jpg",
    "mark2.jpg",
    "minute1.jpg",
    "minute2.jpg",
    "palm1.jpg",
    "palm2.jpg",
    "park1.jpg",
    "park2.jpg",
    "patient1.jpg",
    "patient2.jpg",
    "peak1.jpg",
    "peak2.jpg",
    "pen1.jpg",
    "pen2.jpg",
    "record1.jpg",
    "record2.jpg",
]
base_path = os.path.join(os.path.dirname(__file__), 'scenes', 'Media')
output_path = os.path.join(base_path, 'Pixelized')

# Create output folder if it doesn't exist
os.makedirs(output_path, exist_ok=True)

for filename in photoList:
    full_path = os.path.join(base_path, filename)

    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        continue

    img = Image.open(full_path)

    pixel_size = (img.width // 60, img.height // 60)

    updatedImage = pixelizeImage(img, pixel_size)
    
    # Save the pixelized image
    output_file = os.path.join(output_path, f"pixelized_{filename}")
    updatedImage.save(output_file)
    print(f"Saved: {output_file}")


# for imagePath in photoList:
#     img = Image.open(full_path)

#     pixel_size = (img.width // 5, img.height // 5)

#     updatedImage = pixelizeImage(img, pixel_size)
#     updatedImage.show()
