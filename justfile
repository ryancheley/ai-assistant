@default:
    just --list

@help:
    uv run ai_assistant.py --help

@claude-xml:
    files-to-claude-xml $(find . -path ./.git \
        -prune -o -name "_claude.xml" \
        -prune -o -name ".env" \
        -prune -o -name ".DS_Store" \
        -prune -o -type f -print)

setup:
    @if test ! -f .env; then cp .env.example .env && echo "Created .env from .env.example"; else echo ".env already exists"; fi