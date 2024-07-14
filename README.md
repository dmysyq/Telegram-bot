## README

### Project: Telegram bot for searching discounted goods

**Description:**

This Python script implements a Telegram bot that allows users to search for discounted goods on various Kazakhstani online stores (shop.kz, sulpak.kz, dns-shop.kz). The bot provides information about products, including title, price, old price, discount, and a link to the product.

**Functionality:**

* **Product search:** User can select a store and product category (smartphones, video cards, laptops) for searching.
* **Sending results:** The bot sends the found products with a discount of more than 15% in the form of text messages.
* **Additional features:**
  * Show channel with mailing list
  * Show user ID
  * "Extend subscription" and "My subscription" functions (in development)
  * Recommend bot

**Technologies:**

* **Python:** Programming language for implementing bot logic and data parsing.
* **aiogram:** Asynchronous library for creating Telegram bots.
* **requests:** Library for sending HTTP requests for parsing data from store sites.
* **BeautifulSoup4:** Library for parsing HTML code.
* **dotenv:** Library for securely storing the bot token in a .env file.
* **logging:** Library for error logging and debugging.

**Project structure:**

* **main.py:** Main file with bot logic and data parsing.
* **.env:** File for storing the bot token (not included in the repository).

**Installation:**

1. Create a virtual environment and activate it.
2. Install the required dependencies:
   ```bash
   pip install aiogram requests beautifulsoup4 dotenv
   ```
3. Create a `.env` file and add the `TELEGRAM_BOT_TOKEN` variable with your bot token.

**Run:**

```bash
python main.py
```

**Notes:**

* Data parsing is performed using basic methods and can be optimized.
* For more complex parsing and data processing, it is recommended to use specialized libraries.
* The "Extend subscription" and "My subscription" functions require additional implementation.
* To improve the user experience, you can add the ability to filter products by price, rating, and other parameters.

**TODO:**

* Develop "Extend subscription" and "My subscription" functions.
* Add the ability to filter products by price, rating, and other parameters.
* Optimize data parsing.
* Add error and exception handling.
* Expand bot functionality (e.g., new product notifications, price comparison).
