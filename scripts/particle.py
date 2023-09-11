class Particle:
    def __init__(self, game, p_type, pos, velocity=[0, 0], frame=0):
        # Khởi tạo một hạt bụi (particle) mới
        self.game = game  # Tham chiếu đến đối tượng trò chơi chính
        self.type = p_type  # Loại của hạt bụi, xác định loại hình ảnh và hoạt ảnh
        self.pos = list(pos)  # Vị trí ban đầu của hạt bụi
        self.velocity = list(velocity)  # Vận tốc ban đầu của hạt bụi
        # Tạo một bản sao của hoạt ảnh của hạt bụi từ tài nguyên của trò chơi
        self.animation = self.game.assets['particle/' + p_type].copy()
        self.animation.frame = frame  # Thiết lập khung hình ban đầu cho hoạt ảnh của hạt bụi
    
    def update(self):
        kill = False
        # Kiểm tra nếu hoạt ảnh của hạt bụi đã hoàn thành
        if self.animation.done:
            kill = True  # Đặt biến "kill" thành "True" để xóa hạt bụi
        
        # Cập nhật vị trí của hạt bụi dựa trên vận tốc của nó
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        
        # Cập nhật hoạt ảnh của hạt bụi
        self.animation.update()
        
        return kill  # Trả về "kill" để cho biết liệu hạt bụi cần xóa hay không
    
    def render(self, surf, offset=(0, 0)):
        # Hiển thị hạt bụi trên màn hình
        img = self.animation.img()
        surf.blit(img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))
