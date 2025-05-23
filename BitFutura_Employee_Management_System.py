# -*- coding: utf-8 -*-
"""PDWD-PFS-0325-Project-Implementation.ipynb
TAN WESLEY PDWD-PFS-0325-A03

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Uqj1iOz2HWEffz1DhRGUi0dlSd0Wq9HL

### Algorithm for Employee Management System

#### Step 1: Define Classes

1. **Class Employee**
    - **Attributes**:
        - `emp_id`: Employee ID
        - `name`: Employee Name
        - `department`: Employee Department
        - `salary`: Employee Salary
        - `contact`: Employee Contact Details
    - **Methods**:
        - `__init__(self, emp_id, name, department, salary, contact)`: Constructor to initialize the employee attributes.
        - `__str__(self)`: Returns a string representation of the employee details.

2. **Class EmployeeManagementSystem**
    - **Attributes**:
        - `employees`: List to store employee objects
    - **Methods**:
        - `__init__(self)`: Constructor to initialize the employees list.
        - `add_employee(self)`: Method to add a new employee.
        - `view_employee(self)`: Method to view an employee by ID.
        - `update_employee(self)`: Method to update an employee by ID.
        - `delete_employee(self)`: Method to delete an employee by ID.
        - `list_all_employees(self)`: Method to list all employees.
        - `department_wise_report(self)`: Method to generate a department-wise report.
        - `main_menu(self)`: Method to display the main menu and prompt user choices.

#### Step 2: Implement Methods


#### Step 3: Execution

1. Create an instance of `EmployeeManagementSystem`.
2. Call `main_menu` method to start the program.

### Pseudocode

```
Class Employee:
    Attributes:
        emp_id, name, department, salary, contact
    Methods:
        __init__(self, emp_id, name, department, salary, contact):
            Initialize attributes
        __str__(self):
            Return string representation of employee details

Class EmployeeManagementSystem:
    Attributes:
        employees (list)
    Methods:
        __init__(self):
            Initialize employees list
        add_employee(self):
            Prompt for employee details
            Create Employee object
            Add to employees list
        view_employee(self):
            Prompt for employee ID
            Search and display employee details
        update_employee(self):
            Prompt for employee ID
            Search and prompt for new details
            Update employee details
        delete_employee(self):
            Prompt for employee ID
            Remove employee from list
        list_all_employees(self):
            Iterate and display employee details
        department_wise_report(self):
            Create dictionary for departments
            Group employees by department
            Display department-wise report
        main_menu(self):
            While True:
                Display menu options
                Prompt for user choice
                Call corresponding method
                Exit if chosen

Start:
    Create instance of EmployeeManagementSystem
    Call main_menu method
```
"""

# Importing necessary modules
import os      # For file existence check
import re      # For regex validation
import csv     # For reading/writing CSV files
from send_email import EmailSender # SMTP and email-related imports
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart


# -1- File Handling Configuration ---
FILE_NAME = "employees.csv" # Name of the CSV file to persist data
DELIMITER = ","             # Delimiter used in CSV
EMPLOYEE_KEYS = ["ID", "Name", "Department", "Salary", "Contact"]  # CSV headers

# -2- Validation Helper Functions ---
def validate_employee_id(emp_id):
    """Validates employee ID starts with 'E' and has 8 digits."""
    return bool(re.fullmatch(r"E\d{8}", emp_id)) # Checks for 'E' followed by 8 digits

def validate_name(name):
    """Validates name (only letters and spaces, max 20 chars)."""
    return bool(re.fullmatch(r"[A-Za-z ]{1,20}", name)) # Only alphabets and spaces, up to 20 characters

def validate_department(department):
    """Validates department (only letters and spaces, max 20 chars)."""
    return bool(re.fullmatch(r"[A-Za-z ]{1,20}", department))

def validate_salary(salary):
    """Validates salary (digits only)."""
    return salary.isdigit() # Accepts only digits (e.g., no decimals)

