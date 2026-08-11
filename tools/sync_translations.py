"""Fill missing locale entries from the canonical English translation file."""

import json
from pathlib import Path


LANG = Path("src/main/resources/assets/builders_palette/lang")


def main():
    english = json.loads((LANG / "en_us.json").read_text(encoding="utf-8"))
    for locale_path in LANG.glob("*.json"):
        if locale_path.name == "en_us.json":
            continue
        locale = json.loads(locale_path.read_text(encoding="utf-8"))
        missing = {key: value for key, value in english.items() if key not in locale}
        if missing:
            locale.update(missing)
            locale_path.write_text(
                json.dumps(locale, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
        print(f"{locale_path.name}: added {len(missing)} fallback name(s)")


if __name__ == "__main__":
    main()
