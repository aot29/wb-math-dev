# Please see DEVELOPERS.md for help
#
# Contributions to this file are welcome but please note that this file is
# minimal by design, with the idea to make it easily extensible via
# docker-compose.override.yml. For help with doing that, please see
# DEVELOPERS.md
version: '3.7'
services:
  mediawiki:
    image: docker-registry.wikimedia.org/dev/buster-php72-fpm:2.0.0-s1
    user: "${MW_DOCKER_UID}:${MW_DOCKER_GID}"
    volumes:
      - ./:/var/www/html/w:cached
    env_file:
      - '.env'
    environment:
      COMPOSER_CACHE_DIR: '/var/www/html/w/cache/composer'
      MW_SERVER: 'http://localhost:${MW_DOCKER_PORT:-8080}'
      MW_SCRIPT_PATH: '/w'
      MW_DBPATH: '/var/www/html/w/cache/sqlite'
      MW_DBTYPE: 'sqlite'
      MW_LANG: 'en'
      MW_USER: '${MEDIAWIKI_USER:-Admin}'
      MW_PASS: '${MEDIAWIKI_PASSWORD:-dockerpass}'
      MW_SITENAME: 'MediaWiki'
      MW_LOG_DIR: /var/www/html/w/cache
      XDEBUG_CONFIG: '${XDEBUG_CONFIG}'
      XDEBUG_ENABLE: '${XDEBUG_ENABLE:-true}'
      XHPROF_ENABLE: '${XHPROF_ENABLE:-true}'

  mediawiki-web:
    image: docker-registry.wikimedia.org/dev/buster-apache2:1.0.0-s1
    user: "${MW_DOCKER_UID}:${MW_DOCKER_GID}"
    ports:
      - "${MW_DOCKER_PORT:-8080}:8080"
    volumes:
      - ./:/var/www/html/w:cached
    env_file:
      - '.env'
    environment:
      MW_LOG_DIR: /var/www/html/w/cache

  mediawiki-jobrunner:
    image: docker-registry.wikimedia.org/dev/buster-php72-jobrunner:1.0.0-s1
    user: "${MW_DOCKER_UID}:${MW_DOCKER_GID}"
    volumes:
      - ./:/var/www/html/w:cached
    env_file:
      - '.env'
    environment:
      MW_LOG_DIR: /var/www/html/w/cache
      MW_INSTALL_PATH: /var/www/html/w
      
  database:
    image: mariadb
    environment:
      MYSQL_ALLOW_EMPTY_PASSWORD: 1
    volumes:
      - /dbdata:/var/lib/mysql
      
volumes:
  dbdata:
    driver: local