mkdir ~p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableC0RS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml