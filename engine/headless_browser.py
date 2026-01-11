from playwright.sync_api import sync_playwright
import time

def sniff_requests(url):
    found = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = browser.new_context()
        page = context.new_page()

        # Tangkap REQUEST
        def on_request(req):
            if ".m3u8" in req.url:
                found.add(req.url)

        # Tangkap RESPONSE (INI PENTING)
        def on_response(res):
            try:
                url = res.url
                if ".m3u8" in url:
                    found.add(url)

                # Scan JSON response
                if "application/json" in res.headers.get("content-type", ""):
                    text = res.text()
                    if ".m3u8" in text:
                        for line in text.split():
                            if ".m3u8" in line:
                                found.add(line.strip('"').strip("'"))
            except:
                pass

        page.on("request", on_request)
        page.on("response", on_response)

        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        # TUNGGU LEBIH LAMA (OTT butuh waktu)
        page.wait_for_timeout(15000)

        browser.close()

    return list(found)
