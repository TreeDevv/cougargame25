
def pixel_to_relative(pixel_coords: (int, int), screen_size: (int, int)) -> (float, float):
    xRel = pixel_coords[0] / screen_size[0]
    yRel = pixel_coords[1] / screen_size[1]
    return (xRel, yRel)
                            
def relative_to_pixel(relative_coords: (float, float), screen_size: (int, int)) -> (int, int):
    xPix = int(relative_coords[0] * screen_size[0])
    yPix = int(relative_coords[1] * screen_size[1])
    return (xPix, yPix)

def anchor_center(position: (int, int), surface_size: (int, int)) -> (int, int):
    xCentered = position[0] - surface_size[0] // 2
    yCentered = position[1] - surface_size[1] // 2
    return (xCentered, yCentered)