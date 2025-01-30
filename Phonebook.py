import json
import os
import re
from datetime import datetime
import dialogs  # Pythonista specific
import console  # Pythonista specific

contacts = {}

def load_contacts():
    if os.path.exists("contacts.json"):
        with open("contacts.json", "r") as file:
            return json.load(file)
    return {}

def save_contacts():
    with open("contacts.json", "w") as file:
        json.dump(contacts, file)

def format_phone_number(phone):
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Format based on length
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    return phone  # Return original if not matching expected formats

def validate_email(email):
    # Basic email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def parse_vcf(file_path):
    imported_contacts = {}
    current_contact = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            
            if line == 'BEGIN:VCARD':
                current_contact = {}
            elif line == 'END:VCARD':
                if 'FN' in current_contact:  # Only add if we have a name
                    imported_contacts[current_contact['FN']] = current_contact
            elif line:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.split(';')[0]  # Remove any parameters
                    
                    if key == 'FN':
                        current_contact['FN'] = value
                    elif key == 'TEL':
                        current_contact['phone'] = format_phone_number(value)
                    elif key == 'EMAIL':
                        current_contact['email'] = value
                    elif key == 'BDAY':
                        # Convert various date formats to YYYY-MM-DD
                        try:
                            date_obj = datetime.strptime(value, '%Y%m%d')
                            current_contact['birthday'] = date_obj.strftime('%Y-%m-%d')
                        except ValueError:
                            pass
    
    return imported_contacts

def import_vcf():
    # Using Pythonista's file picker
    file_paths = dialogs.pick_document(types=['public.vcard'])
    
    if file_paths:
        try:
            imported = parse_vcf(file_paths)
            if imported:
                contacts.update(imported)
                save_contacts()
                console.hud_alert(f'Imported {len(imported)} contacts!', 'success', 1.5)
            else:
                console.hud_alert('No valid contacts found', 'error', 1.5)
        except Exception as e:
            console.hud_alert(f'Import failed: {str(e)}', 'error', 1.5)
    else:
        console.hud_alert('Import cancelled', 'error', 1.5)

def main_menu():
    while True:
        # Clear screen (Pythonista specific)
        console.clear()
        
        print("\nPhone Book Menu:")
        print("1. Add New Contact")
        print("2. Look Up Contact")
        print("3. Delete Contact")
        print("4. Show All Contacts")
        print("5. Import VCF File")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            saved_name = add_contact()
            stored_contact(saved_name)
        elif choice == "2":
            lookup_contact()
        elif choice == "3":
            delete_contact()
        elif choice == "4":
            contacts_list()
        elif choice == "5":
            import_vcf()
        elif choice == "6":
            console.hud_alert('Goodbye!', 'success', 1.5)
            break
        else:
            console.hud_alert('Invalid choice!', 'error', 1.5)
        
        if choice != "6":
            input("\nPress Enter to continue...")

def format_contact(name, details):
    formatted = f"Name: {name}\n"
    if 'phone' in details:
        formatted += f"Phone: {details['phone']}\n"
    if 'email' in details:
        formatted += f"Email: {details['email']}\n"
    if 'birthday' in details:
        formatted += f"Birthday: {details['birthday']}\n"
    formatted += "-" * 30
    return formatted

def add_contact():
    # Using Pythonista's form dialog with text fields instead of specialized types
    fields = [
        {'type': 'text', 'key': 'name', 'title': 'Name'},
        {'type': 'text', 'key': 'phone', 'title': 'Phone Number'},
        {'type': 'text', 'key': 'email', 'title': 'Email (optional)'},
        {'type': 'text', 'key': 'birthday', 'title': 'Birthday (YYYY-MM-DD, optional)'}
    ]
    
    result = dialogs.form_dialog(title='Add Contact', fields=fields)
    
    if result:
        name = result['name'].strip()
        if not name:  # Check if name is empty
            console.hud_alert('Name is required!', 'error', 1.5)
            return None
            
        if name in contacts:
            if not dialogs.alert('Contact Exists', 
                               f'Overwrite {name}?', 
                               'Yes', 'No'):
                return None
        
        contact_info = {}
        
        # Phone
        phone = result['phone'].strip()
        if phone:
            contact_info['phone'] = format_phone_number(phone)
        else:
            console.hud_alert('Phone number is required!', 'error', 1.5)
            return None
        
        # Email
        if result['email']:
            email = result['email'].strip()
            if validate_email(email):
                contact_info['email'] = email
            else:
                console.hud_alert('Invalid email format', 'error', 1.5)
        
        # Birthday
        if result['birthday']:
            birthday = result['birthday'].strip()
            if validate_date(birthday):
                contact_info['birthday'] = birthday
            else:
                console.hud_alert('Invalid date format', 'error', 1.5)
        
        contacts[name] = contact_info
        save_contacts()
        return name
    
    return None

def stored_contact(name):
    if name:
        console.hud_alert(f'{name} saved!', 'success', 1.5)

def contacts_list():
    if not contacts:
        console.hud_alert('No contacts found!', 'error', 1.5)
        return
    
    console.clear()
    print("\n=== Phone Book Contacts ===")
    for name, details in sorted(contacts.items()):
        print(f"\n{format_contact(name, details)}")

def lookup_contact():
    if not contacts:
        console.hud_alert('No contacts found!', 'error', 1.5)
        return
    
    # Using input() instead of text_dialog
    console.clear()
    print("\nSearch Contacts")
    search_term = input("Enter name to search (or part of name): ").strip().lower()
    
    if search_term:
        found_contacts = {}
        for name, details in contacts.items():
            if search_term in name.lower():
                found_contacts[name] = details
        
        console.clear()
        if found_contacts:
            print("\n=== Found Contacts ===")
            for name, details in found_contacts.items():
                print(f"\n{format_contact(name, details)}")
        else:
            console.hud_alert(f'No matches for "{search_term}"', 'error', 1.5)
    else:
        console.hud_alert('Search cancelled', 'error', 1.5)

def delete_contact():
    if not contacts:
        console.hud_alert('No contacts to delete!', 'error', 1.5)
        return
    
    # Create a list of contacts for the picker
    contact_list = sorted(contacts.keys())
    selected = dialogs.list_dialog(title='Select Contact to Delete',
                                 items=contact_list)
    
    if selected:
        if dialogs.alert('Confirm Delete', 
                        f'Delete {selected}?', 
                        'Delete', 'Cancel'):
            del contacts[selected]
            save_contacts()
            console.hud_alert(f'{selected} deleted!', 'success', 1.5)
        else:
            console.hud_alert('Deletion cancelled', 'error', 1.5)

# Load contacts from file at the start
contacts = load_contacts()

# Call the main menu when the script starts
if __name__ == "__main__":
    console.clear()
    main_menu()