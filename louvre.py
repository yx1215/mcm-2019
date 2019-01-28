from adjacency_matrix import Louvre_matrix, Louvre_weight, is_stairs, accessible, Louvre_list, Louvre_vertex_adj_num, weight_sum
import random
import numpy
random.seed(0)
WIDE = 10
STAIR_WIDE = 5
STAIR_LENGTH = 15
EXIT = [8, 25, 27, 53]
TEST_TIME = 200


def Fruin_model(u, v, N, L, stair=False):
    if not stair:
        D = N / (WIDE * L)
        velocity = 1.427 - 0.3549 * D
    else:
        # go downstairs
        D = N / (STAIR_WIDE * L)
        if u > v:
            velocity = 0.6502 - 0.0972 * D
        else:
            velocity = 0.564 - 0.0765 * D
    return velocity


class Louvre:
    def __init__(self):
        self.adj_matrix = Louvre_matrix
        self.adj_list = Louvre_list
        self.length = Louvre_weight
        self.is_stairs = is_stairs
        self.accessible = accessible
        self.adj_num = Louvre_vertex_adj_num
        self.num_of_people = [0 for i in range(90)]
        self.people_on_edge = [[0 for i in range(90)] for j in range(90)]
        self.v = [[None for i in range(90)] for j in range(90)]
        self.time = [[None for i in range(90)] for j in range(90)]
        self.total_time = [float("inf") for i in range(90)]
        self.route = [None for i in range(90)]
        self.best_route = [None for i in range(90)]
        self.weight_sum = weight_sum

        self.new_adj_list = [[] for i in range(90)]
        self.new_time = [[None for i in range(90)] for j in range(90)]

        self.change = [False for i in range(90)]
        self.partial_time = [None for i in range(90)]

    def cut_route(self, u, v):
        self.accessible[u - 1][v - 1] = False

    def set_people(self, u):
        self.num_of_people[u] = int(random.randint(1, 50) * self.weight_sum[u])

    def input_people(self, l):
        self.num_of_people = l

    def generalize_people(self):
        for i in range(90):
            if i + 1 not in EXIT:
                self.set_people(i)

    def distribute_people(self):
        self.generalize_people()
        self.distribute_people_without_generalize()

    def distribute_people_without_generalize(self):
        for i in range(90):
            for j in self.adj_list[i]:
                self.people_on_edge[i][j - 1] = self.num_of_people[i] / self.adj_num[i] + self.num_of_people[j - 1] / self.adj_num[j - 1]

    def compute_v(self):
        for i in range(90):
            for j in self.adj_list[i]:
                N = self.people_on_edge[i][j - 1]
                if self.is_stairs[i][j - 1]:
                    self.v[i][j - 1] = Fruin_model(i, j - 1, N, STAIR_LENGTH, stair=True)
                else:
                    self.v[i][j - 1] = Fruin_model(i, j - 1, N, 30 * self.length[i][j - 1])

    def compute_time(self):
        self.compute_v()
        for i in range(90):
            for j in self.adj_list[i]:
                if self.is_stairs[i][j - 1]:
                    self.time[i][j - 1] = STAIR_LENGTH / self.v[i][j - 1]
                else:
                    self.time[i][j - 1] = self.length[i][j - 1] * 30/ self.v[i][j - 1]

    def test(self):
        for i in range(90):
            for j in range(90):
                if self.time[i][j] is not None:
                    if self.time[i][j] < 0:
                        print(i, j)
                        print(self.v[i][j])
                        return False
        return True

    def test_finish(self):
        for i in range(90):
            for j in self.adj_list[i]:
                if self.people_on_edge[i][j - 1] != 0:
                    return False
        return True

    def reverse_graph(self):
        for i in range(90):
            for v in self.adj_list[i]:
                self.new_adj_list[v - 1].append(i + 1)
                self.new_time[v - 1][i] = self.time[i][v - 1]

    def find_min_total_time(self, l):
        m = l[0]
        for i in l:
            if self.total_time[i] < self.total_time[m]:
                m = i
        return m

    def dijkstra(self, u):
        self.total_time[u - 1] = 0
        F = [i for i in range(90)]
        while len(F) != 0:

            v = self.find_min_total_time(F)
            for j in self.new_adj_list[v]:
                if self.total_time[j - 1] > self.total_time[v] + self.new_time[v][j - 1]:
                    self.route[j - 1] = v + 1
                    self.total_time[j - 1] = self.total_time[v] + self.new_time[v][j - 1]
            F.remove(v)

    def initiate_list(self):
        self.total_time = [float("inf") for i in range(90)]
        self.route = [None for i in range(90)]

    def generate_best_route(self):
        result = []
        route = []
        final_route = [None for i in range(90)]
        final_result = [float("inf") for i in range(90)]
        self.distribute_people()
        self.compute_time()
        self.reverse_graph()
        for end in EXIT:
            self.initiate_list()
            self.dijkstra(end)
            result.append(self.total_time)
            route.append(self.route)
            # print(self.total_time)
            # print(self.route)
        for i in range(90):
            min_route = find_min(result, i)
            final_route[i] = route[min_route][i]
            final_result[i] = result[min_route][i]
        return final_route


    # def generate_partial_time(self):
    #     result = [None for i in range(90)]
    #     for i in self.route
def find_min(l, index):
    min = 0
    for i in range(4):
        if l[i][index] < l[min][index]:
            min = i
    return min


def test_need_adjust_position():
    total_route = []

    for k in range(TEST_TIME):
        Graph = Louvre()
        final_route = Graph.generate_best_route()
        total_route.append(final_route)
    count = [{} for i in range(90)]

    for i in range(90):
        for j in range(TEST_TIME):
            try:
                count[i][total_route[j][i]] += 1
            except:
                count[i][total_route[j][i]] = 1
    # print(count)
    need_adjust = []
    for i in range(90):
        dic = count[i]
        M = max(dic.values())
        if M / TEST_TIME < 0.7:
            need_adjust.append(i)

    print(need_adjust)
    return need_adjust
    # print(need_adjust)
# def generate_partial_time(best_route):
#     result = [None for i in range(90)]
#     for i in best_route:
#         if i is not None:



if __name__ == '__main__':
    # result = []
    # route = []
    # final_route = [None for i in range(90)]
    # final_result = [float("inf") for i in range(90)]
    L = []
    p = {}
    final_p = []
    N = 30
    for i in range(N):
        L.append(test_need_adjust_position())
    for i in L:
        for j in i:
            try:
                p[j] += 1
            except:
                p[j] = 1
    print(p)
    for i in p.keys():
        if p[i] >= 0.7 * N:
            final_p.append(i)
    print(final_p)
    # print(Graph.people_on_edge)
    # print(Graph.v)
    # print(Graph.time)
    # print(Graph.test())


