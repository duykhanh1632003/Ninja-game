import math  # Import thư viện math để sử dụng các hàm toán học
import pygame  # Import thư viện pygame để vẽ và cập nhật đối tượng trò chơi

class Spark:
    def __init__(self, pos, angle, speed):
        """
        Khởi tạo một đối tượng Spark (tia lửa).

        :param pos: Vị trí ban đầu của tia lửa.
        :param angle: Góc di chuyển ban đầu của tia lửa (tính bằng radian).
        :param speed: Tốc độ ban đầu của tia lửa.
        """
        self.pos = list(pos)  # Lưu trữ vị trí ban đầu của tia lửa dưới dạng danh sách
        self.angle = angle  # Lưu trữ góc di chuyển ban đầu của tia lửa
        self.speed = speed  # Lưu trữ tốc độ ban đầu của tia lửa
        
    def update(self):
        """
        Cập nhật tia lửa.

        :return: True nếu tia lửa đã tắt, ngược lại là False.
        """
        self.pos[0] += math.cos(self.angle) * self.speed  # Cập nhật vị trí theo phương x dựa trên cosinus của góc di chuyển và tốc độ
        self.pos[1] += math.sin(self.angle) * self.speed  # Cập nhật vị trí theo phương y dựa trên sin của góc di chuyển và tốc độ
        self.speed = max(0, self.speed - 0.1)  # Giảm tốc độ tia lửa theo thời gian và đảm bảo nó không âm
        return not self.speed  # Trả về True nếu tốc độ đã giảm xuống dưới 0, ngụ ý rằng tia lửa đã tắt
    
    def render(self, surf, offset=(0, 0)):
        """
        Vẽ tia lửa lên bề mặt.

        :param surf: Bề mặt để vẽ tia lửa lên.
        :param offset: Sự dịch chuyển để áp dụng cho vị trí của tia lửa trên bề mặt.
        """
        render_points = [
            (self.pos[0] + math.cos(self.angle) * self.speed * 3 - offset[0], self.pos[1] + math.sin(self.angle) * self.speed * 3 - offset[1]),
            (self.pos[0] + math.cos(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[0], self.pos[1] + math.sin(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[1]),
            (self.pos[0] + math.cos(self.angle + math.pi) * self.speed * 3 - offset[0], self.pos[1] + math.sin(self.angle + math.pi) * self.speed * 3 - offset[1]),
            (self.pos[0] + math.cos(self.angle - math.pi * 0.5) * self.speed * 0.5 - offset[0], self.pos[1] + math.sin(self.angle - math.pi * 0.5) * self.speed * 0.5 - offset[1]),
        ]  # Tạo danh sách các điểm để vẽ tia lửa dưới dạng đa giác
        
        pygame.draw.polygon(surf, (255, 255, 255), render_points)  # Vẽ tia lửa lên bề mặt dưới dạng đa giác màu trắng
