# Générer en .dot
pyreverse -ASmy -o dot \
    -b \
    -k \
    $(find . -type f -name "__init__.py" \
    ! -path "*/tests/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/.venv/*" \
    ! -path "*/site-packages/*" \
    -exec dirname {} \;)

# Conversion en SVG avec texte plus grand et nœuds plus larges
dot -Tsvg \
    -Grankdir=TB \
    -Gsize="8,8\!" \
    -Gratio=fill \
    -Gfontsize=16 \
    -Nfontsize=14 \
    -Nwidth=2 \
    -Nheight=1 \
    classes.dot -o classes.svg

dot -Tsvg \
    -Grankdir=TB \
    -Gsize="8,8\!" \
    -Gratio=fill \
    -Gfontsize=16 \
    -Nfontsize=14 \
    -Nwidth=2 \
    -Nheight=1 \
    packages.dot -o packages.svg