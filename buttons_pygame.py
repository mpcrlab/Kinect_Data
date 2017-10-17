import pygame
import inputbox

class Option:

    hovered = False
    
    def __init__(self, text, pos, font, _screen):
        self.text = text
        self.pos = pos
        self.set_rect(font)
        self.draw(_screen, font)
            
    def draw(self, _screen, font):
        self.set_rend(font)
        _screen.blit(self.rend, self.rect)
        
    def set_rend(self, font):
        self.rend = font.render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.hovered:
            return (255, 255, 255)
        else:
            return (100, 100, 100)
        
    def set_rect(self, font):
        self.set_rend(font)
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((480, 320))
    menu_font = pygame.font.Font(None, 40)
    options = [Option("NEW GAME", (140, 105)), Option("LOAD GAME", (135, 155)),
            Option("OPTIONS", (145, 205))]

    print(inputbox.ask(screen, "Enter your name"))

    while True:
        pygame.event.pump()

        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                for option in options:
                    if option.rect.collidepoint(pygame.mouse.get_pos()):
                        option.hovered = not option.hovered

        screen.fill((0, 0, 0))
        for option in options:
            option.draw()
        pygame.display.update()