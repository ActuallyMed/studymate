import ollama


def menu():
    print("Hello. I am your very own, StudyMate.")
    print("Please select an option:\n (A): Chat\n (B): Summarise\n (C): Quiz\n (D): Exit")
    opt = input(":")
    if opt.lower() == 'a':
        print("Chat Mode")
        while True:
            request = input(">>>")
            if request.lower() == 'back':
                menu()
            print("\n...")
            response = ollama.chat(
                model='mistral:7b-instruct-q4_K_M',
                messages=[
                    {'role': 'user', 'content': request}
                ]
            )
            ai_reply = response.get('message', {}).get('content', '[No response]')
            print(":" + ai_reply)
    if opt.lower() == 'd':
        quit()
menu()
