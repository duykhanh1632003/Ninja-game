import pygame
import os

BASE_IMG_PATH = 'data/images/'

# Hàm load_image(path) dùng để tải hình ảnh từ đường dẫn và thiết lập màu trong suốt
def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()  # Sử dụng pygame.image.load thay vì pygame.load_image
    img.set_colorkey((0, 0, 0))  # Đặt màu đen là màu trong suốt trong hình ảnh
    return img

# Hàm load_images(path) tải một loạt các hình ảnh từ thư mục và trả về danh sách
def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

# Lớp Animation đại diện cho chức năng tạo và quản lý animation
class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images  # Danh sách các hình ảnh sử dụng trong animation
        self.loop = loop  # Biến xác định animation có lặp lại không
        self.img_duration = img_dur  # Độ dài mỗi khung hình
        self.done = False  # Biến xác định animation đã kết thúc hay chưa
        self.frame = 0  # Khung hình hiện tại

    # Phương thức copy() để sao chép animation
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    # Phương thức update() cập nhật animation
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    # Phương thức img() trả về hình ảnh hiện tại trong animation
    def img(self):
        return self.images[int(self.frame / self.img_duration)]
