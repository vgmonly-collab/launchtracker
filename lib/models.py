# lib/models.py
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Dict, Any
from datetime import datetime

Step = Literal["Estimate","Content Update","Content Signoff","MSTN","Pricing","PO","Availability"]
Status = Literal["On Track","At Risk","Delayed","Launched"]
ActionType = Literal["DETAILS","ALIGNED","PROPOSE_CHANGE"]
Role = Literal["viewer","csp","am","admin"]

class Action(BaseModel):
    ts: str
    actor: str
    role: Role
    type: ActionType
    payload: Dict[str, Any] = {}

class Launch(BaseModel):
    id: str
    title: str
    customer: str
    launch_month: str
    signoff_date: Optional[str] = None
    content_in_date: Optional[str] = None
    content_signoff_date: Optional[str] = None
    next_step: Step
    delayed_at: Optional[Step] = None
    status: Status = "On Track"
    timeline: List[Action] = Field(default_factory=list)

    def log(self, actor: str, role: Role, type: ActionType, payload: Dict[str,Any]):
        self.timeline.append(Action(ts=datetime.utcnow().isoformat(), actor=actor, role=role, type=type, payload=payload))
