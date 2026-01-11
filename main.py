from engine.headless_browser import sniff_requests
from extractor.m3u_builder import build_m3u
import os

def main():
    all_streams = []

    os.makedirs("output", exist_ok=True)

    with open("targets.txt") as f:
        targets = [x.strip() for x in f if x.strip()]

    for url in targets:
        print(f"[+] Scan: {url}")
        streams = sniff_requests(url)
        print(f"[+] Found {len(streams)} streams")

        for s in streams:
            print("   ", s)

        all_streams.extend(streams)

    all_streams = sorted(set(all_streams))

    if not all_streams:
        print("[!] TIDAK ADA STREAM DITEMUKAN")
    else:
        build_m3u(all_streams, "output/playlist.m3u")
        print("[✓] playlist.m3u updated")

if __name__ == "__main__":
    main()
