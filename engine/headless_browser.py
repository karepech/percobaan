from playwright.sync_api import sync_playwright

def sniff_requests(url):
    found = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = browser.new_context()
        page = context.new_page()

        def on_request(req):
            if ".m3u8" in req.url:
                found.add(req.url)

        def on_response(res):
            try:
                if ".m3u8" in res.url:
                    found.add(res.url)

                ctype = res.headers.get("content-type", "")
                if "application/json" in ctype:
                    text = res.text()
                    if ".m3u8" in text:
                        for part in text.split():
                            if ".m3u8" in part:
                                found.add(
                                    part.strip('"').strip("'").strip(",")
                                )
            except:
                pass

        page.on("request", on_request)
        page.on("response", on_response)

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(15000)
        except:
            pass

        browser.close()

    return list(found)
