
PLATFORM_SPRITE_TEMPLATE = {
    "color_key": (1, 255, 1),
    "image_path": None,
    "coordinate_data": {
        "p00": ((0, 0), (32, 32)),
        "p01": ((32, 0), (32, 32)),
        "p02": ((64, 0), (32, 32)),
        "p10": ((0, 32), (32, 32)),
        "p11": ((32, 32), (32, 32)),
        "p12": ((64, 32), (32, 32)),
        "p20": ((0, 64), (32, 32)),
        "p21": ((32, 64), (32, 32)),
        "p22": ((64, 64), (32, 32)),
    }
}

plat_num = 4

PLATFORM_SPRITES = []
for n in range(plat_num):
    PLATFORM_SPRITES.append(PLATFORM_SPRITE_TEMPLATE.copy())
    PLATFORM_SPRITES[-1]["image_path"] = "img/platform"+str(n)+".png"
    
def get_sprite(n):
    return PLATFORM_SPRITES[n]
