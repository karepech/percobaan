from playwright.sync_api import sync_playwright

def sniff_requests(url):
    found = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.new_page()

        def handle_request(request):
            if ".m3u8" in request.url:
                found.append(request.url)

        page.on("request", handle_request)

        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(5000)

        browser.close()

    return found
