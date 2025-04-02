from crewai import Crew, Process
from config.Agents import (
    Researcher_Agent,
    Formatter_Agent,
    Reviewer_Agent,
    Suitability_Checker_Agent,
)


from config.Tasks import (
    Researcher_Task,
    Formatter_Task,
    Reviewer_Task,
    SuitabilityCheckerTask,
)
import agentops
import os

os.environ["AGENTOPS_API_KEY"] = "9761238a-3851-43eb-976d-fa790cf86e3b"

agentops.init(
    api_key="9761238a-3851-43eb-976d-fa790cf86e3b", skip_auto_end_session=True
)
CV_crew = Crew(
    agents=[
        Researcher_Agent,
        Formatter_Agent,
        Reviewer_Agent,
        Suitability_Checker_Agent,
    ],
    tasks=[Researcher_Task, Formatter_Task, Reviewer_Task, SuitabilityCheckerTask],
    process=Process.sequential,
)
crew_results = CV_crew.kickoff()

print("done")
