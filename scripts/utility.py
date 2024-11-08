import os, pygame

def load_assets(asset_path):
    imgs = []
    for f in os.listdir(asset_path):
        imgs.append(pygame.image.load(asset_path+f).convert_alpha())        
    
    return imgs

def load_image(img_path):
    return [pygame.image.load(img_path).convert_alpha()]

def resize_image(img, size, relative=False, standard_size=1):
    if relative:
        ori_size = img.get_size()
        return pygame.transform.scale(img, (size/standard_size * ori_size[0], size/standard_size * ori_size[1]))
    else:
        return pygame.transform.scale(img, (size, size))