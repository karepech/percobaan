import os
import requests
from engine.headless_browser import sniff_requests
from extractor.m3u_builder import build_m3u

def is_direct_playlist(url):
    return url.endswith(".m3u") or url.endswith(".m3u8")

def fetch_direct_playlist(url):
    streams = []
    try:
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            for line in r.text.splitlines():
                line = line.strip()
                if line.startswith("http") and ".m3u8" in line:
                    streams.append(line)
    except:
        pass
    return streams

def main():
    os.makedirs("output", exist_ok=True)
    all_streams = []

    with open("targets.txt") as f:
        targets = [x.strip() for x in f if x.strip()]

    for url in targets:
        print(f"[+] Scan: {url}")

        if is_direct_playlist(url):
            print("    mode: direct playlist")
            streams = fetch_direct_playlist(url)
        else:
            print("    mode: website resolver")
            streams = sniff_requests(url)

        print(f"    Found {len(streams)} streams")
        for s in streams:
            print("      ", s)

        all_streams.extend(streams)

    all_streams = sorted(set(all_streams))

    if all_streams:
        build_m3u(all_streams, "output/playlist.m3u")
        print("[✓] playlist.m3u updated")
    else:
        print("[!] TIDAK ADA STREAM DITEMUKAN")

if __name__ == "__main__":
    main()
