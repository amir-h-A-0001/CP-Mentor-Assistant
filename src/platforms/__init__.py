from . import codeforces

PLATFORMS = {
    "codeforces": codeforces
    }

def get_platform(name):
    return PLATFORMS[name]

def get_platform_from_url(url):
    for platform in PLATFORMS.values():
        if platform.supports(url):
            return platform

    raise ValueError(f"Unknown platform: {url}")
