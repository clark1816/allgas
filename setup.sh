mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = 5432\n\
enableCORS = true\n\
\n\
" > ~/.streamlit/config.toml
