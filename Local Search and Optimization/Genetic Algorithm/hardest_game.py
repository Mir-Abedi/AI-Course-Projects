import pygame


class Goal:
    def __init__(self, x, y, r, color=(255, 255, 0)):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y,), self.r + 1, self.r + 1)
        return pygame.draw.circle(screen, self.color, (self.x, self.y,), self.r, self.r)


class Player:
    def __init__(self, x, y, width, height, vel=5, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.color = color

    def move_AI(self, key, l1, l2):
        if key == 'a':
            t1 = False
            for l in l1:
                if self.y + self.height > l.y1 and self.y < l.y2 and self.x >= l.x1 > self.x - self.vel:
                    t1 = True
                    break
            if not t1:
                self.x -= self.vel
        if key == 'd':
            t1 = False
            for l in l1:
                if self.y + self.height > l.y1 and self.y < l.y2 and self.x + self.width <= l.x1 < self.x + self.vel + self.width:
                    t1 = True
                    break
            if not t1:
                self.x += self.vel
        if key == 's':
            t1 = False
            for l in l2:
                if self.x + self.width > l.x1 and self.x < l.x2 and self.y + self.height <= l.y1 < self.y + self.vel + self.height:
                    t1 = True
                    break
            if not t1:
                self.y += self.vel
        if key == 'w':
            t1 = False
            for l in l2:
                if self.x + self.width > l.x1 and self.x < l.x2 and self.y >= l.y1 > self.y - self.vel:
                    t1 = True
                    break
            if not t1:
                self.y -= self.vel

    def move_player(self, keys, l1, l2):
        if keys[pygame.K_a]:
            t1 = False
            for l in l1:
                if self.y + self.height > l.y1 and self.y < l.y2 and self.x >= l.x1 > self.x - self.vel:
                    t1 = True
                    self.x = l.x1
                    break
            if not t1:
                self.x -= self.vel
        if keys[pygame.K_d]:
            t1 = False
            for l in l1:
                if self.y + self.height > l.y1 and self.y < l.y2 and self.x + self.width <= l.x1 < self.x + self.vel + self.width:
                    t1 = True
                    break
            if not t1:
                self.x += self.vel
        if keys[pygame.K_s]:
            t1 = False
            for l in l2:
                if self.x + self.width > l.x1 and self.x < l.x2 and self.y + self.height <= l.y1 < self.y + self.vel + self.height:
                    t1 = True
                    break
            if not t1:
                self.y += self.vel
        if keys[pygame.K_w]:
            t1 = False
            for l in l2:
                if self.x + self.width > l.x1 and self.x < l.x2 and self.y >= l.y1 > self.y - self.vel:
                    t1 = True
                    break
            if not t1:
                self.y -= self.vel

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x - 1, self.y - 1, self.width + 2, self.height + 2))
        return pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class Enemy:
    def __init__(self, x, y, r, vel=8, color=(0, 0, 255), type_of_move=1, r_move=0):
        self.x = x
        self.y = y
        self.r = r
        self.vel = vel
        self.color = color
        self.type_of_move = type_of_move
        self.r_move = r_move

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y,), self.r + 1, self.r + 1)
        return pygame.draw.circle(screen, self.color, (self.x, self.y,), self.r, self.r)

    def move(self, l1, l2):
        if self.type_of_move == 1:
            for l in l1:
                if self.x - self.r >= l.x1 and self.y + self.r >= l.y1 and self.y - self.r <= l.y2 and self.x - self.r - self.vel < l.x1:
                    self.type_of_move = 2
                    return
            self.x -= self.vel
        elif self.type_of_move == 2:
            for l in l1:
                if self.x + self.r <= l.x1 and self.y + self.r >= l.y1 and self.y - self.r <= l.y2 and self.x + self.r + self.vel > l.x1:
                    self.type_of_move = 1
                    return
            self.x += self.vel
        elif self.type_of_move == 3:
            for l in l2:
                if self.y + self.r <= l.y1 and self.x + self.r >= l.x1 and self.x - self.r <= l.x2 and self.y + self.r + self.vel > l.y1:
                    self.type_of_move = 4
                    return
            self.y += self.vel
        else:
            for l in l2:
                if self.y - self.r >= l.y1 and self.x + self.r >= l.x1 and self.x - self.r <= l.x2 and self.y - self.r - self.vel < l.y1:
                    self.type_of_move = 3
                    return
            self.y -= self.vel


class Line:
    def __init__(self, x1, y1, x2, y2, color=(0, 0, 0)):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.color = color

    def draw(self, screen):
        pygame.draw.line(screen, self.color, (self.x1, self.y1), (self.x2, self.y2))


class Start:
    def __init__(self, x, y, w, h, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))

    def __repr__(self) -> str:
        return f'{self.x} - {self.y} - {self.h} - {self.w}'

class End:
    def __init__(self, x, y, w, h, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def draw(self, screen):
        return pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))


