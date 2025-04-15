from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from crews.query_crew.generate_query_crew import QueryCrew, QueryGenCrew

from dotenv import load_dotenv

load_dotenv()

class QueryState(BaseModel):
    query : str = "" 
    sql_query : str = ""
    final_response : str = ""


class QueryFlow(Flow[QueryState]):

    @start()
    def generate_sentence_count(self):
        query = input("🤖   Please enter your query :   ")
        self.state.query = query
        return query

    @listen(generate_sentence_count)
    def generate_query(self):
        print("🚀   Delegating to DB agent...")
        result = QueryCrew().crew().kickoff(inputs={"query": self.state.query})

        print("✅   Generated Query : ", result.raw)
        self.state.sql_query = result.raw

        return self.state.sql_query

    @listen(generate_query)
    def execute_query(self):
        print("Executing Query...")
        result = QueryGenCrew().crew().kickoff(inputs={"sql_query": self.state.sql_query})
        self.state.final_response = result.raw
        return self.state.final_response

if __name__ == "__main__":
    query_flow = QueryFlow()
    first_result = query_flow.kickoff()

    print("😍 Final response from bot : ")
    print(first_result)
