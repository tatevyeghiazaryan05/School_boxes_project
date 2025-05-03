from fastapi import APIRouter
import main

user_router = APIRouter()


@user_router.get("/api/user/get/products")
def user_get_products():
    pass


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


@user_router.get("/api/user/filter/products/by/status/{is_active}")
def filter_products_by_status(is_active: bool):
    main.cursor.execute("SELECT * FROM products WHERE is_active = %s",
                        (is_active,))
    products = main.cursor.fetchall()
    return products


@user_router.get("/api/user/filter/products/by/tags")
def filter_products_by_tags(tags: str):
    main.cursor.execute("SELECT * FROM products WHERE tags LIKE %s",
                        ('%' + tags + '%',))
    products = main.cursor.fetchall()
    return products
