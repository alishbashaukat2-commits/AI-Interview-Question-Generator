import pandas as pd
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# ============================================================
# 1. FILES
# ============================================================

QUESTION_BANK_FILE = "question_bank.csv"
INTERN_FILE = "intern_profiles.csv"
JOB_FILE = "job_descriptions.csv"

MODEL_NAME = "google/flan-t5-small"


# ============================================================
# 2. LOAD DATA
# ============================================================

print("\nLoading datasets...")

question_bank = pd.read_csv(QUESTION_BANK_FILE)
intern_profiles = pd.read_csv(INTERN_FILE)
job_descriptions = pd.read_csv(JOB_FILE)

print("Question Bank:", question_bank.shape)
print("Intern Profiles:", intern_profiles.shape)
print("Job Descriptions:", job_descriptions.shape)


# ============================================================
# 3. HELPER FUNCTIONS
# ============================================================

def clean_text(text):
    if pd.isna(text):
        return ""

    return str(text).strip()


def normalize(text):
    text = clean_text(text).lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_values(text):
    """
    Converts:
    Python; Pandas; NumPy
    into a list.
    """

    if not text:
        return []

    values = re.split(r"[;,|]", clean_text(text))

    return [
        value.strip()
        for value in values
        if value.strip()
    ]


def find_column(data, names):

    normalized_columns = {
        normalize(column): column
        for column in data.columns
    }

    # Exact match
    for name in names:

        name_normalized = normalize(name)

        if name_normalized in normalized_columns:
            return normalized_columns[name_normalized]

    # Partial match
    for column in data.columns:

        column_normalized = normalize(column)

        for name in names:

            if normalize(name) in column_normalized:
                return column

    return None


def get_value(row, names, default=""):

    for name in names:

        for column in row.index:

            if normalize(column) == normalize(name):

                value = row[column]

                if pd.isna(value):
                    return default

                return clean_text(value)

    return default


# ============================================================
# 4. FIND IMPORTANT COLUMNS
# ============================================================

intern_id_column = find_column(
    intern_profiles,
    ["id", "intern_id", "candidate_id"]
)

job_id_column = find_column(
    job_descriptions,
    ["id", "job_id", "position_id"]
)

question_column = find_column(
    question_bank,
    ["question", "question_text", "interview_question"]
)

difficulty_column = find_column(
    question_bank,
    ["difficulty", "difficulty_level", "level"]
)

category_column = find_column(
    question_bank,
    ["category", "type", "question_type"]
)


if intern_id_column is None:
    print("\nERROR: Candidate ID column not found.")
    print("Available columns:", list(intern_profiles.columns))
    exit()


if job_id_column is None:
    print("\nERROR: Job ID column not found.")
    print("Available columns:", list(job_descriptions.columns))
    exit()


if question_column is None:
    print("\nERROR: Question column not found.")
    print("Available columns:", list(question_bank.columns))
    exit()


# ============================================================
# 5. USER INPUT
# ============================================================

print("\n==============================================")
print("       AI INTERVIEW QUESTION GENERATOR")
print("==============================================")

print("\nAvailable Candidate IDs:")
print(", ".join(intern_profiles[intern_id_column].astype(str)))

candidate_id = input("\nEnter Candidate ID: ").strip()


print("\nAvailable Job IDs:")
print(", ".join(job_descriptions[job_id_column].astype(str)))

job_id = input("\nEnter Job ID: ").strip()


# ============================================================
# 6. FIND CANDIDATE
# ============================================================

candidate_rows = intern_profiles[
    intern_profiles[intern_id_column]
    .astype(str)
    .str.strip()
    .str.lower()
    == candidate_id.lower()
]

if candidate_rows.empty:

    print("\nERROR: Candidate ID not found.")
    exit()

candidate = candidate_rows.iloc[0]


# ============================================================
# 7. FIND JOB
# ============================================================

job_rows = job_descriptions[
    job_descriptions[job_id_column]
    .astype(str)
    .str.strip()
    .str.lower()
    == job_id.lower()
]

if job_rows.empty:

    print("\nERROR: Job ID not found.")
    exit()

job = job_rows.iloc[0]


# ============================================================
# 8. DIFFICULTY
# ============================================================

print("\nDifficulty Levels:")
print("1. Beginner")
print("2. Intermediate")
print("3. Advanced")

difficulty_choice = input("\nSelect difficulty (1-3): ").strip()

difficulty_map = {
    "1": "Easy",
    "2": "Medium",
    "3": "Hard"
}

if difficulty_choice not in difficulty_map:

    print("\nERROR: Invalid difficulty.")
    exit()

difficulty = difficulty_map[difficulty_choice]

print("\nSelected Difficulty:", difficulty)


# ============================================================
# 9. CANDIDATE INFORMATION
# ============================================================

education = get_value(
    candidate,
    ["education", "degree", "qualification"],
    "Not specified"
)

