import sys
from pockemon_ui import PockeMonGame
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QEventLoop, QTimer
from method import import_info, wild_pokemon, import_move, use, catch_rate, escape_rate
import random
from trainer import tr
from PyQt5.QtMultimedia import QSound

cmd = -1
printList = True
selected = ["num", "name"]
wild = -1
pick = -1
temp_me = -1
temp_opp = -1
me_max_hp = -1
opp_max_hp = -1
me_mv_list = []
opp_mv_list = []
rd = -1
ongoing = 0  # 1: 배틀 진행중, 0: 배틀 끝남
life = 3
battle_end = 0  # 1: 승리, 2: 패배, 3: 포획, 4: 도망, 0: 배틀 안 끝남
sound = None


def story(step, command):
    global printList, cmd, selected, wild, pick, temp_me, temp_opp, me_max_hp, opp_max_hp, me_mv_list, opp_mv_list, rd, gameStep, ongoing, life, battle_end, sound

    if step == 0:
        if command == 1:
            sound = QSound("./pokemon_music/opening.wav")
            sound.setLoops(QSound.Infinite)
            sound.play()

            pockeMonGame.addStory("")
            pockeMonGame.addStory("포켓몬의 세계에 오신 것을 환영합니다.")
            pockeMonGame.addStory("포켓몬 6마리를 잡아 포켓몬 마스터가 되십시오!")
            pockeMonGame.addStory("")
            pockeMonGame.addStory("이제 사용하실 포켓몬을 선택하셔야 합니다.")
            pockeMonGame.addStory("목록에 있는 포켓몬의 번호를 입력하면 해당 포켓몬에 대한 설명을 볼 수 있습니다.")
            pockeMonGame.addStory("")
            pockeMonGame.addStory("1: 포켓몬 목록 보기")

            gameStep = gameStep + 1
        elif command == 0:
            app.quit()

    elif step == 1:
        pockeMonGame.changeImage("./pokemon_image/monsterball.jpg")
        if printList:
            import csv
            with open('정보.csv', 'rt') as f:
                first_line = f.readline()
                reader = csv.reader(f, delimiter=',')
                no = 0
                pockeMonGame.addStatus("< 내 포켓몬 >")
                pockeMonGame.addMetList("<만난 포켓몬>")
                if len(tr) != 0:
                    for i in tr:
                        pockeMonGame.addStatus(import_info(i).name)

                pockeMonGame.addStory("포켓몬 목록 로딩 중.")
                delay(0.5)
                pockeMonGame.storyText.insertPlainText(".")
                delay(0.5)
                pockeMonGame.storyText.insertPlainText(".")
                delay(0.5)
                pockeMonGame.addStory("")
                monsterArray = []
                for row in reader:
                    monsterArray.append(row[0] + '. ' + row[1])

                order = []
                for monster in monsterArray:
                    order.append(monster)
                    no += 1
                    if no % 3 == 0:
                        rightMargin01 = 30
                        rightMargin02 = 30

                        rightMargin01 -= len(order[no-2])
                        rightMargin02 -= len(order[no-1])

                        monsterList = '{:>0} {:>' + str(rightMargin01) + '} {:>' + str(rightMargin02) + '}'
                        monsterList = monsterList.format(order[no-3], order[no-2], order[no-1])
                        pockeMonGame.addStory(monsterList + "\n")

                remainMonsterCount = no % 3
                if remainMonsterCount == 1:
                    monsterList = '{:>0}'.format(order[no-1])
                    pockeMonGame.addStory(monsterList + "\n")
                elif remainMonsterCount == 2:
                    monsterList = '{:>0} {:>20}'.format(order[no-2], order[no-1])
                    pockeMonGame.addStory(monsterList + "\n")

            f.close()
        gameStep = gameStep + 1

    elif step == 2:
        sel = cmd
        sel_po = import_info(sel)
        pockeMonGame.changeImage_pokemon("./pokemon_image/list/" + str(sel) + ".png")

        info_str = sel_po.get_info_move()
        selected[0] = info_str[0]
        selected[1] = info_str[1]

        pockeMonGame.addStory("")
        pockeMonGame.addStory("이름: " + info_str[1])
        pockeMonGame.addStory("타입: " + info_str[2])
        pockeMonGame.addStory("설명: " + info_str[3])
        pockeMonGame.addStory("")
        pockeMonGame.addStory("HP: " + str(info_str[4]))
        pockeMonGame.addStory("공격: " + str(info_str[5]))
        pockeMonGame.addStory("방어: " + str(info_str[6]))
        pockeMonGame.addStory("특수공격: " + str(info_str[7]))
        pockeMonGame.addStory("특수방어: " + str(info_str[8]))
        pockeMonGame.addStory("스피드: " + str(info_str[9]))
        pockeMonGame.addStory("")
        pockeMonGame.addStory("기술1: " + info_str[10])
        pockeMonGame.addStory("기술2: " + info_str[11])
        pockeMonGame.addStory("기술3: " + info_str[12])
        pockeMonGame.addStory("기술4: " + info_str[13])

        pockeMonGame.addStory("")
        pockeMonGame.addStory("1: 이 포켓몬으로 시작")
        pockeMonGame.addStory("0: 다른 포켓몬 선택")

        gameStep = gameStep + 1

    elif step == 3:
        if cmd == 1:
            pockeMonGame.changeImage("./pokemon_image/chose.gif")
            tr.append(selected[0])
            pockeMonGame.addSoundEffect("./pokemon_soundeffect/button.wav")
            pockeMonGame.addStory("")
            pockeMonGame.addStory(selected[1] + " 너로 정했다!")
            delay(1)
            pockeMonGame.addStatus(import_info(selected[0]).name)

            pockeMonGame.addStory("이제 야생 포켓몬들을 만나게 됩니다. 야생 포켓몬을 쓰러뜨리거나 몬스터볼을 던져서 잡으세요!")
            pockeMonGame.addStory("")
            pockeMonGame.addStory("1: 야생 포켓몬 만나러 가기")
            gameStep = gameStep + 1

        elif cmd == 0:
            pockeMonGame.addStory("")
            pockeMonGame.addStory("포켓몬 번호를 다시 입력해주세요.")
            printList = False
            gameStep = 1
            inputCommand("1", 0)

    elif step == 4:
        if len(tr) == 5:
            if sound.fileName() != "./pokemon_music/legend battle.wav":
                pockeMonGame.addSoundEffect("./pokemon_soundeffect/thunder.wav")
                sound.stop()
                sound = QSound("./pokemon_music/legend battle.wav")
                sound.setLoops(QSound.Infinite)
                sound.play()
            else:
                pockeMonGame.addSoundEffect("./pokemon_soundeffect/thunder.wav")

            pockeMonGame.changeImage("./pokemon_image/wild2.jpg")

        else:
            pockeMonGame.changeImage("./pokemon_image/wild.png")

        ongoing = 0
        battle_end = 0
        wild = wild_pokemon(6 - len(tr))
        temp = import_info(wild)
        pockeMonGame.addStory("")
        pockeMonGame.addStory(".")
        delay(0.5)
        pockeMonGame.storyText.insertPlainText(".")
        delay(0.5)
        pockeMonGame.storyText.insertPlainText(".")
        delay(0.5)
        pockeMonGame.storyText.insertPlainText("앗! 야생 " + temp.name + "가(이) 튀어나왔다!")

        delay(1)
        pockeMonGame.addMetList(temp.name)
        pockeMonGame.addStory("")
        pockeMonGame.addStory("내보낼 포켓몬을 선택해주세요.")
        pockeMonGame.addStory("(번호 + 10: 해당 포켓몬 정보 조회)")
        pockeMonGame.addStory("(0: 야생 포켓몬 정보 조회)")
        pockeMonGame.addStory("")
        for i in range(len(tr)):
            pockeMonGame.addStory(str(i+1) + ". " + import_info(tr[i]).name)
        gameStep = gameStep + 1

    elif step == 5:
        pockeMonGame.changeImage("./pokemon_image/battle.png")
        if ongoing == 1:
            pockeMonGame.addStory("")
            pockeMonGame.addStory(temp_me.name)
            pockeMonGame.addStory("HP: " + str(temp_me.hp) + "/" + str(me_max_hp))
            pockeMonGame.addStory(temp_opp.name)
            pockeMonGame.addStory("HP: " + str(temp_opp.hp) + "/" + str(opp_max_hp))
            pockeMonGame.addStory("")
            pockeMonGame.addStory("1. 싸운다.")
            pockeMonGame.addStory("2. 몬스터볼을 던진다.")
            pockeMonGame.addStory("3. 도망간다.")

            gameStep = gameStep + 1
        else:
            if cmd in range(1, len(tr) + 1):
                pick = tr[cmd-1]
                temp_me = import_info(pick)
                temp_opp = import_info(wild)
                me_max_hp = temp_me.hp
                opp_max_hp = temp_opp.hp

                me_mv_list = []
                opp_mv_list = []

                me_mv_list.append(import_move(temp_me.mv1))
                me_mv_list.append(import_move(temp_me.mv2))
                me_mv_list.append(import_move(temp_me.mv3))
                me_mv_list.append(import_move(temp_me.mv4))
                opp_mv_list.append(import_move(temp_opp.mv1))
                opp_mv_list.append(import_move(temp_opp.mv2))
                opp_mv_list.append(import_move(temp_opp.mv3))
                opp_mv_list.append(import_move(temp_opp.mv4))

                pockeMonGame.addSoundEffect("./pokemon_soundeffect/pokemon out.wav")
                pockeMonGame.addStory("")
                pockeMonGame.addStory("나와라 " + temp_me.name + "!")
                delay(1)

                pockeMonGame.addStory("")
                pockeMonGame.addStory(temp_me.name)
                pockeMonGame.addStory("HP: " + str(temp_me.hp) + "/" + str(me_max_hp))
                pockeMonGame.addStory(temp_opp.name)
                pockeMonGame.addStory("HP: " + str(temp_opp.hp) + "/" + str(opp_max_hp))
                pockeMonGame.addStory("")
                pockeMonGame.addStory("1. 싸운다.")
                pockeMonGame.addStory("2. 몬스터볼을 던진다.")
                pockeMonGame.addStory("3. 도망간다.")

                gameStep = gameStep + 1

            elif cmd in range(11, len(tr) + 11):
                info_str = import_info(tr[cmd - 11]).get_info_move()
                pockeMonGame.addStory("")
                pockeMonGame.addStory("이름: " + info_str[1])
                pockeMonGame.addStory("타입: " + info_str[2])
                pockeMonGame.addStory("설명: " + info_str[3])
                pockeMonGame.addStory("")
                pockeMonGame.addStory("HP: " + str(info_str[4]))
                pockeMonGame.addStory("공격: " + str(info_str[5]))
                pockeMonGame.addStory("방어: " + str(info_str[6]))
                pockeMonGame.addStory("특수공격: " + str(info_str[7]))
                pockeMonGame.addStory("특수방어: " + str(info_str[8]))
                pockeMonGame.addStory("스피드: " + str(info_str[9]))
                pockeMonGame.addStory("")
                pockeMonGame.addStory("기술1: " + info_str[10])
                pockeMonGame.addStory("기술2: " + info_str[11])
                pockeMonGame.addStory("기술3: " + info_str[12])
                pockeMonGame.addStory("기술4: " + info_str[13])
                pockeMonGame.addStory("")
                pockeMonGame.addStory("내보낼 포켓몬을 선택해주세요.")
                pockeMonGame.addStory("(번호 + 10: 해당 포켓몬 정보 조회)")
                pockeMonGame.addStory("(0: 야생 포켓몬 정보 조회)")
                pockeMonGame.addStory("")
                for i in range(len(tr)):
                    pockeMonGame.addStory(str(i + 1) + ". " + import_info(tr[i]).name)

            elif cmd == 0:
                info_str = import_info(wild).get_info_move()
                pockeMonGame.addStory("")
                pockeMonGame.addStory("이름: " + info_str[1])
                pockeMonGame.addStory("타입: " + info_str[2])
                pockeMonGame.addStory("설명: " + info_str[3])
                pockeMonGame.addStory("")
                pockeMonGame.addStory("HP: " + str(info_str[4]))
                pockeMonGame.addStory("공격: " + str(info_str[5]))
                pockeMonGame.addStory("방어: " + str(info_str[6]))
                pockeMonGame.addStory("특수공격: " + str(info_str[7]))
                pockeMonGame.addStory("특수방어: " + str(info_str[8]))
                pockeMonGame.addStory("스피드: " + str(info_str[9]))
                pockeMonGame.addStory("")
                pockeMonGame.addStory("기술1: " + info_str[10])
                pockeMonGame.addStory("기술2: " + info_str[11])
                pockeMonGame.addStory("기술3: " + info_str[12])
                pockeMonGame.addStory("기술4: " + info_str[13])
                pockeMonGame.addStory("")
                pockeMonGame.addStory("내보낼 포켓몬을 선택해주세요.")
                pockeMonGame.addStory("(번호 + 10: 해당 포켓몬 정보 조회)")
                pockeMonGame.addStory("(0: 야생 포켓몬 정보 조회)")
                pockeMonGame.addStory("")
                for i in range(len(tr)):
                    pockeMonGame.addStory(str(i + 1) + ". " + import_info(tr[i]).name)

    elif step == 6:
        rd = random.choice(list(range(1, 5)))
        if cmd == 1:
            pockeMonGame.addStory("")
            pockeMonGame.addStory("기술1: " + temp_me.mv1)
            pockeMonGame.addStory("기술2: " + temp_me.mv2)
            pockeMonGame.addStory("기술3: " + temp_me.mv3)
            pockeMonGame.addStory("기술4: " + temp_me.mv4)
            pockeMonGame.addStory("")
            pockeMonGame.addStory("사용할 기술을 선택하십시오.")
            pockeMonGame.addStory("(번호 + 10: 해당 기술 정보 조회)")

            gameStep = gameStep + 1

        elif cmd == 2:
            while True:
                pockeMonGame.addStory("")
                pockeMonGame.addStory("가랏! 몬스터볼!")
                cr = catch_rate(opp_max_hp, temp_opp.hp, temp_opp.tot)

                if cr <= 3:
                    old_hp_opp = temp_opp.hp
                    old_hp_me = temp_me.hp

                    for i in range(cr):
                        delay(2)
                        pockeMonGame.addStory("..흔들..")
                    delay(1)
                    pockeMonGame.addStory("앗! 야생 " + temp_opp.name + "가(이) 몬스터볼에서 튀어나왔다!")

                    delay(1)

                    # 상대 공격 차례
                    pockeMonGame.addStory("")
                    rt = use(1, rd, temp_opp, temp_me, opp_mv_list, 0)
                    for i in rt[2]:
                        pockeMonGame.addStory(i)
                        delay(1)
                    if rt[1] == 1:
                        show_hp(temp_me.name, old_hp_me, temp_me.hp)

                    if temp_me.hp == 0:
                        pockeMonGame.addStory(temp_me.name + "가(이) 쓰러졌다!")  # 패배
                        battle_end = 2
                        break

                    if len(rt) == 4:
                        if rt[3] == 5:
                            pockeMonGame.addStory(temp_me.name + "는(은) 풀이 죽어 움직일 수 없다!")
                            flinch = 1
                        elif rt[3][0] == 6 or rt[3][0] == 10 or rt[3][0] == 12:
                            for i in rt[3][2]:
                                pockeMonGame.addStory(i)
                                delay(1)
                            show_hp(temp_opp.name, old_hp_opp, temp_opp.hp)
                        elif rt[3][0] == 9:
                            for i in rt[3][1]:
                                pockeMonGame.addStory(i)
                                delay(1)
                        elif rt[3][0] == 28:
                            show_hp(temp_opp.name, old_hp_opp, temp_opp.hp)
                        else:
                            print("rt값 에러")

                    if temp_opp.hp == 0:
                        pockeMonGame.addStory(temp_opp.name + "가(이) 쓰러졌다!")  # 승리
                        battle_end = 1
                        break

                elif cr == 4:
                    for i in range(3):
                        delay(2)
                        pockeMonGame.addStory("..흔들..")
                    delay(1)
                    pockeMonGame.addSoundEffect("./pokemon_soundeffect/gotcha.wav")
                    pockeMonGame.addStory("야생 " + temp_opp.name + "를(을) 잡았다!")
                    delay(1)
                    pockeMonGame.addStatus(temp_opp.name)
                    pockeMonGame.addStory(temp_opp.name + " 넌 내꺼야!")
                    tr.append(temp_opp.no)
                    battle_end = 3
                    break
                elif cr == 5:
                    delay(1)
                    pockeMonGame.addSoundEffect("./pokemon_soundeffect/gotcha.wav")
                    pockeMonGame.addStory("야생 " + temp_opp.name + "를(을) 잡았다!")
                    delay(1)
                    pockeMonGame.addStatus(temp_opp.name)
                    pockeMonGame.addStory(temp_opp.name + " 넌 내꺼야!")
                    tr.append(temp_opp.no)
                    battle_end = 3
                    break
                else:
                    print("catch_rate return 값 에러")

                break

            if battle_end == 1:
                delay(1)
                pockeMonGame.changeImage("./pokemon_image/win.gif")
                pockeMonGame.addStory("")
                pockeMonGame.addStory("배틀에서 승리했습니다. 게임을 계속하시겠습니까?")
                pockeMonGame.addStory("1: 게임 계속")
                pockeMonGame.addStory("0: 게임 종료")
                gameStep = 99
            elif battle_end == 2:
                delay(1)
                pockeMonGame.changeImage("./pokemon_image/lose.jpg")
                life -= 1
                if life == 0:
                    pockeMonGame.addStory("")
                    pockeMonGame.addStory("배틀에서 패배했습니다. 라이프를 모두 사용하여 게임이 종료됩니다.")
                    pockeMonGame.addStory("5초 후 창이 닫힙니다.")
                    delay(5)
                    sound.stop()
                    exit()
                pockeMonGame.addStory("")
                pockeMonGame.addStory("배틀에서 패배했습니다. 게임을 계속하시겠습니까? (라이프: " + str(life) + "/3)")
                pockeMonGame.addStory("1: 게임 계속")
                pockeMonGame.addStory("0: 게임 종료")
                gameStep = 99
            elif battle_end == 3:
                delay(1)
                if len(tr) == 6:
                    delay(0.5)
                    pockeMonGame.addSoundEffect("./pokemon_soundeffect/button.wav")
                    sound.stop()
                    sound = QSound("./pokemon_music/ending.wav")
                    sound.setLoops(QSound.Infinite)
                    sound.play()
                    delay(0.5)

                    pockeMonGame.changeImage("./pokemon_image/master2.jpg")
                    pockeMonGame.addStory("")
                    pockeMonGame.addStory("축하합니다! 6마리의 포켓몬을 모두 잡아 포켓몬 마스터가 되었습니다!")
                    delay(20)
                    sound.stop()
                    exit()
                pockeMonGame.changeImage("./pokemon_image/catch.png")
                pockeMonGame.addStory("")
                pockeMonGame.addStory("새로운 포켓몬을 잡았습니다. 게임을 계속하시겠습니까?")
                pockeMonGame.addStory("1: 게임 계속")
                pockeMonGame.addStory("0: 게임 종료")
                gameStep = 99
            elif battle_end == 4:
                delay(1)
                pockeMonGame.changeImage("./pokemon_image/escape.jpg")
                pockeMonGame.addStory("")
                pockeMonGame.addStory("배틀에서 도망쳤습니다. 게임을 계속하시겠습니까?")
                pockeMonGame.addStory("1: 게임 계속")
                pockeMonGame.addStory("0: 게임 종료")
                gameStep = 99
            else:  # 0인 경우
                ongoing = 1
                gameStep = 5
                inputCommand("1", 0)

        elif cmd == 3:
            while True:
                e = escape_rate(temp_me.spd, temp_opp.spd)
                if e == 0:
                    old_hp_opp = temp_opp.hp
                    old_hp_me = temp_me.hp

                    pockeMonGame.addStory("")
                    pockeMonGame.addStory("도망치는데 실패했다!")

                    delay(1)

                    # 상대 공격 차례
                    pockeMonGame.addStory("")
                    rt = use(1, rd, temp_opp, temp_me, opp_mv_list, 0)
                    for i in rt[2]:
                        pockeMonGame.addStory(i)
                        delay(1)
                    if rt[1] == 1:
                        show_hp(temp_me.name, old_hp_me, temp_me.hp)

                    if temp_me.hp == 0:
                        pockeMonGame.addStory(temp_me.name + "가(이) 쓰러졌다!")  # 패배
                        battle_end = 2
                        break

                    if len(rt) == 4:
                        if rt[3] == 5:
                            pockeMonGame.addStory(temp_me.name + "는(은) 풀이 죽어 움직일 수 없다!")
                            flinch = 1
                        elif rt[3][0] == 6 or rt[3][0] == 10 or rt[3][0] == 12:
                            for i in rt[3][2]:
                                pockeMonGame.addStory(i)
                                delay(1)
                            show_hp(temp_opp.name, old_hp_opp, temp_opp.hp)

                        elif rt[3][0] == 9:
                            for i in rt[3][1]:
                                pockeMonGame.addStory(i)
                                delay(1)
                        elif rt[3][0] == 28:
                            show_hp(temp_opp.name, old_hp_opp, temp_opp.hp)
                        else:
                            print("rt값 에러")

                    if temp_opp.hp == 0:
                        pockeMonGame.addStory(temp_opp.name + "가(이) 쓰러졌다!")  # 승리
                        battle_end = 1
                        break
                elif e == 1:
                    pockeMonGame.addSoundEffect("./pokemon_soundeffect/escape.wav")
                    pockeMonGame.addStory("")
                    pockeMonGame.addStory("무사히 도망쳤다!")
                    battle_end = 4
                    break
                else:
                    print("escape_rate return 값 에러")

                break

            if battle_end == 1:
                delay(1)
                pockeMonGame.changeImage("./pokemon_image/win.gif")
                pockeMonGame.addStory("")
                pockeMonGame.addStory("배틀에서 승리했습니다. 게임을 계속하시겠습니까?")
                pockeMonGame.addStory("1: 게임 계속")
                pockeMonGame.addStory("0: 게임 종료")
                gameStep = 99
            elif battle_end == 2:
                delay(1)
                pockeMonGame.changeImage("./pokemon_image/lose.jpg")
                life -= 1
                if life == 0:
                    pockeMonGame.addStory("")
                    pockeMonGame.addStory("배틀에서 패배했습니다. 라이프를 모두 사용하여 게임이 종료됩니다.")
                    pockeMonGame.addStory("5초 후 창이 닫힙니다.")
                    delay(5)
                    sound.stop()
                    exit()
                pockeMonGame.addStory("")
                pockeMonGame.addStory("배틀에서 패배했습니다. 게임을 계속하시겠습니까? (라이프: " + str(life) + "/3)")
                pockeMonGame.addStory("1: 게임 계속")
                pockeMonGame.addStory("0: 게임 종료")
                gameStep = 99
            elif battle_end == 3:
                delay(1)
                if len(tr) == 6:
                    pockeMonGame.changeImage("./pokemon_image/master2.jpg")
                    pockeMonGame.addStory("")
                    pockeMonGame.addStory("축하합니다! 6마리의 포켓몬을 모두 잡아 포켓몬 마스터가 되었습니다!")
                    delay(20)
                    sound.stop()
                    exit()
                pockeMonGame.changeImage("./pokemon_image/catch.png")
                pockeMonGame.addStory("")
                pockeMonGame.addStory("새로운 포켓몬을 잡았습니다. 게임을 계속하시겠습니까?")
                pockeMonGame.addStory("1: 게임 계속")
                pockeMonGame.addStory("0: 게임 종료")
                gameStep = 99
            elif battle_end == 4:
                delay(1)
                pockeMonGame.changeImage("./pokemon_image/escape.jpg")
                pockeMonGame.addStory("")
                pockeMonGame.addStory("배틀에서 도망쳤습니다. 게임을 계속하시겠습니까?")
                pockeMonGame.addStory("1: 게임 계속")
                pockeMonGame.addStory("0: 게임 종료")
                gameStep = 99
            else:  # 0인 경우
                ongoing = 1
                gameStep = 5
                inputCommand("1", 0)

    elif step == 7:  # 싸운다
        me_first = -1
        flinch = 0
        if cmd in range(1, 5):
            while True:
                if (me_mv_list[cmd - 1].cl1 == "1" and me_mv_list[cmd - 1].cl2 == "13") and (opp_mv_list[rd - 1].cl1 == "1" and opp_mv_list[rd - 1].cl2 == "13"):  # 둘 다 선공기
                    if temp_me.spd >= temp_opp.spd:
                        me_first = True
                    else:
                        me_first = False
                elif (me_mv_list[cmd - 1].cl1 == "1" and me_mv_list[cmd - 1].cl2 == "13") and not (opp_mv_list[rd - 1].cl1 == "1" and opp_mv_list[rd - 1].cl2 == "13"):  # 나만 선공기
                    me_first = True
                elif not (me_mv_list[cmd - 1].cl1 == "1" and me_mv_list[cmd - 1].cl2 == "13") and (opp_mv_list[rd - 1].cl1 == "1" and opp_mv_list[rd - 1].cl2 == "13"):  # 상대만 선공기
                    me_first = False
                else:  # 둘 다 선공기 x
                    if temp_me.spd >= temp_opp.spd:
                        me_first = True
                    else:
                        me_first = False

                if me_first == True:  # 선공
                    old_hp_opp = temp_opp.hp
                    old_hp_me = temp_me.hp

                    # 내 공격 차례
                    rt = use(0, cmd, temp_me, temp_opp, me_mv_list, 1)
                    for i in rt[2]:
                        pockeMonGame.addStory(i)
                        delay(1)
                    if rt[1] == 1:
                        show_hp(temp_opp.name, old_hp_opp, temp_opp.hp)

                    if temp_opp.hp == 0:
                        pockeMonGame.addStory(temp_opp.name + "가(이) 쓰러졌다!")  # 승리
                        battle_end = 1
                        break

                    if len(rt) == 4:
                        if rt[3] == 5:
                            pockeMonGame.addStory(temp_opp.name + "는(은) 풀이 죽어 움직일 수 없다!")
                            flinch = 1
                        elif rt[3][0] == 6 or rt[3][0] == 10 or rt[3][0] == 12:
                            for i in rt[3][2]:
                                pockeMonGame.addStory(i)
                                delay(1)
                            show_hp(temp_me.name, old_hp_me, temp_me.hp)
                        elif rt[3][0] == 9:
                            for i in rt[3][1]:
                                pockeMonGame.addStory(i)
                                delay(1)
                        elif rt[3][0] == 28:
                            show_hp(temp_me.name, old_hp_me, temp_me.hp)
                        else:
                            print("rt값 에러")

                    if temp_me.hp == 0:
                        pockeMonGame.addStory(temp_me.name + "가(이) 쓰러졌다!")  # 패배
                        battle_end = 2
                        break

                    if flinch == 1:
                        break

                    delay(1)

                    # 상대 공격 차례
                    pockeMonGame.addStory("")
                    rt = use(1, rd, temp_opp, temp_me, opp_mv_list, 0)
                    for i in rt[2]:
                        pockeMonGame.addStory(i)
                        delay(1)
                    if rt[1] == 1:
                        show_hp(temp_me.name, old_hp_me, temp_me.hp)

                    if temp_me.hp == 0:
                        pockeMonGame.addStory(temp_me.name + "가(이) 쓰러졌다!")  # 패배
                        battle_end = 2
                        break

                    if len(rt) == 4:
                        if rt[3] == 5:
                            pockeMonGame.addStory(temp_me.name + "는(은) 풀이 죽어 움직일 수 없다!")
                            flinch = 1
                        elif rt[3][0] == 6 or rt[3][0] == 10 or rt[3][0] == 12:
                            for i in rt[3][2]:
                                pockeMonGame.addStory(i)
                                delay(1)
                            show_hp(temp_opp.name, old_hp_opp, temp_opp.hp)
                        elif rt[3][0] == 9:
                            for i in rt[3][1]:
                                pockeMonGame.addStory(i)
                                delay(1)
                        elif rt[3][0] == 28:
                            show_hp(temp_opp.name, old_hp_opp, temp_opp.hp)
                        else:
                            print("rt값 에러")

                    if temp_opp.hp == 0:
                        pockeMonGame.addStory(temp_opp.name + "가(이) 쓰러졌다!")  # 승리
                        battle_end = 1
                        break

                elif me_first == False:  # 후공
                    old_hp_opp = temp_opp.hp
                    old_hp_me = temp_me.hp

                    # 상대 공격 차례
                    rt = use(1, rd, temp_opp, temp_me, opp_mv_list, 1)
                    for i in rt[2]:
                        pockeMonGame.addStory(i)
                        delay(1)
                    if rt[1] == 1:
                        show_hp(temp_me.name, old_hp_me, temp_me.hp)

                    if temp_me.hp == 0:
                        pockeMonGame.addStory(temp_me.name + "가(이) 쓰러졌다!")  # 패배
                        battle_end = 2
                        break

                    if len(rt) == 4:
                        if rt[3] == 5:
                            pockeMonGame.addStory(temp_me.name + "는(은) 풀이 죽어 움직일 수 없다!")
                            flinch = 1
                        elif rt[3][0] == 6 or rt[3][0] == 10 or rt[3][0] == 12:
                            for i in rt[3][2]:
                                pockeMonGame.addStory(i)
                                delay(1)
                            show_hp(temp_opp.name, old_hp_opp, temp_opp.hp)
                        elif rt[3][0] == 9:
                            for i in rt[3][1]:
                                pockeMonGame.addStory(i)
                                delay(1)
                        elif rt[3][0] == 28:
                            show_hp(temp_opp.name, old_hp_opp, temp_opp.hp)
                        else:
                            print("rt값 에러")

                    if temp_opp.hp == 0:
                        pockeMonGame.addStory(temp_opp.name + "가(이) 쓰러졌다!")  # 승리
                        battle_end = 1
                        break

                    if flinch == 1:
                        break

                    delay(1)

                    # 내 공격 차례
                    pockeMonGame.addStory("")
                    rt = use(0, cmd, temp_me, temp_opp, me_mv_list, 0)
                    for i in rt[2]:
                        pockeMonGame.addStory(i)
                        delay(1)
                    if rt[1] == 1:
                        show_hp(temp_opp.name, old_hp_opp, temp_opp.hp)

                    if temp_opp.hp == 0:
                        pockeMonGame.addStory(temp_opp.name + "가(이) 쓰러졌다!")  # 승리
                        battle_end = 1
                        break

                    if len(rt) == 4:
                        if rt[3] == 5:
                            pockeMonGame.addStory(temp_opp.name + "는(은) 풀이 죽어 움직일 수 없다!")
                            flinch = 1
                        elif rt[3][0] == 6 or rt[3][0] == 10 or rt[3][0] == 12:
                            for i in rt[3][2]:
                                pockeMonGame.addStory(i)
                                delay(1)
                            show_hp(temp_me.name, old_hp_me, temp_me.hp)
                        elif rt[3][0] == 9:
                            for i in rt[3][1]:
                                pockeMonGame.addStory(i)
                                delay(1)
                        elif rt[3][0] == 28:
                            show_hp(temp_me.name, old_hp_me, temp_me.hp)
                        else:
                            print("rt값 에러")

                    if temp_me.hp == 0:
                        pockeMonGame.addStory(temp_me.name + "가(이) 쓰러졌다!")  # 패배
                        battle_end = 2
                        break

                else:
                    print("me_first 값 에러")

                break

            if battle_end == 1:
                delay(1)
                pockeMonGame.changeImage("./pokemon_image/win.gif")
                pockeMonGame.addStory("")
                pockeMonGame.addStory("배틀에서 승리했습니다. 게임을 계속하시겠습니까?")
                pockeMonGame.addStory("1: 게임 계속")
                pockeMonGame.addStory("0: 게임 종료")
                gameStep = 99
            elif battle_end == 2:
                delay(1)
                pockeMonGame.changeImage("./pokemon_image/lose.jpg")
                life -= 1
                if life == 0:
                    pockeMonGame.addStory("")
                    pockeMonGame.addStory("배틀에서 패배했습니다. 라이프를 모두 사용하여 게임이 종료됩니다.")
                    pockeMonGame.addStory("5초 후 창이 닫힙니다.")
                    delay(5)
                    sound.stop()
                    exit()
                pockeMonGame.addStory("")
                pockeMonGame.addStory("배틀에서 패배했습니다. 게임을 계속하시겠습니까? (라이프: " + str(life) + "/3)")
                pockeMonGame.addStory("1: 게임 계속")
                pockeMonGame.addStory("0: 게임 종료")
                gameStep = 99
            elif battle_end == 3:
                delay(1)
                if len(tr) == 6:
                    pockeMonGame.changeImage("./pokemon_image/master2.jpg")
                    pockeMonGame.addStory("")
                    pockeMonGame.addStory("축하합니다! 6마리의 포켓몬을 모두 잡아 포켓몬 마스터가 되었습니다!")
                    delay(20)
                    sound.stop()
                    exit()
                pockeMonGame.changeImage("./pokemon_image/catch.png")
                pockeMonGame.addStory("")
                pockeMonGame.addStory("새로운 포켓몬을 잡았습니다. 게임을 계속하시겠습니까?")
                pockeMonGame.addStory("1: 게임 계속")
                pockeMonGame.addStory("0: 게임 종료")
                gameStep = 99
            elif battle_end == 4:
                delay(1)
                pockeMonGame.changeImage("./pokemon_image/escape.jpg")
                pockeMonGame.addStory("")
                pockeMonGame.addStory("배틀에서 도망쳤습니다. 게임을 계속하시겠습니까?")
                pockeMonGame.addStory("1: 게임 계속")
                pockeMonGame.addStory("0: 게임 종료")
                gameStep = 99
            else:  # 0인 경우
                ongoing = 1
                gameStep = 5
                inputCommand("1", 0)

        elif cmd in range(11, 15):
            pockeMonGame.addStory("")
            pockeMonGame.addStory("이름: " + me_mv_list[cmd-11].name)
            pockeMonGame.addStory("타입: " + me_mv_list[cmd - 11].typ)
            pockeMonGame.addStory("분류: " + me_mv_list[cmd - 11].cate)
            pockeMonGame.addStory("위력: " + me_mv_list[cmd - 11].power)
            pockeMonGame.addStory("명중률: " + me_mv_list[cmd - 11].acc)
            pockeMonGame.addStory("설명: " + me_mv_list[cmd - 11].exp)
            pockeMonGame.addStory("")
            pockeMonGame.addStory("사용할 기술을 선택하십시오.")
            pockeMonGame.addStory("(번호 + 10: 해당 기술 정보 조회)")

    elif step == 99:  # end step
        if cmd == 1:
            gameStep = 4
            inputCommand("1", 0)
        elif cmd == 0:
            pockeMonGame.changeImage("./pokemon_image/bye.png")
            pockeMonGame.addStory("수고하셨습니다!")
            pockeMonGame.addStory("5초 후 창이 닫힙니다.")
            delay(5)
            sound.stop()
            exit()
        else:
            print("cmd 값 에러")


