'''
运行调度
'''
from main import app
import fire_all_engine
from multiprocessing import Process

app.debug = True
process_list = []
#process_list.append(Process(target=app.run))
process_list.append(Process(target=fire_all_engine.emergency_smoke))
process_list.append(Process(target=fire_all_engine.emergency_mail))
process_list.append(Process(target=fire_all_engine.historiographer))


if __name__ == "__main__":
    #with open('1.txt','w') as f:
    #    f.write('df')
    #app.run()
    for i in process_list:
        i.start()
