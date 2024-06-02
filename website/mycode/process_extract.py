import time
import os
import sys
import spacy
import json

nlp = spacy.load("en_core_web_sm")
state_list = []
def extract_keywords(sentence):
    doc = nlp(sentence)
    status = []
    object = []
    color = []
    negation_flag = False 
    for i, token in enumerate(doc):
        if token.text == "arm":
            next_index = i + 1
            if next_index < len(doc) and doc[next_index].text in ["1", "2", "3"]:
                combined_word = " ".join([doc[i-1].text, token.text, doc[next_index].text])
                object.append(combined_word)
            else:
                continue
        elif token.text == "at":
            next_index = i + 2
            if next_index < len(doc):
                combined_word = "".join([token.text, doc[next_index].text])
                status.append(combined_word)
                
        elif token.dep_ == "ROOT":  # 找到动作词
            # if token.pos_ != "VERB" and token.text not in ["is", "am", "are"]:  # 排除动词 "is", "am", "are"
            #     if negation_flag:  # 如果有否定词，添加到状态中
            #         status.append("not " + token.text)
            #         negation_flag = False
            #     else:
            #         status.append(token.text)
            if token.pos_ == "NOUN":
                object.append(token.text)
            elif token.pos_ == "VERB":
                status.append(token.text)
        elif token.dep_ == "nsubj" or token.dep_ == "nsubjpass" or token.dep_ == "dobj" or token.dep_ == "compound":  # 找到主语、宾语和复合词
            object.append(token.text)
        elif token.dep_ == "acomp" or token.dep_ == "advmod" or token.dep_ == "ccomp" or token.dep_ == "attr":  # 找到动词的状态
            if negation_flag:  # 如果有否定词，添加到状态中
                status.append("not " + token.text)
                negation_flag = False
            else:
                status.append(token.text)
        elif token.dep_ == "neg":  # 找到否定词
            negation_flag = True
        elif token.pos_ == "ADJ":  # 找到形容词  
            flag = False
            for i in status:
                if token.text in i:
                    flag = True
                    break
            if(not flag):
                color.append(token.text)
            
    return color, object, status
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
            state_dict = {"workpiece": 1, "barrier": 0, "sorting_1": 2, "sorting_2": 2}
            state_list.append(state_dict)
            with open("log.txt", "a") as f:
                f.write("The conveyor belt starts to move and transfer the workpiece to the barrier arm.\n")
            
            self.conveyor = False
    
    def color_detection(self, color): # return number 1(red) 2(metallic) 3(black)
        print("detect the color of the workpiece using the detection module")
        state_dict = {"workpiece": 1, "barrier": 0, "sorting_1": 2, "sorting_2": 2}
        state_list.append(state_dict)
        with open("log.txt", "a") as f:
            f.write("detect the color of the workpiece using the detection module.\n")
        
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
        state_dict = {"workpiece": 4, "barrier": 1, "sorting_1": 2, "sorting_2": 2}
        state_list.append(state_dict)
        with open("log.txt", "a") as f:
            f.write("Retract the barrier arm.\n")
        
        print("Sort black workpieces")
        state_dict = {"workpiece": 7, "barrier": 1, "sorting_1": 2, "sorting_2": 2}
        state_list.append(state_dict)
        with open("log.txt", "a") as f:
            f.write("Sort black workpieces.\n")
    
    def metrllic(self):
        self.sorting_2 = False
        print("Extend the sorting arm 2")
        state_dict = {"workpiece": 1, "barrier": 0, "sorting_1": 2, "sorting_2": 1}
        state_list.append(state_dict)
        with open("log.txt", "a") as f:
            f.write("Extend the sorting arm 2.\n")
        
        self.barrier = False
        state_dict = {"workpiece": 3, "barrier": 1, "sorting_1": 2, "sorting_2": 1}
        state_list.append(state_dict)
        print("Retract the barrier arm")
        with open("log.txt", "a") as f:
            f.write("Retract the barrier arm.\n")
        
        self.chute_2 += 1
        print("Sort metallic workpieces")
        state_dict = {"workpiece": 6, "barrier": 1, "sorting_1": 2, "sorting_2": 0}
        state_list.append(state_dict)
        with open("log.txt", "a") as f:
            f.write("Sort metallic workpieces.\n")
        
        self.sorting_2 = True
        print("Retract the sorting arm 2")
        state_dict = {"workpiece": -1, "barrier": 1, "sorting_1": 2, "sorting_2": 2}
        state_list.append(state_dict)
        with open("log.txt", "a") as f:
            f.write("Retract the sorting arm 2.\n")
    
    def red(self):
        self.sorting_1 = False
        print("Extend the sorting arm 1")
        state_dict = {"workpiece": 1, "barrier": 0, "sorting_1": 1, "sorting_2": 2}
        state_list.append(state_dict)
        with open("log.txt", "a") as f:
            f.write("Extend the sorting arm 1.\n")
        
        self.barrier = False
        state_dict = {"workpiece": 2, "barrier": 1, "sorting_1": 1, "sorting_2": -1}
        state_list.append(state_dict)
        print("Retract the barrier arm")
        with open("log.txt", "a") as f:
            f.write("Retract the barrier arm.\n")
        
        self.chute_1 += 1
        state_dict = {"workpiece": 5, "barrier": 1, "sorting_1": 0, "sorting_2": -1}
        state_list.append(state_dict)
        print("Sort red workpieces")
        with open("log.txt", "a") as f:
            f.write("Sort red workpieces.\n")
        
        self.sorting_1 = True
        state_dict = {"workpiece": -1, "barrier": -1, "sorting_1": 2, "sorting_2": -1}
        state_list.append(state_dict)
        print("Retract the sorting arm 1")
        with open("log.txt", "a") as f:
            f.write("Retract the sorting arm 1.\n")
    
    def end(self):
        self.conveyor = True
        state_dict = {"workpiece": -1, "barrier": -1, "sorting_1": -1, "sorting_2": -1}
        state_list.append(state_dict)
        print("Stop the conveyor belt")
        with open("log.txt", "a") as f:
            f.write("Stop the conveyor belt.\n")
        
        self.barrier = True
        state_dict = {"workpiece": -1, "barrier": 0, "sorting_1": -1, "sorting_2": -1}
        state_list.append(state_dict)
        print("Extend the barrier arm")
        with open("log.txt", "a") as f:
            f.write("Extend the barrier arm.\n")
        
        print("Sorting done.")
        state_dict = {"workpiece": -1, "barrier": -1, "sorting_1": -1, "sorting_2": -1}
        state_list.append(state_dict)
        with open("log.txt", "a") as f:
            f.write("Sorting done.\n")

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
    
