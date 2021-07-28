class Move:
    def __init__(self, no, name, typ, cate, power, acc, exp, cl1, cl2):
        self.no = no
        self.name = name
        self.typ = typ
        self.cate = cate
        self.power = power
        self.acc = acc
        self.exp = exp
        self.cl1 = cl1
        self.cl2 = cl2

    def get_info(self):
        info = []

        info.append(self.no)
        info.append(self.name)
        info.append(self.typ)
        info.append(self.cate)
        info.append(self.power)
        info.append(self.acc)
        info.append(self.exp)
        info.append(self.cl1)
        info.append(self.cl2)

        return info




