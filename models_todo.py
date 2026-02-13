from pydantic import BaseModel, Field
from typing import Optional

class ToDoRequest(BaseModel):
    # id: Optional[int] = Field(description="ID is not required for creating data entry.", default=None)
    title: str = Field(description = "Heading for the Task.", min_length=3)
    description: str = Field(description="Details for the Task.", min_length=5)
    priority: int = Field(description="Add the priority for the task")
    complete: bool = Field(description="Is the task completed?", default=False)

    model_config = {
        "json_schema_extra": {
            "exmaple":{
                "title": "A New Todo Task Name.",
                "description": "A Description for the task.",
                "priority": 2,
                "complete": False
            }

        }
    }