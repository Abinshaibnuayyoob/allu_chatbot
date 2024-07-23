import re
def extract_session_id(session_str: str):
    match = re.search(r"sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string
    else:
        print("sorry, user")
def get_str_from_food_dict(food_dict: dict):
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])

if __name__ == "__main__":
    print(get_str_from_food_dict({"samosa": 2, "lazzi": 1}))


    #print(type(extract_session_id("projects/chef-de-cuisine-rgut/agent/sessions/99b5d770-ef80-99a0-1efc-52192b0bdd4c/contexts/ongoing-order")))


