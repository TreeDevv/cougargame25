import pygame;

from src.util.math import relative_to_pixel;

class TextLabel:
    def __init__(self, text: str, font: pygame.font.Font, color: tuple, position: (int, float, int ,float), anchor_point: (float, float) = (0, 0)):
        self.text = text;
        self.font = font;
        self.color = color;
        self.position = position;
        self.anchor_point = anchor_point;
        self.surface = self.font.render(self.text, True, self.color);
    def get_pos(self):
        rel_pos = (self.position[1], self.position[3]);
        abs_pos = (self.position[0], self.position[2]);
        rel_pix = relative_to_pixel(rel_pos, pygame.display.get_surface().get_size());
        anchor_offset = (self.surface.get_width() * self.anchor_point[0], self.surface.get_height() * self.anchor_point[1]);
        return ((abs_pos[0] + rel_pix[0]) - anchor_offset[0], (abs_pos[1] + rel_pix[1]) - anchor_offset[1]);
    def get_surface(self):
        return self.surface;
    def set_text(self, new_text: str):
        self.text = new_text;
        self.surface = self.font.render(self.text, True, self.color);