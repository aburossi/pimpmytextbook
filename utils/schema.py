# utils/schema.py

from pydantic import BaseModel, Field
from typing import List


class OverviewItem(BaseModel):
    PageReference: str
    Summary: str


class AssignmentItem(BaseModel):
    Focus: str
    Goal: str


class MindmapNode(BaseModel):
    ParentNode: str
    ChildNodes: List[str]
    StudentGuidance: str


class MindmapIntegration(BaseModel):
    PageReference: str
    DidacticPurpose: str
    Nodes: List[MindmapNode]


class TheoreticalItem(BaseModel):
    Topic: str
    Content: str
    LegalReferences: List[str]
    Assignments: List[AssignmentItem]
    MindmapIntegration: MindmapIntegration


class PracticalActivity(BaseModel):
    Title: str
    Overview: str
    Steps: List[str]


class KickOff(BaseModel):
    TargedGroup: str
    Overview: List[OverviewItem]
    LearningGoals: List[str]


class ClosingRemarks(BaseModel):
    Summary: str
    KeyPassages: List[str]
    SpecialConsiderations: str


class LessonPlan(BaseModel):
    LessonUnit: str
    Kick_Off: KickOff = Field(..., alias="Kick-Off")
    TheoreticalFundamentals: List[TheoreticalItem]
    PracticalActivities: List[PracticalActivity]
    ClosingRemarks: ClosingRemarks