class Game:
    def __init__(self, map_name='map1.txt', game_type='player'):
        self.game_type = game_type
        self.map_name = map_name
        a = open(map_name)
        X1, Y1, X2, Y2 = map(int, a.readline().split())
        self.start = Start(X1, Y1, X2 - X1, Y2 - Y1)
        X1, Y1, X2, Y2 = map(int, a.readline().split())
        self.end = End(X1, Y1, X2 - X1, Y2 - Y1)
        NVLine = int(a.readline())
        self.Hlines = list()
        for _ in range(NVLine):
            x1, y1, x2, y2 = map(int, a.readline().split())
            self.Hlines.append(Line(x1, y1, x2, y2))
        MVLine = int(a.readline())
        self.Vlines = list()
        for _ in range(MVLine):
            x1, y1, x2, y2 = map(int, a.readline().split())
            self.Vlines.append(Line(x1, y1, x2, y2))
        self.player_x, self.player_y = map(int, a.readline().split())
        pygame.init()
        self.player = Player(self.player_x, self.player_y, 20, 20)
        self.screen = pygame.display.set_mode((725, 425))
        N = int(a.readline())
        self.enemies = list()
        self.initial_enemies = list()
        for i in range(N):
            X, Y, T, R = map(int, a.readline().split())
            self.initial_enemies.append([X, Y, T, R])
            self.enemies.append(Enemy(X, Y, 8, type_of_move=T, r_move=R))
        self.goals = list()
        goal_count = int(a.readline())
        for i in range(goal_count):
            xx, yy = map(int, a.readline().split())
            self.goals.append([Goal(xx, yy, r=8), False])
        self.hasDied = False
        self.hasWon = False
        self.players = list()
        self.goal_player = list()
        self.dont_show = False
        for _ in range(len(self.goals)):
            self.goal_player.append(list())

    def run_player_mode(self):
        self.isRunning = True

        while self.isRunning:
            pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
            self.update()
            self.draw()

        pygame.quit()

    def run_AI_moves_graphic(self, moves):
        self.isRunning = True
        for i in range(len(moves)):
            pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
            self.update(i, moves)
            self.draw()
            if self.hasDied or self.hasWon:
                break
        return self

    def run_AI_moves_no_graphic(self, moves):
        self.isRunning = True
        self.dont_show = True
        for i in range(len(moves)):
            # pygame.time.delay(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
            self.update(i, moves)
            self.draw()
            if self.hasDied or self.hasWon:
                break
        return self

    def update(self, i=-1, moves=''):
        for e in self.enemies:
            e.move(self.Vlines, self.Hlines)
        if self.game_type == 'AI':
            self.player.move_AI(moves[i], self.Vlines, self.Hlines)
        else:
            keys = pygame.key.get_pressed()
            self.player.move_player(keys, self.Vlines, self.Hlines)

    def draw(self):
        self.screen.fill((183, 175, 250))
        self.start.draw(self.screen)
        end = self.end.draw(self.screen)
        x = self.player.draw(self.screen)
        for g in self.goals:
            if not g[1]:
                goal = g[0].draw(self.screen)
                if x.collidelist([goal]) != -1:
                    g[1] = True
        if x.collidelist([end]) != -1:
            can_win = True
            for g in self.goals:
                if not g[1]:
                    can_win = False
            if can_win:
                if self.game_type == 'player':
                    self.player.x = self.player_x
                    self.player.y = self.player_y
                    for g in self.goals:
                        g[1] = False
                    self.draw()
                    print('you win!')
                if self.game_type == 'AI':
                    self.hasWon = True
        for l in self.Vlines:
            l.draw(self.screen)
        for l in self.Hlines:
            l.draw(self.screen)
        for e in self.enemies:
            y = e.draw(self.screen)
            if x.collidelist([y]) != -1:
                if self.game_type == 'player':
                    self.player.x = self.player_x
                    self.player.y = self.player_y
                    self.draw()
                    return
                if self.game_type == 'AI':
                    self.hasDied = True
        if self.dont_show:
            self.screen.fill((183, 175, 250))
        pygame.display.update()


    def run_generation(self, list_of_moves, move_len):
        N = len(list_of_moves)
        for gp in self.goal_player:
            for _ in range(N):
                gp.append(False)
        for _ in range(N):
            self.players.append([Player(self.player_x, self.player_y, 20, 20), -1, False])
        self.isRunning = True
        for i in range(move_len):
            pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
            self.update_gen(list_of_moves, i)
            self.draw_gen(len(list_of_moves), i)
        return self

    def update_gen(self, list_of_moves, i):
        for e in self.enemies:
            e.move(self.Vlines, self.Hlines)
        for j in range(len(list_of_moves)):
            if self.players[j][1] == -1 and self.players[j][2] == False:
                self.players[j][0].move_AI(list_of_moves[j][i], self.Vlines, self.Hlines)

    def draw_gen(self, N, j):
        self.screen.fill((183, 175, 250))
        self.start.draw(self.screen)
        end = self.end.draw(self.screen)
        X = list()
        for i in range(N):
            if self.players[i][1] != -1:
                X.append(False)
                continue
            x = self.players[i][0].draw(self.screen)
            X.append(x)
        Y = list()
        for i in range(len(self.goals)):
            y = self.goals[i][0].draw(self.screen)
            Y.append(y)
        for i in range(len(X)):
            if not X[i]:
                continue
            for j in range(len(Y)):
                if X[i].collidelist([Y[j]]) != -1:
                    self.goal_player[j][i] = True
            if X[i].collidelist([end]) != -1:
                self.players[i][2] = True
                self.players[i][0].x = self.player_x
                self.players[i][0].y = self.player_y
        for l in self.Vlines:
            l.draw(self.screen)
        for l in self.Hlines:
            l.draw(self.screen)
        for e in self.enemies:
            y = e.draw(self.screen)
            for i in range(len(X)):
                if not X[i]:
                    continue
                if X[i].collidelist([y]) != -1:
                    self.players[i][1] = j
        pygame.display.update()
