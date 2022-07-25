import math


def HS_k(k, n, proportion):
    k1, k2 = k
    n1, n2 = n
    f1 = proportion / 100
    f2 = 1 - proportion / 100

    if k1 == k2:
        return k

    if ((k1 - k2) * (n1 - n2) > 0) or (n1 == n2):
        bulk_bounds = sorted([k1 + f2 / (1 / (k2 - k1) + f1 / (k1 + 4 * n1 / 3)),
                               k2 + f1 / (1 / (k1 - k2) + f2 / (k2 + 4 * n2 / 3))])
    else:
        if k1 > k2:
            if k1 + 0.5 / (1 / (k2 - k1) + 0.5 / (k1 + 4 * n1 / 3)) > k2 + 0.5 / (
                    1 / (k1 - k2) + 0.5 / (k2 + 4 * n2 / 3)):
                bulk_bounds = [k2 + f1 / (1 / (k1 - k2) + f2 / (k2 + 4 * n2 / 3)),
                               k1 + f2 / (1 / (k2 - k1) + f1 / (k1 + 4 * n1 / 3))]
            else:
                bulk_bounds = [k1 + f2 / (1 / (k2 - k1) + f1 / (k1 + 4 * n1 / 3)),
                               k2 + f1 / (1 / (k1 - k2) + f2 / (k2 + 4 * n2 / 3))]
        else:
            if k1 + 0.5 / (1 / (k2 - k1) + 0.5 / (k1 + 4 * n1 / 3)) > k2 + 0.5 / (
                    1 / (k1 - k2) + 0.5 / (k2 + 4 * n2 / 3)):
                bulk_bounds = [k2 + f1 / (1 / (k1 - k2) + f2 / (k2 + 4 * n2 / 3)),
                               k1 + f2 / (1 / (k2 - k1) + f1 / (k1 + 4 * n1 / 3))]
            else:
                bulk_bounds = [k1 + f2 / (1 / (k2 - k1) + f1 / (k1 + 4 * n1 / 3)),
                               k2 + f1 / (1 / (k1 - k2) + f2 / (k2 + 4 * n2 / 3))]

    return bulk_bounds


def HS_n(k, n, proportion):
    k1, k2 = k
    n1, n2 = n
    f1 = proportion / 100
    f2 = 1 - proportion / 100

    if n1 == n2:
        return n

    if ((k1 - k2) * (n1 - n2) > 0) or (k1 == k2):
        shear_bounds = sorted([n1 + f2 / (1 / (n2 - n1) + 2 * f1 * (k1 + 2 * n1) / (5 * n1 * (k1 + 4 * n1 / 3))),
                               n2 + f1 / (1 / (n1 - n2) + 2 * f2 * (k2 + 2 * n2) / (5 * n2 * (k2 + 4 * n2 / 3)))])
    else:
        if n1 > n2:
            if n2 + 0.5 / (1 / (n1 - n2) + 0.5 / (n2 + min(n) * ((9 * min(k) + 8 * min(n)) / (
                    min(k) + 2 * min(n))) / 6)) > n1 + 0.5 / (
                    1 / (n2 - n1) + 0.5 / (n1 + max(n) * ((9 * max(k) + 8 * max(n)) / (max(k) + 2 * max(n))) / 6)):
                shear_bounds = [n1 + f2 / (1 / (n2 - n1) + f1 / (
                                    n1 + max(n) * ((9 * max(k) + 8 * max(n)) / (max(k) + 2 * max(n))) / 6)),
                                n2 + f1 / (
                                        1 / (n1 - n2) + f2 / (
                                            n2 + min(n) * ((9 * min(k) + 8 * min(n)) / (min(k) + 2 * min(n))) / 6))]
            else:
                shear_bounds = [n2 + f1 / (
                    1 / (n1 - n2) + f2 / (n2 + min(n) * ((9 * min(k) + 8 * min(n)) / (min(k) + 2 * min(n))) / 6)),
                            n1 + f2 / (1 / (n2 - n1) + f1 / (
                                    n1 + max(n) * ((9 * max(k) + 8 * max(n)) / (max(k) + 2 * max(n))) / 6))]
        else:
            if n2 + f1 / (1 / (n1 - n2) + f2 / (n2 + max(n) * ((9 * max(k) + 8 * max(n)) / (
                    max(k) + 2 * max(n))) / 6)) > n1 + f2 / (
                    1 / (n2 - n1) + f1 / (n1 + min(n) * ((9 * min(k) + 8 * min(n)) / (min(k) + 2 * min(n))) / 6)):
                shear_bounds = [n1 + f2 / (
                        1 / (n2 - n1) + f1 / (n1 + min(n) * ((9 * min(k) + 8 * min(n)) / (min(k) + 2 * min(n))) / 6)),
                                n2 + f1 / (1 / (n1 - n2) + f2 / (
                                        n2 + max(n) * ((9 * max(k) + 8 * max(n)) / (max(k) + 2 * max(n))) / 6))]
            else:
                shear_bounds = [n2 + f1 / (1 / (n1 - n2) + f2 / (
                                        n2 + max(n) * ((9 * max(k) + 8 * max(n)) / (max(k) + 2 * max(n))) / 6)),
                                n1 + f2 / (1 / (n2 - n1) + f1 / (
                                        n1 + min(n) * ((9 * min(k) + 8 * min(n)) / (min(k) + 2 * min(n))) / 6))]

    return shear_bounds


