import telebot
import json

phonebook = {}
current_contact = ""
current_property = ""
API_TOKEN = #Your token#
bot = telebot.TeleBot(API_TOKEN)

def load_phonebook():
    try:
        with open("phonebook.json", "r", encoding="utf-8") as phonebook_json:
            for k, v in json.load(phonebook_json).items():
                phonebook[k] = v
    except:
        return -1


def save_changes():
    with open("phonebook.json", "w", encoding="utf-8") as phonebook_json:
        phonebook_json.write(json.dumps(phonebook, ensure_ascii=False))


def is_phone_exists(phone: str) -> bool:
    for k, v in phonebook.items():
        if phone in v["phone"]:
            return True
    return False


def reset_current_globals():
    global current_contact
    global current_property
    current_contact = ""
    current_property = ""


@bot.message_handler(commands=['start'])
def start_message(message):
    if load_phonebook() != -1:
        bot.send_message(message.chat.id, "Phonebook is loaded from file!")
    else:
        bot.send_message(message.chat.id, "Can't find phonebook file! But you can add data manually")
    bot.send_message(message.chat.id, "You can:\n1. /add - add contact\n2. /find - find contact (and then edit)\n3. "
                                      "/delete - delete contact\n4. /show_all - see what have you done...")


@bot.message_handler(commands=['add'])
def add_contact(message):
    bot.send_message(message.chat.id, "Enter name: ")
    bot.register_next_step_handler(message, add_name)


def add_name(message):
    if message.text in phonebook:
        bot.send_message(message.chat.id, "Name is already in phonebook. Enter another: ")
        bot.register_next_step_handler(message, add_name)
    else:
        global current_contact
        current_contact = message.text
        phonebook[current_contact] = {}
        phonebook[current_contact]["phone"] = []
        bot.send_message(message.chat.id, "Do you want to add contact property? (yes|no): ")
        bot.register_next_step_handler(message, add_properties)


def add_properties(message):
    if str(message.text).lower() == "no":
        reset_current_globals()
        save_changes()
        bot.send_message(message.chat.id, "Contact saved: ")
        return
    elif str(message.text).lower() == "yes":
        bot.send_message(message.chat.id, "Enter property name: ")
        bot.register_next_step_handler(message, add_properties)
    elif str(message.text).lower() == "name":
        bot.send_message(message.chat.id, "You can't set additional name, choose another property to set: ")
        bot.register_next_step_handler(message, add_properties)
    else:
        global current_property
        current_property = str(message.text).lower()
        bot.send_message(message.chat.id, f"Enter {current_property}: ")
        bot.register_next_step_handler(message, add_property)


def add_property(message):
    if current_property == "phone" and is_phone_exists(message.text):
        bot.send_message(message.chat.id, f"Phone is already in phonebook! Add another: ")
        bot.register_next_step_handler(message, add_property)
    else:
        if current_property == "phone":
            phonebook[current_contact]["phone"].append(message.text)
        else:
            phonebook[current_contact][current_property] = message.text
        bot.send_message(message.chat.id, "Do you want to add another contact property? (yes|no): ")
        bot.register_next_step_handler(message, add_properties)


@bot.message_handler(commands=['delete'])
def deletion(message):
    bot.send_message(message.chat.id, "Enter name and contact will be deleted: ")
    bot.register_next_step_handler(message, del_contact)


def del_contact(message):
    if message.text in phonebook.keys():
        phonebook.pop(message.text)
        save_changes()
        bot.send_message(message.chat.id, "Contact is deleted: ")
    else:
        bot.send_message(message.chat.id, "Contact doesn't exist")


@bot.message_handler(commands=['find'])
def finding(message):
    if len(phonebook.keys()):
        bot.send_message(message.chat.id, "Enter name to find contact: ")
        bot.register_next_step_handler(message, find_contact)
    else:
        bot.send_message(message.chat.id, "Phonebook is empty.")


def find_contact(message):
    if message.text not in phonebook:
        bot.send_message(message.chat.id, "There is no such contact in phonebook. Enter another: ")
        bot.register_next_step_handler(message, find_contact)
    else:
        global current_contact
        current_contact = message.text
        bot.send_message(message.chat.id, f"{show_contact(current_contact)}")
        bot.send_message(message.chat.id, f"Do you want to edit this contact? (yes|no): ")
        bot.register_next_step_handler(message, edit_contact)


def edit_contact(message):
    if str(message.text).lower() == "no":
        reset_current_globals()
        save_changes()
    elif str(message.text).lower() == "yes":
        bot.send_message(message.chat.id, "Enter property name for change: ")
        bot.register_next_step_handler(message, edit_contact)
    elif str(message.text).lower() == "phone":
        bot.send_message(message.chat.id, "Do you want to delete or edit number or add the new one? (del|edit|add): ")
        bot.register_next_step_handler(message, edit_phones)
    elif str(message.text).lower() == "name":
        bot.send_message(message.chat.id, "Enter new name: ")
        bot.register_next_step_handler(message, set_name)
    else:
        global current_property
        current_property = str(message.text).lower()
        bot.send_message(message.chat.id, f"Do you want to delete or edit {current_property}? (del|set): ")
        bot.register_next_step_handler(message, edit_property)


