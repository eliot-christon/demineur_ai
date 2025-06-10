from src.core.game_logic import GameLogic
from src.core.board import Board
from src.core.player import Player
from math import floor
import pygame


class PygameBoard:
    
    def __init__(self, name:str, dimension:tuple[int, int], pixels_per_unit:int=40, case_percentage:int=95,
                 bg_color:tuple[int, int, int]=(255, 255, 255),
                 hidden_color:tuple[int, int, int]=(155, 155, 155),
                 empty_color:list[tuple[int, int, int]]=[
                     (80, 255, 80),  # 0
                     (80, 230, 120), # 1
                     (80, 210, 145), # 2
                     (80, 190, 170), # 3
                     (80, 170, 190), # 4
                     
                     (80, 150, 200), # 5
                     (80, 120, 220), # 6
                     (80, 100, 240), # 7
                     (0, 0, 250)],   # 8
                 mine_color:tuple[int, int, int]=(255, 100, 100),
                 progress_color:tuple[int, int, int]=(50, 255, 50),
                 ) -> None:
        self.progress = 0.0
        self.drop_down = 50
        self.case_percentage = case_percentage
        self.dimension = dimension
        self.pixel_dimension = (dimension[0] * pixels_per_unit, dimension[1] * pixels_per_unit + self.drop_down)
        self.pixels_per_unit = pixels_per_unit
        self.screen = pygame.display.set_mode(self.pixel_dimension)
        self.colors = {'bg':bg_color, 'hidden':hidden_color, 'empty':empty_color, 'mine':mine_color, 'progress':progress_color}
        pygame.display.set_caption(name)
        self.display(Board(width=dimension[0], height=dimension[1]))
    
    def pixel2pos(self, pix_pos:tuple[int, int]) -> tuple[int, int]:
        """Return the position from a pixel position"""
        return (floor(pix_pos[0] / self.pixels_per_unit), floor(pix_pos[1] / self.pixels_per_unit))
    
    def pos2pixel(self, pos:tuple[int, int]) -> tuple[int, int]:
        """Return the pixel position of a position"""
        return (pos[0] * self.pixels_per_unit, pos[1] * self.pixels_per_unit)
    
    def draw_rectangle(self, pos:tuple[int, int], color=tuple[int, int, int]) -> None:
        pixel_margin = round((100 - self.case_percentage) * self.pixels_per_unit / 100)
        pixx, pixy = self.pos2pixel(pos)
        pixx, pixy = pixx+pixel_margin//2, pixy+pixel_margin//2
        pygame.draw.rect(
            surface=self.screen, 
            rect=((pixx, pixy), (self.pixels_per_unit - pixel_margin, self.pixels_per_unit - pixel_margin)), 
            color=color
            )
    
    def draw_progress_bar(self, margin_x:float=0.1, pixel_width:int=3) -> None:
        pixel_margin_x = margin_x * self.pixel_dimension[0]
        top_left = (pixel_margin_x, self.pixel_dimension[1] - 2*self.drop_down//3)
        length = (self.pixel_dimension[0] - (2*pixel_margin_x), self.drop_down//3)
        pygame.draw.rect(
            surface=self.screen,
            rect=((top_left[0]-pixel_width, top_left[1]-pixel_width), (length[0]+(2*pixel_width), length[1]+(2*pixel_width))),
            color = (0, 0, 0)
        )
        pygame.draw.rect(
            surface=self.screen,
            rect=(top_left, length),
            color = self.colors['bg']
        )
        pygame.draw.rect(
            surface=self.screen,
            rect=(top_left, (round(length[0]*self.progress), length[1])),
            color = self.colors['progress']
        )
    
    def write_text(self, text:str, pos:tuple[int, int], color:tuple[int, int, int]) -> None:
        pixx, pixy = self.pos2pixel(pos)
        pixx, pixy = pixx + self.pixels_per_unit//2, pixy + self.pixels_per_unit//2
        font = pygame.font.SysFont('didot.ttc', self.pixels_per_unit)
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        rect.center = (pixx, pixy)
        self.screen.blit(surface, rect)
    
    def display(self, board:Board) -> None:        
        self.screen.fill(self.colors['bg'])
        
        self.draw_progress_bar()
        
        for x in range(self.dimension[0]):
            for y in range(self.dimension[1]):
                c_case = board.get_cell(x, y)
                if not c_case.is_revealed():
                    color = self.colors['hidden']
                    if c_case.is_flagged():
                        text = '+'
                    else:
                        text = ''
                elif c_case.is_mine():
                    color = self.colors['mine']
                    text = 'X'
                else:
                    color = self.colors['empty'][c_case.adjacent_mines]
                    text = str(c_case.adjacent_mines)
                self.draw_rectangle(pos=(x, y), color=color)
                self.write_text(text=text, pos=(x, y), color=(0, 0, 0))
                
        pygame.display.flip()
    

class GraphicalUI:
    """Graphical user interface for the Minesweeper game using Pygame."""
    
    def __init__(self, game_logic:GameLogic) -> None:
        """Initialize the graphical UI with the game logic."""
        self.game_logic = game_logic
        self.board = PygameBoard(name='Minesweeper', dimension=(game_logic.board.width, game_logic.board.height), pixels_per_unit=20)
    
    def start_game(self) -> None:
        """Start the game and handle user input."""
        print(f"Welcome to Minesweeper, {self.game_logic.player.name}!")
        self.board.display(self.game_logic.board)
        
        running = True
        while running:
            action = self.game_logic.player.make_move(self.game_logic.board)
            if action is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pixel_pos = event.pos
                        pos = self.board.pixel2pos(pix_pos=pixel_pos)
                        if pos[0] < self.game_logic.board.width and pos[1] < self.game_logic.board.height:
                            action = (pos[0], pos[1], "reveal")
                            if event.button == 3:  # Right click
                                action = (pos[0], pos[1], "flag")
                            self.game_logic.make_move(*action)
            else:
                self.game_logic.make_move(*action)
            
            if self.game_logic.is_game_over():
                running = False
                
            self.board.progress = self.game_logic.board.get_revealed_count() / (self.game_logic.board.width * self.game_logic.board.height)
            self.board.display(self.game_logic.board)
            self.board.draw_progress_bar()
        # delay for a moment to show the final board state
        pygame.time.delay(1000)
            


if __name__ == "__main__":
    
    from src.core.player import HumanPlayer, RandomPlayer
    
    # Example usage:
    pygame.init()
    game_logic = GameLogic(width=10, height=10, mine_count=00, player=HumanPlayer(name="Player1"))
    graphical_ui = GraphicalUI(game_logic)
    graphical_ui.start_game()
    
    pygame.quit()
    
    
    
    # from pygame.locals import QUIT, MOUSEBUTTONDOWN
    # from src.core.game_logic import GameLogic
    # from src.core.player import HumanPlayer
    
    # pygame.init()
    
    # dimension = (13, 12)
    
    # game_logic = GameLogic(width=dimension[0], height=dimension[1], mine_count=20, player=HumanPlayer(name="Player1"))
    
    # test_py_board = PygameBoard(name='test', dimension=dimension, pixels_per_unit=20)
    # test_board = game_logic.board
    
    # for x in range(dimension[0]):
    #     for y in range(dimension[1]):
    #         c_case = test_board.get_cell(x, y)
    #         c_case.reveal()
        
    # test_py_board.display(test_board)
    
    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             running = False
    #         if event.type == MOUSEBUTTONDOWN:
    #             pixel_pos = event.pos
    #             pos = test_py_board.pixel2pos(pix_pos=pixel_pos)
    #             print("pixel: {}\tpos: {}".format(pixel_pos, pos))
    
    # pygame.quit()