def SCA(k, n, a):
    k1, k2 = k
    n1, n2 = n
    asp1, asp2 = a

    kbr = []
    nbr = []
    por = []

    if asp1 == 1:
        asp1 = 0.99
    if asp2 == 1:
        asp2 = 0.99

    if asp1 < 1:
        theta1 = (asp1 / ((1 - asp1 ** 2) ** (3 / 2))) * (math.acos(asp1) - asp1 * math.sqrt(1 - asp1 ** 2))
        fn1 = (asp1 ** 2 / (1 - asp1 ** 2)) * (3 * theta1 - 2)

    if asp2 < 1:
        theta2 = (asp2 / ((1 - asp2 ** 2) ** (3 / 2))) * (math.acos(asp2) - asp2 * math.sqrt(1 - asp2 ** 2))
        fn2 = (asp2 ** 2 / (1 - asp2 ** 2)) * (3 * theta2 - 2)

    if asp1 > 1:
        theta1 = (asp1 / ((asp1 ** 2 - 1) ** (3 / 2))) * (asp1 * math.sqrt(asp1 ** 2 - 1) - math.acosh(asp1))
        fn1 = (asp1 ** 2 / (asp1 ** 2 - 1)) * (2 - 3 * theta1)

    if asp2 > 1:
        theta2 = (asp2 / ((asp2 ** 2 - 1) ** (3 / 2))) * (asp2 * math.sqrt(asp2 ** 2 - 1) - math.acosh(asp2))
        fn2 = (asp2 ** 2 / (asp2 ** 2 - 1)) * (2 - 3 * theta2)

    epsilon = 1e-7
    for x1 in [epsilon] + [i / 100 for i in range(1, 100)] + [1 - epsilon]:
        x2 = 1 - x1

        ksc = x1 * k1 + x2 * k2
        nsc = x1 * n1 + x2 * n2
        knew = 0
        nnew = 0
        tol = 1e-6 * k1
        d = abs(ksc - knew)
        niter = 0

        if nsc == 0:
            pass

        while (d > abs(tol)) and (niter < 3000):
            nusc = (3 * ksc - 2 * nsc) / (2 * (3 * ksc + nsc))
            a1 = n1 / nsc - 1
            a2 = n2 / nsc - 1
            b1 = (1 / 3) * (k1 / ksc - n1 / nsc)
            b2 = (1 / 3) * (k2 / ksc - n2 / nsc)
            r = (1 - 2 * nusc) / (2 * (1 - nusc))

            f11 = 1 + a1 * ((3 / 2) * (fn1 + theta1) - r * ((3 / 2) * fn1 + (5 / 2) * theta1 - (4 / 3)))
            f12 = 1 + a2 * ((3 / 2) * (fn2 + theta2) - r * ((3 / 2) * fn2 + (5 / 2) * theta2 - (4 / 3)))

            f21 = 1 + a1 * (1 + (3 / 2) * (fn1 + theta1) - (r / 2) * (3 * fn1 + 5 * theta1)) + b1 * (3 - 4 * r)
            f21 = f21 + (a1 / 2) * (a1 + 3 * b1) * (3 - 4 * r) * (fn1 + theta1 - r * (fn1 - theta1 + 2 * theta1 ** 2))
            f22 = 1 + a2 * (1 + (3 / 2) * (fn2 + theta2) - (r / 2) * (3 * fn2 + 5 * theta2)) + b2 * (3 - 4 * r)
            f22 = f22 + (a2 / 2) * (a2 + 3 * b2) * (3 - 4 * r) * (fn2 + theta2 - r * (fn2 - theta2 + 2 * theta2 ** 2))

            f31 = 1 + a1 * (1 - (fn1 + (3 / 2) * theta1) + r * (fn1 + theta1))
            f32 = 1 + a2 * (1 - (fn2 + (3 / 2) * theta2) + r * (fn2 + theta2))

            f41 = 1 + (a1 / 4) * (fn1 + 3 * theta1 - r * (fn1 - theta1))
            f42 = 1 + (a2 / 4) * (fn2 + 3 * theta2 - r * (fn2 - theta2))

            f51 = a1 * (-fn1 + r * (fn1 + theta1 - (4 / 3))) + b1 * theta1 * (3 - 4 * r)
            f52 = a2 * (-fn2 + r * (fn2 + theta2 - (4 / 3))) + b2 * theta2 * (3 - 4 * r)

            f61 = 1 + a1 * (1 + fn1 - r * (fn1 + theta1)) + b1 * (1 - theta1) * (3 - 4 * r)
            f62 = 1 + a2 * (1 + fn2 - r * (fn2 + theta2)) + b2 * (1 - theta2) * (3 - 4 * r)

            f71 = 2 + (a1 / 4) * (3 * fn1 + 9 * theta1 - r * (3 * fn1 + 5 * theta1)) + b1 * theta1 * (3 - 4 * r)
            f72 = 2 + (a2 / 4) * (3 * fn2 + 9 * theta2 - r * (3 * fn2 + 5 * theta2)) + b2 * theta2 * (3 - 4 * r)

            f81 = a1 * (1 - 2 * r + (fn1 / 2) * (r - 1) + (theta1 / 2) * (5 * r - 3)) + b1 * (1 - theta1) * (3 - 4 * r)
            f82 = a2 * (1 - 2 * r + (fn2 / 2) * (r - 1) + (theta2 / 2) * (5 * r - 3)) + b2 * (1 - theta2) * (3 - 4 * r)

            f91 = a1 * ((r - 1) * fn1 - r * theta1) + b1 * theta1 * (3 - 4 * r)
            f92 = a2 * ((r - 1) * fn2 - r * theta2) + b2 * theta2 * (3 - 4 * r)

            p1 = 3 * f11 / f21
            p2 = 3 * f12 / f22
            q1 = (2 / f31) + (1 / f41) + ((f41 * f51 + f61 * f71 - f81 * f91) / (f21 * f41))
            q2 = (2 / f32) + (1 / f42) + ((f42 * f52 + f62 * f72 - f82 * f92) / (f22 * f42))

            p1 = p1 / 3
            p2 = p2 / 3
            q1 = q1 / 5
            q2 = q2 / 5

            knew = (x1 * k1 * p1 + x2 * k2 * p2) / (x1 * p1 + x2 * p2)
            nnew = (x1 * n1 * q1 + x2 * n2 * q2) / (x1 * q1 + x2 * q2)

            d = abs(ksc - knew)
            ksc = knew
            nsc = nnew
            niter = niter + 1

        kbr.append(ksc)
        nbr.append(nsc)
        por.append(x1)

    return kbr, nbr, por
