# miniERP
Your Organization's Laptop Administration, Made Easy.

[![miniERP CI](https://github.com/9akashnp8/mini-ERP/actions/workflows/main.yaml/badge.svg)](https://github.com/9akashnp8/mini-ERP/actions/workflows/main.yaml)

## About
---
miniERP, a Free and Opensource web application to easily manage the laptops at your organization covering the following areas:

1. **Onboarding**: Add new employees and assign them laptops based on the available laptops at the respective branch.
2. **Replacement**: Process Laptop Replacement requests where existing laptops assigned to the employee are returned and new one's assigned based on the availability at the branch. 
3. **Employee Exit**: Process the exit of employees with emphasis on return of the laptop assigned to them.

## Features
---
- Edit History Tracking
- Employee Self Service Portal
- Auto Generated Hardware ID
- API Integration
- ...

## Installation
---
1. Set up & Activate virtual environment

   ```
   1. python -m venv venv
   2. cd venv
   3. Scripts\activate.bat
   4. cd ..
   ```
2. Install All requirements

    ```
    pip install -r requirements.txt
    ```
3. Run the server

    ```
    python manage.py runserver
    ```