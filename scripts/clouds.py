import pygame
import random

# Lớp đại diện cho một đám mây trong trò chơi
class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)  # Vị trí của đám mây
        self.img = img  # Hình ảnh đám mây
        self.speed = speed  # Tốc độ di chuyển của đám mây
        self.depth = depth  # Độ sâu của đám mây, ảnh hưởng đến tốc độ di chuyển và hiển thị

    def update(self):
        # Cập nhật vị trí của đám mây dựa trên tốc độ
        self.pos[0] += self.speed

    def render(self, surf, offset=(0, 0)):
        render_pos = (
            self.pos[0] - offset[0] * self.depth,  # Tính toán vị trí hiển thị dựa trên offset và độ sâu
            self.pos[1] - offset[1] * self.depth
        )
        render_x = render_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width()
        render_y = render_pos[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height()
        # Hiển thị đám mây lên bề mặt (surf) với vị trí hiển thị tính toán
        surf.blit(self.img, (render_x, render_y))

# Lớp quản lý tất cả các đám mây trong trò chơi
class Clouds:
    def __init__(self, cloud_images, count=16):
        self.clouds = []
        for i in range(count):
            # Tạo và thêm các đám mây ngẫu nhiên vào danh sách
            self.clouds.append(Cloud(
                (random.random() * 9999, random.random() * 999),  # Vị trí ngẫu nhiên
                random.choice(cloud_images),  # Chọn một hình ảnh đám mây ngẫu nhiên
                random.random() * 0.05 + 0.05,  # Tốc độ di chuyển ngẫu nhiên
                random.random() * 0.6 + 0.2  # Độ sâu ngẫu nhiên
            ))
        # Sắp xếp các đám mây theo độ sâu để đảm bảo sự hiển thị đúng thứ tự
        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        # Cập nhật tất cả các đám mây trong danh sách
        for cloud in self.clouds:
            cloud.update()

    def render(self, surf, offset=(0, 0)):
        # Hiển thị tất cả các đám mây lên bề mặt (surf) với sự sử dụng của offset
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)
