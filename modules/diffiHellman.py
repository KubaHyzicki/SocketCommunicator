from math import pow

class DiffiHellman:
    # "Module containing Diffi-Hellman protocol mathematic operations"
    def __init__(self, keys, ab):
        self.keys = keys
        self.ab = ab

    def calc_AB(self):
        # "Calculate A or B based on keys and a/b"
        self.AB = pow(self.keys['g'], self.ab) % self.keys['p']
        return int(self.AB)

    def calc_s(self, AB_2):
        # "Calculate final secret based on a/b, keys and calculated A/B value"
        return int(pow(AB_2, self.ab) % self.keys['p'])
