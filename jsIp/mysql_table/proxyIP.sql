CREATE TABLE proxies (
    ipPort          varchar(21) NOT NULL,
    proxyType       varchar(7) NOT NULL,
    anonymity       varchar(4) NOT NULL,
    city            varchar(40) NOT NULL,
    bang            varchar(5) NOT NULL,
    hostName        varchar(80) NOT NULL,
    lastUpdate      TIMESTAMP NOT NULL,
    dlTimestamp     varchar(26) NOT NULL,
    PRIMARY KEY(ipPort)
    ) ENGINE = InnoDB CHAR SET=utf9;

CREATE TABLE IPcountry (
    TLD         VARCHAR(5) NOT NULL,
    country     VARCHAR(25) NOT NULL,
    count       SMALLINT UNSIGNED DEFAULT 0,
    dlTimestamp     varchar(26) NOT NULL,
    PRIMARY KEY (TLD, country)
) ENGINE = InnoDB CHAR SET=utf8;