candidate_skills_text = get_value(
    candidate,
    ["skills", "technical_skills"],
    ""
)

projects = get_value(
    candidate,
    ["projects", "project", "project_experience"],
    "Not specified"
)

experience = get_value(
    candidate,
    ["experience", "experience_level"],
    "Not specified"
)

candidate_skills = split_values(candidate_skills_text)


# ============================================================
# 10. JOB INFORMATION
# ============================================================

job_title = get_value(
    job,
    ["job", "job_title", "role", "position"],
    job_id
)

required_skills_text = get_value(
    job,
    ["required_skills", "required_skill", "skills_required"],
    ""
)

responsibilities = get_value(
    job,
    ["responsibilities", "responsibility"],
    "Not specified"
)

required_skills = split_values(required_skills_text)


# ============================================================
# 11. SKILL ANALYSIS
# ============================================================

matched_skills = []
missing_skills = []

candidate_skill_names = [
    normalize(skill)
    for skill in candidate_skills
]

for skill in required_skills:

    skill_normalized = normalize(skill)

    found = False

    for candidate_skill in candidate_skill_names:

        if (
            skill_normalized == candidate_skill
            or skill_normalized in candidate_skill
            or candidate_skill in skill_normalized
        ):
            found = True
            break

    if found:
        matched_skills.append(skill)

    else:
        missing_skills.append(skill)


# ============================================================
# 12. DISPLAY PROFILE
# ============================================================

print("\n==============================================")
print("             CANDIDATE PROFILE")
print("==============================================")

print("ID:", candidate_id)
print("Education:", education)
print("Skills:", candidate_skills_text)
print("Projects:", projects)
print("Experience:", experience)


print("\n==============================================")
print("             JOB DESCRIPTION")
print("==============================================")

print("Job:", job_title)
print("Required Skills:", required_skills_text)
print("Responsibilities:", responsibilities)


print("\n==============================================")
print("              SKILL ANALYSIS")
print("==============================================")

print("Matched Job Skills:")

if matched_skills:
    print(", ".join(matched_skills))
else:
    print("None")


print("\nMissing / Learning Areas:")

if missing_skills:
    print(", ".join(missing_skills))
else:
    print("None")


# ============================================================
# 13. SELECT QUESTION BANK BY DIFFICULTY
# ============================================================

if difficulty_column is not None:

    selected_bank = question_bank[
        question_bank[difficulty_column]
        .astype(str)
        .str.strip()
        .str.lower()
        == difficulty.lower()
    ].copy()

else:

    selected_bank = question_bank.copy()


print(
    "\nQuestion Bank Questions at",
    difficulty + ":",
    len(selected_bank)
)


# ============================================================
# 14. FIND RELEVANT BANK QUESTIONS
# ============================================================

def get_relevant_questions():

    scored_questions = []

    for _, row in selected_bank.iterrows():

        question = clean_text(row[question_column])

        question_normalized = normalize(question)

        score = 0

        # Missing skills are most important
        for skill in missing_skills:

            if normalize(skill) in question_normalized:
                score += 5

        # Required skills
        for skill in required_skills:

            if normalize(skill) in question_normalized:
                score += 3

        # Candidate skills
        for skill in candidate_skills:

            if normalize(skill) in question_normalized:
                score += 2

        scored_questions.append(
            (score, question)
        )

    scored_questions.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        question
        for score, question in scored_questions
        if question
    ]


relevant_questions = get_relevant_questions()


# ============================================================
# 15. LOAD TEXT GENERATION MODEL
# ============================================================

print("\nLoading text generation model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)

print("Model loaded successfully.")


# ============================================================
# 16. GENERATE CUSTOM QUESTION
# ============================================================

def generate_custom_question(
    original_question,
    question_type,
    focus
):

    prompt = f"""
Rewrite this interview question for the candidate and job below.

Original question:
{original_question}

Candidate education:
{education}

Candidate skills:
{candidate_skills_text}

Candidate project:
{projects}

Job:
{job_title}

Focus:
{focus}

Question type:
{question_type}

Difficulty:
{difficulty}

Create ONE clear interview question.
Keep the meaning of the original question.
Make it relevant to the candidate and job.
Return only the question.
"""

    try:

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        outputs = model.generate(
            **inputs,
            max_new_tokens=50,
            num_beams=4,
            do_sample=False
        )

        result = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        ).strip()

        # Remove common prefixes
        result = re.sub(
            r"^(question:|answer:)\s*",
            "",
            result,
            flags=re.IGNORECASE
        )

        result = result.strip()

        # Reject bad model output
        bad_outputs = [
            "do you have",
            "generate a question",
            "write a question",
            "return only",
            "original question",
            "candidate education",
            "question type"
        ]

        result_lower = result.lower()

        for bad in bad_outputs:

            if bad in result_lower:
                return ""

        # Must look like a real question
        if len(result) < 20:
            return ""

        if "?" not in result:
            return ""

        return result

    except Exception:

        return ""


