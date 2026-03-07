#!/bin/bash
# Comprehensive demonstration of fontmeta tool

source venv/bin/activate

echo "========================================="
echo "FONT LICENSE METADATA READER DEMO"
echo "========================================="
echo ""

echo "1. Display full license text from WOFF2 file"
echo "-------------------------------------------"
python -m fontmeta.cli fonts/inter/extras/woff-hinted/Inter-Bold.woff2 --license
echo ""

echo "2. Verify against OSI canonical license"
echo "-------------------------------------------"
python -m fontmeta.cli fonts/roboto/Roboto-Regular.ttf --verify-canonical
echo ""

echo "3. Quick batch verification"
echo "-------------------------------------------"
echo "Checking 5 Inter WOFF2 fonts:"
for font in fonts/inter/extras/woff-hinted/Inter-{Regular,Bold,Light,Medium,Black}.woff2; do
    if [ -f "$font" ]; then
        python -m fontmeta.cli "$font" --verify
    fi
done
echo ""

echo "4. JSON export (sample)"
echo "-------------------------------------------"
python -m fontmeta.cli fonts/inter/extras/woff-hinted/Inter-Regular.woff2 --format json | head -20
echo "    ... (truncated)"
echo ""

echo "========================================="
echo "DEMO COMPLETE"
echo "========================================="
