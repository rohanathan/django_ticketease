# 🎟️ TicketEase - Event & Movie Booking System

## 📌 About
A Django-based ticket booking system that allows users to book **movies & events** with payment integration and email notifications.

## 🚀 Features
- User authentication (registration, login, password reset)
- Movie booking with seat selection (grid-based)
- Event booking with seat categories
- Secure **Stripe** payments & refunds
- Email notifications for bookings, cancellations
- Admin panel for managing bookings & sales reports

---

### **🔧 Step-by-Step Developer Setup Guide**

This guide is **detailed** and will ensure that anyone can set up the project smoothly. Follow **each step carefully**:

---

## **📌 1️⃣ Install Poetry (If Not Installed)**

Before running any command, **Poetry must be installed**. If it's not installed, follow this:

### **🔹 Install Poetry**

Run this in **your terminal**:


`curl -sSL https://install.python-poetry.org | python3 -`

### **🔹 Verify Installation**

To check if Poetry is installed, run:


`poetry --version`

**✅ Output should be something like:**


`Poetry 1.8.0`

If Poetry is installed, **proceed to the next step.**

---

## **📌 2️⃣ Clone the Project**

Go to a folder where you want to keep the project and **clone the repository**:


`git clone https://2980262S@dev.azure.com/2980262S/ticketease/_git/ticketease`
`cd ticketease`

✅ **Ensure that you are inside the `ticketease` project folder before proceeding.**

---

## **📌 3️⃣ Setup Virtual Environment**

Poetry uses **virtual environments** to manage dependencies.

### **🔹 Create & Activate Virtual Environment**

Run:


`poetry install`

✅ **This will automatically create a virtual environment and install all required dependencies.**

If you face **any issues** like `poetry not found`, restart the terminal and try again.

---

## **📌 4️⃣ Activate the Virtual Environment**

Before running Django commands, **activate the virtual environment**:


`poetry shell`

✅ **Once activated, your terminal should show something like this:**


`(ticketease-py3.12) user@hostname:~/ticketease$`

This means you are inside the virtual environment. **Now, all commands must be run inside this shell.**


## Install Docker Desktop
brew install --cask docker

After installation, open Docker Desktop and enable it to start at login.

## Install Poetry

brew install poetry

## Starting the Containers
Run the following command to build and start the containers:

docker-compose up --build

Verify Services are Running

docker ps