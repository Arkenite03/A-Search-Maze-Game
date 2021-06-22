from queue import PriorityQueue
import pygame

class myPriorityQueue:

    def __init__(self):

        self.queue = set()
        self.inf = 1000000

    def empty(self):

        return len(self.queue) == 0

    def get(self):

        mn = self.inf

        for spot in self.queue:

            if mn >= spot[0]:

                mn = spot[0]
                tup = spot


        self.queue.remove(tup)
        return tup


    def put(self, tup):

        self.queue.add(tup)


class Algorithm:
    def h(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)


    def reconstruct_path(self, came_from, current, draw):
        while current in came_from:
            current = came_from[current]
            current.make_path()
            draw()
        current.make_start()

    def algorithm(self, draw, grid, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for row in grid for spot in row}
        g_score[start] = 0
        f_score = {spot: float("inf") for row in grid for spot in row}
        f_score[start] = self.h(start.get_pos(), end.get_pos())

        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)
            print("\n\nCurrent : " + str(current.get_pos()[0]) + " " + str(current.get_pos()[1]))
            print("neighbors : ",end= " ")

            if current == end:
                self.reconstruct_path(came_from, end, draw)
                end.make_end()
                return True

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.h(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()
                        print("F = " + str(f_score[neighbor]) + "  " + str(neighbor.get_pos()[0]) + " " + str(neighbor.get_pos()[1]),end = " | ")


            draw()
            print("open_set : ",end=" ")
            for i in open_set_hash:

                print(str(i.get_pos()[0]) + " " + str(i.get_pos()[1]), end=" | ")

            if current != start:
                current.make_closed()

        return False