# ============================================================
# 17. TECHNICAL QUESTIONS
# ============================================================

print("\n==============================================")
print("       GENERATING TECHNICAL QUESTIONS")
print("==============================================")


technical_questions = []


# We want questions around job skills.
technical_focus = required_skills.copy()

if not technical_focus:

    technical_focus = candidate_skills.copy()


# Generate one question for each important skill
for skill in technical_focus:

    original_question = ""

    # Find bank question related to this skill
    for question in relevant_questions:

        if normalize(skill) in normalize(question):

            original_question = question
            break

    # If no matching question exists,
    # use another bank question
    if not original_question:

        if relevant_questions:

            original_question = relevant_questions[
                len(technical_questions)
                % len(relevant_questions)
            ]

    if not original_question:
        continue

    generated = generate_custom_question(
        original_question,
        "Technical",
        skill
    )

    if generated:

        # Avoid duplicates
        if generated not in technical_questions:

            technical_questions.append(generated)

    if len(technical_questions) == 5:
        break


# ============================================================
# 18. TECHNICAL FALLBACK
# ============================================================

technical_fallback = []

invalid_phrases = [
    "job description of the candidate",
    "job title of the candidate",
    "candidate and job",
    "generate a question",
    "write a question",
    "return only"
]

for question in relevant_questions:

    question_lower = question.lower()

    # Skip invalid or instruction-like questions
    if any(phrase in question_lower for phrase in invalid_phrases):
        continue

    # Avoid duplicates
    if question not in technical_questions:
        technical_fallback.append(question)

    if len(technical_questions) + len(technical_fallback) >= 5:
        break


technical_questions.extend(technical_fallback)


# Ensure five questions are available if the question bank is insufficient
generic_questions = [
    "What is the purpose of text preprocessing in an NLP project?",
    "How would you divide a dataset into training and testing sets?",
    "What is supervised learning?",
    "What is the difference between classification and regression?",
    "How would you evaluate a machine learning model?"
]

for question in generic_questions:

    if len(technical_questions) >= 5:
        break

    if question not in technical_questions:
        technical_questions.append(question)

# ============================================================
# 19. BEHAVIORAL QUESTIONS
# ============================================================

print("\n==============================================")
print("      GENERATING BEHAVIORAL QUESTIONS")
print("==============================================")


behavioral_questions = []


# Candidate-specific behavioral questions
project_name = projects

learning_skill = (
    missing_skills[0]
    if missing_skills
    else "a new technology"
)


behavioral_questions.append(
    f"Tell me about your {project_name} project and a challenge you faced while completing it."
)

behavioral_questions.append(
    f"Why are you interested in the {job_title} role?"
)

behavioral_questions.append(
    f"How would you learn {learning_skill} if you were asked to use it during this internship?"
)

behavioral_questions.append(
    "Describe a time when you made a mistake in a project. How did you handle it?"
)

behavioral_questions.append(
    "How do you manage your work when you have a difficult deadline?"
)


# ============================================================
# FINAL QUESTION VALIDATION
# ============================================================

invalid_phrases = [
    "job description of the candidate",
    "candidate and job",
    "job title of the person",
    "what is the job description",
    "what is the job title"
]

# Remove invalid technical questions
technical_questions = [
    q for q in technical_questions
    if not any(
        phrase in q.lower()
        for phrase in invalid_phrases
    )
]

# Add suitable questions if any were removed
replacement_questions = [
    "What is the purpose of text preprocessing in NLP?",
    "What is the difference between classification and regression?",
    "Why do we split data into training and testing sets?",
    "What is supervised learning?",
    "How can we evaluate a machine learning model?"
]

for question in replacement_questions:

    if len(technical_questions) >= 5:
        break

    if question not in technical_questions:
        technical_questions.append(question)
# ============================================================
# 20. FINAL OUTPUT
# ============================================================

print("\n\n==============================================")
print("       CUSTOM TECHNICAL INTERVIEW QUESTIONS")
print("==============================================")


for number, question in enumerate(
    technical_questions[:5],
    1
):

    print(f"\n{number}. {question}")


print("\n\n==============================================")
print("      CUSTOM BEHAVIORAL INTERVIEW QUESTIONS")
print("==============================================")


for number, question in enumerate(
    behavioral_questions[:5],
    1
):

    print(f"\n{number}. {question}")


# ============================================================
# 21. SUMMARY
# ============================================================

print("\n\n==============================================")
print("                SUMMARY")
print("==============================================")

print("Candidate:", candidate_id)
print("Job:", job_title)
print("Difficulty:", difficulty)

print(
    "Technical Questions:",
    len(technical_questions[:5])
)

print(
    "Behavioral Questions:",
    len(behavioral_questions[:5])
)

print("\nInterview question generation completed.")