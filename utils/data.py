import heapq


# class PrioQueue():
#     def __init__(self):
#         self.data = list()
#
#     def get(self):
#         return self.data.pop(0)
#
#     def put(self, prio_item):
#         self.data.append(prio_item)
#
#         self.data.sort(key=lambda pi: (pi[0], (pi[1][1], pi[1][0])))
#
#     def empty(self):
#         return len(self.data) == 0


class PriorityQueue():
    """A subclass of Queue; retrieves entries in priority order (lowest first).

    Entries are typically tuples of the form: (priority number, data).
    """
    def __init__(self):
        self._queue = []

    def put(self, item):
        heapq.heappush(self._queue, item)

    def get(self):
        return heapq.heappop(self._queue)

    def empty(self):
        return len(self._queue) == 0