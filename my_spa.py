import spacy

nlp = spacy.load("en_core_web_sm")

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

# sentence = "The red workpiece is located at the front end of the conveyor belt."
# color, object, status = extract_keywords(sentence)

# print("Status: ", status)
# print("Object: ", object)
# print("Color: ",color)
