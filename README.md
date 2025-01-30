# Enhanced Phone Book Application

A Python-based phone book application built for Pythonista 3 on iOS/iPadOS. This application allows you to manage contacts with multiple fields and supports VCF file imports.

## Features

- Add contacts with multiple fields:
  - Name
  - Phone number (automatically formatted)
  - Email (with validation)
  - Birthday
- Search contacts by name
- View all contacts in a formatted list
- Delete contacts
- Import contacts from VCF files
- Data persistence using JSON storage

## Requirements

- Pythonista 3 for iOS/iPadOS
- Required modules (all included in Pythonista 3):
  - json
  - os
  - re
  - datetime
  - dialogs
  - console

## Installation

1. Open Pythonista 3
2. Create a new Python file
3. Copy the entire code into the file
4. Save the file (e.g., as `phonebook.py`)

## Usage

### Running the Application

1. Open the script in Pythonista 3
2. Tap the play button or run the script
3. Use the numbered menu to access different features

### Menu Options

1. **Add New Contact**
   - Enter name (required)
   - Enter phone number (required, automatically formatted)
   - Enter email (optional, validated)
   - Enter birthday (optional, YYYY-MM-DD format)

2. **Look Up Contact**
   - Search by full name or partial name
   - Displays all matching contacts

3. **Delete Contact**
   - Select contact from list
   - Confirm deletion

4. **Show All Contacts**
   - Displays all contacts in a formatted list
   - Sorted alphabetically by name

5. **Import VCF File**
   - Select a VCF file using the document picker
   - Automatically imports contacts

6. **Exit**
   - Saves and exits the application

## Data Storage

- Contacts are stored in a `contacts.json` file
- The file is automatically created in the same directory as the script
- Data persists between sessions

## Phone Number Format

Phone numbers are automatically formatted as:
- XXX-XXX-XXXX (for 10-digit numbers)
- X-XXX-XXX-XXXX (for 11-digit numbers starting with 1)

## VCF Import Support

The application supports importing VCF (vCard) files with the following fields:
- Full Name (FN)
- Telephone (TEL)
- Email (EMAIL)
- Birthday (BDAY)

## Error Handling

- Validates email format
- Validates date format
- Checks for required fields
- Provides clear error messages
- Confirms before overwriting existing contacts
```​​​​​​​