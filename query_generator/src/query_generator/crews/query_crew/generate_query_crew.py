from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.custom_tool import query_executer 
@CrewBase
class QueryCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    @agent
    def query_gen_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["database_agent"],
        )
    @task
    def query_gen_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_sql_task"],
            agent=self.query_gen_agent(),
        )
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
@CrewBase
class QueryGenCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def query_executer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["generate_human_language"],
            tools=[query_executer],
        )
    @task
    def query_executer_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_human_language_task"],
            agent=self.query_executer_agent(),
        )
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )