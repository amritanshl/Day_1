from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import math

app = FastAPI(
    title="Geometric Mensuration API",
    description="An API to manage geometric shapes and automatically calculate their Area and Perimeter.",
    version="1.0.0"
)

# ==========================================
# 1. SCHEMAS & MODELS (Pydantic)
# ==========================================

class ShapeInput(BaseModel):
    name: str = Field(..., description="Unique user-defined identifier for the shape instance", example="my-circle")
    type: str = Field(..., description="Type of shape: 'square', 'rectangle', or 'circle'", example="circle")
    dimension_x: float = Field(..., gt=0, description="Radius, Side, or Length (must be positive)", example=5.0)
    dimension_y: Optional[float] = Field(None, gt=0, description="Width for rectangles (leave null for square/circle)", example=None)

class ShapeResponse(ShapeInput):
    id: int = Field(..., description="Auto-incremented database ID")
    area: float = Field(..., description="Calculated area of the shape")
    perimeter: float = Field(..., description="Calculated perimeter or circumference of the shape")


# ==========================================
# 2. IN-MEMORY DATABASE & HELPER
# ==========================================
# Simulating database records
SHAPE_DB: Dict[int, dict] = {}
next_id = 1

def compute_mensuration(shape_type: str, dx: float, dy: Optional[float]) -> tuple[float, float]:
    """Helper logic to process geometric formulas."""
    st = shape_type.lower()
    if st == "square":
        area = dx * dx
        perimeter = 4 * dx
    elif st == "rectangle":
        if dy is None:
            raise HTTPException(status_code=400, detail="dimension_y (width) is required for rectangles.")
        area = dx * dy
        perimeter = 2 * (dx + dy)
    elif st == "circle":
        area = math.pi * (dx ** 2)
        perimeter = 2 * math.pi * dx
    else:
        raise HTTPException(status_code=400, detail="Invalid shape type. Choose 'square', 'rectangle', or 'circle'.")
    
    return round(area, 4), round(perimeter, 4)


# ==========================================
# 3. ROUTE IMPLEMENTATIONS (CRUD)
# ==========================================

# CREATE (POST)
@app.post("/api/v1/shapes", response_model=ShapeResponse, status_code=status.HTTP_201_CREATED)
def create_shape(payload: ShapeInput):
    global next_id
    
    # Calculate geometric outputs
    area, perimeter = compute_mensuration(payload.type, payload.dimension_x, payload.dimension_y)
    
    new_shape = {
        "id": next_id,
        "name": payload.name,
        "type": payload.type.lower(),
        "dimension_x": payload.dimension_x,
        "dimension_y": payload.dimension_y,
        "area": area,
        "perimeter": perimeter
    }
    
    SHAPE_DB[next_id] = new_shape
    next_id += 1
    return new_shape


# READ ALL (GET)
@app.get("/api/v1/shapes", response_model=List[ShapeResponse])
def get_all_shapes():
    return list(SHAPE_DB.values())


# READ SINGLE (GET)
@app.get("/api/v1/shapes/{shape_id}", response_model=ShapeResponse)
def get_shape_by_id(shape_id: int):
    if shape_id not in SHAPE_DB:
        raise HTTPException(status_code=404, detail=f"Shape record with ID {shape_id} not found.")
    return SHAPE_DB[shape_id]


# UPDATE (PUT)
@app.put("/api/v1/shapes/{shape_id}", response_model=ShapeResponse)
def update_shape(shape_id: int, payload: ShapeInput):
    if shape_id not in SHAPE_DB:
        raise HTTPException(status_code=404, detail=f"Shape record with ID {shape_id} not found.")
    
    # Recalculate metrics based on new incoming sizes
    area, perimeter = compute_mensuration(payload.type, payload.dimension_x, payload.dimension_y)
    
    updated_shape = {
        "id": shape_id,
        "name": payload.name,
        "type": payload.type.lower(),
        "dimension_x": payload.dimension_x,
        "dimension_y": payload.dimension_y,
        "area": area,
        "perimeter": perimeter
    }
    
    SHAPE_DB[shape_id] = updated_shape
    return updated_shape


# DELETE (DELETE)
@app.delete("/api/v1/shapes/{shape_id}", status_code=status.HTTP_200_OK)
def delete_shape(shape_id: int):
    if shape_id not in SHAPE_DB:
        raise HTTPException(status_code=404, detail=f"Shape record with ID {shape_id} not found.")
    
    deleted_item = SHAPE_DB.pop(shape_id)
    return {"message": "Shape record successfully expunged.", "deleted_item": deleted_item}