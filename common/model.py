from dataclasses import dataclass
@dataclass
class Todo:
    user_id: str
    title: str
    remind_time: str = ""
@dataclass
class Remind:
    title: str
    remind_time: str
