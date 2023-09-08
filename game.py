# Import các thư viện cần thiết
import sys
import pygame
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

# Định nghĩa lớp Game để quản lý trò chơi
class Game:
    def __init__(self):
        pygame.init()

        # Cài đặt cửa sổ trò chơi
        pygame.display.set_caption('ninja game')
        self.screen = pygame.display.set_mode((640, 480))  # Tạo cửa sổ kích thước 640x480 pixel
        self.display = pygame.Surface((320, 240))  # Tạo bề mặt con kích thước 320x240 pixel để vẽ nội dung trò chơi

        # Khởi tạo đồng hồ để đồng bộ thời gian
        self.clock = pygame.time.Clock()

        # Trạng thái di chuyển của người chơi (trái/phải)
        self.movement = [False, False]  # [LEFT, RIGHT]

        # Tài nguyên hình ảnh và âm thanh
        self.assets = {
            'decor': load_images('tiles/decor'),  # Nạp hình ảnh từ thư mục 'tiles/decor' cho loại tile 'decor'
            'grass': load_images('tiles/grass'),  # Nạp hình ảnh từ thư mục 'tiles/grass' cho loại tile 'grass'
            'large_decor': load_images('tiles/large_decor'),  # Nạp hình ảnh từ thư mục 'tiles/large_decor' cho loại tile 'large_decor'
            'stone': load_images('tiles/stone'),  # Nạp hình ảnh từ thư mục 'tiles/stone' cho loại tile 'stone'
            'player': load_image('entities/player.png'),  # Nạp hình ảnh người chơi từ 'entities/player.png'
            'background': load_image('background.png'),  # Nạp hình ảnh nền từ 'background.png'
            'clouds': load_images('clouds'),  # Nạp hình ảnh đám mây từ thư mục 'clouds'
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),  # Tạo animation cho trạng thái đứng yên của người chơi
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),  # Tạo animation cho trạng thái chạy của người chơi
            'player/jump': Animation(load_images('entities/player/jump')),  # Tạo animation cho trạng thái nhảy của người chơi
            'player/slide': Animation(load_images('entities/player/slide')),  # Tạo animation cho trạng thái trượt của người chơi
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),  # Tạo animation cho trạng thái trượt trên tường của người chơi
        }

        # Đám mây nền
        self.clouds = Clouds(self.assets['clouds'], count=16)

        # Khởi tạo người chơi
        self.player = Player(self, (50, 50), (8, 15))  # Tạo người chơi tại vị trí (50, 50) với kích thước (8, 15)
       
        # Khởi tạo bản đồ ô vuông
        self.tilemap = Tilemap(self, tile_size=16)  # Khởi tạo bản đồ ô vuông với kích thước ô vuông là 16 pixel
        self.tilemap.load('map.json')
        # Biến scroll để điều chỉnh sự di chuyển của camera
        self.scroll = [0, 0]  # Điều chỉnh sự di chuyển của camera

    # Phương thức chạy trò chơi
    def run(self):
        while True:
            # Vẽ nền trò chơi
            self.display.blit(self.assets['background'], (0, 0))  # Vẽ hình ảnh nền lên bề mặt con

            # Tính toán scroll để theo dõi người chơi
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))  # Làm tròn scroll

            # Cập nhật và vẽ đám mây
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)  # Vẽ đám mây trên bề mặt con

            # Vẽ bản đồ ô vuông
            self.tilemap.render(self.display, offset=render_scroll)  # Vẽ bản đồ ô vuông trên bề mặt con

            # Cập nhật và vẽ người chơi
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))  # Cập nhật trạng thái của người chơi
            self.player.render(self.display, offset=render_scroll)  # Vẽ người chơi trên bề mặt con

            # Xử lý sự kiện đóng cửa sổ
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Nếu người chơi đóng cửa sổ
                    pygame.quit()  # Tắt pygame
                    sys.exit()  # Thoát khỏi chương trình
                if event.type == pygame.KEYDOWN:  # Nếu có sự kiện phím được nhấn
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True  # Khi người chơi nhấn mũi tên trái, đặt movement[0] thành True (di chuyển sang trái)
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True  # Khi người chơi nhấn mũi tên phải, đặt movement[1] thành True (di chuyển sang phải)
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3  # Khi người chơi nhấn mũi tên lên, đặt vận tốc y của người chơi thành -3 để nhảy lên
                if event.type == pygame.KEYUP:  # Nếu có sự kiện phím được thả ra
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False  # Khi người chơi thả mũi tên trái ra, đặt movement[0] thành False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False  # Khi người chơi thả mũi tên phải ra, đặt movement[1] thành False

            # Hiển thị trò chơi lên màn hình
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))  # Vẽ bề mặt con lên màn hình
            pygame.display.update()  # Cập nhật màn hình
            self.clock.tick(60)  # Giới hạn frame rate của trò chơi

# Chạy trò chơi
if __name__ == "__main__":
    Game().run()  # Tạo đối tượng trò chơi và chạy trò chơi
