import json


# name
# phone
# birthday
# city


def load_phonebook():
    try:
        with open("phonebook.json", "r", encoding="utf-8") as phonebook_json:
            return json.load(phonebook_json)
    except:
        return {}


def import_phonebook(path_to_pb: str):
    try:
        with open(path_to_pb, "r", encoding="utf-8") as phonebook_json:
            for k, v in json.load(phonebook_json).items():
                if k in phonebook.keys():
                    phonebook[f"{k}(2)"] = v
                else:
                    phonebook[k] = v
    except:
        print("Can't find such file or directory")
    save_changes()


def save_changes():
    with open("phonebook.json", "w", encoding="utf-8") as phonebook_json:
        phonebook_json.write(json.dumps(phonebook, ensure_ascii=False))



def delete_contact(user_name: str):
    if user_name in phonebook:
        phonebook.pop(user_name)
    else:
        print("Can't find this contact!")


def add_contact():
    name = input("Enter name: ")
    if name in phonebook:
        print("Contact already exists")
        return

    phonebook[name] = {}
    set_contact_property("city", name)
    set_contact_property("birthday", name)
    phonebook[name]["phone"] = []
    answer: str = ""
    while answer != "n":
        if answer == "y" or not answer:
            set_contact_property("phone", name, answer)
        answer = input(f"Do you want to add another phone?(y/n)\n")
    save_changes()


def set_contact_property(prop_name: str, user_name: str, answer: str = "not sure"):
    if answer != "y":
        while answer != "y" and answer != "n":
            answer = input(f"Do you want to add {prop_name}?(y/n)\n")
    if answer == "y":
        if prop_name == "phone":
            phone = input(f"Enter {prop_name}: ")
            if not is_phone_exists(phone):
                phonebook[user_name][prop_name].append(phone)
            else:
                print("Phone is already added!")
        else:
            phonebook[user_name][prop_name] = input(f"Enter {prop_name}: ")


def is_phone_exists(phone: str) -> bool:
    for k, v in phonebook.items():
        if phone in v["phone"]:
            return True
    return False


def edit_contact(user_name: str):
    if user_name not in phonebook:
        print("There's not contact with this name!")
    else:
        answer = ""
        while answer != "n":
            user_prop = input("What do you want to change?\n")
            if user_prop == "phone":
                while answer != "edit" and answer != "add":
                    answer = input("Do you want to edit or add number?(edit/add)\n")
                    if answer == "add":
                        set_contact_property(user_prop, user_name, "y")
                    else:
                        edit_phones(phonebook[user_name][user_prop])
            elif user_prop == "name":
                new_name = input("Enter new name:\n")
                if new_name not in phonebook:
                    phonebook[new_name] = phonebook[user_name]
                    phonebook.pop(user_name)
                else:
                    print("This name is already in phonebook!")
            else:
                set_contact_property(user_prop, user_name, "y")
            answer = input("Do you want to change anything else?(y/n)\n")
    save_changes()


def edit_phones(phones: list):
    answer = ""
    while answer != "n":
        phone = input("What number do you want to edit?\n")
        if phone not in phones:
            print("Can't find this number!")
        else:
            while answer != "change" and answer != "del":
                answer = input("Do you want to change or delete number?(change/del)\n")
                if answer == "del":
                    phones.remove(phone)
                elif answer == "change":
                    phone_index = phones.index(phone)
                    new_phone = input("Enter new phone: ")
                    if not is_phone_exists(phone):
                        phones[phone_index] = new_phone
                    else:
                        print("This phone is already exist")
        answer = input("Any more phone changes? :D (y/n)\n")


def show_contact(user_name: str):
    print(f"{user_name}:")
    for k, v in phonebook[user_name].items():
        if k == "phone" and len(v) > 0:
            if len(v) == 1:
                print(f"\t{k}: {v[0]}")
            else:
                for i in range(len(v)):
                    print(f"\t{k} {i + 1}: {v[i]}")
        elif k != "phone":
            print(f"\t{k}: {v}")
    print()


def show_contacts():
    for k in phonebook.keys():
        show_contact(k)


def find_contact(user_name: str):
    if user_name in phonebook:
        show_contact(user_name)
    else:
        print("Can't find this contact!")


phonebook: dict = load_phonebook()
print("You can:\n/add - add contact\n/del - delete contact\n/edit - edit contact\n/find - find contact\n"
      "/show_all - show all!\n/import - import contact")

while True:
    command = input("Enter command!\n")
    if command == "/add":
        add_contact()
    elif command == "/del":
        del_name = input("Enter name of contact for delete the whole contact\n")
        delete_contact(del_name)
    elif command == "/find":
        find_name = input("Enter name and get contact info\n")
        find_contact(command)
    elif command == "/edit":
        edit_name = input("Enter name and change contact\n")
        edit_contact(edit_name)
    elif command == "/show_all":
        show_contacts()
    elif command == "/import":
        path = input("Enter path to the phonebook\n")
        import_phonebook(path)
    else:
        print("Wrong command! Try again!")
