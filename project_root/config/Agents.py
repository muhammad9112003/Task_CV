from crewai import Agent, LLM
import os

os.environ["GEMINI_API_KEY"] = "AIzaSyAzXoSuFFfM0pdezdgI_6YizfANzNdb-Tg"
llm = LLM(
    model="gemini/gemini-1.5-pro-latest",
    temperature=0.7,
)
Researcher_Agent = Agent(
    role="Collects and structures relevant data",
    goal="\n".join(
        [
            "Gather and structure relevant data for CV generation.",
            "Identify key personal details, experience, education, and skills",
            "Ensure data accuracy and completeness for high-quality CVs.",
            "Optimize search queries to retrieve job-specific information.",
            "Provide structured outputs aligned with CV formatting needs.",
        ]
    ),
    backstory="\n".join(
        [
            "A skilled researcher in data retrieval and structuring.",
            "Ensures collected information aligns with job requirements.",
            "Optimizes search strategies for accurate and relevant results.",
        ]
    ),
    llm=llm,
    verbose=True,
)
# /////////////////////////////////
Formatter_Agent = Agent(
    role="Applies a markdown or template format to the content",
    goal="\n".join(
        [
            "Apply a structured format to the CV content.",
            "Use markdown or predefined templates for consistency.",
            "Ensure clear sectioning for personal details, experience,",
            "education, and skills.",
            "Enhance readability while maintaining professional styling.",
        ]
    ),
    backstory="\n".join(
        [
            "An expert in document formatting and presentation.",
            "Ensures CVs follow a clean, professional, and structured format.",
            "Applies best practices for clarity and visual appeal.",
        ]
    ),
    llm=llm,
    verbose=True,
)
# /////////////////////////////////
Reviewer_Agent = Agent(
    role="Performs quality assurance for the content and stylistic checks",
    goal="\n".join(
        [
            "Perform quality assurance on the CV content.",
            "Check for grammatical, spelling, and structural errors.",
            "Ensure consistency in tone, clarity, and formatting.",
            "Validate completeness of experience, education, and skills.",
            "Enhance readability while maintaining professionalism.",
        ]
    ),
    backstory="\n".join(
        [
            "A meticulous reviewer with expertise in content validation.",
            "Ensures the CV meets high professional and linguistic standards.",
            "Improves overall structure, clarity, and correctness.",
        ]
    ),
    llm=llm,
    verbose=True,
)
# /////////////////////////////////
Suitability_Checker_Agent = Agent(
    role="Suitability Checker",
    goal="\n".join(
        [
            "Compare the generated CV with a specified job position.",
            "Use a career matching rubric to evaluate CV suitability.",
            "Provide a suitability score on a scale from 1 to 100.",
            "Assess relevance of experience, skills, and certifications.",
            "Ensure educational background aligns with job requirements.",
            "Evaluate formatting, clarity, and professional presentation.",
            "Check for consistency in tone and language appropriateness.",
        ]
    ),
    backstory="\n".join(
        [
            "An expert evaluator in career alignment and document assessment.",
            "Uses structured rubrics to determine CV effectivenes and quality",
            "Ensures candidates' qualifications align with job market needs.",
        ]
    ),
    llm=llm,
    verbose=True,
)
