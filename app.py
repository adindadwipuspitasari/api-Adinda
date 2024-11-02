from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Sample data for perfume items
perfume_items = [
    {"id": 1, "name": "Fresh Citrus", "brand": "CitrusCo", "price": 250, "available": True, "size": "100ml", "scent": "Citrus", "stock": 30},
    {"id": 2, "name": "Mystic Oud", "brand": "OudHouse", "price": 500, "available": True, "size": "50ml", "scent": "Oud", "stock": 15},
    {"id": 3, "name": "Floral Bliss", "brand": "FloraFame", "price": 300, "available": True, "size": "75ml", "scent": "Floral", "stock": 20},
    {"id": 4, "name": "Woody Harmony", "brand": "NatureEssence", "price": 450, "available": True, "size": "100ml", "scent": "Woody", "stock": 10},
    {"id": 5, "name": "Ocean Breeze", "brand": "AquaFresh", "price": 350, "available": True, "size": "50ml", "scent": "Aqua", "stock": 25}
]

# Helper function to get a new ID
def get_new_id():
    if perfume_items:
        return max(item["id"] for item in perfume_items) + 1
    return 1

# GET all perfumes
class GetAllPerfumes(Resource):
    def get(self):
        return {"error": False, "message": "success", "count": len(perfume_items), "items": perfume_items}

# POST new perfume
class AddPerfume(Resource):
    def post(self):
        data = request.json
        new_id = get_new_id()
        
        new_item = {
            "id": new_id,
            "name": data.get("name"),
            "brand": data.get("brand"),
            "price": data.get("price"),
            "available": data.get("available", True),
            "size": data.get("size", "50ml"),
            "scent": data.get("scent", "Unknown"),
            "stock": data.get("stock", 0)
        }
        perfume_items.append(new_item)
        
        return {"error": False, "message": "Perfume added successfully", "item": new_item}, 201

# GET perfume by ID
class GetPerfumeById(Resource):
    def get(self, item_id):
        item = next((item for item in perfume_items if item["id"] == item_id), None)
        if not item:
            return {"error": True, "message": "Perfume not found"}, 404
        return {"error": False, "message": "success", "item": item}

# PUT (update) perfume by ID
class UpdatePerfume(Resource):
    def put(self, item_id):
        data = request.json
        item = next((item for item in perfume_items if item["id"] == item_id), None)
        if not item:
            return {"error": True, "message": "Perfume not found"}, 404
        
        # Update item data
        item.update({
            "name": data.get("name", item["name"]),
            "brand": data.get("brand", item["brand"]),
            "price": data.get("price", item["price"]),
            "available": data.get("available", item["available"]),
            "size": data.get("size", item["size"]),
            "scent": data.get("scent", item["scent"]),
            "stock": data.get("stock", item["stock"])
        })
        
        return {"error": False, "message": "Perfume updated successfully", "item": item}

# DELETE perfume by ID
class DeletePerfume(Resource):
    def delete(self, item_id):
        global perfume_items
        perfume_items = [item for item in perfume_items if item["id"] != item_id]
        
        return {"error": False, "message": "Perfume deleted successfully"}

# Registering resources with endpoints
api.add_resource(GetAllPerfumes, "/perfumes")               # GET all perfumes
api.add_resource(AddPerfume, "/perfumes/add")                # POST new perfume
api.add_resource(GetPerfumeById, "/perfumes/<int:item_id>")  # GET perfume by ID
api.add_resource(UpdatePerfume, "/perfumes/update/<int:item_id>")  # PUT update perfume by ID
api.add_resource(DeletePerfume, "/perfumes/delete/<int:item_id>")  # DELETE perfume by ID

if __name__ == "__main__":
    app.run(debug=True)
