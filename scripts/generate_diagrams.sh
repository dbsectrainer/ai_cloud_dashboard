#!/bin/bash

# Create output directory if it doesn't exist
mkdir -p docs/diagrams/images

# Generate PNG files from DOT files
for dot_file in docs/diagrams/*.dot; do
    filename=$(basename "$dot_file" .dot)
    dot -Tpng "$dot_file" -o "docs/diagrams/images/$filename.png"
done

echo "Diagrams generated successfully in docs/diagrams/images/"
