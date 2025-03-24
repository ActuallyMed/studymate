import ollama
import random
import json

# File paths
MEMORY_FILE = 'memory.txt'
QUESTION_FILE = 'questions.json'

# Function to summarize and clean paragraph
def summarize_paragraph(paragraph):
    prompt = (
        "Summarize the following paragraph. Remove trivial information, keep only key points:\n\n"
        f"{paragraph}\n\n"
        "Return only factual bullet points."
    )
    response = ollama.chat(
        model='mistral:7b-instruct-q4_K_M',
        messages=[
            {'role': 'user', 'content': prompt}
        ]
    )
    summary = response['message']['content'].strip()
    print("\nSummary:\n" + summary)
    return summary

# Function to generate questions from summary
def generate_questions(summary):
    prompt = (
        f"Based on these key points:\n{summary}\n\n"
        "Create:\n"
        "1. One Multiple Choice Question (MCQ) with 4 options and correct answer.\n"
        "2. One subjective question with answer.\n"
        "3. One fill-in-the-blank question with answer.\n"
        "Format clearly."
    )
    response = ollama.chat(
        model='mistral:7b-instruct-q4_K_M',
        messages=[
            {'role': 'user', 'content': prompt}
        ]
    )
    print("\nGenerated Questions:\n" + response['message']['content'])
    return response['message']['content']

# Function to store summary in memory
def store_summary(summary):
    with open(MEMORY_FILE, 'a') as mem_file:
        mem_file.write(summary + "\n")

# Function to store questions
def store_questions(question_block):
    try:
        with open(QUESTION_FILE, 'r') as f:
            all_questions = json.load(f)
    except FileNotFoundError:
        all_questions = []

    all_questions.append(question_block)
    with open(QUESTION_FILE, 'w') as f:
        json.dump(all_questions, f, indent=4)

# Function to quiz user
def quiz_user():
    try:
        with open(QUESTION_FILE, 'r') as f:
            all_questions = json.load(f)
    except FileNotFoundError:
        print("No questions available! Add paragraphs first.")
        return

    score = 0
    print("\nStarting Quiz!\n")

    for q in random.sample(all_questions, len(all_questions)):
        print("\n" + q)
        user_answer = input("Your answer: ").strip()

        # Simple manual grading (can be improved!)
        if user_answer.lower() in q.lower():
            print("✅ Correct!")
            score += 1
        else:
            print("❌ Incorrect!")

    print(f"\nYour Score: {score}/{len(all_questions)}")

# --- Main Menu ---

while True:
    print("\nStudyMate Menu:")
    print("1. Add Paragraph & Summarize")
    print("2. Generate Quiz Questions")
    print("3. Take Quiz")
    print("4. Exit")

    choice = input("Select: ").strip()

    if choice == '1':
        paragraph = input("\nEnter paragraph:\n")
        summary = summarize_paragraph(paragraph)
        store_summary(summary)
    elif choice == '2':
        try:
            with open(MEMORY_FILE, 'r') as mem_file:
                summaries = mem_file.readlines()
        except FileNotFoundError:
            print("No summaries found! Add paragraph first.")
            continue

        for summary in summaries:
            question_block = generate_questions(summary)
            store_questions(question_block)
    elif choice == '3':
        quiz_user()
    elif choice == '4':
        print("Goodbye!")
        break
    else:
        print("Invalid option!")