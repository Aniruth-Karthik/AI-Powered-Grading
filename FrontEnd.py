import streamlit as st
import pandas as pd
import csv

from scratcher import information,main_keywords,key_similarity

questions = []
answers = []
answer_keys = []
n = ''



def evaluate():
    st.text(answer_keys)
    for q,a,k in zip(questions,answers,answer_keys):
        st.text("evaluating...")
        st.subheader(q)
        st.text(a)
        raw_text = information(q)
        sim,keywrds = main_keywords(raw_text,a)

        st.subheader("Keywords:")
        st.dataframe(keywrds[:10])
        st.text(f"{(sim[0][0] * 200)//1}%")

        
        if k!='':
            st.subheader("answer key similarity:")
            sim = key_similarity(k,a)
            st.text(f"{(sim[0][0] * 200)//1}%")



st.title("AI Powered Grading")

option = st.selectbox('Please select one option',('None','Answer script evaluation','Set questions'))

if(option == 'Answer script evaluation'):
    with open(r"question_file.csv",'r') as f:
        reader = csv.reader(f)
        row = 0
        for i in reader:
            if(row==0) :questions = i
            else: answer_keys = i
            row+=1
        for ind,val in enumerate(questions):
            ar = st.text_area(f"Q{ind+1})\n{val}")
            if(ar!=''):
                answers.append(ar)
    if(st.button('submit')):
        evaluate()

       
elif(option == 'Set questions'):
    n = st.text_input("Numer of Questions:")
    #data = pd.read_csv()
    if(n!=''):
        for i in range(int(n)):
            ar = st.text_area(f"enter question{i+1}")
            if(ar!=''):
                questions.append(ar)
            
            k = ''
            if(st.checkbox("give answer key",key=i)):
                k = st.text_area("provide key",key=i+int(n))
            answer_keys.append(k)
    
    if(st.button('submit')):
        if(len(questions)<int(n)):
            st.error("all questions must be filled")
        else:
            st.success("Thank you")
            with open(r"question_file.csv",'w',newline="") as f:
                writer = csv.writer(f)
                writer.writerow(questions)
                writer.writerow(answer_keys)