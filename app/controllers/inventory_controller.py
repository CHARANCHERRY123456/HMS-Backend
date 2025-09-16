from sqlalchemy.orm import Session
from models.inventory import InventoryItem
from schemas.inventory_schema import InventoryItemCreate, InventoryItemUpdate

def create_item(db: Session, item: InventoryItemCreate):
    db_item = InventoryItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all_items(db: Session):
    return db.query(InventoryItem).all()

def get_item_by_id(db: Session, item_id: int):
    return db.query(InventoryItem).filter(InventoryItem.id == item_id).first()

def update_item(db: Session, item_id: int, item_update: InventoryItemUpdate):
    db_item = get_item_by_id(db, item_id)
    if not db_item:
        return None
    for field, value in item_update.dict(exclude_unset=True).items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item_by_id(db, item_id)
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item
