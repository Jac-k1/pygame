import pygame as pg
import time
import random
pg.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("some game")
BG = pg.transform.scale(pg.image.load("bg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH, PLAYER_HEIGHT = 100, 20
PROJECTILE_WIDTH, PROJECTILE_HEIGHT = 10, 20
PLAYER_VEL = 5
PROJECTILE_VEL = 3

FONT = pg.font.SysFont("comicsans", 20)

def draw(player, elapsed, projectiles):
    WIN.blit(BG, (0, 0))

    pg.draw.rect(WIN, "green", player)

    for projectile in projectiles:
        pg.draw.rect(WIN, "red", projectile)

    time_text = FONT.render(f"Time: {round(elapsed)}s", 1, (0, 0, 255))
    WIN.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

    pg.display.update()

def main():
    run = True
    clock = pg.time.Clock()
    start = time.time()
    elapsed = 0
    player = pg.Rect(450, 560, PLAYER_HEIGHT, PLAYER_WIDTH)


    projectile_increment = 2000

    projectile_count = 0

    projectiles = []

    hit = False

    while run:
        projectile_count += clock.tick(60)
        elapsed = time.time() - start
        
        if projectile_count > projectile_increment:
            for _ in range(0, 10):
                projectile_x = random.randint(0, WIDTH - PROJECTILE_WIDTH)
                projectile = pg.Rect(projectile_x, -PROJECTILE_HEIGHT, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
                projectiles.append(projectile)
            
            projectile_increment = max(1000, projectile_increment - 100)
            projectile_count = 0
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break

        keys = pg.key.get_pressed()
        if keys[pg.K_a] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pg.K_d] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL


        for projectile in projectiles[:]:
            projectile.y += PROJECTILE_VEL
            if projectile.y > HEIGHT:
                projectiles.remove(projectile)
            elif projectile.y + projectile.height >= player.y and projectile.colliderect(player):
                projectiles.remove(projectile)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You lost!", 1, (255, 0, 0))
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pg.display.update()
            pg.time.delay(2000)
            break

        draw(player, elapsed, projectiles)


    pg.quit()


if __name__ == "__main__":
    main()