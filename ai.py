import google.generativeai as genai

genai.configure(api_key="AIzaSyB01ouUyKFz7IGzCgEnBdHnEY9QRQXPfIQ")

affiliate_links_db = [
    {"product_name": "Alienware m15 R6", "product_link": "https://affiliate-link.com/product123"},
    {"product_name": "Gaming Laptop XYZ", "product_link": "https://affiliate-link.com/product456"},
    {"product_name": "Laptop ABC", "product_link": "https://affiliate-link.com/product789"},
    {"product_name": "Smartwatch 7", "product_link": "https://affiliate-link.com/product124"},
    {"product_name": "Fitness Smartwatch 3", "product_link": "https://affiliate-link.com/product789"},
    {"product_name": "iPhone 13", "product_link": "https://affiliate-link.com/product101"},
    {"product_name": "Samsung Galaxy S21", "product_link": "https://affiliate-link.com/product102"}
]

def get_best_match_from_db(user_input):
    """
    This function uses Gemini AI to analyze the user input and match it to the closest product in the affiliate links database.
    Here, we use only one combined prompt.
    """
    prompt = f"""
    You are a helpful shopping assistant that recommends products based on user preferences and provides affiliate links for the products.
    You will receive user queries, and based on those queries, you should find the best matching products from the following database. Return only the relevant products from the database, including their names and links.

    User is looking for a product related to: {user_input}.
    Here is the product database:
    {affiliate_links_db}
    Please identify the best match from this list, and only return relevant products related to the query.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([prompt])
        generated_content = response.candidates[0].content.parts[0].text
        return generated_content

    except Exception as e:
        return f"An error occurred while processing the request: {str(e)}"

def get_bot_response(user_input):
    """
    This function processes the user input and responds with affiliate links if available.
    """
    affiliate_message = get_best_match_from_db(user_input)
    return affiliate_message

user_input = "I'm looking for a new smartphone."
bot_response = get_bot_response(user_input)
print(bot_response)