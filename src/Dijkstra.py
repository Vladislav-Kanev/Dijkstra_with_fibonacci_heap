from src.FibonacciHeap import FibonacciHeap


def dijkstra_with_labels(graph: list[(int, int)], start: int):
    n = len(graph)
    distance = [float('inf')] * n
    distance[start] = 0
    used = [False] * n

    for _ in range(n):
        v = None

        for j in range(n):
            if not used[j] and (v is None or distance[j] < distance[v]):
                v = j

        if distance[v] == float('inf'):
            break
        used[v] = True

        for edge, weight in graph[v]:
            if distance[v] + weight < distance[edge]:
                distance[edge] = distance[v] + weight

    return distance


def dijkstra_fibonacci_heap(adjList, source):
    n = len(adjList)
    distance = [float('inf')]*n
    heap = FibonacciHeap()

    nodes_list = []

    for vert in range(len(adjList)):
        if vert != source:
            nodes_list.append(heap.insert(float('inf'), vert))
        else:
            nodes_list.append(heap.insert(0, vert))
            distance[vert] = 0

    while (heap.no_nodes):
        next_vert = heap.get_min()

        heap.delete_min()

        if (distance[next_vert.val] == float('inf')):
            break

        for vertex, weight in adjList[next_vert.val]:
            if (distance[next_vert.val] + weight) < distance[vertex]:
                distance[vertex] = distance[next_vert.val] + weight
                heap.decrease_key(
                    nodes_list[vertex], distance[vertex]
                )

    return distance
