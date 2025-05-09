import random

from fastapi import APIRouter
import main

user_router = APIRouter()


@user_router.get("/api/user/get/products")
def user_get_products():
    main.cursor.execute("SELECT DISTINCT category FROM  products")
    products_category = main.cursor.fetchall()
    main_products={}
    for c in products_category:
        main.cursor.execute("SELECT * FROM products WHERE category=%s",
                            (dict(c).get('category'),))
        products=main.cursor.fetchall()
        random.shuffle(products)
        selected_products = products[:2]
        main_products[dict(c).get('category')] = selected_products

    return main_products


@user_router.get("/api/user/filter/products/by/brand/{product_brand}")
def filter_products_by_brand(product_brand: str):
    main.cursor.execute("SELECT * FROM products WHERE product_brand = %s",
                        (product_brand,))
    products = main.cursor.fetchall()
    return products


@user_router.get("/api/user/filter/products/by/category/{category}")
def filter_products_by_category(category: str):
    main.cursor.execute("SELECT * FROM products WHERE category = %s",
                        (category,))
    products = main.cursor.fetchall()
    return products


@user_router.get("/api/user/filter/products/by/price")
def filter_products_by_price(min_price: float = None, max_price: float = None):
    if min_price is not None and max_price is not None:
        main.cursor.execute(
            "SELECT * FROM products WHERE price BETWEEN %s AND %s", (min_price, max_price)
        )
    elif min_price is not None:
        main.cursor.execute("SELECT * FROM products WHERE price >= %s", (min_price,))
    elif max_price is not None:
        main.cursor.execute("SELECT * FROM products WHERE price <= %s", (max_price,))
    else:
        main.cursor.execute("SELECT * FROM products")

    products = main.cursor.fetchall()
    return products


@user_router.get("/api/user/filter/products/by/color/{color}")
def filter_products_by_color(color: str):
    main.cursor.execute("SELECT * FROM products WHERE color = %s",
                        (color,))
    products = main.cursor.fetchall()
    return products


@user_router.get("/api/user/filter/products/by/tags")
def filter_products_by_tags(tags: str):
    main.cursor.execute("SELECT * FROM products WHERE tags LIKE %s",
                        ('%' + tags + '%',))
    products = main.cursor.fetchall()
    return products


