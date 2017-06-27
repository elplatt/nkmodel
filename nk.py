import random

class NK(object):
    
    def __init__(self, N, K):
        self.N = N
        self.K = K
        loci = range(N)
        self.values = [{} for n in loci]
        self.dependence = [sorted([n] + random.sample(set(loci) - set([n]), K)) for n in loci]
    
    def get_value(self, state):
        total_value = 0.0
        for n in range(self.N):
            label = tuple([state[i] for i in self.dependence[n]])
            try:
                total_value += self.values[n][label]
            except KeyError:
                v = random.random()
                self.values[n][label] = v
                total_value += v
        total_value /= float(self.N)
        return total_value