def inputCommand(inputCommand, print = 1):
    if inputCommand == "":
        return -1

    outOfRange = False
    try:
        command = int(inputCommand)
        if checkRange(command) :
            outOfRange = True
            raise ValueError("")
        if print == 1:
            # pockeMonGame.addStory("입력된 명령어 : {inputCommand}".format(inputCommand=inputCommand))
            pass
        global cmd
        cmd = int(inputCommand)
        story(gameStep, command)
    except(ValueError):
        errorMsg = ""
        if outOfRange:
            errorMsg = "명령어의 범위를 넘어섰습니다. 다시 입력해주세요."
        else:
            errorMsg = "숫자(정수)만 입력 가능합니다. 다시 입력해주세요."
        pockeMonGame.addStory(errorMsg)
    finally:        
        pockeMonGame.clearCommandEdit()


def checkRange(value):  # out of range일 때 1 return
    if gameStep == 0:
        if value == 0 or value == 1:
            return 0
        else:
            return 1
    elif gameStep == 1:
        if value == 1:
            return 0
        else:
            return 1
    elif gameStep == 2:
        if 1 <= value <= 151:
            return 0
        else:
            return 1
    elif gameStep == 3:
        if value == 0 or value == 1:
            return 0
        else:
            return 1
    elif gameStep == 4:
        if value == 1:
            return 0
        else:
            return 1
    elif gameStep == 5:
        if value in range(1, len(tr) + 1) or value in range(11, len(tr) + 11) or value == 0:
            return 0
        else:
            return 1
    elif gameStep == 6:
        if value in range(1, 4):
            return 0
        else:
            return 1
    elif gameStep == 7:
        if value in range(1, 5) or value in range(11, 15):
            return 0
        else:
            return 1
    elif gameStep == 99:
        if value == 0 or value == 1:
            return 0
        else:
            return 1


def delay(sec):
    loop = QEventLoop()
    QTimer.singleShot(sec*1000, loop.quit)
    loop.exec_()


def show_hp(pokemon_name, old_hp, new_hp):
    if old_hp > new_hp:
        pockeMonGame.addSoundEffect("./pokemon_soundeffect/hit.wav")
        delay(0.7)
    pockeMonGame.addStory(pokemon_name + " HP: " + str(old_hp))
    delay(0.5)
    pockeMonGame.storyText.insertPlainText(' -> ')
    delay(0.5)
    pockeMonGame.storyText.insertPlainText(str(new_hp))
    delay(0.5)


if __name__ == "__main__":
    pockeMonGame = None
    gameStep = 0

    app = QApplication(sys.argv)
    pockeMonGame = PockeMonGame()
    pockeMonGame.show()
    pockeMonGame.setCallBack(inputCommand)
    pockeMonGame.inputCmdEdit.setFocus()

    pockeMonGame.addStory("===================== Welcome! =====================")
    pockeMonGame.addStory("1 : 게임 시작")
    pockeMonGame.addStory("0 : 게임 종료")

    exit(app.exec_())