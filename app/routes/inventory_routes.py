from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.inventory_schema import InventoryItemCreate, InventoryItemUpdate, InventoryItemOut
from controllers import inventory_controller

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/", response_model=InventoryItemOut)
def create_inventory_item(item: InventoryItemCreate, db: Session = Depends(get_db)):
    return inventory_controller.create_item(db, item)

@router.get("/", response_model=list[InventoryItemOut])
def list_inventory_items(db: Session = Depends(get_db)):
    return inventory_controller.get_all_items(db)

@router.get("/{item_id}", response_model=InventoryItemOut)
def get_inventory_item(item_id: int, db: Session = Depends(get_db)):
    item = inventory_controller.get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=InventoryItemOut)
def update_inventory_item(item_id: int, item_update: InventoryItemUpdate, db: Session = Depends(get_db)):
    item = inventory_controller.update_item(db, item_id, item_update)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/{item_id}", response_model=InventoryItemOut)
def delete_inventory_item(item_id: int, db: Session = Depends(get_db)):
    item = inventory_controller.delete_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
