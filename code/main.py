from my_spa import *
import time
class system:
    def __init__(self): # True represents stopped, extended, retracted
        self.conveyor = True
        self.barrier = True
        self.sorting_1 = True
        self.sorting_2 = True
        self.chute_3 = 0 # black,barrier
        self.chute_2 = 0 # metallic, sorting_2
        self.chute_1 = 0 # red, sorting_1
        self.max = 3
    def restart(self):
        time.sleep(1)
        print("Set the machine to the initial position.")
        self.conveyor = True
        self.barrier = True
        self.sorting_1 = True
        self.sorting_2 = True
        
    def check(self):
        if(not self.conveyor or not self.barrier or not self.sorting_1 or not self.sorting_2):
            print("Due to the machine not being in its initial state, it stopped operating")
            return False
        return True
    
    def check_3(self, che): # black,barrier
        if(self.chute_3 == self.max and che):
            print("The chute 3 is full.Stop the machine.")
            return False
        elif(self.chute_3 == self.max):
            print("The chute 3 is full.Please do not put the black workpiece any more.")
        return True
    
    def check_2(self, che):# metallic, sorting_2
        if(self.chute_2 == self.max and che):
            print("The chute 2 is full.Stop the machine.")
            return False
        elif(self.chute_2 == self.max):
            print("The chute 2 is full.Please do not put the metallic workpiece any more.")
        return True
    
    def check_1(self,che): # red, sorting_1
        if(self.chute_1 == self.max and che):
            print("The chute 1 is full.Stop the machine.")
            return False
        elif(self.chute_1 == self.max):
            print("The chute 1 is full.Please do not put the red workpiece any more.")
        return True
    
    def operate(self, flag):
        if(flag):
            print("The conveyor belt starts to move and transfer the workpiece to the barrier arm")
            time.sleep(1)
            self.conveyor = False
    
    def color_detection(self, color): # return number 1(red) 2(metallic) 3(black)
        print("detect the color of the workpiece using the detection module")
        time.sleep(1)
        if(color == "red"):
            print("The color of the workpiece is red.")
            return 1
        elif(color == "metallic"):
            print("The color of the workpiece is metallic.")
            return 2
        elif(color == "black"):
            print("The color of the workpiece is black.")
            return 3
        else:
            print("The color is not the needed color")
            return 4
    
    def black(self):
        self.barrier = False
        self.chute_3 += 1
        print("Retract the barrier arm")
        time.sleep(1)
        print("Sort black workpieces")
    
    def metrllic(self):
        self.sorting_2 = False
        print("Extend the sorting arm 2")
        time.sleep(1)
        self.barrier = False
        print("Retract the barrier arm")
        time.sleep(1)
        self.chute_2 += 1
        print("Sort metallic workpieces")
        time.sleep(1)
        self.sorting_2 = True
        print("Retract the sorting arm 2")
    
    def red(self):
        self.sorting_1 = False
        print("Extend the sorting arm 1")
        time.sleep(1)
        self.barrier = False
        print("Retract the barrier arm")
        time.sleep(1)
        self.chute_1 += 1
        print("Sort red workpieces")
        time.sleep(1)
        self.sorting_1 = True
        print("Retract the sorting arm 1")
    
    def end(self):
        self.conveyor = True
        print("Stop the conveyor belt")
        time.sleep(1)
        self.barrier = True
        print("Extend the barrier arm")
        time.sleep(1)
        print("Sorting done.")

def check_object(object): # object = []
    flag = False
    flag_1 = False
    for i in object:
        if(i == "workpiece"):
            flag = True
        if(i == "conveyor"):
            flag_1 = True
        if(i == "workpieces"):
            print("Put so many workpieces at the same time.")
            return False
    if(not flag):
        print("The object is not the needed workpiece")
        return False
    if(not flag_1):
        print("The located place is not the conveyor belt")
        return False
    return True
    
if __name__ == "__main__":
    
    print("begin the sorting process.")
    sorting_unit = system()
    while(True):
        while(True): # 颜色不对或者物体不对或者没放在传送带上 都会停止运行 并且我们规定一次只能放一个物体
            print(" ")
            sentence = input("please input the sentence: ")
            print(" ")
            sentence = sentence.lower()
            if(sentence == "stop"): # 当输入是stop时，直接停止程序
                break
            color = []
            object = []
            status = []
            color, object, status = extract_keywords(sentence) # 调用model，返回三个list，color里面需要有颜色，status里面需要有atfront，
                                                    # object里面需要有workpiece和conveyor
            time.sleep(1)
            if(not check_object(object)):
                break
            if(not sorting_unit.check()):
                break
            flag = False
            for i in status:
                if(i == "atfront"):
                    print("The workpiece is at the front of the conveyor belt.")
                    flag = True
                    break
            if(not flag):
                print("The workpiece is not at the front of the conveyor belt")
                print("Stop.")
                break
            time.sleep(1)
            sorting_unit.operate(flag)  # 启动传送带
            if(len(color) == 0):
                print("Can not detect the color of the workpiece.")
                break
            number = sorting_unit.color_detection(color = color[0])   # check the color
            time.sleep(1)
            if(number == 1):
                if(not sorting_unit.check_1(True)):
                    break
                sorting_unit.red()
            elif(number == 2):
                if(not sorting_unit.check_2(True)):
                    break
                sorting_unit.metrllic()
            elif(number == 3):
                if(not sorting_unit.check_3(True)):
                    break
                sorting_unit.black()
            else:
                break
            time.sleep(1) # 加入一些时间延迟使得过程更real
            sorting_unit.end()
            time.sleep(1)  # 检查溜槽是否已满并给出提醒
            if(number == 1):
                sorting_unit.check_1(False)
            elif(number == 2):
                sorting_unit.check_2(False)
            elif(number == 3):
                sorting_unit.check_3(False)
        flag_input = True
        while(True):
            s = input("Choose whether or not to restart the machine(Y/N/C): ") # C means only clear the putting workpiece
            s = s.lower()
            if(s == "n"): #当程序停止时，输入n意味着关闭 y意味着全部重启
                print("close the system.")
                flag_input = False
                break
            elif(s == "y"):
                print("Restart the system and clear all the workpieces.")
                sorting_unit = system()
                break
            elif(s == "c"):
                print("Only clear the present workpiece.")
                sorting_unit.restart()
                break
            else:
                print("The wrong input.Please input again!")
        if(flag_input == False):
            break               
    print("The process is finished.")
    