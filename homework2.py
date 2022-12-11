from statemachine import StateMachine, State
import pandas as pd
import numpy as np
import nlpcloud

class ScoreMachine(StateMachine):
    hanging = State("Hanging", initial=True)
    intro = State("Intro")
    name = State("Name")
    exam = State("Exam")
    scores = State("Scores")

    forwardtointro = hanging.to(intro)
    forwardtoname = intro.to(name)
    backtointro = name.to(intro)
    backtohanging = intro.to(hanging)
    backtohanging2 = name.to(hanging)
    forwardtoexam = name.to(exam)
    backtohanging3 = exam.to(hanging)
    backtointro2 = exam.to(intro)
    forwardtoscores = hanging.to(scores)
    backtohanging4 = scores.to(hanging)

score_machine = ScoreMachine()

student_names = [
    "melih senturk",
    "michael jordan",
    "kobe bryant",
    "lebron james"]
classroom_df = pd.DataFrame(student_names, columns=["names"])
classroom_df["first"] = np.zeros(4)
classroom_df["second"] = np.zeros(4)
classroom_df["third"] = np.zeros(4)

flag = 1

intent_client = nlpcloud.Client(
    "fast-gpt-j",
    "2e672310ff4c6d9afb5c21d9ae08d1a4c42ae7cf",
    True)
entity_client = nlpcloud.Client(
    "en_core_web_lg",
    "2e672310ff4c6d9afb5c21d9ae08d1a4c42ae7cf")
answering_client = nlpcloud.Client(
    "finetuned-gpt-neox-20b",
    "2e672310ff4c6d9afb5c21d9ae08d1a4c42ae7cf",
    True)

print("Hello there! I am Notty. Could you summarize your request? Ex: add score or learn score")
text = input().lower()
while text != "quit":
    if score_machine.is_hanging:
        if flag:
            intent_class = intent_client.intent_classification(text)
            if(intent_class["intent"] == "add a score" or
               intent_class["intent"] == "add score" or
               intent_class["intent"] == "add some score" or
               intent_class["intent"] == "add another score"):
                score_machine.forwardtointro()
            elif(intent_class["intent"] == "learn a score" or
                 intent_class["intent"] == "learn score" or
                 intent_class["intent"] == "learn some score"):
                    score_machine.forwardtoscores()
            else:
                print(answering_client.chatbot(text)["response"])
                text = input().lower()
        else:
            flag = 1
            text = input().lower()
    if score_machine.is_intro:
        add_list = []
        print("Please tell the name of the student or write <top> to return to a top menu")
        text = input().lower()
        if(text == "top"):
            print("You are returning to the top menu")
            print("*-------------------------------*")
            print("Hello there! I am Notty. Could you summarize your request? Ex: add score or learn score")
            flag = 0
            score_machine.backtohanging()
        else:
            if(text == x for x in student_names):
                entity_class = entity_client.entities(text)
                for i in range(len(entity_class["entities"])):
                    if(entity_class["entities"][i]["type"] == "PERSON"):
                        add_list.append(entity_class["entities"][i]["text"])
                        score_machine.forwardtoname()
            else:
                print("Please write a name belongs to class")
    if score_machine.is_name:
        print("Please write which exam do you want to fill. Ex: First, second or third or write <top> to return to a top menu")
        text = input().lower()
        if(text == "top"):
            print("You are returning to the top menu")
            print("*-------------------------------*")
            print("Hello there! I am Notty. Could you summarize your request? Ex: add score or learn score")
            flag = 0
            score_machine.backtohanging2()
        else:
            entity_class = entity_client.entities(text)
            for i in range(len(entity_class["entities"])):
                if(entity_class["entities"][i]["type"] == "ORDINAL"):
                    add_list.append(entity_class["entities"][i]["text"])
                    score_machine.forwardtoexam()
    if score_machine.is_exam:
        print("Please write the point. Ex: 87, 85.4 or write <top> to return to a top menu")
        text = input().lower()
        if(text == "top"):
            print("You are returning to the top menu")
            print("*-------------------------------*")
            print("Hello there! I am Notty. Could you summarize your request? Ex: add score or learn score")
            flag = 0
            score_machine.backtohanging3()
        else:
            entity_class = entity_client.entities(text)
            for i in range(len(entity_class["entities"])):
                if(entity_class["entities"][i]["type"] == "CARDINAL"):
                    add_list.append(entity_class["entities"][i]["text"])
                    classroom_df.loc[classroom_df["names"] == add_list[0], add_list[1]] = add_list[2]
            print("Would you like to add another? Please write <yes> otherwise type anything to go back to top menu")
            text = input().lower()
            if(text == "yes"):
                score_machine.backtointro2()
            else:
                print("You are returning to the top menu")
                print("*-------------------------------*")
                print("Hello there! I am Notty. Could you summarize your request? Ex: add score or learn score")
                flag = 0
                score_machine.backtohanging3()
    if score_machine.is_scores:
        print("\n")
        print(classroom_df)
        print("\n")
        print("You are returning to the top menu")
        print("*-------------------------------*")
        print("Hello there! I am Notty. Could you summarize your request? Ex: add score or learn score")
        flag = 0
        score_machine.backtohanging4()

print("Goodbye!")   