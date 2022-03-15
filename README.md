dmitrii-ageev.openssl-gost
==========================

Ansible роль для установки и настройки библиотеки OpenSSL совместно с шифрами ГОСТ и сертификатами официальных удостоверяющих центров РФ: УЦ АО «ПФ «СКБ Контур», УЦ ООО «Сертум‑Про», УЦ ООО «ЦИБ‑Сервис», УЦ ООО «РСЦ «Инфо‑Бухгалтер», Минцифры России, Федерального органа в сфере электронной подписи и Удостоверяющего центра Федерального казначейства.



## Требования

Эту роль можно использовать с любым дистрибутивом основанном на Debian Linux.



## Параметры конфигурации

Для получения информации о всех переменных используемых данной ролью обратитесь к файлу `defaults/main.yml`.

Некоторые, наиболее важные по мнению автора, переменные указаны ниже:


* `openssl__validate_certs`: флаг отвечающий за проверку TLS сертификатов веб серверов с которых загружается информация. Значение `false` отключает проверку.
* `openssl__certificates`: список гиперссылок на сертификаты УЦ РФ.
* `openssl__get_certificates_from_origin`: флаг регулирующий установку сертификатов. По умолчанию сертификаты будут загружены из официальных источников. При установке значения флага в `false` будут установлены копии сертификатов поставляемых вместе с данной ролью. **Обратите внимание:** на сервере gosuslugi.ru настроен очень жёсткий фильтр от DDOS атак, поэтому некоторые соединения могут не пройти.
* `openssl__default_config`: содержит базовую конфигурацию библиотеки OpenSSL. 
* `openssl__config`: дополнительная конфигурация со стороны пользователя, параметры указанные в данной переменной переопределяют одноимённые в `openssl__default_config` (см. примеры использования).



## Примеры использования

В этом примере библиотека OpenSSL будет установлена и сконфигурированна для использования протокола TLS версии не ниже 1.3 и набором шифров ГОСТ и "HIGH", что в практическом плане означает те шифры у которых длина ключа шифрования 128 и более бит.


```
---
- name: "Example playbook: OpenSSL library and GOST ciphers installation"
  hosts: all
  become: true
  vars:
    openssl__get_certificates_from_origin: false
    
    openssl__config:
      system_default_sect:
        MinProtocol: TLSv1.3
        CipherString: "GOST89MAC:aGOST01:kGOST:HIGH"

  roles:
      - dmitrii-ageev.openssl-gost
```



## Лицензия

Данное программное обеспечение может быть использовано гражданами РФ в некоммерческих целях. 
Во всех остальных случаях необходмо получить согласие автора.



## Автор

Агеев Дмитрий <dmitrii@opsworks.ru>
