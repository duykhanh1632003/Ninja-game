import math  # Import thư viện math để sử dụng các hàm toán học
import random  # Import thư viện random để tạo số ngẫu nhiên
import pygame  # Import thư viện pygame để vẽ và cập nhật đối tượng trò chơi
from scripts.particle import Particle  # Import lớp Particle từ module scripts.particle
from scripts.spark import Spark  # Import lớp Spark từ module scripts.spark

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        """
        Khởi tạo một đối tượng PhysicsEntity (đối tượng vật lý).

        :param game: Đối tượng Game chứa thông tin trò chơi.
        :param e_type: Loại đối tượng (ví dụ: 'player', 'enemy').
        :param pos: Vị trí ban đầu của đối tượng.
        :param size: Kích thước của đối tượng.
        """
        self.game = game  # Lưu trữ đối tượng Game
        self.type = e_type  # Lưu trữ loại đối tượng
        self.pos = list(pos)  # Lưu trữ vị trí ban đầu của đối tượng dưới dạng danh sách
        self.size = size  # Lưu trữ kích thước của đối tượng
        self.velocity = [0, 0]  # Lưu trữ vận tốc của đối tượng
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}  # Xác định các va chạm
        
        self.action = ''  # Hành động hiện tại của đối tượng
        self.anim_offset = (-3, -3)  # Điều chỉnh offset cho hoạt ảnh của đối tượng
        self.flip = False  # Xác định hướng của đối tượng (True: phải, False: trái)
        self.set_action('idle')  # Đặt hành động mặc định cho đối tượng
        
        self.last_movement = [0, 0]  # Lưu trữ hành động di chuyển trước đó của đối tượng
    
    def rect(self):
        """
        Trả về hình chữ nhật pygame đại diện cho đối tượng.

        :return: Hình chữ nhật pygame.
        """
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        """
        Đặt hành động cho đối tượng và cập nhật hoạt ảnh tương ứng.

        :param action: Hành động cần đặt.
        """
        if action != self.action:
            self.action = action  # Cập nhật hành động
            self.animation = self.game.assets[self.type + '/' + self.action].copy()  # Lấy hoạt ảnh từ tài nguyên trò chơi
        
    def update(self, tilemap, movement=(0, 0)):
        """
        Cập nhật trạng thái của đối tượng vật lý.

        :param tilemap: Đối tượng Tilemap chứa thông tin về map.
        :param movement: Hành động di chuyển (đổi vị trí) của đối tượng.
        """
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}  # Đặt lại trạng thái va chạm
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])  # Tính toán vận tốc của khung hình
        
        self.pos[0] += frame_movement[0]  # Cập nhật vị trí theo phương x
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1]  # Cập nhật vị trí theo phương y
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
                
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
            
        self.last_movement = movement
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
            
        self.animation.update()
        
    def render(self, surf, offset=(0, 0)):
        """
        Vẽ đối tượng lên bề mặt.

        :param surf: Bề mặt để vẽ đối tượng lên.
        :param offset: Sự dịch chuyển để áp dụng cho vị trí của đối tượng trên bề mặt.
        """
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        """
        Khởi tạo một đối tượng Enemy (đối tượng kẻ địch).

        :param game: Đối tượng Game chứa thông tin trò chơi.
        :param pos: Vị trí ban đầu của đối tượng.
        :param size: Kích thước của đối tượng.
        """
        super().__init__(game, 'enemy', pos, size)  # Gọi hàm khởi tạo của lớp cha (PhysicsEntity)
        
        self.walking = 0  # Số bước đi của đối tượng

    def update(self, tilemap, movement=(0, 0)):
        """
        Cập nhật trạng thái của đối tượng kẻ địch.

        :param tilemap: Đối tượng Tilemap chứa thông tin về map.
        :param movement: Hành động di chuyển (đổi vị trí) của đối tượng.
        """
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
                if (self.collisions['right'] or self.collisions['left']):
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking:
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if (abs(dis[1]) < 16):
                    if (self.flip and dis[0] < 0):
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                    if (not self.flip and dis[0] > 0):
                        self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)
        
        super().update(tilemap, movement=movement)
        
        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
            
        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                self.game.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                return True
            
    def render(self, surf, offset=(0, 0)):
        """
        Vẽ đối tượng kẻ địch lên bề mặt.

        :param surf: Bề mặt để vẽ đối tượng lên.
        :param offset: Sự dịch chuyển để áp dụng cho vị trí của đối tượng trên bề mặt.
        """
        super().render(surf, offset=offset)
        
        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surf.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        """
        Khởi tạo một đối tượng Player (đối tượng người chơi).

        :param game: Đối tượng Game chứa thông tin trò chơi.
        :param pos: Vị trí ban đầu của đối tượng.
        :param size: Kích thước của đối tượng.
        """
        super().__init__(game, 'player', pos, size)  # Gọi hàm khởi tạo của lớp cha (PhysicsEntity)
        self.air_time = 0  # Thời gian không tiếp xúc với mặt đất
        self.jumps = 1  # Số lần nhảy còn lại
        self.wall_slide = False  # Xác định trạng thái trượt tường
        self.dashing = 0  # Trạng thái dash (di chuyển nhanh)

    def update(self, tilemap, movement=(0, 0)):
        """
        Cập nhật trạng thái của đối tượng người chơi.

        :param tilemap: Đối tượng Tilemap chứa thông tin về map.
        :param movement: Hành động di chuyển (đổi vị trí) của đối tượng.
        """
        super().update(tilemap, movement=movement)
        
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1
            
        self.wall_slide = False
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')
        
        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')
        
        if abs(self.dashing) in {60, 50}:
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
                
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
    
    def render(self, surf, offset=(0, 0)):
        """
        Vẽ đối tượng người chơi lên bề mặt.

        :param surf: Bề mặt để vẽ đối tượng lên.
        :param offset: Sự dịch chuyển để áp dụng cho vị trí của đối tượng trên bề mặt.
        """
        if abs(self.dashing) <= 50:
            super().render(surf, offset=offset)
            
    def jump(self):
        """
        Thực hiện hành động nhảy của đối tượng người chơi.

        :return: True nếu nhảy thành công, False nếu không thể nhảy.
        """
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
                
        elif self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
            return True
    
    def dash(self):
        """
        Thực hiện hành động dash của đối tượng người chơi.
        """
        if not self.dashing:
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60
