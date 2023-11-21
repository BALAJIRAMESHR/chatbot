import json
from difflib import get_close_matches

def load_knowledge_base(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, createdata):
    for q in createdata['questions']:
        if isinstance(q['question'], list):
            matches = get_close_matches(user_question, q['question'], n=1)
            if matches:
                return matches[0]
        else: # it's a string
            if q['question'] == user_question:
                return q['question']
    return None

def get_answer_for_question(question: str, createdata: dict):
    for q in createdata['questions']:
        if isinstance(q['question'], list) and question in q['question']:
            return q["answer"]
        elif q['question'] == question:  # it's a string
            return q["answer"]
    return None

def chat_bot():
    createdata = load_knowledge_base('createdata.json')

    while True:
        user_input = input('You : ')

        if user_input.lower() == "quit":
            break

        best_match = find_best_match(user_input, createdata)

        if best_match:
            answer = get_answer_for_question(best_match, createdata)
            print(f'Bot : {answer}')
        else:
            print(f'Bot : I don\'t know')
            new_answer = input('Type the answer or "skip":')

            if new_answer.lower() != 'skip':
                createdata["questions"].append({"question": [user_input], "answer": new_answer})
                save_knowledge_base('createdata.json', createdata)

if __name__ == "__main__":
    chat_bot()


