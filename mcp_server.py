# mcp_server.py
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional

MENU_DB: List[Dict[str, Any]] = [
    {"name": "Classic Bruschetta", "category": "Appetizer", "price": 6.50, "description": "Toasted bread with fresh tomatoes, garlic, basil, and olive oil."},
    {"name": "Tomato Soup", "category": "Appetizer", "price": 5.90, "description": "Creamy soup made from sun-ripened tomatoes with a touch of cream."},
    {"name": "Wiener Schnitzel", "category": "Main Course", "price": 18.90, "description": "Classic veal cutlet in a crispy breading, served with french fries and a side salad."},
    {"name": "Spaghetti Carbonara", "category": "Main Course", "price": 14.50, "description": "Spaghetti with a creamy sauce of egg, pancetta, parmesan, and black pepper."},
    {"name": "Grilled Salmon Fillet", "category": "Main Course", "price": 22.50, "description": "Grilled salmon fillet on a bed of Mediterranean vegetables."},
    {"name": "Tiramisu", "category": "Dessert", "price": 7.50, "description": "Homemade Tiramisu based on an original Italian recipe."},
    {"name": "Panna Cotta", "category": "Dessert", "price": 6.90, "description": "Cooked cream dessert served with a fresh strawberry sauce."},
    {"name": "Mineral Water", "category": "Beverage", "price": 3.00, "description": "A bottle of still or sparkling water."},
    {"name": "Apple Spritzer", "category": "Beverage", "price": 3.50, "description": "Refreshing mix of apple juice and sparkling water."},
]

mcp = FastMCP("Restaurant Menu Service", stateless_http=True, port=8001)

@mcp.tool(
    description=(
        "Searches the restaurant menu. "
        "Can be filtered by 'category' or by a specific dish 'name'. "
        "Returns the entire menu if no parameters are provided."
    )
)
def get_menu_items(
    category: Optional[str] = None,
    name: Optional[str] = None
) -> List[Dict[str, Any]]:
    # --- DEBUG-PRINTS ---
    print("\n" + "="*30)
    print("|| MCP-SERVER: Tool 'get_menu_items' was called!")
    print(f"|| -> Received category: {category}")
    print(f"|| -> Received name: {name}")
    print("="*30 + "\n")
    items = MENU_DB
    if category:
        items = [item for item in items if category.lower() in item['category'].lower()]
    if name:
        items = [item for item in items if name.lower() in item['name'].lower()]
    return items

if __name__ == "__main__":
    print("▶️  Starting standalone MCP Server...")
    mcp.run(transport="streamable-http")