# Utilizando a versão slim para manter a imagem leve
FROM python:3.12-slim

# Variáveis de ambiente para Python e Poetry
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=2.3.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/opt/poetry/bin"

ARG POETRY_WITHOUT="--without dev"

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    ca-certificates \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# # Instalação de dependências do sistema e Google Chrome
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    wget \
    unzip \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgbm1 \
    libgcc1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1
    # libxtst6 \
    # lsb-release \
    # xdg-utils && \
    # list

RUN apt-get update && \
    apt-get install -y google-chrome-stable
#     # Limpeza de cache para reduzir o tamanho da imagem
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# Instalação do Poetry 2.3
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

# Configuração do diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependência
COPY pyproject.toml poetry.lock* ./

# Instala as dependências do projeto (sem pacotes de desenvolvimento)
RUN poetry install --no-root --no-interaction --no-ansi

RUN rm -rf "$POETRY_CACHE_DIR"

# Copia o resto do código
COPY . .

CMD ["python", "src/main.py"]