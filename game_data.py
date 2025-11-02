#Clase para guardar los datos de la partida
class GameData:
    def __init__(self, width, height, ball_reset_speed):
        self.ball_reset_speed = ball_reset_speed
        self.reset(width, height)
        self.p1_name = "Vero"
        self.p2_name = "Juan"

    def reset(self, width, height):
        
        self.p1_score = 0
        self.p2_score = 0

        self.ball_real = [width * 0.5, height * 0.5]
        self.ball_vel = [0, 0]
        self.ball_speed = self.ball_reset_speed
        