import re
import urllib.parse

def clean_name(text):
    text = urllib.parse.unquote(text)
    text = re.sub(r'\.m3u8.*$', '', text)
    text = re.sub(r'[_\-]+', ' ', text)
    text = re.sub(r'\d+p|\d+kbps', '', text, flags=re.I)
    return text.strip().title() or "Channel"

def guess_channel_name(url, index):
    parts = url.split("/")
    for p in reversed(parts):
        if ".m3u8" in p:
            name = clean_name(p)
            if len(name) > 3:
                return name
    return f"Channel {index}"

def build_m3u(streams, output):
    with open(output, "w") as f:
        f.write("#EXTM3U\n\n")

        for i, url in enumerate(streams, start=1):
            name = guess_channel_name(url, i)

            # LOGO dari nama channel (BUKAN dari stream)
            logo = f"https://logo.clearbit.com/{name.replace(' ', '').lower()}.com"

            f.write(
                f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{logo}",{name}\n'
            )
            f.write(url + "\n\n")
