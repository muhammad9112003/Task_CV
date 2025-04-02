from crewai import Task
from .Agents import (
    Researcher_Agent,
    Formatter_Agent,
    Reviewer_Agent,
    Suitability_Checker_Agent,
)
from pydantic import BaseModel, Field
from typing import Dict, List
import os

output_directory = os.path.join(os.getcwd(), "project_root", "outputs")
os.makedirs(output_directory, exist_ok=True)
print(output_directory)

nomOfinfo = 1


class Researcher_Task_Queries(BaseModel):
    queries: List[str] = Field(
        ...,
        title="A list of well-structured and varied search queries",
        min_length=1,
        max_length=nomOfinfo,
    )


Researcher_Task = Task(
    description="\n".join(
        [
            "The Researcher Agent gathers and structures key information for CV generation.",
            "Candidate Name: Mohammed",
            "Applying for Position: Front-End Developer",
            "Experience: 3 years in Front-End Development",
            "Education: Bachelor's degree in Computer Science",
            "Key Skills: HTML, CSS, JavaScript",
            "LinkedIn Profile: Mohammed Ayman",
            "Responsibilities:",
            "- Collects and verifies personal details, education, skills, and experience.",
            "- Uses advanced search techniques to ensure accuracy and completeness.",
            "- Structures data systematically for seamless processing by other agents.",
            "- Enhances CV quality by providing precise and reliable information.",
            "Required Information Count: 13 key details.",
        ]
    ),
    expected_output="/n".join(
        [
            "A list of well-structured and varied search queries",
        ]
    ),
    output_json=Researcher_Task_Queries,
    output_file=os.path.join(output_directory, "step_1_Researcher_Agent"),
    agent=Researcher_Agent,
)


class Header(BaseModel):
    name: str
    position: str
    linkedin: str


class Experience(BaseModel):
    years: int
    field: str


class Education(BaseModel):
    degree: str


class FormatterTaskOutput(BaseModel):
    formatted_cv: dict

    class Config:
        fields = {"formatted_cv": "formatted_cv"}


output_data = FormatterTaskOutput(
    formatted_cv={
        "header": {
            "name": "Mohammed",
            "position": "Front-End Developer",
            "linkedin": "Mohammed Ayman",
        },
        "experience": [{"years": 3, "field": "Front-End Development"}],
        "education": {"degree": "Bachelor's in Computer Science"},
        "skills": ["HTML", "CSS", "JavaScript"],
        "summary": "A structured and professionally formatted CV ready for review.",
    }
)

Formatter_Task = Task(
    description="\n".join(
        [
            "The Formatter Agent ensures that the collected information is properly structured.",
            "It applies professional formatting, ensuring clarity, readability, and a polished layout.",
            "Responsibilities:",
            "- Formats the CV using a structured template (Markdown or predefined layout).",
            "- Ensures consistency in headings, bullet points, and spacing.",
            "- Enhances readability by applying professional design principles.",
            "- Standardizes font styles, section alignment, and content spacing.",
            "- Removes redundant or unnecessary details while preserving key information.",
            "- Prepares the document for review by the next agent in the workflow.",
            "Output should be well-structured, visually appealing, and ready for quality review.",
        ]
    ),
    expected_output="\n".join(
        [
            "A professionally formatted CV in Markdown or structured layout.",
        ]
    ),
    output_json=FormatterTaskOutput,
    output_file=os.path.join(output_directory, "step_2_Formatter_Agent"),
    agent=Formatter_Agent,
)


class ReviewerTaskOutput(BaseModel):
    polished_document: str
    feedback: List[str]


class Config:
    orm_mode = True


