from typing import List, Tuple
MAX_TURNS=5

def add_to_memory(memory: List[Tuple[str,str]], user_query:str,assistant_answer:str):
    memory.append((user_query,assistant_answer))
    return memory[-MAX_TURNS:]


def format_memory(memory: List[Tuple[str,str]])->str:
    formatted=""
    for i, (q,a) in enumerate(memory,1):
        formatted+=f"User Question {i} : {q}\n"
        formatted+=f"Assistant Answer {i}: {a}\n\n"
    return formatted.strip()