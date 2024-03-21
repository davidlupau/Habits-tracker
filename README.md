# MindMold: Your Personal Habit Tracker App

## What is MindMold?
MindMold is a user-friendly command-line interface (CLI) application designed to help individuals cultivate and maintain beneficial habits. It simplifies the process of habit tracking, enabling users to create, monitor, and analyze their habits over time. With MindMold, users can easily manage their daily routines and work towards achieving their personal growth goals.

### Features
* __Create Habits__: Add new habits with names and periodicities.
* __View Habits__: See a list of all your habits and their details.
* __Update Habits__: Change the details of an existing habit.
* __Complete Habits__: Mark habits as completed and track your progress.
* __Analyze Habits__: Analyze your habits with comprehensive streak data.
* __Predefined Demos__: View demo analyses using predefined habits.

## Installation
To install the app, you need Python installed on your machine. Verify it's installed on your system by running the below command in your terminal.
```shell
python --version
```
If not, download and install it from python.org. Then, you can install the required dependencies by running:
```shell
pip install -r requirements.txt
```

## Usage
To start the application, navigate to the app directory in your terminal and run:
```shell
python main.py
```
You will be greeted with a welcome message and a main menu. Navigate through the options by entering the corresponding number for each action you want to perform. The app is interactive and will guide you through each step needed to manage your habits.

## Testing
MindMold utilizes pytest for running its suite of tests to ensure functionality and reliability. Follow these steps to install pytest and run the tests:
### Installing pytest
pytest is a powerful testing framework for Python that makes it easy to write simple and scalable test cases. If you haven't already installed pytest, you can do so by running the following command in your terminal:
```shell
pip install pytest
```
This command installs pytest and any dependencies required to run your tests.

### Running Tests
Once pytest is installed, you can run the tests for MindMold to ensure everything is working as expected. Navigate to the project directory in your terminal and run:
```shell
pytest .
```
This command searches for test files in your project directory, runs the tests, and reports the outcomes in the terminal. 