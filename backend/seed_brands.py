"""
Seed script for brands and phone models
"""
import json
from database import SessionLocal, engine, Base, Brand, PhoneModel

def create_tables():
    """Create brand and model tables"""
    Base.metadata.create_all(bind=engine)

def seed_brands_and_models():
    """Seed brands and models data"""
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(PhoneModel).delete()
        db.query(Brand).delete()
        
        # Brand data with aliases
        brands_data = [
            {
                "name": "Apple",
                "display_name": "Apple",
                "aliases": json.dumps(["iPhone", "iOS"]),
                "parent_brand": None
            },
            {
                "name": "Samsung",
                "display_name": "Samsung",
                "aliases": json.dumps(["Galaxy", "Note", "Samsung Galaxy"]),
                "parent_brand": None
            },
            {
                "name": "Xiaomi",
                "display_name": "Xiaomi",
                "aliases": json.dumps(["Redmi", "Mi", "POCO", "Redmi Note"]),
                "parent_brand": None
            },
            {
                "name": "OnePlus",
                "display_name": "OnePlus",
                "aliases": json.dumps(["OnePlus", "OP"]),
                "parent_brand": None
            },
            {
                "name": "Google",
                "display_name": "Google",
                "aliases": json.dumps(["Pixel", "Google Pixel"]),
                "parent_brand": None
            },
            {
                "name": "Realme",
                "display_name": "Realme",
                "aliases": json.dumps(["Realme", "GT", "Realme GT"]),
                "parent_brand": None
            },
            {
                "name": "Vivo",
                "display_name": "Vivo",
                "aliases": json.dumps(["Vivo", "X", "Vivo X"]),
                "parent_brand": None
            },
            {
                "name": "Motorola",
                "display_name": "Motorola",
                "aliases": json.dumps(["Moto", "Motorola", "Edge"]),
                "parent_brand": None
            },
            {
                "name": "Nothing",
                "display_name": "Nothing",
                "aliases": json.dumps(["Nothing", "Nothing Phone"]),
                "parent_brand": None
            }
        ]
        
        # Insert brands
        for brand_data in brands_data:
            brand = Brand(**brand_data)
            db.add(brand)
        
        db.commit()
        
        # Get brand IDs for models
        brand_map = {brand.name: brand.id for brand in db.query(Brand).all()}
        
        # Phone model data
        models_data = [
            {
                "name": "iPhone 15 Pro",
                "brand_id": brand_map["Apple"],
                "search_terms": json.dumps(["iPhone 15 Pro", "15 Pro", "iPhone 15"]),
                "model_variants": json.dumps(["15 Pro", "15 Pro Max"])
            },
            {
                "name": "iPhone 15",
                "brand_id": brand_map["Apple"],
                "search_terms": json.dumps(["iPhone 15", "15"]),
                "model_variants": json.dumps(["15"])
            },
            {
                "name": "Samsung Galaxy S24 Ultra",
                "brand_id": brand_map["Samsung"],
                "search_terms": json.dumps(["S24 Ultra", "Galaxy S24 Ultra", "S24"]),
                "model_variants": json.dumps(["S24 Ultra", "S24+", "S24"])
            },
            {
                "name": "Samsung Galaxy S24",
                "brand_id": brand_map["Samsung"],
                "search_terms": json.dumps(["S24", "Galaxy S24"]),
                "model_variants": json.dumps(["S24"])
            },
            {
                "name": "Samsung Galaxy A55 5G",
                "brand_id": brand_map["Samsung"],
                "search_terms": json.dumps(["A55", "Galaxy A55", "A55 5G"]),
                "model_variants": json.dumps(["A55 5G"])
            },
            {
                "name": "Samsung Galaxy M14 5G",
                "brand_id": brand_map["Samsung"],
                "search_terms": json.dumps(["M14", "Galaxy M14", "M14 5G"]),
                "model_variants": json.dumps(["M14 5G"])
            },
            {
                "name": "Redmi 12C",
                "brand_id": brand_map["Xiaomi"],
                "search_terms": json.dumps(["Redmi 12C", "12C", "Redmi 12"]),
                "model_variants": json.dumps(["12C"])
            },
            {
                "name": "Xiaomi 14 Ultra",
                "brand_id": brand_map["Xiaomi"],
                "search_terms": json.dumps(["14 Ultra", "Xiaomi 14 Ultra", "14"]),
                "model_variants": json.dumps(["14 Ultra", "14 Pro", "14"])
            },
            {
                "name": "OnePlus 12",
                "brand_id": brand_map["OnePlus"],
                "search_terms": json.dumps(["OnePlus 12", "12", "OP12"]),
                "model_variants": json.dumps(["12", "12R"])
            },
            {
                "name": "OnePlus 12R",
                "brand_id": brand_map["OnePlus"],
                "search_terms": json.dumps(["OnePlus 12R", "12R", "OP12R"]),
                "model_variants": json.dumps(["12R"])
            },
            {
                "name": "Google Pixel 8 Pro",
                "brand_id": brand_map["Google"],
                "search_terms": json.dumps(["Pixel 8 Pro", "8 Pro", "Pixel 8"]),
                "model_variants": json.dumps(["8 Pro", "8", "8a"])
            },
            {
                "name": "Google Pixel 8a",
                "brand_id": brand_map["Google"],
                "search_terms": json.dumps(["Pixel 8a", "8a", "Pixel 8a"]),
                "model_variants": json.dumps(["8a"])
            },
            {
                "name": "Realme GT 6",
                "brand_id": brand_map["Realme"],
                "search_terms": json.dumps(["GT 6", "Realme GT 6", "GT6"]),
                "model_variants": json.dumps(["GT 6"])
            },
            {
                "name": "Vivo X100 Pro",
                "brand_id": brand_map["Vivo"],
                "search_terms": json.dumps(["X100 Pro", "Vivo X100 Pro", "X100"]),
                "model_variants": json.dumps(["X100 Pro", "X100"])
            },
            {
                "name": "Motorola Edge 50 Pro",
                "brand_id": brand_map["Motorola"],
                "search_terms": json.dumps(["Edge 50 Pro", "Moto Edge 50 Pro", "Edge 50"]),
                "model_variants": json.dumps(["Edge 50 Pro"])
            },
            {
                "name": "Nothing Phone (2a)",
                "brand_id": brand_map["Nothing"],
                "search_terms": json.dumps(["Phone 2a", "Nothing Phone 2a", "2a"]),
                "model_variants": json.dumps(["2a"])
            }
        ]
        
        # Insert models
        for model_data in models_data:
            model = PhoneModel(**model_data)
            db.add(model)
        
        db.commit()
        print(f"Successfully seeded {len(brands_data)} brands and {len(models_data)} phone models")
        
    except Exception as e:
        print(f"Error seeding brands and models: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    seed_brands_and_models()
