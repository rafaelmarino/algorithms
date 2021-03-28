# python3



class JobQueue:
    #  total run time = number of jobs x number of sifts = O(n(log(n)))
    def SiftDown(self, i):
        # run time O(log(n))
        min_i = i
        l = 2*i + 1
        r = 2*i + 2

        if l <= len(self.nft) - 1:  # if l is a valid node
            if self.nft[l][1] < self.nft[min_i][1]:
                min_i = l
            elif self.nft[l][1] == self.nft[min_i][1] and self.nft[l][0] < self.nft[min_i][0]:
                min_i = l

        if r <= len(self.nft) - 1:  # if r is a valid node
            if self.nft[r][1] < self.nft[min_i][1]:
                min_i = r
            elif self.nft[r][1] == self.nft[min_i][1] and self.nft[r][0] < self.nft[min_i][0]:
                min_i = r

        if i != min_i:  # swap the whole entry for worker i with new min worker
            self.nft[i], self.nft[min_i] = self.nft[min_i], self.nft[i]
            self.SiftDown(min_i)

    def read_data(self):
        # 2 ints; count(threads), count(jobs)
        self.num_workers, m = map(int, input().split())
        self.jobs = list(map(int, input().split()))  # vector of times for each job
        assert m == len(self.jobs)

    def write_response(self):
        for i in range(len(self.jobs)):
          print(self.assigned_workers[i], self.start_times[i]) 

    def assign_jobs(self):
        # TODO: replace this code with a faster algorithm.
        self.assigned_workers = [None] * len(self.jobs)
        self.start_times = [None] * len(self.jobs)
        next_free_time = [0] * self.num_workers
        for i in range(len(self.jobs)):
          next_worker = 0
          for j in range(self.num_workers):
            if next_free_time[j] < next_free_time[next_worker]:
              next_worker = j
          self.assigned_workers[i] = next_worker
          self.start_times[i] = next_free_time[next_worker]
          next_free_time[next_worker] += self.jobs[i]

    def assign_heap(self):
        self.assigned_workers = [None] * len(self.jobs)
        self.start_times = [None] * len(self.jobs)
        self.nft = [[x, 0] for x in range(self.num_workers)]

        for i in range(len(self.jobs)):
            self.assigned_workers[i] = self.nft[0][0]  # index of worker zero
            self.start_times[i] = self.nft[0][1]  # time of worker zero
            self.nft[0][1] += self.jobs[i]  # update start time of worker zero
            self.SiftDown(0)  # always sift down the newly updated worker zero

    def solve(self):
        self.read_data()
        self.assign_heap()
        self.write_response()

if __name__ == '__main__':
    job_queue = JobQueue()
    job_queue.solve()

