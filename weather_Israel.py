from mcp.server.fastmcp import FastMCP
from playwright.async_api import TimeoutError as PlaywrightTimeout
from playwright.async_api import async_playwright


mcp = FastMCP("weather-Israel")

FORECAST_URL = "https://www.weather2day.co.il/forecast"

# משתנים גלובליים לשמירת מצב הדפדפן בין הפעלות הכלים השונים
_playwright_context = None
_browser = None
_page = None

async def get_active_page():
    """מחזירה את הדף הפעיל, או מאתחלת את הדפדפן אם עדיין לא נפתח"""
    global _playwright_context, _browser, _page
    if _page is None:
        _playwright_context = await async_playwright().start()
        # headless=False קריטי כאן כדי שנראה את הדפדפן נפתח ולא ירוץ ברקע
        _browser = await _playwright_context.chromium.launch(headless=False)
        _page = await _browser.new_page()
    return _page

@mcp.tool()
async def open_weather_forecast_israel() -> str:
    """
    STEP 1: Opens the browser and navigates to the Israel weather website.
    CRITICAL: You MUST call this tool FIRST before searching for any city!
    """
    page = await get_active_page()
    await page.goto(FORECAST_URL)
    return "Navigated to weather2day.co.il forecast page successfully."

@mcp.tool()
async def enter_weather_forecast_city_israel(city: str) -> str:
    """
    STEP 2: Enters the city name into the search box.
    CRITICAL: You MUST call this tool only AFTER successfully calling open_weather_forecast_israel.
    CRITICAL: The website is in Hebrew. You MUST translate the city name to Hebrew! For example, pass 'ירושלים' instead of 'Jerusalem'.
    """
    page = await get_active_page()
    
    search_box = page.locator('#city_search_forecast')
    await search_box.clear()
    await search_box.press_sequentially(city, delay=200)
    await page.wait_for_timeout(1000)
    
    return f"Entered the city: {city} into the search box and waited for autocomplete."

@mcp.tool()
async def select_weather_forecast_city_israel() -> str:
    """
    STEP 3: Selects the first item from the autocomplete dropdown list.
    CRITICAL: You MUST call this tool only AFTER successfully calling enter_weather_forecast_city_israel.
    """
    page = await get_active_page()
    
    await page.keyboard.press("ArrowDown")
    await page.keyboard.press("Enter")
    
    return "Selected the first city from the autocomplete dropdown."

@mcp.tool()
async def extract_weather_data_israel() -> str:
    """
    STEP 4: Extracts the weather forecast text from the page.
    CRITICAL: You MUST call this tool ONLY AFTER successfully selecting the city in STEP 3.
    Use the extracted data to answer the user's question about the weather.
    """
    page = await get_active_page()

    await page.wait_for_timeout(3000)
    
    raw_text = await page.evaluate("document.body.innerText")
    
    # ניקוי הטקסט: פיצול לשורות והסרת שורות ריקות לחלוטין
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    cleaned_text = '\n'.join(lines)
    
    return f"Extracted Weather Data for the user:\n{cleaned_text[:3000]}"


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
