import random

class NK(object):
    
    def __init__(self, N, K):
        self.N = N
        self.K = K
        self.loci = range(N)
        self.values = [{} for n in self.loci]
        self.dependence = [sorted([n] + random.sample(set(self.loci) - set([n]), K)) for n in self.loci]
        # Reverse lookup for dependence
        self.depends_on = [set() for n in self.loci]
        for n in self.loci:
            for d in self.dependence[n]:
                self.depends_on[d].add(n)
    
    def get_value(self, state):
        total_value = 0.0
        for n in self.loci:
            label = tuple([state[i] for i in self.dependence[n]])
            try:
                total_value += self.values[n][label]
            except KeyError:
                v = random.random()
                self.values[n][label] = v
                total_value += v
        total_value /= float(self.N)
        return total_value
    
    def get_values(self, states):
        results = [0] * len(states)
        dependence = self.dependence
        values = self.values
        loci = self.loci
        N = float(self.N)
        for state_num, state in enumerate(states):
            total_value = 0.0
            for n in loci:
                label = [state[i] for i in dependence[n]]
                label = tuple(label)
                try:
                    total_value += values[n][label]
                except KeyError:
                    v = random.random()
                    values[n][label] = v
                    total_value += v
            results[state_num] = total_value / N
        return results
            
    def get_hillclimb_values(self, states, loci=None):
        '''Generate values for each state with each of `loci` flipped.'''
        if loci is None:
            loci = [self.loci for state in states]
        if len(loci) != len(states):
            raise ValueError
        N = self.N
        base_locus_values = [0.0] * N
        result_states = []
        result_values = []
        depends_on = self.depends_on
        dependence = self.dependence
        for state_num, state in enumerate(states):
            state_values = []
            state_states = []
            # Calculate value of each locus before hill climbing
            for n in self.loci:
                label = tuple([state[i] for i in dependence[n]])
                try:
                    v = self.values[n][label]
                except KeyError:
                    v = random.random()
                    self.values[n][label] = v
                base_locus_values[n] = v
            # Alter each locus
            for l in loci[state_num]:
                locus_values = list(base_locus_values)
                s = list(state)
                s[l] = 1 - s[l]
                for n in depends_on[l]:
                    label = tuple([s[i] for i in dependence[n]])
                    try:
                        v = self.values[n][label]
                    except KeyError:
                        v = random.random()
                        self.values[n][label] = v
                    locus_values[n] = v
                state_states.append(s)
                state_values.append(sum(locus_values) / float(N))
            result_states.append(state_states)
            result_values.append(state_values)
        return result_states, result_values