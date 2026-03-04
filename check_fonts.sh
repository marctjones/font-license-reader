#!/bin/bash
# Batch font license checker
# Usage: ./check_fonts.sh <directory> [output_format]

if [ -z "$1" ]; then
    echo "Usage: $0 <directory> [text|json|verify]"
    echo ""
    echo "Examples:"
    echo "  $0 fonts/inter/ verify          # Quick verification"
    echo "  $0 fonts/ text                  # Detailed text output"
    echo "  $0 fonts/roboto/ json > out.json # JSON output"
    exit 1
fi

DIR="$1"
MODE="${2:-verify}"

source venv/bin/activate

case "$MODE" in
    verify)
        echo "Verifying licenses in: $DIR"
        echo "========================================"
        find "$DIR" -type f \( -name "*.ttf" -o -name "*.otf" -o -name "*.woff" -o -name "*.woff2" \) | while read font; do
            python fontmeta.py "$font" --verify
        done
        ;;
    json)
        echo "["
        first=true
        find "$DIR" -type f \( -name "*.ttf" -o -name "*.otf" -o -name "*.woff" -o -name "*.woff2" \) | while read font; do
            if [ "$first" = true ]; then
                first=false
            else
                echo ","
            fi
            python fontmeta.py "$font" --format json
        done
        echo "]"
        ;;
    text)
        find "$DIR" -type f \( -name "*.ttf" -o -name "*.otf" -o -name "*.woff" -o -name "*.woff2" \) | while read font; do
            python fontmeta.py "$font" --all
            echo ""
        done
        ;;
    *)
        echo "Unknown mode: $MODE"
        echo "Use: verify, json, or text"
        exit 1
        ;;
esac
