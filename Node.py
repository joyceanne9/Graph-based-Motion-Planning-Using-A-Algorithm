import pygame
pygame.font.init()
SquareFont = pygame.font.SysFont('arial ', 10)
class Node:
    def __init__(self, surface, x, y, squareSize):
        self.surface = surface
        self.x = x
        self.y = y
        self.squareSize = squareSize
        self.g = 0
        self.f = 0
        self.h = 0
        self.state = -1
        self.previous = None
        # 0 is open
        # 1 is Start
        # 2 is End
        # 3 is Blocked
        # 4 is Closed

    def draw(self):
        if self.state == -1:
            pygame.draw.rect(self.surface, (0, 0, 0),
                             [self.x * self.squareSize + 1, self.y * self.squareSize + 1, self.squareSize - 2,
                              self.squareSize - 2], 2)
        if self.state == 0:
            pygame.draw.rect(self.surface, (0, 255, 0),
                             [self.x * self.squareSize + 1, self.y * self.squareSize + 1, self.squareSize - 2,
                              self.squareSize - 2])
        if self.state == 1:
            pygame.draw.rect(self.surface, (0, 0, 255),
                             [self.x * self.squareSize + 1, self.y * self.squareSize + 1, self.squareSize - 2,
                              self.squareSize - 2])
        if self.state == 3:
            pygame.draw.rect(self.surface, (0, 0, 0),
                             [self.x * self.squareSize + 1, self.y * self.squareSize + 1, self.squareSize - 2,
                              self.squareSize - 2])
        if self.state == 4:
            pygame.draw.rect(self.surface, (255, 0, 0),
                             [self.x * self.squareSize + 1, self.y * self.squareSize + 1, self.squareSize - 2,
                              self.squareSize - 2])
        if self.state == 5:
            pygame.draw.rect(self.surface, (255, 255, 0),
                             [self.x * self.squareSize + 1, self.y * self.squareSize + 1, self.squareSize - 2,
                              self.squareSize - 2])
        # hSurf = SquareFont.render(str(round(self.h,1)), True, (0,0,0))
        # gSurf = SquareFont.render(str(round(self.g,1)), True, (0,0,0))
        # fSurf = SquareFont.render(str(round(self.f,1)), True, (0,0,0))
        # if self.h != -1:
        #     self.surface.blit(hSurf,(self.x *self.squareSize ,self.y*self.squareSize))
        # if self.g != -1:
        #     self.surface.blit(gSurf,(self.x *self.squareSize ,self.y*self.squareSize + 20))
        # if self.f != -1:
        #     self.surface.blit(fSurf,(self.x *self.squareSize ,self.y*self.squareSize + 40))


