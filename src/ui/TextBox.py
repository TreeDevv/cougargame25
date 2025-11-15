import pygame;

from src.util.math import relative_to_pixel, anchor_center

instances = []

class TextBox:
    def __init__(
            self, 
            font: pygame.font.Font, 
            color: tuple, 
            box_color: tuple, 
            position: (int, float, int ,float), 
            size: (int, float, int ,float), 
            anchor_point: (float, float) = (0, 0)):
        self.font = font;
        self.color = color;
        self.box_color = box_color;
        self.position = position;
        self.size = size;
        self.anchor_point = anchor_point;
        self.text = "";
        self.surface = None;
        self.click_callback = None;
        self.update_surface();
        instances.append(self);
    def get_pos(self):
        rel_pos = (self.position[1], self.position[3]);
        abs_pos = (self.position[0], self.position[2]);
        rel_pix = relative_to_pixel(rel_pos, pygame.display.get_surface().get_size());
        anchor_offset = (self.get_size()[0] * self.anchor_point[0], self.get_size()[1] * self.anchor_point[1]);
        return ((abs_pos[0] + rel_pix[0]) - anchor_offset[0], (abs_pos[1] + rel_pix[1]) - anchor_offset[1]);
    def get_size(self):
        rel_size = (self.size[1], self.size[3]);
        abs_size = (self.size[0], self.size[2]);
        rel_pix = relative_to_pixel(rel_size, pygame.display.get_surface().get_size());
        return (abs_size[0] + rel_pix[0], abs_size[1] + rel_pix[1]);
    def on_click(self, callback):
        self.click_callback = callback;
    def update_surface(self):
        box_size = self.get_size();
        self.surface = pygame.Surface(box_size);
        self.surface.fill(self.box_color);
        text_surf = self.font.render(self.text, True, self.color);
        text_rect = text_surf.get_rect(center=(box_size[0] // 2, box_size[1] // 2));
        self.surface.blit(text_surf, anchor_center(relative_to_pixel((0.5, 0.5), self.surface.get_size()), text_surf.get_size()));
    def get_surface(self):
        return self.surface;
    def set_text(self, new_text: str):
        self.text = new_text;
        self.update_surface();
    def __del__(self):
        instances.remove(self);