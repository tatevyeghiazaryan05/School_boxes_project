import random

from fastapi import APIRouter, HTTPException
import main

home_page_router = APIRouter()


@home_page_router.get("/api/home_page/get/products")
def home_page_get_products():
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


@home_page_router.get("/api/home_page/filter/products/by/brand/{product_brand}")
def filter_products_by_brand(product_brand: str):
    main.cursor.execute("SELECT * FROM products WHERE product_brand = %s",
                        (product_brand,))
    products = main.cursor.fetchall()
    return products


@home_page_router.get("/api/home_page/filter/products/by/category/{category}")
def filter_products_by_category(category: str):
    main.cursor.execute("SELECT * FROM products WHERE category = %s",
                        (category,))
    products = main.cursor.fetchall()
    return products


@home_page_router.get("/api/home_page/filter/products/by/price/{min_price}/{max_price}")
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


@home_page_router.get("/api/home_page/filter/products/by/color/{color}")
def filter_products_by_color(color: str):
    main.cursor.execute("SELECT * FROM products WHERE color = %s",
                        (color,))
    products = main.cursor.fetchall()
    return products


@home_page_router.get("/api/home_page/filter/products/by/tags/{tags}")
def filter_products_by_tags(tags: str):
    try:
        main.cursor.execute("SELECT * FROM products WHERE %s = ANY(tags)",
                            (tags,))
        products = main.cursor.fetchall()
        return products
    except Exception as e:
        main.conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
