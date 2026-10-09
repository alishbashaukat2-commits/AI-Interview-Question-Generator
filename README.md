# AI Interview Question Generator 🎯

## 📌 Project Overview

The **AI Interview Question Generator** is a Python-based project developed as Task 4 of a remote internship. It helps prepare technical and behavioral interview questions for internship candidates using candidate profiles, job descriptions, and an existing question bank.

The system allows users to select a candidate, choose a job role, and set the interview difficulty level. It also analyzes matched and missing skills to highlight potential learning areas.

## 🎯 Objectives

* Generate technical and behavioral interview questions.
* Use candidate profiles and job descriptions as input.
* Support Easy, Medium, and Hard difficulty levels.
* Identify matched skills and missing job-related skills.
* Integrate a pre-trained text-generation model.
* Display a structured interview question set.

## 🛠️ Technologies Used

* **Python** — Main programming language
* **Pandas** — Data loading and processing
* **Hugging Face Transformers** — Model integration
* **Google FLAN-T5 Small** — Pre-trained text-to-text model
* **CSV** — Dataset storage
* **Visual Studio Code** — Development environment

## 📂 Project Structure

```text
AI-Interview-Question-Generator/
│
├── AI-Interview-Question-Generator.py
├── question_bank.csv
├── intern_profiles.csv
├── job_descriptions.csv
├── AI_Interview_Question_Generator_Report.pdf
└── README.md
```

## 📊 Datasets

The project uses three CSV datasets:

### 1. Question Bank

`question_bank.csv`

Contains existing interview questions organized by difficulty level:

* Easy
* Medium
* Hard

### 2. Intern Profiles

`intern_profiles.csv`

Contains candidate information, including:

* Candidate ID
* Education
* Skills
* Projects
* Experience level

### 3. Job Descriptions

`job_descriptions.csv`

Contains internship job information, including:

* Job ID
* Job title
* Required skills
* Responsibilities

## ⚙️ How It Works

1. Load the required CSV datasets.
2. Select an intern using their candidate ID.
3. Select an internship using its job ID.
4. Choose the interview difficulty level.
5. Display the candidate profile and job description.
6. Compare candidate skills with job requirements.
7. Identify matched skills and missing learning areas.
8. Load the pre-trained FLAN-T5 Small model.
9. Prepare technical questions using the question bank and text-generation workflow.
10. Prepare behavioral questions using predefined templates.
11. Display five technical and five behavioral questions.

## ✨ Key Features

* Candidate selection using unique IDs
* Job-role selection
* Three difficulty levels
* Candidate skill-gap analysis
* Technical interview question preparation
* Behavioral interview question preparation
* Structured results and execution summary

## 💻 Installation and Usage

### Step 1: Install Python

Install Python if it is not already available on your computer.

### Step 2: Install Required Libraries

Open a terminal in the project folder and run:

```bash
pip install pandas transformers torch sentencepiece
```

### Step 3: Run the Program

Execute:

```bash
python AI-Interview-Question-Generator.py
```

### Step 4: Follow the Prompts

* Select a candidate ID.
* Select a job ID.
* Choose a difficulty level.
* Review the skill analysis and generated interview questions.

**Note:** The first model run may require an internet connection to download the model files from Hugging Face. Subsequent runs may use the locally cached model.

## 🧪 Sample Test

**Candidate ID:** INT009

**Education:** BS Software Engineering

**Skills:** Python, SQL, Testing, Git

**Job Role:** NLP Intern

**Difficulty:** Easy

The program identifies matched and missing skills and displays five technical and five behavioral interview questions.

## ⚠️ Limitations

* Some technical questions may be general rather than fully specific to the selected job.
* Model-generated output may occasionally be unsuitable.
* Existing question-bank questions are used as a fallback when necessary.
* Behavioral questions currently use predefined templates.
* Question quality has not been formally evaluated.

## 🚀 Future Improvements

* Improve job-specific question relevance.
* Expand the technical and behavioral question banks.
* Improve prompts for more reliable text generation.
* Add a graphical user interface.
* Add an option to export generated questions.
* Evaluate question relevance across different job roles and difficulty levels.

## 📄 Project Report

The detailed project report is available in:

`AI_Interview_Question_Generator_Report.pdf`

## 👩‍💻 Author

**Alishba Shaukat**
BS Artificial Intelligence Student

## 📝 Acknowledgment

This project was developed as part of a remote internship task to explore AI-assisted interview preparation using structured data and a pre-trained language model.
