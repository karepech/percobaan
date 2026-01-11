def build_m3u(streams, output):
    with open(output, "w") as f:
        f.write("#EXTM3U\n")
        for i, url in enumerate(streams, start=1):
            f.write(f"#EXTINF:-1,Auto Channel {i}\n")
            f.write(url + "\n")
