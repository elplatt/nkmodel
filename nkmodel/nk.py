import itertools
import math
import random

class NK(object):
    """The NK class produces objects representing a single NK model.
    
    Constructor params:
    N: The number of loci
    K: The number of loci, in addition to self, each locus depends on
    exponent: (default 1) The raw model values are raised to this exponent, 
    
    For each locus, a lookup table maps K+1 length tuples to values in [0,1].
    These tuples are the state values of that loci's _concern_ (the K+1 loci it depends on),
    in order of increasing index.
    """
    
    def __init__(self, N, K, exponent=1):
        self.N = N
        self.K = K
        self.exponent = exponent
        self.loci = range(N)
        self.values = [{} for n in self.loci]
        # For locus i, dependence[i] stores the indeces of loci it depends on
        self.dependence = [
            sorted([n] + random.sample(set(self.loci) - set([n]), K))
            for n in self.loci]
        # Reverse lookup for dependence, depends_on[i] gives indeces of all loci that depend on i
        self.depends_on = [set() for n in self.loci]
        for n in self.loci:
            for d in self.dependence[n]:
                self.depends_on[d].add(n)
    
    def get_value(self, state):
        total_value = 0.0
        for n in self.loci:
            # Construct locus 
            label = tuple([state[i] for i in self.dependence[n]])
            try:
                total_value += self.values[n][label]
            except KeyError:
                v = random.random()
                self.values[n][label] = v
                total_value += v
        # Normalize value to [0,1]
        total_value /= float(self.N)
        # Adjust value distribution by raising to power of self.exponent
        if self.exponent != 1:
            total_value = math.pow(total_value, self.exponent)
        return total_value
    
    def get_values(self, states):
        """Get the NK model values for each agent in states.
        
        Parameters
        states: a dict mapping agent ids to states.
        
        Returns: a dict mapping agent ids to nk model values.
        """
        results = dict(states)
        dependence = self.dependence
        values = self.values
        loci = self.loci
        N = float(self.N)
        for state_num, state in states.items():
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
            # Adjust value distribution by raising to power of self.exponent
            if self.exponent != 1:
                results[state_num] = math.pow(results[state_num], self.exponent)
        return results
      
    def get_hillclimb_values(self, states, loci=None):
        '''Generate values for each state with each of `loci` flipped.'''
        if loci is None:
            loci = dict([(state, self.loci) for state in states])
        if len(loci) != len(states):
            raise ValueError
        N = self.N
        base_locus_values = [0.0] * N
        result_states = {}
        result_values = {}
        depends_on = self.depends_on
        dependence = self.dependence
        for state_num, state in states.items():
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
                value = sum(locus_values) / float(N)
                # Adjust value distribution by raising to power of self.exponent
                if self.exponent != 1:
                    value = math.pow(value, self.exponent)
                state_values.append(value)
            result_states[state_num] = state_states
            result_values[state_num] = state_values
        return result_states, result_values
    
    def get_global_max(self):
        # Prevent unnecessary lookups
        loci = self.loci
        values = self.values
        dependence = self.dependence
        
        # Loop through all states
        max_value = 0.0
        max_state = None
        all_states = itertools.product((0, 1), repeat=self.N)
        for state in all_states:
            total_value = 0.0
            # Calculate value of each locus
            for n in loci:
                # Construct locus lookup key
                label = tuple([state[i] for i in dependence[n]])
                try:
                    total_value += values[n][label]
                except KeyError:
                    # If key has not been looked up before, generate a value
                    v = random.random()
                    values[n][label] = v
                    total_value += v
            # Compare state value to total value
            if total_value > max_value:
                max_value = total_value
                max_state = state
            elif total_value == max_value:
                raise Exception('Two states tied for max_value')
        # Divide by N to normalize model value
        max_value = max_value / self.N
        # Adjust value distribution by raising to power of self.exponent
        if self.exponent != 1:
            max_value = math.pow(max_value, self.exponent)
        return (max_state, max_value)