echo "Building site..."
python3 src/main.py
cd public && python3 -m http.server 8888

echo "Finished building site"
