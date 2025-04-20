import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("cookbook")

# Constants
COOKBOOK_URL = "/path/of/your/cookbook"

@mcp.tool()
async def get_all_dishes() -> list:
    """Get the names of all dishes in the cookbook

     :return: all dishes in the cookbook
    """
    all_dishes = []
    for _, _, files in os.walk(COOKBOOK_URL):
        for file in files:
            if file.lower().endswith(".md"):
                dish_name = file.rsplit(".")[:-1][0]
                all_dishes.append(dish_name)
    return all_dishes


@mcp.tool()
async def get_recipe(dish: str) -> str:
    """Get the recipe of a dish
    Args:
        dish: the name of the dish
    :return: the recipe of the dish
    """
    dish_recipe_url = None
    for root, dirs, files in os.walk(COOKBOOK_URL):
        for file in files:
            if file.lower().endswith(".md") and dish.lower() in file.lower():
                dish_recipe_url = os.path.join(root, file)
    if not dish_recipe_url:
        return f"未找到: {dish} 这道菜的菜谱"
    try:
        with open(dish_recipe_url, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        content = f"{dish} 菜谱打开失败"
    return content

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')