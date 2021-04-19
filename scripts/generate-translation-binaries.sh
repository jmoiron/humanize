set -e

for d in src/humanize/locale/*/; do
    locale="$(basename $d)"
    echo "$locale"
    # compile to binary .mo
    msgfmt --check -o src/humanize/locale/$locale/LC_MESSAGES/humanize{.mo,.po}
done
