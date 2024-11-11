import pygame, sys, random, json

from tile import *


pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
COLOR = '#241b16'

clock = pygame.time.Clock()

running = True

# tile
load_data()
current_tile_type = 0 
current_tile_variant = 0
tiles = {}  

holding_shift = False
camera_offset = [0, 0]

while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera_offset[1] -= 16
    elif keys[pygame.K_s]:
        camera_offset[1] += 16
    
    if keys[pygame.K_a]:
        camera_offset[0] -= 16
    elif keys[pygame.K_d]:
        camera_offset[0] += 16

    # position
    mpos = pygame.mouse.get_pos()
    tile_pos = (mpos[0] + camera_offset[0]) // tile_size, (camera_offset[1] + mpos[1]) // tile_size

    mbutton = pygame.mouse.get_pressed()

    # drawing
    screen.fill(COLOR)

    clipped_img = get_surface(tile_sprites[tile_types[current_tile_type]], TILES_IDS[tile_types[current_tile_type]].get(current_tile_variant), tile_size)

    [tile.draw(screen, camera_offset) for tile in tiles.values()]
    # screen.blit(tile_sprites['sandstone'], (0, 0))
    screen.blit(clipped_img, (tile_pos[0] * tile_size - camera_offset[0], tile_pos[1] * tile_size - camera_offset[1]))

    if mbutton[0]: # add/create tile
        # try:
        #     tiles[tile_pos]
        # except KeyError:
        for variants in variants_spawnrates:
            if current_tile_variant in variants:
                picked_variant = random.choices(variants, variants_spawnrates[variants])[0]
                tiles[tile_pos] = Tile(tile_types[current_tile_type], picked_variant, tile_pos, get_surface(tile_sprites[tile_types[current_tile_type]], TILES_IDS[tile_types[current_tile_type]].get(picked_variant), tile_size))
                break

        else:
            tiles[tile_pos] = Tile(tile_types[current_tile_type], current_tile_variant, tile_pos, get_surface(tile_sprites[tile_types[current_tile_type]], TILES_IDS[tile_types[current_tile_type]].get(current_tile_variant), tile_size))
        if holding_shift:
            tiles = auto_tile(tiles, [
                # offsets

                tile_pos, # middle

                (tile_pos[0] + 1, tile_pos[1]), # right
                (tile_pos[0] - 1, tile_pos[1]), # left
                (tile_pos[0], tile_pos[1] - 1), # top
                (tile_pos[0], tile_pos[1] + 1), # bottom

                (tile_pos[0] + 1, tile_pos[1] - 1), # topright
                (tile_pos[0] + 1, tile_pos[1] + 1), # bottomright
                (tile_pos[0] - 1, tile_pos[1] - 1), # topleft
                (tile_pos[0] - 1, tile_pos[1] + 1) # bottomleft
            ])

    elif mbutton[2]: # deleting tile
        try:
            del tiles[tile_pos]
        
            if holding_shift:
                tiles = auto_tile(tiles, [
                # offsets

                tile_pos, # middle

                (tile_pos[0] + 1, tile_pos[1]), # right
                (tile_pos[0] - 1, tile_pos[1]), # left
                (tile_pos[0], tile_pos[1] - 1), # top
                (tile_pos[0], tile_pos[1] + 1), # bottom

                (tile_pos[0] + 1, tile_pos[1] - 1), # topright
                (tile_pos[0] + 1, tile_pos[1] + 1), # bottomright
                (tile_pos[0] - 1, tile_pos[1] - 1), # topleft
                (tile_pos[0] - 1, tile_pos[1] + 1) # bottomleft
            ])

        except KeyError:
            pass

    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                holding_shift = True
            if event.key == pygame.K_k:
                print(tiles)
                f = open('map.json', 'w')
                json.dump(tiles, f)
                f.close()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                holding_shift = False
        
        if event.type == pygame.MOUSEWHEEL:
            if event.y == -1:
                if not holding_shift:
                    current_tile_variant = (current_tile_variant - 1) % (max(TILES_IDS[tile_types[current_tile_type]].keys()) + 1)
                else:
                    current_tile_type = (current_tile_type - 1) % len(tile_types)
            elif event.y == 1:
                if not holding_shift:
                    current_tile_variant = (current_tile_variant + 1) % (max(TILES_IDS[tile_types[current_tile_type]].keys()) + 1)
                else:
                    current_tile_type = (current_tile_type + 1) % len(tile_types)
            print(current_tile_variant)
        if event.type == pygame.MOUSEMOTION:
            print(tile_pos)

pygame.quit()
sys.exit()
