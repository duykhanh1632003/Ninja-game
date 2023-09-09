import sys
import math
import random
import pygame
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark

# Định nghĩa lớp Game để quản lý trò chơi
class Game:
    def __init__(self):
        pygame.init()  # Khởi tạo thư viện pygame

        pygame.display.set_caption('ninja game')  # Đặt tiêu đề cửa sổ trò chơi
        self.screen = pygame.display.set_mode((640, 480))  # Tạo cửa sổ kích thước 640x480 pixel
        self.display = pygame.Surface((320, 240))  # Tạo bề mặt con kích thước 320x240 pixel để vẽ nội dung trò chơi
        self.clock = pygame.time.Clock()  # Khởi tạo đồng hồ để đồng bộ thời gian trò chơi

        self.movement = [False, False]  # Trạng thái di chuyển của người chơi (trái/phải)

        # Tạo từ điển assets chứa tất cả các tài nguyên hình ảnh và animation cho trò chơi
        self.assets = {
            'decor': load_images('tiles/decor'),  # Nạp hình ảnh từ thư mục 'tiles/decor' cho loại tile 'decor'
            'grass': load_images('tiles/grass'),  # Nạp hình ảnh từ thư mục 'tiles/grass' cho loại tile 'grass'
            'large_decor': load_images('tiles/large_decor'),  # Nạp hình ảnh từ thư mục 'tiles/large_decor' cho loại tile 'large_decor'
            'stone': load_images('tiles/stone'),  # Nạp hình ảnh từ thư mục 'tiles/stone' cho loại tile 'stone'
            'player': load_image('entities/player.png'),  # Nạp hình ảnh người chơi từ 'entities/player.png'
            'background': load_image('background.png'),  # Nạp hình ảnh nền từ 'background.png'
            'clouds': load_images('clouds'),  # Nạp hình ảnh đám mây từ thư mục 'clouds'
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),  # Tạo animation cho trạng thái đứng yên của đối thủ
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),  # Tạo animation cho trạng thái chạy của đối thủ
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),  # Tạo animation cho trạng thái đứng yên của người chơi
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),  # Tạo animation cho trạng thái chạy của người chơi
            'player/jump': Animation(load_images('entities/player/jump')),  # Tạo animation cho trạng thái nhảy của người chơi
            'player/slide': Animation(load_images('entities/player/slide')),  # Tạo animation cho trạng thái trượt của người chơi
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),  # Tạo animation cho trạng thái trượt trên tường của người chơi
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),  # Tạo animation cho hạt lá
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),  # Tạo animation cho hạt bụi
            'gun': load_image('gun.png'),  # Nạp hình ảnh súng
            'projectile': load_image('projectile.png'),  # Nạp hình ảnh đạn
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)  # Đám mây nền

        self.player = Player(self, (50, 50), (8, 15))  # Khởi tạo người chơi

        self.tilemap = Tilemap(self, tile_size=16)  # Khởi tạo bản đồ ô vuông

        self.load_level(0)  # Nạp cấp độ 0

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')  # Nạp bản đồ từ tệp JSON

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))

        self.projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [0, 0]
        self.dead = 0

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))  # Vẽ nền trò chơi

            if self.dead:
                self.dead += 1
                if self.dead > 40:
                    self.load_level(0)  # Nếu người chơi chết, tải lại cấp độ 0

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))  # Tính toán scroll để theo dõi người chơi

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)  # Cập nhật và vẽ đám mây

            self.tilemap.render(self.display, offset=render_scroll)  # Vẽ bản đồ ô vuông

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Xử lý sự kiện đóng cửa sổ
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True  # Xử lý sự kiện phím bấm trái
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True  # Xử lý sự kiện phím bấm phải
                    if event.key == pygame.K_UP:
                        self.player.jump()  # Xử lý sự kiện phím bấm lên
                    if event.key == pygame.K_x:
                        self.player.dash()  # Xử lý sự kiện phím bấm 'x'
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False  # Xử lý sự kiện phím thả trái
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False  # Xử lý sự kiện phím thả phải

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))  # Hiển thị trò chơi lên màn hình
            pygame.display.update()  # Cập nhật màn hình
            self.clock.tick(60)  # Giới hạn frame rate của trò chơi

# Chạy trò chơi
if __name__ == "__main__":
    Game().run()  # Tạo đối tượng trò chơi và chạy trò chơi
