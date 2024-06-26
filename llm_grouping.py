import pandas as pd
import functions as fu
import settings as se


def llm_grouping(_key_characteristics):
    # Prepare user data
    user_data = pd.read_csv(f"data/{se.file_name}", delimiter=";")
    user_data_list = user_data.values.tolist()

    prompt = [
        {
            "role": "user",
            "content": f"Here are user data:\n{user_data_list}\n\n"
                       f"Group the user data by \"{_key_characteristics}\".\n"
                       f"Generate a single persona for each group.\n\n"
                       "You must follow the rules below when generating the personas:\n"
                       f"- Rule 1: Do not add any information that does not exist in the user data.\n"
                       f"- Rule 2: You may combine, synthesize, or rephrase multiple user data into a single persona.\n"
                       f"- Rule 3: The persona should have detailed descriptions of the following information:\n {se.content_demography + se.content_design}\n"
                       f"- Rule 4: Write {se.content_design} from the first person perspective.\n"
                       f"After generating personas, compare the personas with the user data to validate Rule 1, 2, 3, and 4.\n"
                       f"Make necessary updates such as updating information in personas, removing personas, or creating new personas.\n"
                       f"Present only the final personas."
        }
    ]

    # get input
    input_prompt = prompt[0]["content"]

    # Display input
    print("\n### Input ###\n")
    print(input_prompt, "\n")

    # save input
    with open("llm_grouping/llm_grouping_input.txt", "w") as text_file:
        text_file.write(input_prompt)

    print(f"\n### Waiting for {se.gpt_model}'s response ... ###\n")

    # compute output
    output = fu.chat_completion(prompt)

    # Display output
    print("\n### Output ###\n")
    print(output, "\n")

    # save output
    with open("llm_grouping/llm_grouping_output.txt", "w") as text_file:
        text_file.write(output)

    print(f"\n### Done. Generated all personas. ###\n")


if __name__ == "__main__":
    # Exemplary key characteristics defined by user researcher
    key_characteristics = "plans and reasons for having children"

    # Generating personas
    llm_grouping(key_characteristics)
