import os
import pandas as pd
import functions as fu


def get_personas():
    # For roleplaying with personas, we use the personas generate from LLM_summarizing.
    # Change the 'directory' below if you want to use personas generated from other workflows.
    directory = "llm_summarizing"
    tag = f"{directory}_output"

    # check if personas exist
    if not any(tag in file for file in os.listdir(directory)):
        print("There are no personas.")
        print(f"Run '{directory}.py' to create personas first.")
        return

    # get personas
    persona_files = [file for file in os.listdir(directory) if tag in file]
    personas = []

    for file in persona_files:
        with open(os.path.join(directory, file), 'r') as f:
            personas.append(f.read())

    print(f"\n### There are {len(personas)} personas. ")

    return personas


def roleplay_with_personas(_max_memory):
    personas = get_personas()

    # to keep the tack of the log
    interaction_log = pd.DataFrame(columns=["request", "response"])

    while True:
        memory = []

        # get the latest request and response for the conversation.
        if len(interaction_log) > 0:
            temp_memory = interaction_log.tail(_max_memory)

            for i in range(len(temp_memory)):
                request = temp_memory.iloc[i]["request"]
                response = temp_memory.iloc[i]["response"]
                memory.append([f"User: \"{request}\", You: \"{response}\""])

        # get user input
        request = input(f"What would you like to ask to them (or type 'c' to stop): ")

        if request == 'c':
            break

        # prompt
        prompt = [
            {
                "role": "user",
                "content": f"Here are personas generated to represent archetypal user groups:\n{personas}\n\n"
                           f"Here are our previous conversation (\"User\" is I and \"You\" are you):\n{memory}\n\n"
                           f"Please respond breifly to the following request based on our previous conversation and as if you are the personas:\n{request}\n"
            }
        ]

        # get input
        input_prompt = prompt[0]["content"]

        print(f"\n### Waiting for response ...\n")

        # compute output
        response = fu.chat_completion(prompt)

        # Display output
        print(f"\n{response}\n")

        # append the new request and response to the interaction_log.
        interaction_log.loc[len(interaction_log)] = [request, response]

    # save interaction_log
    interaction_log.to_csv("llm_summarizing/roleplay/roleplay.csv", index=False)


if __name__ == "__main__":
    # the maximum number of the latest dialogues for LLMs to consider when generating responses.
    max_number_of_memory = 3

    # Generating responses
    roleplay_with_personas(max_number_of_memory)
