"""
Governance schemas for rules, voting, and appeals.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, List


class RuleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    hierarchy_level: str  # galaxy, planet, territory, plot, object
    rule_json: Dict[str, Any]


class RuleCreate(RuleBase):
    parent_entity_id: Optional[int] = None
    parent_entity_type: Optional[str] = None


class RuleResponse(RuleBase):
    id: int
    parent_entity_id: Optional[int] = None
    parent_entity_type: Optional[str] = None
    is_active: bool
    is_violated: bool
    created_at: datetime
    updated_at: datetime
    created_by_id: int
    
    class Config:
        from_attributes = True


class VoteBase(BaseModel):
    vote_value: int  # 1 for yes, -1 for no, 0 for abstain
    comment: Optional[str] = None


class VoteCreate(VoteBase):
    governance_action_id: int


class VoteResponse(VoteBase):
    id: int
    governance_action_id: int
    voter_id: int
    vote_weight: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class AppealBase(BaseModel):
    appeal_type: str  # rule_violation, governance_decision, ban_appeal
    reason: str


class AppealCreate(AppealBase):
    evidence_json: Optional[List[Dict[str, Any]]] = None
    related_rule_id: Optional[int] = None
    related_action_id: Optional[int] = None


class AppealResponse(AppealBase):
    id: int
    appellant_id: int
    status: str
    resolution: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
