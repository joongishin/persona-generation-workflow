import os
import pandas as pd
import functions as fu
import settings as se


def llm_summarizing():
    # check if the text embedding already exists
    if not os.path.exists(f"llm_summarizing/exploration/grouped_{se.file_name}"):
        print(f"File grouped_{se.file_name} does not exists.")
        print("Run 'explore_user_groups.py' to create user groups first.")
        return

    # Prepare user data
    user_data = pd.read_csv(f"llm_summarizing/exploration/grouped_{se.file_name}")
    num_group = user_data["user_group"].max() + 1

    # Summarize each user group
    for group_num in range(num_group):
        print(f"\n### Generating a persona for user group {group_num + 1}/{num_group} ... ###\n")

        # prepare user data per group
        grouped_data = user_data[user_data["user_group"] == group_num]
        grouped_data = grouped_data.drop(columns=["user_group"])
        grouped_data_list = grouped_data.values.tolist()

        prompt = [
            {
                "role": "user",
                "content": f"Here are user data:\n{grouped_data_list}\n\n"
                           f"Generate a single persona to represent the user data.\n\n"
                           "You must follow the rules below when generating the persona:\n"
                           f"- Rule 1: Do not add any information that does not exist in the user data.\n"
                           f"- Rule 2: You may combine, synthesize, or rephrase multiple user data into a single persona.\n"
                           f"- Rule 3: The persona should have detailed descriptions of the following information:\n {se.content_demography + se.content_design}\n"
                           f"- Rule 4: Write {se.content_design} from the first person perspective.\n"
                           f"After generating persona, compare the persona with the user data to validate Rule 1, 2, 3, and 4.\n"
                           f"Make necessary updates such as updating information in the persona.\n"
                           f"Present only the final persona."
            }
        ]

        # get input
        input_prompt = prompt[0]["content"]

        # Display input
        print("\n### Input ###\n")
        print(input_prompt, "\n")

        # save input
        with open(f"llm_summarizing/llm_summarizing_input_{group_num}.txt", "w") as text_file:
            text_file.write(input_prompt)

        print(f"\n### Waiting for {se.gpt_model}'s response {group_num + 1}/{num_group} ... ###\n")

        # compute output
        output = fu.chat_completion(prompt)

        # Display output
        print("\n### Output ###\n")
        print(output, "\n")

        # save output
        with open(f"llm_summarizing/llm_summarizing_output_{group_num}.txt", "w") as text_file:
            text_file.write(output)

    print(f"\n### Done. Generated all personas. ###\n")

if __name__ == "__main__":
    # Generating personas
    llm_summarizing()

