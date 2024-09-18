import dotenv
import streamlit as st
import requests
import openai
import os
import json
import regex as re
from langchain.prompts import PromptTemplate
dotenv.load_dotenv()

# Configure Streamlit
st.title("Student Database")

# Initialize LangChain or Llama model
openai.api_key = os.getenv('OPENAI_API_KEY')
print(openai)


def query_openai(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # You can use other models if needed
        messages=prompt,
        max_tokens=50
    )
    return response.choices[0].message.content


def add_student(student_name, student_id):
    # Prepare the data for the POST request
    data = {
        "student_name": student_name,
    }

    # Include student_id only if provided
    if student_id:
        data["id"] = student_id

    # Call the POST API to add the student
    api_url = "http://127.0.0.1:5000/add_student"  # Adjust the URL as necessary
    try:
        api_response = requests.post(api_url, json=data)

        # Check the API response
        if api_response.status_code == 201:
            return {"Student added successfully!"}
        else:
            return {"error": f"Failed to add student: {api_response.json().get('error', 'Unknown error')}"}

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def add_subject(subjectname):
    data = {
        "subjectname": subjectname,
    }

    # Call the POST API to add the student
    api_url = "http://127.0.0.1:5000/add_subject"  # Adjust the URL as necessary
    try:
        api_response = requests.post(api_url, json=data)

        # Check the API response
        if api_response.status_code == 201:
            return {"Subject added successfully!"}
        else:
            return {"error": f"Failed to add student: {api_response.json().get('error', 'Unknown error')}"}

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def add_marks(subjectname,student_name,marks):
    data = {
        "student_name":student_name,
        "subject_name": subjectname,
        "marks": marks
    }

    # Call the POST API to add the student
    api_url = "http://127.0.0.1:5000/add_marks"  # Adjust the URL as necessary
    try:
        api_response = requests.post(api_url, json=data)

        # Check the API response
        if api_response.status_code == 201:
            return {"Subject added successfully!"}
        else:
            return {"error": f"Failed to add student: {api_response.json().get('error', 'Unknown error')}"}

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def display_marks(subjectname,student_name):
    data = {
        "student_name": student_name,
        "subject_name": subjectname,
    }
    print(data)

    # Call the POST API to add the student
    api_url = "http://127.0.0.1:5000/get_student_marks"  # Adjust the URL as necessary
    try:
        api_response = requests.get(api_url, json=data)
        print(api_response.json())
        return api_response.json()

        # Check the API resp

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}




def process_instruction(instruction):
    global subjectname
    messages = [
        {"role": "system", "content":"""
        You are a helpful assistant. Your task is to:
        1. Extract the action and data from user instructions.
        2. Identify the intent from the instruction (e.g., Add Student, Add Marks, Add Subject, Display Data).
        3. Extract relevant data based on the identified intent. The data will be formatted as follows:
            - For `Add Student`: Extract `student_name`
            - For `Add Subject`: Extract `subject_name`
            - For `Add Marks`: Extract `marks`
            - For `Display Data`: Extract `student_name`, `subject_name`, and `marks` if available
        4. Return the action and extracted data in the string:
                action= Action type
                // Include only fields for which data is available
                //only string not in dictionary
                student: Extracted student name,
                subject: Extracted subject name,
                marks: Extracted marks
                ID: Extracted ID
                """},
        {"role": "user", "content": instruction}
    ]
    response = query_openai(messages)

    if "add student" in response.lower():

        # Extracting student name and ID from the response string
        # Assuming the response format is consistent
        student_name = None
        student_id = None

        # Split response into lines and look for relevant data
        for line in response.splitlines():
            if "student" in line.lower() or "name" in line.lower():
                # Split by the first occurrence of `:` or `=` and ensure the split result has at least two parts
                parts = re.split(r'[:\=]', line, 1)
                if len(parts) > 1:
                    student_name = parts[1].strip()
            if "ID" in line.strip():
                parts = re.split(r'[=\-]', line, 1)
                if len(parts) > 1:
                    student_id = parts[1].strip()
        # Call the add_student function
        return add_student(student_name, student_id)

    elif "add subject" in response.lower():

        # Assuming the response format is consistent
        for line in response.splitlines():
            if "subject" in line.lower():
                parts = re.split(r'[:\=]', line, 1)
                if len(parts) > 1:
                    subjectname = parts[1].strip()
            else:
                print("Error: Delimiter ':' or '-' not found in 'subject' field")

        # Call the add_subject function with the extracted subject name
        if subjectname:
            add_subject(subjectname)
        else:
            print("No subject found.")

    elif "add marks" in response.lower():

        # Extracting student name and ID from the response string
        # Assuming the response format is consistent

        # Split response into lines and look for relevant data
        for line in response.splitlines():
            line = line.strip()  # Remove leading and trailing whitespace

            # Extract student name
            if "student" in line.lower():
                parts = re.split(r'[:\=\-]', line, 1)
                if len(parts) > 1:
                    student_name = parts[1].strip()
                    print(student_name)

            # Extract marks
            if "marks" in line.lower():
                parts = re.split(r'[:\=\-]', line, 1)
                if len(parts) > 1:
                    marks = parts[1].strip()

            # Extract subject name
            if "subject" in line.lower():
                parts = re.split(r'[:\=\-]', line, 1)
                if len(parts) > 1:
                    subjectname = parts[1].strip()

        # Call the add_student function
        return add_marks(subjectname,student_name,marks)

    elif "display" in response.lower():

        # Extracting student name and ID from the response string
        # Assuming the response format is consistent
        subjectname=None
        student_name=None


        # Split response into lines and look for relevant data
        for line in response.splitlines():
            line = line.strip()
            if "student" in line.lower():
                parts = re.split(r'[:\=\-]', line, 1)
                if len(parts) > 1:
                    student_name = parts[1].strip()

            # Extract subject name
            if "subject" in line.lower():
                parts = re.split(r'[:\=\-]', line, 1)
                if len(parts) > 1:
                    subjectname = parts[1].strip()


        # Call the add_student function
        json=display_marks(subjectname,student_name)
        json=str(json)
        mes = [
            {"role": "system", "content": """You are a helpfulbot ehere i will send you json you need to convert in message . Example Aman score 80 in Maths"""},
            {"role": "user", "content": json}
        ]
        response = query_openai(mes)
        return response




instruction = st.text_area("Student Database: ADMIN", "")

if st.button("Enter"):
    if instruction:
        action = process_instruction(instruction)
        st.write(action)