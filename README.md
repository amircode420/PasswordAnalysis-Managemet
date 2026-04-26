-----THIS IS THE README FOR PASSWORD ANALYSIS AND MANAGEMENT TOOL-----

# PASSWORD ANALYSIS AND MANAGEMENT TOOL

## Introduction
The Password analysis and management tool is a tool that can be used for
-**Password Analysis**
-**Password Generation**
-**Storing Passwords in an Encrypted Password Vault**
This tool is local and built using **Python's PyQT5** and **SQLite**.

## Installation

To get started with this application please install the required dependencies 

```bash
git clone https://github.com/amircode420/PasswordAnalysis-Management.git
```

After cloning the repository, change your directory into the file

```bash
cd PasswordAnalysis-Management
```

After that,

```bash
pip install -r requirements.txt
```

After installing the dependencies, run the following command

```bash
python main.py 
```

This will launch the application on your desktop and you can start using it.

## This application consists of 3 Main Features.

- The Password Analyzer
- The Password Generator
- The Encrypted Password Vault

--- PASSWORD ANALYZER ---
On launching, you can access the Password analyzer, 
where the application will analyze your password, give you a few basic information, 
Check the password against patterns to ensure it is strong and provide recommendation to improve the password if needed.

--- PASSWORD GENERATOR ---
The user can click on the "Password Generator" button at the bottom left corner of the main application.
which pops up a window and allows the user to generate a password based on the length they prefer. 
The user can copy the password and use it for their purposes.

--- ENCRYPTED PASSWORD VAULT ----
The user can access the vault by clicking the "Password Vault" Button in the bottom right corner of the main application.
The Vault prompts up the One Time Master Password Setup window where the user can create their master password.
Once the Master Password is created, the application also creates the vault.
The user can click on the "Password Vault" Button again and the Login window pops up, prompting user to enter their master password.

After login, The user can see their Credentials in a tabular format.

--- Adding Credentials to the Vault ---
Users can find the "Add Credentials" button at the bottom of the credentials table. This opens another window that allows the user to enter 
their information such as;

- Service 
- Username/Email used in the servicie
- Password

After entering these details, the user can click "Save" and the credentials will be loaded into the table.
The users can copy the passwords from the table and use it in the respected services.

--- NOTE ----

The passwords are encrypted at all times except when the vault is unlocked. 
This secures the user's password in the Encrypted Vault.

--- UPDATES ----

There will be further updates to this application in the future.

------------------------------------------------------------------------------------------------------------------------------------------------------------