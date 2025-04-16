from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start, router

from crews.query_crew.generate_query_crew import QueryCrew, QueryGenCrew, IDUGenCrew

from dotenv import load_dotenv

load_dotenv()


class QueryState(BaseModel):
    query : str = "" 
    history : list = []
    sql_query : str = ""
    final_response : str = ""

class QueryFlow(Flow[QueryState]):

    @start()
    def generate_query(self):
        # chat_history = QueryState.history
        # history = '\n'.join(chat_history)
        # query   = QueryState.query
        # print(f"query inside generate_query function : {query}")
        # print(f"chat history inside generate_query function is : {history}")
        # print("🚀  Delegating to DB agent...")
        user_input = input("🤖  Please enter your query (or type 'exit') :   ")
        self.state.query = user_input
        result = QueryCrew().crew().kickoff(inputs={"query": self.state.query, "history" : self.state.history})

        # print("✅  Generated Query : ", result.raw)
        self.state.sql_query = result.raw

        return self.state.sql_query
    
    @router(generate_query)
    def router_func(self):
        if 'SELECT' in self.state.sql_query:
            return "SELECT"
        elif 'INSERT' in self.state.sql_query or 'DELETE'  in self.state.sql_query or'UPDATE' in self.state.sql_query:
            return "IDU"

    @listen("SELECT")
    def select_query(self):
        print("🔴🔴🔴🔴🔴Executing Query...")
        result = QueryGenCrew().crew().kickoff(inputs={"sql_query": self.state.sql_query})
        self.state.final_response = result.raw
        self.state.history.append(f"AI Response : {self.state.final_response}")
        return self.state.final_response
    
    @listen("IDU")
    def idu_query(self):
        print("🍒🍒🍒🍒🍒This is IDU Query...")
        result = IDUGenCrew().crew().kickoff(inputs={"sql_query": self.state.sql_query})
        self.state.final_response = result.raw
        self.state.history.append(f"AI Response : {self.state.final_response}")
        return self.state.final_response

if __name__ == "__main__":

    query_state = QueryState()
    query_flow = QueryFlow()
    response = query_flow.kickoff()
    # while True:
    #     user_input = input("🤖  Please enter your query (or type 'exit') :   ")
    #     if user_input.lower() == 'exit':
    #         break
    #     print(f"User query is : {user_input}")
    #     query_state.history.append(f"user : {user_input}")
    #     print(f"Initial history is : {query_state.history}")
    #     query_state.query = user_input
    #     print(f"query in state is : {query_state.query}")
    #     response = query_flow.kickoff(inputs={"query" : user_input, "history" : QueryState.history})

    # print("😍 Final response from bot : ")
    # print(response)
