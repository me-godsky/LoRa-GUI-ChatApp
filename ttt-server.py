import pygame
from grid import Grid

class ttt_server():
    def __init__(self, lora):

        self.lora = lora
        import os
        os.environ['SDL_VIDEO_WINDOW_POS'] = '650,225'

        surface = pygame.display.set_mode((600,600))
        pygame.display.set_caption('Tic-tac-toe')

        import threading
        def create_thread(target):
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()

        

        def receive_data():
            global turn
            while True:
                try:
                    self.lora.set_mode(MODE.RXCONT)
                    data = self.lora.on_rx_done()
                    data = data.split('-')
                    x, y = int(data[0]), int(data[1])
                    if data[2] == 'yourtur':
                        turn = True
                    if data[3] == 'False':
                        grid.game_over = True
                    if grid.get_cell_value(x, y) == 0:
                        grid.set_cell_value(x, y, 'O')
                    

                except KeyboardInterrupt:
                    sys.stdout.flush()
                    print("Exit")
                    sys.stderr.write("KeyboardInterrupt\n")
                finally:
                    sys.stdout.flush()
                    print("Exit")
                    lora.set_mode(MODE.SLEEP)
                BOARD.teardown()
                 
                
        create_thread(receive_data)

        grid = Grid()
        running = True
        player = "X"
        turn = True
        playing = 'True'

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if turn and not grid.game_over:
                            pos = pygame.mouse.get_pos()
                            cellX, cellY = pos[0] // 200, pos[1] // 200
                            grid.get_mouse(cellX, cellY, player)
                            if grid.game_over:
                                playing = 'False'
                            send_data = '{}-{}-{}-{}'.format(cellX, cellY, 'yourtur', playing).encode()
                            self.lora.set_mode(MODE.TX)
                            start_time = time.time()
                            while (time.time() - start_time < 3): 
                                self.lora.start(msg[i])
                            turn = False
                            self.lora.set_mode(MODE.RXCON)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and grid.game_over:
                        grid.clear_grid()
                        grid.game_over = False
                        playing = 'True'
                    elif event.key == pygame.K_ESCAPE:
                        running = False


            surface.fill((0,0,0))

            grid.draw(surface)

            pygame.display.flip()