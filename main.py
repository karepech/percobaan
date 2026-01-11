from engine.headless_browser import sniff_requests
from extractor.m3u_builder import build_m3u
import os

def main():
    streams_all = []

    if not os.path.exists("output"):
        os.makedirs("output")

    with open("targets.txt", "r") as f:
        targets = [x.strip() for x in f.readlines() if x.strip()]

    for url in targets:
        try:
            print(f"[+] Scanning: {url}")
            streams = sniff_requests(url)
            streams_all.extend(streams)
        except Exception as e:
            print(f"[!] Error {url}: {e}")

    streams_all = sorted(set(streams_all))
    build_m3u(streams_all, "output/playlist.m3u")

if __name__ == "__main__":
    main()
