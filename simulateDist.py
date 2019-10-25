import sys
import math
import random as rng
rng.seed(35)



class distributions():

    def __init__(self):
        self.X = []

    def bernoulli(self, s_size, args):
        if len(args) != 1: self.exitProgram()
        p = float(args[0])
        if p < 0.0 or p > 1.0: sys.exit('Incorrect probability value : ' + str(p))
        for i in range(s_size):
            if rng.random() <= p:
                self.X.append(1)
            else:
                self.X.append(0)
        return self.X

    def binomial(self, s_size, args):
        if len(args) != 2: self.exitProgram()
        n = int(args[0])
        p = float(args[1])
        if p < 0.0 or p > 1.0: sys.exit('Incorrect probability value : ' + str(p))
        for i in range(s_size):
            nS = 0
            for j in range(n):
                if rng.random() <= p:
                    nS = nS + 1
            self.X.append(nS)
        return self.X

    def geometric(self, s_size, args):
        if len(args) != 1: self.exitProgram()
        p = float(args[0])
        if p < 0.0 or p > 1.0: sys.exit('Incorrect probability value : ' + str(p))
        for i in range(s_size):
            t = 1
            while rng.random() > p:
                t = t + 1
            self.X.append(t)
        return self.X

    def negBinomial(self, s_size, args):
        if len(args) != 2: self.exitProgram()
        k = int(args[0])
        p = args[1:len(args)]
        for i in range(s_size):
            self.X.append(sum(self.geometric(k, p)))
        return self.X

    def poisson(self, s_size, args):
        if len(args) != 1: self.exitProgram()
        lda = float(args[0])
        for i in range(s_size):
            k = 0
            u = rng.random()
            while u >= math.exp((0.0 - lda)):
                k = k + 1
                u = u * rng.random()
            self.X.append(k)
        return self.X

    def cdfDisc(self, p):
        F = []
        for i in range(len(p)):
            F.append(sum(p[0:i + 1]))
        return F

    def arbDiscrete(self, s_size, args):
        p = []
        for v in args:
            p.append(float(v))
        F = self.cdfDisc(p)
        if F[-1] != 1: sys.exit('Probabilites need to add up 1')
        for i in range(s_size):
            t = 0
            u = rng.random()
            while F[t] <= u:
                t = t + 1
                self.X.append(t)
        return self.X

    def uniform(self, s_size, args):
        if len(args) != 2: self.exitProgram()
        a = float(args[0])
        b = float(args[1])
        if a > b:
            t = a;
            a = b;
            b = t;
        for i in range(s_size):
            self.X.append(a + ((b - a) * rng.random()))
        return self.X

    def exponential(self, s_size, args):
        if len(args) != 1: self.exitProgram()
        lda = float(args[0])
        for i in range(s_size):
            self.X.append((0 - (1 / lda)) * math.log(1 - rng.random()))
        return self.X

    def gamma(self, s_size, args):
        if len(args) != 2: self.exitProgram()
        alp = int(args[0])
        lda = args[1:len(args)]
        for i in range(s_size):
            self.X.append(sum(self.exponential(alp, lda)))
        return self.X

    def normal(self, s_size, args):
        if len(args) != 2: self.exitProgram()
        s_size2 = int(math.ceil(float(s_size) / 2))
        mu = float(args[0])
        sd = float(args[1])
        for i in range(s_size2):
            u1 = rng.random()
            u2 = rng.random()
            z1 = math.sqrt((0 - 2) * math.log(u1)) * math.cos(2 * math.pi * u2)
            z2 = math.sqrt((0 - 2) * math.log(u1)) * math.sin(2 * math.pi * u2)
            self.X.append(mu + z1 * sd)
            self.X.append(mu + z2 * sd)
        if s_size % 2 == 0:
            return self.X
        else:
            return self.X[0:len(self.X) - 1]

    def sMean(self, smpl):
        return (float(sum(smpl)) / float(len(smpl)))

    def sVar(self, smpl, mean):
        t = 0.0
        for i in smpl:
            t = t + float((i - mean) * (i - mean))
        if len(smpl) == 1:
            return t
        return t / float(len(smpl) - 1)

    def exitProgram(self):
        sys.exit('Incorrect number of arguments')


def main(argv):
    dist = distributions()
    try:
        s_size = int(argv[1])
        args = argv[3:len(argv)]
        lower = argv[2].lower()
        if lower == 'bernoulli':
            res = dist.bernoulli(s_size, args)
        elif lower == 'binomial':
            res = dist.binomial(s_size, args)
        elif lower == 'geometric':
            res = dist.geometric(s_size, args)
        elif lower == 'neg-binomial':
            res = dist.negBinomial(s_size, args)
        elif lower == 'poisson':
            res = dist.poisson(s_size, args)
        elif lower == 'arb-discrete':
            res = dist.arbDiscrete(s_size, args)
        elif lower == 'uniform':
            res = dist.uniform(s_size, args)
        elif lower == 'exponential':
            res = dist.exponential(s_size, args)
        elif lower == 'gamma':
            res = dist.gamma(s_size, args)
        elif lower == 'normal':
            res = dist.normal(s_size, args)
        else:
            sys.exit('Distribution ' + args[2] + ' is not supported')
        print 'Values: ' + str(res)
        mean = dist.sMean(res)
        print '\nSample Mean: ' + str(mean)
        print 'Sample Variance: ' + str(dist.sVar(res, mean))
    except ValueError:
        print 'Incorrect number format'


if __name__ == '__main__':
    main(sys.argv)
