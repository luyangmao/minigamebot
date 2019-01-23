import  time
import tools.minigame as minigame


def nullLoop():
    while True:
        data = yield (gr2,"空转一下")
        workLoop()



def workLoop():
    while True:
        data = yield (gr1,"判断投注")
        minigame.run()
        print('机器人 ', data)
        time.sleep(minigame.sleepCount)
        print('开始休眠 ', data)


gr1 = workLoop()
gr2 = nullLoop()
gr1.__next__()
gr2.__next__()


def do_mini():
    co, data = gr1, 'minigamebot开始'
    while True:
        co, data = co.send(data)
