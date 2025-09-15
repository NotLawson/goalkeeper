# Justfile
# no one actually used this but whatever
set windows-shell := ["C:\\Program Files\\Git\\bin\\sh.exe","-c"] # fix for windows
dev:
    @docker compose down; docker compose pull; docker compose build; docker compose up -d;