def validate_contact(contact):
    """Validates email format and max 20 characters."""
    return bool(re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", contact)) and len(contact) <= 20


# -3- # --- Employee Class ---
class Employee:
    """Class to represent an Employee"""

    def __init__(self, emp_id, name, department, salary, contact):
        # Initialize employee attributes
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.salary = float(salary) # Stored as float for calculations
        self.contact = contact
    
    def __str__(self):
        # Return a string representation of the employee details
        return (f"ID: {self.emp_id}\nName: {self.name}\nDepartment: {self.department}\n"
                f"Salary: ${self.salary:.2f}\nContact: {self.contact}\n" + "-"*40)

    def to_dict(self):
        # Return a dictionary of the employee details
        # Converts the object to a dict for CSV writing
        return { 
            "ID": self.emp_id,
            "Name": self.name,
            "Department": self.department,
            "Salary": f"{self.salary:.2f}",
            "Contact": self.contact
        }

# -4- # --- Employee Management System Class ---
class EmployeeManagementSystem:
    """Class to manage employees"""
    def __init__(self):
        # Initialize the list to store employees
        # Loads employee records on startup
        self.employees = self.load_employees()
        ## Use app password from Gmail [point to send_email.py]
        self.email_sender = EmailSender("wt.wn01@gmail.com", "kejl uxmj ohhg ujhr") # Use app password from Gmail

    # -1- File Operations ---
    def load_employees(self):
        """Load employees from CSV file."""
        employees = []
        if os.path.exists(FILE_NAME):
            try:
                with open(FILE_NAME, 'r', newline='') as f:
                    reader = csv.DictReader(f, delimiter=DELIMITER)
                    for row in reader:
                        if set(row.keys()) >= set(EMPLOYEE_KEYS): # Ensure valid headers
                            emp = Employee(row['ID'], row['Name'], row['Department'], row['Salary'], row['Contact'])
                            employees.append(emp)
                print(f"Loaded {len(employees)} employee records.")
            except Exception as e:
                print(f"Error loading employees: {e}")
        else:
            print("No existing employee data found")
        return employees

    def save_employees(self):
        """Save employees to CSV file."""
        try:
            with open(FILE_NAME, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=EMPLOYEE_KEYS, delimiter=DELIMITER)
                writer.writeheader()
                for emp in self.employees:
                    writer.writerow(emp.to_dict())
        except Exception as e:
            print(f"Error saving employees: {e}")

    def find_employee_by_id(self, emp_id):
        return next((emp for emp in self.employees if emp.emp_id == emp_id), None)


    def add_employee(self):
        """Add a new employee with unique ID and email validation, with confirmation before saving."""
        try:
            # Prompt and validate employee ID
            emp_id = input("Enter Employee ID (Format: E12345678): ").strip()
            if not validate_employee_id(emp_id):
                print("Invalid Employee ID format.")
                return

            # Check for duplicate employee ID
            if self.find_employee_by_id(emp_id):
                print("Employee ID already exists.")
                return 

            # Prompt and validate name
            name = input("Enter Name: ").strip()
            if not validate_name(name):
                print("Invalid Name.")
                return

            # Prompt and validate department
            dept = input("Enter Department: ").strip()
            if not validate_department(dept):
                print("Invalid Department")
                return

            # Prompt and validate salary
            salary = input("Enter Salary: ").strip()
            if not validate_salary(salary):
                print("Invalid Salary")
                return

            # Prompt and validate contact email
            contact = input("Enter Contact Email: ").strip()
            if not validate_contact(contact) or any(emp.contact.lower() == contact.lower() for emp in self.employees):
                print("Invalid or duplicate Contact Email.")
                return

            # Show a preview before confirmation
            print("\n📋 Review Employee Details:")
            print(f"ID: {emp_id}")
            print(f"Name: {name}")
            print(f"Department: {dept}")
            print(f"Salary: ${float(salary):.2f}")
            print(f"Contact: {contact}")
            print("-" * 40)

            # Ask for user confirmation
            confirm = input("⚠️ Confirm add this employee? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("Employee addition cancelled.")
                return

            # Create and store new employee
            new_emp = Employee(emp_id, name, dept, salary, contact)
            self.employees.append(new_emp)
            self.save_employees()
            print("Employee added successfully.")

            # Send confirmation email
            subject = f"Welcome to the Company, {name}!"
            body = (
                f"Hi {name},\n\n"
                f"Your employee ID is {emp_id}.\n"
                f"You have been successfully added to the system under the {dept} department.\n"
                f"Your registered email is {contact}.\n\n"
                "Thank you,\nHR Department"
            )
            self.email_sender.send_email(name, contact, subject, body)

        except Exception as e:
            print(f"Error adding employee: {e}")


    def view_employee(self):
        """
        Prompts for an employee ID and displays their details if found.
        """
        try:
        # Prompt for employee ID
            emp_id = input("Enter Employee ID to view: ").strip()
        
            # Optional: Validate ID format
            if not validate_employee_id(emp_id):
                print("Invalid Employee ID format.")
                return

            # Attempt to find the employee record
            emp = self.find_employee_by_id(emp_id)

            # If employee is found, prompt for confirmation
            if emp:
                confirm = input(f"⚠️ View report for employee '{emp_id}'? (yes/no): ").strip().lower()
                if confirm != "yes":
                    print("❎ Report cancelled by user.")
                    return
                # Show employee details
                print("\n Employee Details:")
                print(emp)
            else:
                # Inform user if no employee is found
                print("Employee not found.")

        except Exception as e:
            # Handle any unexpected errors gracefully
            print(f"Error viewing employee: {e}")


    def update_employee(self):
        """Update an employee's details with validation and confirmation before saving."""
        try:
            # Ask user to input the Employee ID to update
            emp_id = input("Enter Employee ID to update: ").strip()

            # Search for employee object using the given ID
            emp = self.find_employee_by_id(emp_id)

            # If employee not found, exit the method
            if not emp:
                print("Employee not found.")
                return

            # Display current employee details using __str__ method
            print("\nCurrent Employee Details:")
            print(emp)

            ## Ask for confirmation before proceeding with the update
            confirm_initial = input("⚠️ Do you want to proceed with updating this employee? (yes/no): ").strip().lower()
            if confirm_initial != "yes":
                print("❎ Update cancelled by user.")
                return 

            # Prompt user for new values (leave blank to retain old value)
            new_name = input(f"New name [{emp.name}]: ").strip()
            new_dept = input(f"New department [{emp.department}]: ").strip()
            new_salary = input(f"New salary [{emp.salary}]: ").strip()
            new_contact = input(f"New email [{emp.contact}]: ").strip()

            # Create a temporary updated employee object with new/old values
            updated_emp = Employee(
                emp_id=emp.emp_id,  # Keep original ID
                name=new_name if new_name else emp.name,
                department=new_dept if new_dept else emp.department,
                salary=new_salary if new_salary else emp.salary,
                contact=new_contact if new_contact else emp.contact
            )

            # --- VALIDATION SECTION ---
            # Validate new name if provided
            if new_name and not validate_name(new_name):
                print("Invalid name format.")
                return

            # Validate new department if provided
            if new_dept and not validate_department(new_dept):
                print("Invalid department format.")
                return

            # Validate new salary if provided
            if new_salary and not validate_salary(new_salary):
                print("Invalid salary input.")
                return

            # Validate new contact email if provided
            if new_contact:
                if not validate_contact(new_contact):
                    print("Invalid email format.")
                    return

                # Ensure new contact is not used by another employee
                if any(e.contact.lower() == new_contact.lower() and e.emp_id != emp.emp_id for e in self.employees):
                    print("Email already exists for another employee.")
                    return

            # Show updated employee preview
            print("\n📋 Preview of Updated Information:")
            print(updated_emp)

            # Ask for confirmation before saving
            confirm = input("⚠️ Save these changes? (yes/no): ").strip().lower()
            if confirm == "yes":
                # Apply validated changes to the original employee object
                emp.name = updated_emp.name
                emp.department = updated_emp.department
                emp.salary = float(updated_emp.salary)  # Ensure salary is float
                emp.contact = updated_emp.contact

                # Save all employees to file
                self.save_employees()
                print(f"Employee {emp_id} updated successfully.")
            else:
                print("Update cancelled.")
        except Exception as e:
            # Catch unexpected errors
            print(f"Error updating employee: {e}")

    def delete_employee(self):
        """Delete an employee based on ID with confirmation."""
        try:
            # Prompt the user to enter the Employee ID they wish to delete
            emp_id = input("Enter Employee ID to delete: ").strip()

            # Attempt to find the employee object from the list using a helper method
            emp = self.find_employee_by_id(emp_id)

            # If no matching employee is found, inform the user and exit
            if not emp:
                print("Employee not found.")
                return
            
            # First confirmation: does user want to continue after finding the employee
            confirm_view = input("⚠️ Do you want to view and proceed with deletion? (yes/no): ").strip().lower()
            if confirm_view != "yes":
                print("❎ Deletion cancelled by user.")
                return

            # Display the found employee's current details using __str__ method
            print("\n Employee Found:")
            print(emp)

            # Second confirmation before final deletion
            confirm_delete = input("⚠️ Are you sure you want to delete this employee? (yes/no): ").strip().lower()
            if confirm_delete == "yes":
                # Remove the employee object from the employees list
                self.employees.remove(emp)

                # Save the updated list to the CSV file
                self.save_employees()

                # Provide feedback that deletion was successful
                print(f"Employee {emp_id} deleted successfully.")
            else:
                # If user does not confirm, cancel the operation
                print("Deletion cancelled.")
            
        except Exception as e:
            # Catch any unexpected runtime errors and display them
            print(f"Error deleting employee: {e}")

    def list_all_employees(self):
        """List all employees in the system."""
        try:
            # Check if the employees list is empty
            if not self.employees:
                print("⚠️ No employees found.")
                return
            
            # Ask for confirmation before displaying the list
            confirm = input("⚠️ View all employee records? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("❎ Listing cancelled by user.")
                return
            
            # Display header
            print("\n All Employee Records")
            print("=" * 40)

            # Loop through each employee object and print using __str__ method
            for emp in self.employees:
                print(emp)  # __str__ in Employee class handles formatting

        except Exception as e:
            # Handle any unexpected errors
            print(f"Error listing all employees: {e}")

    def department_wise_report(self):
        """Generate a report for a specific department, showing all employees and total salary."""
        try:
            # Prompt user for department name to search
            dept_name = input("Enter department to filter: ").strip().lower()

            # Filter employees matching the department (case-insensitive)
            matching_employees = [emp for emp in self.employees if emp.department.lower() == dept_name]

            # Check if any employees found in the department
            if not matching_employees:
                print(" No employees found in that department.")
                return
            
            # Ask for confirmation before displaying the report
            confirm = input(f"⚠️ View report for department '{dept_name.title()}'? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("❎ Report cancelled by user.")
                return
        
            # Proceed to print department report header
            print(f"\n Employees in Department: {dept_name.title()}")
            print("=" * 40)

            # Initialize total salary
            total_salary = 0.0

            # Display each employee and accumulate salary
            for emp in matching_employees:
                print(emp)
                total_salary += emp.salary

            # Display total salary budget for the department
            print("=" * 40)
            print(f"Total Budgeted Salary for '{dept_name.title()}': ${total_salary:.2f}")

        except Exception as e:
            print(f"Error generating department-wise report: {e}")

    
    def main_menu(self):
        """Main function to run the Employee Management System."""
        while True:
            # Display menu options
            print("\nEmployee Management System")
            print("1. Add Employee")
            print("2. View Employee")
            print("3. Update Employee")
            print("4. Delete Employee")
            print("5. List All Employees")
            print("6. Department Wise Report")
            print("7. Exit")
            # Get user choice
            choice = input("Enter your choice: ")

            # Call the corresponding function based on user choice
            if choice == '1':
                self.add_employee()
            elif choice == '2':
                self.view_employee()
            elif choice == '3':
                self.update_employee()
            elif choice == '4':
                self.delete_employee()
            elif choice == '5':
                self.list_all_employees()
            elif choice == '6':
                self.department_wise_report()
            elif choice == '7':
                print("Exiting the system.")
                break
            else:
                print("Invalid choice! Please try again.")

# Start the program
if __name__ == "__main__":
    ems = EmployeeManagementSystem()
    ems.main_menu()