def process(color):
    global state_list
    # 新建一个log文件，记录整个过程
    if(os.path.exists("log.txt")):
        os.remove("log.txt")
    if(os.path.exists("state.json")):
        os.remove("state.json")
    sorting_unit = system()
    while(True):
        while(True): # 颜色不对或者物体不对或者没放在传送带上 都会停止运行 并且我们规定一次只能放一个物体
            print(" ")
            sentence = "put a " + color + " workpiece at the front of the conveyor belt"
            print(" ")
            sentence = sentence.lower()
            if(sentence == "stop"): # 当输入是stop时，直接停止程序
                break
            color = []
            object = []
            status = []
            color, object, status = extract_keywords(sentence) # 调用model，返回三个list，color里面需要有颜色，status里面需要有atfront，
                                                    # object里面需要有workpiece和conveyor
            
            if(not check_object(object)):
                break
            if(not sorting_unit.check()):
                break
            flag = False
            for i in status:
                if(i == "atfront"):
                    print("The workpiece is at the front of the conveyor belt.")
                    state_dict = {"workpiece": 0, "barrier": 0, "sorting_1": 2, "sorting_2": 2}
                    state_list.append(state_dict)
                    with open("log.txt", "a") as f:
                        f.write("The workpiece is at the front of the conveyor belt.\n")
                    flag = True
                    break
            if(not flag):
                print("The workpiece is not at the front of the conveyor belt")
                print("Stop.")
                break
            
            sorting_unit.operate(flag)  # 启动传送带
            if(len(color) == 0):
                print("Can not detect the color of the workpiece.")
                break
            number = sorting_unit.color_detection(color = color[0])   # check the color
            
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
             # 加入一些时间延迟使得过程更real
            sorting_unit.end()
              # 检查溜槽是否已满并给出提醒
            if(number == 1):
                sorting_unit.check_1(False)
            elif(number == 2):
                sorting_unit.check_2(False)
            elif(number == 3):
                sorting_unit.check_3(False)
            break
        break    
    # 将state_list转为json格式保存
    json_state = json.dumps(state_list, ensure_ascii=False, indent=4)
    with open('state.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_state)     
    state_list = []
if __name__ == "__main__":
    args = sys.argv
    if(len(args) != 2):
        print("Please input the color of the workpiece")
        sys.exit()
    color = args[1]
    process(color)
    
    
    