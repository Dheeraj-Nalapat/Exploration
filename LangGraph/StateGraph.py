from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from typing_extensions import TypedDict, Annotated
from langgraph.checkpoint.memory import MemorySaver

def reducer(a: list,b: int | None) -> list:
    if b is not None:
        return a + [b]
    return a

class State(TypedDict):
    x: Annotated[list, reducer]

class ConfigSchema(TypedDict):
    r: float

graph = StateGraph(State,config_schema=ConfigSchema) 

def node(state: State, config: RunnableConfig) -> dict:
    r = config["configurable"].get("r",1.0)
    x = state["x"][-1]
    next_value = x * r * (1 - x)
    return {"x": next_value}

graph.add_node("A",node,metadata={"description":"this a node that multiplies some values"})
graph.set_entry_point("A")
graph.set_finish_point("A")
compiled = graph.compile()

print(compiled.config_specs)
step1 = compiled.invoke({"x":0.5}, {"configurable":{"r": 3.0}})
print(step1)