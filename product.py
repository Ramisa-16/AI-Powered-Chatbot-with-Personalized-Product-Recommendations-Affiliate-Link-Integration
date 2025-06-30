import google.generativeai as genai
import json
import urllib.parse
import random

genai.configure(api_key="AIzaSyB01ouUyKFz7IGzCgEnBdHnEY9QRQXPfIQ")

affiliate_links_db = [
    {"category": "Phone", "product_name": "iPhone 14 Pro Max", "product_link": "https://www.apple.com/iphone-14-pro", "product_price": "$1,099"},
    {"category": "Phone", "product_name": "Samsung Galaxy S23 Ultra", "product_link": "https://www.samsung.com/us/smartphones/galaxy-s23-ultra/", "product_price": "$1,199"},
    {"category": "Phone", "product_name": "Google Pixel 7 Pro", "product_link": "https://store.google.com/us/product/pixel_7_pro?hl=en-US", "product_price": "$899"},
    {"category": "Laptop", "product_name": "Alienware m15 R6", "product_link": "https://affiliate-link.com/product123", "product_price": "$1,500"},
    {"category": "Smartwatch", "product_name": "Fitness Smartwatch 3", "product_link": "https://affiliate-link.com/product789", "product_price": "$150"}
]

def get_best_match_from_db(user_input, affiliate_links_db):
    """
    This function matches the user query with relevant products from the affiliate links database.
    It uses Gemini AI (GenAI) to detect the category dynamically and also generate an intro line.
    If no match is found, it provides recommendations from popular e-commerce sites like Amazon, Alibaba, or others using keywords.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"User is asking for a product. Based on the input '{user_input}', determine the product category they are asking for (e.g., 'Phone', 'Laptop', 'Smartwatch'). Reply only with the category."
        
        response = model.generate_content([prompt])
        generated_content = response.candidates[0].content.parts[0].text 
        category_from_input = generated_content.strip().lower()  
        
        if not category_from_input:
            return {"intro": "Sorry, I couldn't understand your request.", "products": []}

        matched_products = [product for product in affiliate_links_db if category_from_input in product["category"].lower()]

        if not matched_products:
            search_query = user_input.strip().lower()
            search_query = urllib.parse.quote_plus(search_query)  
            
            platforms = [
                f"https://www.amazon.com/s?k={search_query}", 
                f"https://www.alibaba.com/trade/search?SearchText={search_query}",  
                f"https://www.ebay.com/sch/i.html?_nkw={search_query}",  
                f"https://www.walmart.com/search/?query={search_query}"  
            ]
            random.shuffle(platforms)
            search_url = platforms[0]

            return {
                "intro": f"Sorry, we couldn't find any products for '{user_input}', but you can explore more options on the following platform: {search_url}",
                "products": []
            }

        intro_prompt = f"User is looking for products related to '{category_from_input}'. Generate an engaging introduction line that will introduce a list of products for this category."
        intro_response = model.generate_content([intro_prompt])
        intro_line = intro_response.candidates[0].content.parts[0].text.strip()  
        if not intro_line:
            intro_line = "Here are some products that match your request:"

        response_data = {
            "intro": intro_line,
            "products": [
                {
                    "product_name": product["product_name"],
                    "product_link": product["product_link"]
                }
                for product in matched_products
            ]
        }

        return json.dumps(response_data, indent=4)

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"intro": "Sorry, there was an error while processing your request.", "products": []}

user_input1 = "show me mobile options"
user_input2 = "gaming laptop"
user_input3 = "smartwatch"
user_input4 = "iphone"
user_input5 = "buy cheap shoes"
user_input6 = "premium camera"

print(get_best_match_from_db(user_input1, affiliate_links_db))
print(get_best_match_from_db(user_input2, affiliate_links_db))
print(get_best_match_from_db(user_input3, affiliate_links_db))
print(get_best_match_from_db(user_input4, affiliate_links_db))
print(get_best_match_from_db(user_input5, affiliate_links_db))
print(get_best_match_from_db(user_input6, affiliate_links_db))