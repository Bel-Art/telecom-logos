# telecom-logos

> Some logos are outdated !

## Add logos

To add or update logos, create a [Pull request](https://github.com/Bel-Art/telecom-logos/pulls)!

## Convert to black and keep transparent background

```bash
convert input.png -background none -fill black -fuzz 99% -alpha set -channel RGBA -opaque white output_black.png
```

## Build && Test

```bash
python3 .github/workflows/build.py
python3 -m http.server
```
