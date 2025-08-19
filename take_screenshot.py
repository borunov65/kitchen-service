import asyncio
from pyppeteer import launch
import os


async def take_full_screenshot():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    output_file = os.path.join(os.getcwd(), "demo.png")

    browser = await launch(
        executablePath=chrome_path,
        headless=True,
        args=['--no-sandbox']
    )
    page = await browser.newPage()

    await page.setViewport({'width': 1440, 'height': 900})

    # Відкриваємо сторінку логіну
    await page.goto(
        "http://127.0.0.1:8000/accounts/login/",
        {'waitUntil': 'networkidle2'}
    )

    # Логін
    await page.type('input[name="username"]', 'admin')
    await page.type('input[name="password"]', 'vetochka04')

    # Натискаємо кнопку та чекаємо навігації
    await asyncio.gather(
        page.click('input[type="submit"]'),
        page.waitForNavigation({'waitUntil': 'networkidle2'})
    )

    # Додаткова пауза для JS
    await asyncio.sleep(2)

    # ✅ Ховаємо тільки Debug Toolbar
    await page.evaluate('''() => {
        const dtb = document.querySelector('#djDebug');
        if (dtb) dtb.style.display = 'none';
    }''')

    # Чекаємо, щоб зміни застосувалися
    await asyncio.sleep(0.5)

    # Встановлюємо viewport по фактичній висоті контенту
    height = await page.evaluate('document.body.scrollHeight')
    await page.setViewport({'width': 1440, 'height': height})

    # Робимо скріншот всієї сторінки
    await page.screenshot({'path': output_file, 'fullPage': False})

    await browser.close()
    print(f"✅ Скріншот збережено у {output_file}")

asyncio.run(take_full_screenshot())
