import json
import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Database connection parameters
DB_URL = "postgresql://sirvana:Sirvana@34.133.20.110:5432/postgres"


def get_restaurant_ids():
    """Read restaurants.json and return a set of URLs"""
    with open("./restaurants_by_category_20250309_092602.json", "r") as f:
        restaurants = json.load(f)
    return {restaurant["url"] for restaurant in restaurants}


def update_products():
    """Update products to isAvailable=false if their restaurant is not in restaurants.json"""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        valid_urls = get_restaurant_ids()

        update_query = """
            UPDATE "Product" p
            SET "isAvailable" = false,
                "updatedAt" = CURRENT_TIMESTAMP
            FROM "Restaurant" r
            WHERE p."restaurantId" = r.id
            AND r.url IS NOT NULL 
            AND r.url NOT IN %s
            RETURNING p.id, p.name, r.url;
        """

        cur.execute(update_query, (tuple(valid_urls),))
        updated_products = cur.fetchall()

        # Commit the transaction
        conn.commit()

        print(f"Updated {len(updated_products)} products to isAvailable=false")

    except Exception as e:
        print(f"An error occurred: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    update_products()