def edit_property(message):
    if current_property not in phonebook[current_contact].keys and str(message.text).lower() == "del":
        bot.send_message(message.chat.id, "This property doesn't exist! Do you want to change another? (yes|no): ")
        bot.register_next_step_handler(message, edit_contact)
    elif current_property in phonebook[current_contact].keys and str(message.text).lower() == "del":
        phonebook[current_contact].pop(current_property)
        bot.send_message(message.chat.id, "Do you want to change another property? (yes|no): ")
        bot.register_next_step_handler(message, edit_contact)
    elif str(message.text).lower() == "edit":
        bot.send_message(message.chat.id, f"Enter {current_property}: ")
        bot.register_next_step_handler(message, set_property)
    else:
        bot.send_message(message.chat.id, "This word has no sense! Do you want to change another property? (yes|no):")
        bot.register_next_step_handler(message, edit_contact)

def set_property(message):
    phonebook[current_contact][current_property] = message
    bot.send_message(message.chat.id, "Do you want to change another property? (yes|no): ")
    bot.register_next_step_handler(message, edit_contact)


def set_name(message):
    if message.text in phonebook:
        bot.send_message(message.chat.id, "Name is already in phonebook. Enter another: ")
        bot.register_next_step_handler(message, set_name)
    else:
        global current_contact
        phonebook[message.text] = phonebook[current_contact]
        phonebook.pop(current_contact)
        current_contact = message.text
        bot.send_message(message.chat.id, "Do you want to change another property? (yes|no): ")
        bot.register_next_step_handler(message, edit_contact)


def edit_phones(message):
    if str(message.text).lower() == "no":
        bot.send_message(message.chat.id, "Do you want to change another property? (yes|no): ")
        bot.register_next_step_handler(message, edit_contact)
    elif str(message.text).lower() == "yes":
        bot.send_message(message.chat.id, "Do you want to delete or edit number or add the new one? (del|edit|add): ")
        bot.register_next_step_handler(message, edit_phones)
    elif (str(message.text).lower() == "del" or str(message.text).lower() == "del") \
            and len(phonebook[current_contact]["phone"]) == 0:
        bot.send_message(message.chat.id, "This contact hasn't any phones yes. You can only add! Do you want to "
                                          "continue editing numbers? (yes|no): ")
        bot.register_next_step_handler(message, edit_phones)
    elif str(message.text).lower() == "add":
        bot.send_message(message.chat.id, "Enter additional number for adding: ")
        bot.register_next_step_handler(message, add_phone)
    elif str(message.text).lower() == "del":
        bot.send_message(message.chat.id, "Enter phone for deleting: ")
        bot.register_next_step_handler(message, del_phone)
    elif str(message.text).lower() == "edit":
        bot.send_message(message.chat.id, "Enter phone for editing: ")
        bot.register_next_step_handler(message, edit_phone)
    else:
        bot.send_message(message.chat.id, "This word has no sense! Do you want to change another property? (yes|no):")
        bot.register_next_step_handler(message, edit_contact)

def add_phone(message):
    if is_phone_exists(message.text):
        bot.send_message(message.chat.id, f"Phone is already in phonebook! Add another: ")
        bot.register_next_step_handler(message, add_phone)
    else:
        phonebook[current_contact]["phone"].append(message.text)
        bot.send_message(message.chat.id, f"Phone is added! Do you want more phone changes? (yes|no): ")
        bot.register_next_step_handler(message, edit_phones)


def del_phone(message):
    if message.text not in phonebook[current_contact]["phone"]:
        bot.send_message(message.chat.id, f"This contact doesn't have entered number! Try to enter another: ")
        bot.register_next_step_handler(message, del_phone)
    else:
        phonebook[current_contact]["phone"].remove(message.text)
        bot.send_message(message.chat.id, f"Phone is deleted! Do you want more phone changes? (yes|no): ")
        bot.register_next_step_handler(message, edit_phones)


def edit_phone(message):
    if message.text not in phonebook[current_contact]["phone"]:
        bot.send_message(message.chat.id, f"This contact doesn't have entered number! Try to enter another: ")
        bot.register_next_step_handler(message, edit_phone)
    else:
        bot.send_message(message.chat.id, f"Enter the new phone: ")
        bot.register_next_step_handler(message, set_phone, message.text)


def set_phone(message, old_phone):
    if is_phone_exists(message.text):
        bot.send_message(message.chat.id, f"Phone is already in phonebook! Enter another: ")
        bot.register_next_step_handler(message, set_phone, old_phone)
    else:
        phonebook[current_contact]["phone"].remove(old_phone)
        phonebook[current_contact]["phone"].push(message.text)
        bot.send_message(message.chat.id, f"Phone is replaced! Do you want more phone changes? (yes|no): ")
        bot.register_next_step_handler(message, edit_phones)


@bot.message_handler(commands=['show_all'])
def show_all(message):
    if len(phonebook.keys()):
        contacts_list: str = ""
        for k in phonebook.keys():
            contacts_list += show_contact(k) + "\n\n"
        bot.send_message(message.chat.id, contacts_list)
    else:
        bot.send_message(message.chat.id, "Похоже справочник пуст. Сперва добавьте в него контакты!")


def show_contact(user_name: str):
    contact_str: str = f"{user_name}:"
    for k, v in phonebook[user_name].items():
        if k == "phone" and len(v) > 0:
            if len(v) == 1:
                contact_str += f"\n\t{k}: {v[0]}"
            else:
                for i in range(len(v)):
                    contact_str += f"\n\t{k} {i + 1}: {v[i]}"
        elif k != "phone":
            contact_str += f"\n\t{k}: {v}"
    return contact_str


bot.polling()