Reviewer_Task = Task(
    description="\n".join(
        [
            "The Reviewer Agent performs a quality assurance check on the content and formatting.",
            "It ensures that the document meets the required standards and checks for consistency in language and style.",
            "Responsibilities:",
            "- Reviews the document for grammatical errors, spelling mistakes, and sentence structure.",
            "- Ensures that the content aligns with the purpose and tone of the document.",
            "- Verifies that formatting is consistent throughout, including headings, bullet points, and font usage.",
            "- Provides feedback on clarity and readability.",
            "- Flags any issues with document flow, style, or structure that need attention.",
            "- Suggests improvements to enhance the document's overall quality and professionalism.",
            "Output should be a clean, polished document ready for final approval or further refinement.",
        ]
    ),
    expected_output="\n".join(
        [
            "A polished and error-free document, ready for final approval or further refinement.",
        ]
    ),
    output_json=ReviewerTaskOutput,
    output_file=os.path.join(output_directory, "step_3_Reviewer_Agent"),
    agent=Reviewer_Agent,
)


class SuitabilityCheckerTaskOutput(BaseModel):
    score: float
    feedback: List[str]
    detailed_assessment: Dict[str, float]

    class Config:
        orm_mode = True


class SuitabilityCheckerAgent:
    def __init__(self, job_requirements: Dict[str, str]):
        self.job_requirements = job_requirements

    def evaluate_cv(self, cv: Dict[str, str]) -> SuitabilityCheckerTaskOutput:
        score = 0
        feedback = []
        detailed_assessment = {}

        experience_relevance = self.evaluate_experience(cv["experience"])
        detailed_assessment["experience_relevance"] = experience_relevance
        score += experience_relevance
        feedback.append(f"Experience Relevance: {experience_relevance}/100")

        skill_match = self.evaluate_skills(cv["skills"])
        detailed_assessment["skill_match"] = skill_match
        score += skill_match
        feedback.append(f"Skill & Certification Match: {skill_match}/100")

        education_relevance = self.evaluate_education(cv["education"])
        detailed_assessment["education_relevance"] = education_relevance
        score += education_relevance
        feedback.append(f"Educational Background: {education_relevance}/100")

        formatting_clarity = self.evaluate_formatting(cv["formatting"])
        detailed_assessment["formatting_clarity"] = formatting_clarity
        score += formatting_clarity
        feedback.append(f"Formatting & Clarity: {formatting_clarity}/100")

        tone_consistency = self.evaluate_tone(cv["tone"])
        detailed_assessment["tone_consistency"] = tone_consistency
        score += tone_consistency
        feedback.append(f"Professional Tone & Consistency: {tone_consistency}/100")

        score /= 5
        return SuitabilityCheckerTaskOutput(
            score=score, feedback=feedback, detailed_assessment=detailed_assessment
        )

    def evaluate_experience(self, experience: str) -> float:
        return 80

    def evaluate_skills(self, skills: str) -> float:
        return 75

    def evaluate_education(self, education: str) -> float:
        return 70

    def evaluate_formatting(self, formatting: str) -> float:
        return 90

    def evaluate_tone(self, tone: str) -> float:
        return 85


SuitabilityCheckerTask = {
    "description": "\n".join(
        [
            "The Suitability Checker Agent evaluates the generated CV for a specific job position.",
            "It compares the CV against the job requirements using a matching evaluation rubric.",
            "Responsibilities:",
            "- Compares professional experience with job requirements.",
            "- Evaluates skill and certification match to the target position.",
            "- Assesses the educational background's suitability for the job.",
            "- Reviews the formatting, clarity, and presentation of the CV.",
            "- Ensures the professional tone and consistency of language in the CV.",
            "Output should be a suitability score and feedback based on the rubric criteria.",
            "and give me a PDF file containing the Professional CV",
        ]
    ),
    "expected_output": "\n".join(
        [
            "A suitability score ranging from 1 to 100.",
            "Feedback with detailed evaluation of each criterion.",
        ]
    ),
    "output_json": SuitabilityCheckerTaskOutput,
    "output_file": os.path.join(
        "project_root", "outputs", "suitability_checker_output.json"
    ),
    "agent": Suitability_Checker_Agent,
}
