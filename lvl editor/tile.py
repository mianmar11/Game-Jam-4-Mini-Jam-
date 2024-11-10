import pygame, os, random


ADJACENT_NEIGHBOR_MAP = {
    tuple(sorted([(0, 1), (1, 0)])): 0, # top left
    tuple(sorted([(0, 1), (1, 0), (-1, 0)])): 1, # top
    tuple(sorted([(0, 1), (-1, 0)])): 3, # top right

    tuple(sorted([(0, -1), (1, 0), (0, 1)])): 4, # left
    tuple(sorted([(0, 1), (-1, 0), (0, -1)])): 7, # right

    tuple(sorted([(0, -1), (1, 0)])): 12, # bottom left
    tuple(sorted([(0, -1), (-1, 0), (1, 0)])): 13, # bottom
    tuple(sorted([(0, -1), (-1, 0)])): 15, # bottom right
}
DOUBLE_NEIGHBOR_MAP = {
    tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (0, 2)])): 5, # middle
    tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (0, -2)])): 9, # middle
}

CORNER_NEIGHBOR_MAP = {
    tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, -1), (-1, 1)])): 9, # topleft corner
    tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, -1), (1, 1)])): 10, # topright corner
    tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, 1)])): 11, # bottomleft corner
    tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (1, -1), (-1, 1), (1, 1)])): 12 # bottomright corner
}
TILES_IDS = {
    'sandstone': {
        0: (0, 0),
        1: (1, 0),
        2: (2, 0),
        3: (3, 0), 
        16: (4, 0),

        4: (0, 1),
        5: (1, 1),
        6: (2, 1),
        7: (3, 1), 
        
        8: (0, 2),
        9: (1, 2),
        10: (2, 2),
        11: (3, 2), 
        17: (4, 2),
        
        12: (0, 3),
        13: (1, 3),
        14: (2, 3),
        15: (3, 3),

    }
} 

variants_spawnrates = {
    
    (1, 2): [.6, .4], # top
    (4, 8): [0.6, 0.4], # left
    (7, 11): [0.4, 0.6], # right
    (13, 14): [0.4, 0.6], # bottom

    (5, 6): [0.5, 0.4], # wall
    (9, 10, 17): [0.25, 0.15, 0.6], # walkable tile
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
                    if tiles[offset].type == tile_type:
                        neighbor_offsets.add(shift)
            
            for variants in variants_spawnrates:
                if ADJACENT_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))] in variants:
                    picked_variant = random.choices(variants, variants_spawnrates[variants])[0]
                    tiles[pos].change(tile_type, ADJACENT_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))], get_surface(tile_sprites[tile_type], TILES_IDS[tile_type].get(picked_variant), tile_size))
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
                # print(neighbor_offsets, DOUBLE_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))])
                if DOUBLE_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))] in variants:
                    print(variants)
                    picked_variant = random.choices(variants, variants_spawnrates[variants])[0]
                    tiles[pos].change(tile_type, DOUBLE_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))], get_surface(tile_sprites[tile_type], TILES_IDS[tile_type].get(picked_variant), tile_size))
                    break
            else:
                tiles[pos].change(tile_type, DOUBLE_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))], get_surface(tile_sprites[tile_type], TILES_IDS[tile_type].get(DOUBLE_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))]), tile_size))
            

            # # corner
            # for shift in corner_neighbor_offsets:
            #     offset = pos[0] + shift[0], pos[1] + shift[1]

            #     if offset in tiles:
            #         if tiles[offset].type == tile_type:
            #             neighbor_offsets.add(shift)
            
            # for variants in variants_spawnrates:
            #     if tile_variant in variants:
            #         tiles[pos].change(tile_type, CORNER_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))], random.choices(variants, variants_spawnrates[variants])[0])
        
        except KeyError as e:
            print(e)

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
    
    def draw(self, draw_surf):
        draw_surf.blit(self.image, self.rect)
    
    def change(self, tile_type, tile_variant, img):
        self.type = tile_type
        self.variant = tile_variant
        self.image = img
