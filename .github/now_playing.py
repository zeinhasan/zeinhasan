#!/usr/bin/env python3
"""Write now-playing.svg + now-playing.html into OUT_DIR. The track rotates every 30 minutes.

Usage: python3 .github/now_playing.py dist
"""
import html, sys, time, pathlib, urllib.parse

# lengths read from the FLAC files in ~/music (floor seconds)
TRACKS = [
    ("Swedish House Mafia", "Moth To A Flame", 234),
    ("The Weeknd", "After Hours", 361),
    ("The Weeknd", "Cry For Me", 224),
    ("The Weeknd", "Save Your Tears", 215),
    ("The Weeknd", "São Paulo", 301),
    ("The Weeknd", "Timeless", 256),
]
SLOT = 30 * 60
RED, BLUE, GREY = "#ff2a3d", "#3b5bff", "#a1a1aa"


def mmss(s):
    return f"{s // 60}:{s % 60:02d}"


def spotify(artist, title):
    # ponytail: search link, swap for exact track URLs if search ever picks a cover version
    return "https://open.spotify.com/search/" + urllib.parse.quote(f"{artist} {title}")


def svg(artist, title, secs, i):
    a, t = html.escape(artist), html.escape(title.upper())
    w = title.split()
    mono = html.escape((w[0][0] + (w[-1][0] if len(w) > 1 else "")).upper())
    split = 30 + (i * 17) % 45  # each cover splits the red/blue light at a different point
    # elapsed clock: one label per second, each visible for 1s of the loop, so it ticks with the bar
    clock = "".join(
        f'<text x="142" y="128" class="d e" style="animation-delay:{s}s">{mmss(s)}</text>' for s in range(secs)
    )
    bars = "".join(
        f'<rect x="{392 + k * 9}" y="100" width="5" height="24" rx="1" class="q" '
        f'style="animation-delay:-{(k * 0.23) % 1:.2f}s"/>'
        for k in range(6)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="140" viewBox="0 0 480 140" role="img" aria-labelledby="t">
<title id="t">Now playing: {html.escape(title)} by {a}, {mmss(secs)}</title>
<style>
.q{{fill:{RED};transform-box:fill-box;transform-origin:bottom;animation:eq .9s ease-in-out infinite alternate}}
.p{{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:prog {secs}s linear infinite}}
.e{{opacity:0;animation:tick {secs}s step-end infinite}}
.s{{animation:hide 0s forwards}}
@keyframes hide{{to{{opacity:0}}}}
@keyframes eq{{0%{{transform:scaleY(.2)}}100%{{transform:scaleY(1)}}}}
@keyframes prog{{0%{{transform:scaleX(0)}}100%{{transform:scaleX(1)}}}}
@keyframes tick{{0%{{opacity:1}}{100 / secs:.4f}%{{opacity:0}}100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.q,.p,.e,.s{{animation:none}}}}
.ttl{{font:700 26px Impact,'Arial Narrow Bold','Helvetica Neue',sans-serif;letter-spacing:.5px}}
.mono{{font:700 56px Impact,'Arial Narrow Bold','Helvetica Neue',sans-serif}}
.art{{font:500 14px 'Helvetica Neue',Arial,sans-serif}}
.d{{font:500 12px 'Helvetica Neue',Arial,sans-serif;fill:{GREY}}}
</style>
<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{BLUE}"/><stop offset="{split}%" stop-color="#14062a"/>
<stop offset="{split + 25}%" stop-color="#2a0508"/><stop offset="1" stop-color="{RED}"/>
</linearGradient>
<clipPath id="c"><rect x="16" y="16" width="108" height="108" rx="6"/></clipPath>
</defs>
<rect width="480" height="140" rx="10" fill="#0b0b0f"/>
<g clip-path="url(#c)">
<rect x="16" y="16" width="108" height="108" fill="url(#g)"/>
<text x="70" y="90" class="mono" fill="#fff" text-anchor="middle">{mono}</text>
</g>
<text x="142" y="56" class="ttl" fill="#fff">{t}</text>
<text x="142" y="80" class="art" fill="{GREY}">{a}</text>
<rect x="142" y="108" width="230" height="3" rx="1.5" fill="#27272a"/>
<rect x="142" y="108" width="230" height="3" class="p" fill="{RED}"/>
<text x="142" y="128" class="d s">0:00</text>
{clock}
<text x="372" y="128" class="d" text-anchor="end">{mmss(secs)}</text>
{bars}
</svg>'''


def redirect(url):
    u = html.escape(url)
    return (f'<!doctype html><meta charset="utf-8"><title>Now playing</title>'
            f'<meta http-equiv="refresh" content="0;url={u}"><a href="{u}">Open on Spotify</a>\n')


def main():
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    out.mkdir(parents=True, exist_ok=True)
    i = int(time.time()) // SLOT % len(TRACKS)
    artist, title, secs = TRACKS[i]
    (out / "now-playing.svg").write_text(svg(artist, title, secs, i), encoding="utf-8")
    (out / "now-playing.html").write_text(redirect(spotify(artist, title)), encoding="utf-8")
    print(f"slot {i}: {artist} - {title}")


if __name__ == "__main__":
    main()
