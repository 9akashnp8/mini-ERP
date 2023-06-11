# miniERP
Your Departmental Routine Tasks, Made Easy.

[![minitests](https://github.com/9akashnp8/mini-ERP/actions/workflows/main.yaml/badge.svg)](https://github.com/9akashnp8/mini-ERP/actions/workflows/main.yaml)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

# About
---
miniERP, a Free and Opensource web application to make easy managing your department by automating and simplifying most routine tasks:

1. Laptop & Employee Managemention
   1. **Onboarding**: Add new employees and assign them laptops based on the available laptops at the respective branch/location.
   2. **Replacement**: Process Laptop Replacement requests where existing laptops assigned to the employee are returned and new one's assigned based on the availability at the branch. 
   3. **Employee Exit**: Process the exit of employees with emphasis on return of the laptop assigned to them.
2. Finance Management
   1. **Manage Services**: Manage the external services being used by the department
   2. **Journal Transactions**: Record payments being made to the services
   3. **Due Reminders**: Automatic & Timely payment due reminders
   4. **Payment Confirmation Mail**: Automatic Payment Complete mail that can be sent to the Finance Dept.

# Features
---
- Free & Open Source
- Built with Django
- REST APIs via DRF for 3rd party integrations
- and much more...

# Installation (Docker)
---
```
git clone https://github.com/9akashnp8/mini-ERP.git
cd mini-ERP
docker-compose build
docker-compose up
```

# Installation (Standard)
---
1. Clone the repo
    ```
    git clone https://github.com/9akashnp8/mini-ERP.git
    cd mini-ERP
    ```
2. Set up & Activate virtual environment

   ```
   1. python -m venv venv
   2. cd venv
   3. Scripts\activate.bat
   4. cd ..
   ```
3. Install All requirements

    ```
    pip install -r requirements.txt
    ```
4. Run Migrations & Run the server

    ```
    python manage.py migrate
    python manage.py runserver
    ```

# Resources
- Docs: *Work In Progress*
- React Front End: *Work In Progress*, [miniERP-next.js](https://github.com/9akashnp8/miniERP-next.js)