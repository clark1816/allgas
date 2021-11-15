mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = server.port $PORT\n\
enableCORS = true\n\
\n\
" > ~/.streamlit/config.toml
