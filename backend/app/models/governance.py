"""
Governance models: Rules, Voting, Appeals.
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Rule(Base):
    """Rules that govern hierarchy levels."""
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    
    # Hierarchy level this rule applies to
    hierarchy_level = Column(String(20), nullable=False)  # galaxy, planet, territory, plot, object
    parent_entity_id = Column(Integer, nullable=True)  # ID of the entity that created this rule
    parent_entity_type = Column(String(20), nullable=True)  # galaxy, planet, territory, plot
    
    # Rule content
    rule_json = Column(JSON, nullable=False)  # Structured rule definition
    
    # Inheritance
    inherits_from = Column(Integer, ForeignKey("rules.id"), nullable=True)
    parent_rule = relationship("Rule", remote_side=[id], backref="child_rules")
    
    # Status
    is_active = Column(Boolean, default=True)
    is_violated = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", foreign_keys=[created_by_id])


class GovernanceAction(Base):
    """Actions that can be taken through governance."""
    __tablename__ = "governance_actions"

    id = Column(Integer, primary_key=True, index=True)
    action_type = Column(String(50), nullable=False)  # create_rule, modify_rule, remove_rule, ban_user, transfer_ownership
    description = Column(Text, nullable=False)
    
    # Target entity
    target_entity_type = Column(String(20), nullable=True)
    target_entity_id = Column(Integer, nullable=True)
    
    # Proposal details
    proposal_json = Column(JSON, nullable=False)
    
    # Status
    status = Column(String(20), default="pending")  # pending, active, passed, rejected, executed
    execution_result = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    proposed_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    proposer = relationship("User", foreign_keys=[proposed_by_id])
    
    # Relationships
    votes = relationship("Vote", back_populates="governance_action")


class Vote(Base):
    """Votes on governance actions."""
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    governance_action_id = Column(Integer, ForeignKey("governance_actions.id"), nullable=False)
    governance_action = relationship("GovernanceAction", back_populates="votes")
    
    voter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    voter = relationship("User", back_populates="votes")
    
    # Vote details
    vote_value = Column(Integer, nullable=False)  # 1 for yes, -1 for no, 0 for abstain
    vote_weight = Column(Float, default=1.0)  # Can be modified by reputation, stake, etc.
    comment = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)


class Appeal(Base):
    """Appeals for rule violations or governance decisions."""
    __tablename__ = "appeals"

    id = Column(Integer, primary_key=True, index=True)
    appellant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    appellant = relationship("User", back_populates="appeals")
    
    # Appeal details
    appeal_type = Column(String(50), nullable=False)  # rule_violation, governance_decision, ban_appeal
    reason = Column(Text, nullable=False)
    evidence_json = Column(JSON, default=list)  # Links to evidence
    
    # Related entities
    related_rule_id = Column(Integer, ForeignKey("rules.id"), nullable=True)
    related_action_id = Column(Integer, ForeignKey("governance_actions.id"), nullable=True)
    
    # Status
    status = Column(String(20), default="pending")  # pending, under_review, accepted, rejected
    resolution = Column(Text, nullable=True)
    resolved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
