"""
Plots router for land management.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.hierarchy import Plot
from app.schemas.hierarchy import PlotCreate, PlotResponse
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/plots", tags=["plots"])


@router.get("/", response_model=List[PlotResponse])
async def get_all_plots(db: Session = Depends(get_db)):
    """Get all plots in the world."""
    plots = db.query(Plot).all()
    return plots


@router.post("/", response_model=PlotResponse)
async def claim_plot(
    plot_data: PlotCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Claim an unowned plot."""
    # Check if plot exists at these coordinates
    existing_plot = db.query(Plot).filter(
        Plot.x == plot_data.x,
        Plot.y == plot_data.y
    ).first()
    
    if existing_plot:
        if existing_plot.owner_id is not None:
            raise HTTPException(status_code=400, detail="Этот участок уже занят")
        # Claim existing unowned plot
        existing_plot.owner_id = current_user.id
        existing_plot.name = plot_data.name or existing_plot.name
        db.commit()
        db.refresh(existing_plot)
        return existing_plot
    
    # Create new plot
    new_plot = Plot(
        x=plot_data.x,
        y=plot_data.y,
        owner_id=current_user.id,
        name=plot_data.name or "Безымянный участок",
    )
    db.add(new_plot)
    db.commit()
    db.refresh(new_plot)
    return new_plot


@router.get("/{plot_id}", response_model=PlotResponse)
async def get_plot(plot_id: int, db: Session = Depends(get_db)):
    """Get a specific plot by ID."""
    plot = db.query(Plot).filter(Plot.id == plot_id).first()
    if not plot:
        raise HTTPException(status_code=404, detail="Участок не найден")
    return plot
