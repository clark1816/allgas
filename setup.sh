mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = 5432
enableCORS = true\n\
\n\
" > ~/.streamlit/config.toml
