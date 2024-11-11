import pygame, os, random


ADJACENT_NEIGHBOR_MAP = {
    tuple(sorted([(0, 1), (1, 0)])): 0, # top left
    tuple(sorted([(0, 1), (1, 0), (-1, 0)])): 1, # top
    tuple(sorted([(0, 1), (-1, 0)])): 3, # top right

    tuple(sorted([(0, -1), (1, 0), (0, 1)])): 4, # left
    tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0)])): 11, # middle
    tuple(sorted([(0, 1), (-1, 0), (0, -1)])): 9, # right

    tuple(sorted([(0, -1), (1, 0)])): 15, # bottom left
    tuple(sorted([(0, -1), (-1, 0), (1, 0)])): 16, # bottom
    tuple(sorted([(0, -1), (-1, 0)])): 18, # bottom right
}
DOUBLE_NEIGHBOR_MAP = {
    tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (0, 2)])): 5, # middle
}

CORNER_NEIGHBOR_MAP = {
    tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, -1), (-1, 1)])): 23, # topleft corner
    tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, -1), (1, 1)])): 22, # topright corner
    tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, 1)])): 21, # bottomleft corner
    tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (1, -1), (-1, 1), (1, 1)])): 20 # bottomright corner
}
TILES_IDS = {
    'sandstone': {
        0: (0, 0),
        1: (1, 0),
        2: (2, 0),
        3: (3, 0), 

        4: (0, 1),
        5: (1, 1),
        6: (2, 1),
        7: (4, 1), 
        8: (5, 1),
        9: (3, 1),

        10: (0, 2),
        11: (1, 2), 
        12: (2, 2),
        13: (4, 2),
        14: (3, 2),
        
        15: (0, 3),
        16: (1, 3),
        17: (2, 3),
        18: (3, 3),
        19: (4, 3),
        
        20: (4, 0),
        21: (5, 0),
        22: (5, 2),
        23: (5, 3),

    }
} 

variants_spawnrates = {
    
    (1, 2): [.6, .4], # top
    (4, 10): [0.6, 0.4], # left
    (9, 14): [0.4, 0.6], # right
    (16, 17): [0.4, 0.6], # bottom

    (5, 6): [0.5, 0.4], # wall
    (11, 12, 13): [0.25, 0.15, 0.6], # walkable tile
}


tile_size = 32
tile_types = ['sandstone']
tile_sprites = {}


sprite_sheets_path = {
    'sandstone': 'assets/tiles/sandstone.png'
}

# loading sprites
def load_surface(image_src, tile_size):
    src = f"{image_src}"
    surf = pygame.image.load(src).convert_alpha()
    surf = pygame.transform.scale(surf, (surf.get_width()/16 * tile_size, surf.get_height()/16 * tile_size))

    return surf

# loading sprite data
def load_data():
    for tile_type in sprite_sheets_path.keys():
        tile_sprites[tile_type] = load_surface(sprite_sheets_path[tile_type], tile_size)

# auto tile
def auto_tile(tiles, tiles_pos):
    tiles = tiles

    for pos in tiles_pos:
        try:
            tile = tiles[pos]
            tile_type = tile.type
            tile_variant = tile.variant

            neighbor_offsets = set()
            adjacent_neighbor_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            double_neighbor_offsets = [(0, -2), (0, 2)]
            corner_neighbor_offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

            # adjacent
            for shift in adjacent_neighbor_offsets:
                offset = pos[0] + shift[0], pos[1] + shift[1]

                if offset in tiles:
                    # if tiles[offset].type == tile_type:
                        neighbor_offsets.add(shift)
            
            for variants in variants_spawnrates:
                if ADJACENT_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))] in variants:
                    picked_variant = random.choices(variants, variants_spawnrates[variants])[0]
                    if not tiles[pos].variant in variants:
                        tiles[pos].change(tile_type, picked_variant, get_surface(tile_sprites[tile_type], TILES_IDS[tile_type].get(picked_variant), tile_size))
                    break
            else:
                tiles[pos].change(tile_type, ADJACENT_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))], get_surface(tile_sprites[tile_type], TILES_IDS[tile_type].get(ADJACENT_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))]), tile_size))
            
            # double
            for shift in double_neighbor_offsets:
                offset = pos[0] + shift[0], pos[1] + shift[1]

                if offset in tiles:
                    if tiles[offset].type == tile_type:
                        neighbor_offsets.add(shift)
            
            for variants in variants_spawnrates:
                if DOUBLE_NEIGHBOR_MAP.get(tuple(sorted(neighbor_offsets))) in variants:
                    picked_variant = random.choices(variants, variants_spawnrates[variants])[0]
                    if not tiles[pos].variant in variants:
                        # print(picked_variant, tiles[pos].variant, variants)
                        tiles[pos].change(tile_type, picked_variant, get_surface(tile_sprites[tile_type], TILES_IDS[tile_type].get(picked_variant), tile_size))
                    break
            if (0, 2) in neighbor_offsets:
                neighbor_offsets.remove((0, 2))
            if (0, -2) in neighbor_offsets:
                neighbor_offsets.remove((0, -2))
            # corner
            for shift in corner_neighbor_offsets:
                offset = pos[0] + shift[0], pos[1] + shift[1]

                if offset in tiles:
                    if tiles[offset].type == tile_type:
                        neighbor_offsets.add(shift)
            
            # for variants in variants_spawnrates:
            #     if tile_variant in variants:
            # print(neighbor_offsets)
            tiles[pos].change(tile_type, CORNER_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))], get_surface(tile_sprites[tile_type], TILES_IDS[tile_type].get(CORNER_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))]), tile_size))
            # print(tiles[pos].variant)
        
        except KeyError as e:
            pass

    return tiles

def get_surface(spritesheet:pygame.Surface, shift_offset, tile_size):
    img = pygame.Surface((tile_size, tile_size)).convert_alpha()
    img.blit(spritesheet, (0, 0), (shift_offset[0] * tile_size, shift_offset[1] * tile_size, tile_size, tile_size))

    return img

class Tile:
    def __init__(self, tile_type, tile_variant, tile_pos, img):
        self.type = tile_type
        self.variant = tile_variant

        self.pos = tile_pos

        self.image = img

        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] * tile_size
        self.rect.y = self.pos[1] * tile_size
    
    def draw(self, draw_surf, camera_offset):
        render_x, render_y = self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]
        draw_surf.blit(self.image, (render_x, render_y))
    
    def change(self, tile_type, tile_variant, img):
        self.type = tile_type
        self.variant = tile_variant
        self.image = img
