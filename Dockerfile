FROM ubuntu:latest

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpcre3-dev \
    zlib1g-dev \
    libssl-dev

# Скачиваем исходный код Nginx
RUN wget http://nginx.org/download/nginx-1.20.1.tar.gz && \
    tar -xzf nginx-1.20.1.tar.gz

# Собираем Nginx с модулем ngx_http_auth_request_module
WORKDIR /nginx-1.20.1
RUN ./configure --with-http_auth_request_module && \
    make && \
    make install

# Копируем вашу конфигурацию Nginx
COPY nginx.conf /usr/local/nginx/conf/nginx.conf

# (Опционально) Копируем другие файлы, если необходимо
# COPY ...

# (Опционально) Указываем порт, который будет открыт
EXPOSE 80

# Запускаем Nginx
CMD ["/usr/local/nginx/sbin/nginx", "-g", "daemon off;"]