from pokemon import Pokemon
from info import typ, typ_re, rank1, rank2, rank3, eff, flinch, move_2, move_3, move_1_8, move_1_9
import random
from move import Move
from prob import prob
from math import floor, sqrt, ceil


def import_info(num):
    import csv

    with open('정보.csv', 'rt') as f:
        first_line = f.readline()
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            # print(row)
            if num == int(row[0]):
                po = Pokemon(int(row[0]), row[1], int(row[9]), int(row[10]), row[15], int(row[2]), int(row[3]),
                             int(row[4]), int(row[5]), int(row[6]), int(row[7]), int(row[8]), row[11], row[12], row[13], row[14])
                break

    f.close()

    return po


def wild_pokemon(tier):

    if tier == 1:
        no = random.randint(1, 6)
    elif tier == 2:
        no = random.randint(7, 17)
    elif tier == 3:
        no = random.randint(18, 47)
    elif tier == 4:
        no = random.randint(48, 101)
    elif tier == 5:
        no = random.randint(102, 151)
    else:
        print("input error")

    import csv

    with open('정보_종족값순.csv', 'rt') as f:
        first_line = f.readline()
        reader = csv.reader(f, delimiter=',')

        for row in reader:
            if int(row[0]) == no:
                wild = int(row[1])
                break

    f.close()

    return wild


def import_move(name):
    try:
        import csv

        with open('기술 목록_1세대.csv', 'rt') as f:
            first_line = f.readline()
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                # print(row)
                if name == row[1]:
                    mo = Move(row[0], row[1], row[2], row[3], row[4], row[5], row[7], row[9], row[10])
                    break

        f.close()

        return mo

    except UnboundLocalError:
        print("엑셀에 존재하지 않는 기술 이름")


def cal_damage(attacker, target, move, cri=0, cri_lt=1):  # cri_lt=0이면 급소 문구 출력 x

    message = []

    try:
        power = int(move.power)
    except ValueError:
        print("위력이 정수값이 아닙니다.")

    if move.cate == '물리':
        a = attacker.at
        d = target.df
    elif move.cate == '특수':
        a = attacker.sp_at
        d = target.sp_df
    else:
        print("기술 분류 error")

    if prob(rank3[cri]) == 1:
        critical = 2
        if cri_lt != 0:
            message.append("급소에 맞았다!")
    else:
        critical = 1

    rand = random.randint(217, 255) / 255

    if move.typ == typ[attacker.typ1] or move.typ == typ[attacker.typ2]:
        stab = 1.5
    else:
        stab = 1

    if target.typ2 == 0:
        type_eff = eff[typ_re[move.typ] - 1][target.typ1 - 1]
    else:
        type_eff = eff[typ_re[move.typ] - 1][target.typ1 - 1] * eff[typ_re[move.typ] - 1][target.typ2 - 1]

    if type_eff == 4 or type_eff == 2:
        message.append("효과는 굉장했다!")
    if type_eff == 1/4 or type_eff == 1/2:
        message.append("효과가 별로인 듯하다..")
    if type_eff == 0:
        message.append("효과가 없다...")

    damage = floor((power*a/d*42/50+2)*critical*rand*stab*type_eff)

    return [damage, message]


def catch_rate(max_hp, current_hp, total_stat):
    rate = 255*(700-total_stat)/700
    a = (3*max_hp - 2*current_hp)*rate/(2*max_hp)

    if a >= 255:
        return 5

    else:
        b = ceil(65535 * sqrt(sqrt(a/255)))
        count = 0
        lst = random.choices(list(range(1, 65536)), k=4)

        for i in range(4):
            if lst[i] <= b:
                count += 1

        return count


def escape_rate(me_spd, opp_spd):  # return 값 1: 도망 성공, 0: 도망 실패
    if me_spd >= opp_spd:
        return 1
    else:
        a = me_spd
        b = (opp_spd // 4) % 256

        if b == 0:
            return 1

        f = a * 32 / b

        if f >= 255:
            return 1
        else:
            c = random.choice(list(range(0, 255)))

            if c <= f:
                return 1
            else:
                return 0


def hit(me, opp, mv):  # return 값 1: 명중, 0: 빗나감
    p = int(mv.acc)/100 * me.acc / opp.eva

    if p >= 1:
        return 1
    elif p <= 0:
        print("확률 error")
    else:
        return prob(p)


def use(who, num, user, p_user, user_mv_list, fli=0):  # flinch=1이면 풀죽음 고려
    message = []
    message2 = []
    message.append(user.name + "의 " + user_mv_list[num-1].name + "!")

    if user_mv_list[num - 1].cl1 == "1":
        if user_mv_list[num - 1].cl2 == "0" or user_mv_list[num - 1].cl2 == "2" or user_mv_list[num - 1].cl2 == "4" or user_mv_list[num - 1].cl2 == "7" or user_mv_list[num - 1].cl2 == "11" or user_mv_list[num - 1].cl2 == "13":
            # 13(선공기)일 때는 turn 함수에서 처리함

            if hit(user, p_user, user_mv_list[num - 1]) == 0:
                message.append("기술이 빗나갔다!")
                return [p_user.hp, 0, message]

            rt = cal_damage(user, p_user, user_mv_list[num - 1])
            damage = rt[0]
            message.extend(rt[1])
            old_hp = p_user.hp

            if p_user.hp - damage > 0:
                p_user.hp -= damage
            else:
                p_user.hp = 0

            return [p_user.hp, 1, message]

        elif user_mv_list[num - 1].cl2 == "1":

            if hit(user, p_user, user_mv_list[num - 1]) == 0:
                message.append("기술이 빗나갔다!")
                return [p_user.hp, 0, message]

            rt = cal_damage(user, p_user, user_mv_list[num - 1], 1)
            damage = rt[0]
            message.extend(rt[1])
            old_hp = p_user.hp

            if p_user.hp - damage > 0:
                p_user.hp -= damage
            else:
                p_user.hp = 0

            return [p_user.hp, 1, message]

        elif user_mv_list[num - 1].cl2 == "3":

            if hit(user, p_user, user_mv_list[num - 1]) == 0:
                message.append("기술이 빗나갔다!")
                return [p_user.hp, 0, message]

            if p_user.typ2 == 0:
                type_eff = eff[typ_re[user_mv_list[num - 1].typ] - 1][p_user.typ1 - 1]
            else:
                type_eff = eff[typ_re[user_mv_list[num - 1].typ] - 1][p_user.typ1 - 1] * \
                           eff[typ_re[user_mv_list[num - 1].typ] - 1][p_user.typ2 - 1]

            if type_eff == 0:
                message.append("효과가 없다...")
                damage = 0
            else:
                message.append("일격필살!")
                damage = p_user.hp

            old_hp = p_user.hp

            if p_user.hp - damage > 0:
                p_user.hp -= damage
            else:
                p_user.hp = 0

        elif user_mv_list[num - 1].cl2 == "5":

            if hit(user, p_user, user_mv_list[num - 1]) == 0:
                message.append("기술이 빗나갔다!")
                return [p_user.hp, 0, message]

            rt = cal_damage(user, p_user, user_mv_list[num - 1])
            damage = rt[0]
            message.extend(rt[1])
            old_hp = p_user.hp

            if p_user.hp - damage > 0:
                p_user.hp -= damage
            else:
                p_user.hp = 0

            if damage != 0 and p_user.hp > 0 and fli == 1:
                p = prob(flinch[int(user_mv_list[num - 1].no)])
                if p == 1:
                    return [p_user.hp, 1, message, 5]

            return [p_user.hp, 1, message]

        elif user_mv_list[num - 1].cl2 == "6":

            if hit(user, p_user, user_mv_list[num - 1]) == 0:
                message.append("기술이 빗나갔다!")
                return [p_user.hp, 0, message]

            rt = cal_damage(user, p_user, user_mv_list[num - 1])
            damage = rt[0]
            message.extend(rt[1])
            old_hp = p_user.hp

            if p_user.hp - damage > 0:
                p_user.hp -= damage
            else:
                p_user.hp = 0

            me_damage = floor(damage/4)
            me_old_hp = user.hp

            if user.hp - me_damage > 0:
                user.hp -= me_damage
            else:
                user.hp = 0

            message2.append("반동 데미지를 입었다!")

            return [p_user.hp, 1, message, [6, user.hp, message2]]

        elif user_mv_list[num - 1].cl2 == "8":

            if hit(user, p_user, user_mv_list[num - 1]) == 0:
                message.append("기술이 빗나갔다!")
                return [p_user.hp, 0, message]

            damage = move_1_8[int(user_mv_list[num - 1].no)]
            old_hp = p_user.hp

            if p_user.hp - damage > 0:
                p_user.hp -= damage
            else:
                p_user.hp = 0

            return [p_user.hp, 1, message]

        elif user_mv_list[num - 1].cl2 == "9":

            if hit(user, p_user, user_mv_list[num - 1]) == 0:
                message.append("기술이 빗나갔다!")
                return [p_user.hp, 0, message]

            rt = cal_damage(user, p_user, user_mv_list[num - 1])
            damage = rt[0]
            message.extend(rt[1])
            old_hp = p_user.hp

            if p_user.hp - damage > 0:
                p_user.hp -= damage
            else:
                p_user.hp = 0

            if p_user.hp > 0:
                if (prob(move_1_9[int(user_mv_list[num - 1].no)][2])) == 1:
                    if move_1_9[int(user_mv_list[num - 1].no)][0] == 1:
                        if p_user.rank_at == -6:
                            message2.append("아무 변화가 없다.")
                            return [p_user.hp, 1, message, [9, message2]]

                        p_user.rank_at += move_1_9[int(user_mv_list[num - 1].no)][1]

                        if p_user.rank_at <= -6:
                            p_user.rank_at = -6

                        p_user.at = import_info(p_user.no).at * rank1[p_user.rank_at]

                        if move_1_9[int(user_mv_list[num - 1].no)][1] == -2:
                            message2.append(p_user.name + "의 공격이 크게 떨어졌다.")
                        elif move_1_9[int(user_mv_list[num - 1].no)][1] == -1:
                            message2.append(p_user.name + "의 공격이 떨어졌다.")
                        else:
                            print("rank 변화가 1, 2가 아닌 값 error")

                    elif move_1_9[int(user_mv_list[num - 1].no)][0] == 2:
                        if p_user.rank_df == -6:
                            message2.append("아무 변화가 없다.")
                            return [p_user.hp, 1, message, [9, message2]]

                        p_user.rank_df += move_1_9[int(user_mv_list[num - 1].no)][1]

                        if p_user.rank_df <= -6:
                            p_user.rank_df = -6

                        p_user.df = import_info(p_user.no).df * rank1[p_user.rank_df]

                        if move_1_9[int(user_mv_list[num - 1].no)][1] == -2:
                            message2.append(p_user.name + "의 방어가 크게 떨어졌다.")
                        elif move_1_9[int(user_mv_list[num - 1].no)][1] == -1:
                            message2.append(p_user.name + "의 방어가 떨어졌다.")
                        else:
                            print("rank 변화가 1, 2가 아닌 값 error")

                    elif move_1_9[int(user_mv_list[num - 1].no)][0] == 3:
                        if p_user.rank_sp_at == -6:
                            message2.append("아무 변화가 없다.")
                            return [p_user.hp, 1, message, [9, message2]]

                        p_user.rank_sp_at += move_1_9[int(user_mv_list[num - 1].no)][1]

                        if p_user.rank_sp_at <= -6:
                            p_user.rank_sp_at = -6

                        p_user.sp_at = import_info(p_user.no).sp_at * rank1[p_user.rank_sp_at]

                        if move_1_9[int(user_mv_list[num - 1].no)][1] == -2:
                            message2.append(p_user.name + "의 특수공격이 크게 떨어졌다.")
                        elif move_1_9[int(user_mv_list[num - 1].no)][1] == -1:
                            message2.append(p_user.name + "의 특수공격이 떨어졌다.")
                        else:
                            print("rank 변화가 1, 2가 아닌 값 error")

                    elif move_1_9[int(user_mv_list[num - 1].no)][0] == 4:
                        if p_user.rank_sp_df == -6:
                            message2.append("아무 변화가 없다.")
                            return [p_user.hp, 1, message, [9, message2]]

                        p_user.rank_sp_df += move_1_9[int(user_mv_list[num - 1].no)][1]

                        if p_user.rank_sp_df <= -6:
                            p_user.rank_sp_df = -6

                        p_user.sp_df = import_info(p_user.no).sp_df * rank1[p_user.rank_sp_df]

                        if move_1_9[int(user_mv_list[num - 1].no)][1] == -2:
                            message2.append(p_user.name + "의 특수방어가 크게 떨어졌다.")
                        elif move_1_9[int(user_mv_list[num - 1].no)][1] == -1:
                            message2.append(p_user.name + "의 특수방어가 떨어졌다.")
                        else:
                            print("rank 변화가 1, 2가 아닌 값 error")

                    elif move_1_9[int(user_mv_list[num - 1].no)][0] == 5:
                        if p_user.rank_spd == -6:
                            message2.append("아무 변화가 없다.")
                            return [p_user.hp, 1, message, [9, message2]]

                        p_user.rank_spd += move_1_9[int(user_mv_list[num - 1].no)][1]

                        if p_user.rank_spd <= -6:
                            p_user.rank_spd = -6

                        p_user.spd = import_info(p_user.no).spd * rank1[p_user.rank_spd]

                        if move_1_9[int(user_mv_list[num - 1].no)][1] == -2:
                            message2.append(p_user.name + "의 스피드가 크게 떨어졌다.")
                        elif move_1_9[int(user_mv_list[num - 1].no)][1] == -1:
                            message2.append(p_user.name + "의 스피드가 떨어졌다.")
                        else:
                            print("rank 변화가 1, 2가 아닌 값 error")

                    else:
                        print("능력치 종류 error")

                return [p_user.hp, 1, message, [9, message2]]

            elif p_user.hp == 0:
                return [p_user.hp, 1, message]
            else:
                print("배틀 후 HP 에러")

        elif user_mv_list[num - 1].cl2 == "10":

            if hit(user, p_user, user_mv_list[num - 1]) == 0:
                message.append("기술이 빗나갔다!")

                me_damage = floor(user.hp/2)
                me_old_hp = user.hp
                user.hp -= me_damage

                message2.append("반동 데미지를 입었다!")

                return [p_user.hp, 0, message, [10, user.hp, message2]]

            damage = cal_damage(user, p_user, user_mv_list[num - 1])
            old_hp = p_user.hp

            if p_user.hp - damage > 0:
                p_user.hp -= damage
            else:
                p_user.hp = 0

            return [p_user.hp, 1, message]

        elif user_mv_list[num - 1].cl2 == "12":

            if hit(user, p_user, user_mv_list[num - 1]) == 0:
                message.append("기술이 빗나갔다!")
                return [p_user.hp, 0, message]

            rt = cal_damage(user, p_user, user_mv_list[num - 1])
            damage = rt[0]
            message.extend(rt[1])
            old_hp = p_user.hp

            if p_user.hp - damage > 0:
                p_user.hp -= damage
            else:
                p_user.hp = 0

            if p_user.hp > 0:

                max_hp = import_info(user.no).hp
                old_hp = user.hp

                if user.hp == max_hp:
                    message2.append("아무 변화가 없다.")
                    return [p_user.hp, 1, message, [12, user.hp, message2]]

                user.hp += ceil(damage * 1 / 2)

                if user.hp >= max_hp:
                    user.hp = max_hp

                message2.append(user.name + "가(이) HP를 회복했다!")

                return [p_user.hp, 1, message, [12, user.hp, message2]]

            elif p_user.hp == 0:
                return [p_user.hp, 1, message]
            else:
                print("배틀 후 HP 에러")

        elif user_mv_list[num - 1].cl2 == "14":

            rt = cal_damage(user, p_user, user_mv_list[num - 1])
            damage = rt[0]
            message.extend(rt[1])
            old_hp = p_user.hp

            if p_user.hp - damage > 0:
                p_user.hp -= damage
            else:
                p_user.hp = 0

            return [p_user.hp, 1, message]

        elif user_mv_list[num - 1].cl2 == "15":

            if hit(user, p_user, user_mv_list[num - 1]) == 0:
                message.append("기술이 빗나갔다!")
                return [p_user.hp, 0, message]

            damage = ceil(p_user.hp/2)
            old_hp = p_user.hp

            if p_user.hp - damage > 0:
                p_user.hp -= damage
            else:
                p_user.hp = 0

            return [p_user.hp, 1, message]

    elif user_mv_list[num - 1].cl1 == "2":
        if user_mv_list[num - 1].cl2 == "1":  # 명중률
            if user.rank_acc == 6:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            user.rank_acc += move_2[int(user_mv_list[num - 1].no)][1]

            if user.rank_acc >= 6:
                user.rank_acc = 6

            user.acc = rank2[user.rank_acc]

            if move_2[int(user_mv_list[num - 1].no)][1] == 2:
                message.append(user.name + "의 명중률이 크게 올라갔다.")
            elif move_2[int(user_mv_list[num - 1].no)][1] == 1:
                message.append(user.name + "의 명중률이 올라갔다.")
            else:
                print("rank 변화가 1, 2가 아닌 값 error")

            return [p_user.hp, 0, message]

        elif user_mv_list[num - 1].cl2 == "2":  # 공격
            if user.rank_at == 6:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            user.rank_at += move_2[int(user_mv_list[num - 1].no)][1]

            if user.rank_at >= 6:
                user.rank_at = 6

            user.at = import_info(user.no).at * rank1[user.rank_at]

            if move_2[int(user_mv_list[num - 1].no)][1] == 2:
                message.append(user.name + "의 공격이 크게 올라갔다.")
            elif move_2[int(user_mv_list[num - 1].no)][1] == 1:
                message.append(user.name + "의 공격이 올라갔다.")
            else:
                print("rank 변화가 1, 2가 아닌 값 error")

            return [p_user.hp, 0, message]

        elif user_mv_list[num - 1].cl2 == "3":  # 특수공격
            if user.rank_sp_at == 6:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            user.rank_sp_at += move_2[int(user_mv_list[num - 1].no)][1]

            if user.rank_sp_at >= 6:
                user.rank_sp_at = 6

            user.sp_at = import_info(user.no).sp_at * rank1[user.rank_sp_at]

            if move_2[int(user_mv_list[num - 1].no)][1] == 2:
                message.append(user.name + "의 특수공격이 크게 올라갔다.")
            elif move_2[int(user_mv_list[num - 1].no)][1] == 1:
                message.append(user.name + "의 특수공격이 올라갔다.")
            else:
                print("rank 변화가 1, 2가 아닌 값 error")

            return [p_user.hp, 0, message]

        elif user_mv_list[num - 1].cl2 == "4":  # 방어
            if user.rank_df == 6:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            user.rank_df += move_2[int(user_mv_list[num - 1].no)][1]

            if user.rank_df >= 6:
                user.rank_df = 6

            user.df = import_info(user.no).df * rank1[user.rank_df]

            if move_2[int(user_mv_list[num - 1].no)][1] == 2:
                message.append(user.name + "의 방어가 크게 올라갔다.")
            elif move_2[int(user_mv_list[num - 1].no)][1] == 1:
                message.append(user.name + "의 방어가 올라갔다.")
            else:
                print("rank 변화가 1, 2가 아닌 값 error")

            return [p_user.hp, 0, message]

        elif user_mv_list[num - 1].cl2 == "5":  # 특수방어
            if user.rank_sp_df == 6:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            user.rank_sp_df += move_2[int(user_mv_list[num - 1].no)][1]

            if user.rank_sp_df >= 6:
                user.rank_sp_df = 6

            user.sp_df = import_info(user.no).sp_df * rank1[user.rank_sp_df]

            if move_2[int(user_mv_list[num - 1].no)][1] == 2:
                message.append(user.name + "의 특수방어가 크게 올라갔다.")
            elif move_2[int(user_mv_list[num - 1].no)][1] == 1:
                message.append(user.name + "의 특수방어가 올라갔다.")
            else:
                print("rank 변화가 1, 2가 아닌 값 error")

            return [p_user.hp, 0, message]

        elif user_mv_list[num - 1].cl2 == "6":  # 스피드
            if user.rank_spd == 6:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            user.rank_spd += move_2[int(user_mv_list[num - 1].no)][1]

            if user.rank_spd >= 6:
                user.rank_spd = 6

            user.spd = import_info(user.no).spd * rank1[user.rank_spd]

            if move_2[int(user_mv_list[num - 1].no)][1] == 2:
                message.append(user.name + "의 스피드가 크게 올라갔다.")
            elif move_2[int(user_mv_list[num - 1].no)][1] == 1:
                message.append(user.name + "의 스피드가 올라갔다.")
            else:
                print("rank 변화가 1, 2가 아닌 값 error")

            return [p_user.hp, 0, message]

        elif user_mv_list[num - 1].cl2 == "7":  # 회피율
            if user.rank_eva == 6:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            user.rank_eva += move_2[int(user_mv_list[num - 1].no)][1]

            if user.rank_eva >= 6:
                user.rank_eva = 6

            user.eva = rank2[user.rank_eva]

            if move_2[int(user_mv_list[num - 1].no)][1] == 2:
                message.append(user.name + "의 회피율이 크게 올라갔다.")
            elif move_2[int(user_mv_list[num - 1].no)][1] == 1:
                message.append(user.name + "의 회피율이 올라갔다.")
            else:
                print("rank 변화가 1, 2가 아닌 값 error")

            return [p_user.hp, 0, message]

        elif user_mv_list[num - 1].cl2 == "8":  # HP (절반 회복)
            max_hp = import_info(user.no).hp
            old_hp = user.hp

            if user.hp == max_hp:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            user.hp += ceil(max_hp * 1/2)

            if user.hp >= max_hp:
                user.hp = max_hp

            message.append(user.name + "가(이) HP를 회복했다.")

            return [p_user.hp, 0, message, [28, user.hp]]

        else:
            print("cl2 값 에러")

    elif user_mv_list[num - 1].cl1 == "3":
        if user_mv_list[num - 1].cl2 == "1":  # 명중률
            if p_user.rank_acc == -6:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            p_user.rank_acc += move_3[int(user_mv_list[num - 1].no)][1]

            if p_user.rank_acc <= -6:
                p_user.rank_acc = -6

            p_user.acc = rank2[p_user.rank_acc]

            if move_3[int(user_mv_list[num - 1].no)][1] == -2:
                message.append(p_user.name + "의 명중률이 크게 떨어졌다.")
            elif move_3[int(user_mv_list[num - 1].no)][1] == -1:
                message.append(p_user.name + "의 명중률이 떨어졌다.")
            else:
                print("rank 변화가 1, 2가 아닌 값 error")

            return [p_user.hp, 0, message]

        elif user_mv_list[num - 1].cl2 == "2":  # 공격
            if p_user.rank_at == -6:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            p_user.rank_at += move_3[int(user_mv_list[num - 1].no)][1]

            if p_user.rank_at <= -6:
                p_user.rank_at = -6

            p_user.at = import_info(p_user.no).at * rank1[p_user.rank_at]

            if move_3[int(user_mv_list[num - 1].no)][1] == -2:
                message.append(p_user.name + "의 공격이 크게 떨어졌다.")
            elif move_3[int(user_mv_list[num - 1].no)][1] == -1:
                message.append(p_user.name + "의 공격이 떨어졌다.")
            else:
                print("rank 변화가 1, 2가 아닌 값 error")

            return [p_user.hp, 0, message]

        elif user_mv_list[num - 1].cl2 == "3":  # 특수공격
            if p_user.rank_sp_at == -6:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            p_user.rank_sp_at += move_3[int(user_mv_list[num - 1].no)][1]

            if p_user.rank_sp_at <= -6:
                p_user.rank_sp_at = -6

            p_user.sp_at = import_info(p_user.no).sp_at * rank1[p_user.rank_sp_at]

            if move_3[int(user_mv_list[num - 1].no)][1] == -2:
                message.append(p_user.name + "의 특수공격이 크게 떨어졌다.")
            elif move_3[int(user_mv_list[num - 1].no)][1] == -1:
                message.append(p_user.name + "의 특수공격이 떨어졌다.")
            else:
                print("rank 변화가 1, 2가 아닌 값 error")

            return [p_user.hp, 0, message]

        elif user_mv_list[num - 1].cl2 == "4":  # 방어
            if p_user.rank_df == -6:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            p_user.rank_df += move_3[int(user_mv_list[num - 1].no)][1]

            if p_user.rank_df <= -6:
                p_user.rank_df = -6

            p_user.df = import_info(p_user.no).df * rank1[p_user.rank_df]

            if move_3[int(user_mv_list[num - 1].no)][1] == -2:
                message.append(p_user.name + "의 방어가 크게 떨어졌다.")
            elif move_3[int(user_mv_list[num - 1].no)][1] == -1:
                message.append(p_user.name + "의 방어가 떨어졌다.")
            else:
                print("rank 변화가 1, 2가 아닌 값 error")

            return [p_user.hp, 0, message]

        elif user_mv_list[num - 1].cl2 == "5":  # 특수방어
            if p_user.rank_sp_df == -6:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            p_user.rank_sp_df += move_3[int(user_mv_list[num - 1].no)][1]

            if p_user.rank_sp_df <= -6:
                p_user.rank_sp_df = -6

            p_user.sp_df = import_info(p_user.no).sp_df * rank1[p_user.rank_sp_df]

            if move_3[int(user_mv_list[num - 1].no)][1] == -2:
                message.append(p_user.name + "의 특수방어가 크게 떨어졌다.")
            elif move_3[int(user_mv_list[num - 1].no)][1] == -1:
                message.append(p_user.name + "의 특수방어가 떨어졌다.")
            else:
                print("rank 변화가 1, 2가 아닌 값 error")

            return [p_user.hp, 0, message]

        elif user_mv_list[num - 1].cl2 == "6":  # 스피드
            if p_user.rank_spd == -6:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            p_user.rank_spd += move_3[int(user_mv_list[num - 1].no)][1]

            if p_user.rank_spd <= -6:
                p_user.rank_spd = -6

            p_user.spd = import_info(p_user.no).spd * rank1[p_user.rank_spd]

            if move_3[int(user_mv_list[num - 1].no)][1] == -2:
                message.append(p_user.name + "의 스피드가 크게 떨어졌다.")
            elif move_3[int(user_mv_list[num - 1].no)][1] == -1:
                message.append(p_user.name + "의 스피드가 떨어졌다.")
            else:
                print("rank 변화가 1, 2가 아닌 값 error")

            return [p_user.hp, 0, message]

        elif user_mv_list[num - 1].cl2 == "7":  # 회피율
            if p_user.rank_eva == -6:
                message.append("아무 변화가 없다.")
                return [p_user.hp, 0, message]

            p_user.rank_eva += move_3[int(user_mv_list[num - 1].no)][1]

            if p_user.rank_eva <= -6:
                p_user.rank_eva = -6

            p_user.eva = rank2[p_user.rank_eva]

            if move_3[int(user_mv_list[num - 1].no)][1] == -2:
                message.append(p_user.name + "의 회피율이 크게 떨어졌다.")
            elif move_3[int(user_mv_list[num - 1].no)][1] == -1:
                message.append(p_user.name + "의 회피율이 떨어졌다.")
            else:
                print("rank 변화가 1, 2가 아닌 값 error")

            return [p_user.hp, 0, message]

        else:
            print("cl2 값 에러")

    elif user_mv_list[num - 1].cl1 == "4":
        message.append("아무 일도 일어나지 않았다...")
        return [p_user.hp, 0, message]



