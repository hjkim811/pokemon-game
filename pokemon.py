from info import typ


class Pokemon:
    eva = 1
    acc = 1
    rank_eva = 0
    rank_acc = 0

    rank_at = 0
    rank_df = 0
    rank_sp_at = 0
    rank_sp_df = 0
    rank_spd = 0

    def __init__(self, no, name, typ1, typ2, exp, hp, at, df, sp_at, sp_df, spd, tot, mv1, mv2, mv3, mv4):
        self.no = no  # int형
        self.name = name
        self.typ1 = typ1  # int형
        self.typ2 = typ2  # int형
        self.exp = exp
        self.hp = hp  # int형
        self.at = at  # int형
        self.df = df  # int형
        self.sp_at = sp_at  # int형
        self.sp_df = sp_df  # int형
        self.spd = spd  # int형
        self.tot = tot  # int형
        self.mv1 = mv1
        self.mv2 = mv2
        self.mv3 = mv3
        self.mv4 = mv4

    def get_info(self):
        info = []

        info.append(self.no)
        info.append(self.name)
        if self.typ2 == 0:
            info.append(typ[self.typ1])
        else:
            info.append(typ[self.typ1] + ", " + typ[self.typ2])
        info.append(self.exp)
        info.append(self.hp)
        info.append(self.at)
        info.append(self.df)
        info.append(self.sp_at)
        info.append(self.sp_df)
        info.append(self.spd)

        return info

    def get_info_move(self):
        info = []

        info.append(self.no)
        info.append(self.name)
        if self.typ2 == 0:
            info.append(typ[self.typ1])
        else:
            info.append(typ[self.typ1] + ", " + typ[self.typ2])
        info.append(self.exp)
        info.append(self.hp)
        info.append(self.at)
        info.append(self.df)
        info.append(self.sp_at)
        info.append(self.sp_df)
        info.append(self.spd)
        info.append(self.mv1)
        info.append(self.mv2)
        info.append(self.mv3)
        info.append(self.mv4)

        return info

