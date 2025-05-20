
CREATE DATABASE IF NOT EXISTS allestacoDB
    CHARACTER SET utf16
    COLLATE utf16_german2_ci;

USE allestacoDB;

CREATE TABLE benutzer (
    benutzer_id INT AUTO_INCREMENT PRIMARY KEY,
    vorname VARCHAR(255) NOT NULL,
    nachname VARCHAR(255) NOT NULL,
    benutzername VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
	password_encrypt VARCHAR(255) NOT NULL,
    rolle ENUM('käufer', 'verkäufer') NOT NULL
);

CREATE TABLE artikel (
    artikel_id INT AUTO_INCREMENT PRIMARY KEY,
	titel VARCHAR(255),
    verkaeufer_id INT NOT NULL,
    beschreibung TEXT,
    preis DECIMAL(10,2) NOT NULL,
    bildpfad VARCHAR(255),
    status ENUM('verfügbar', 'verkauft') NOT NULL,
    bestand INT NOT NULL,
    kategorie VARCHAR(255),
    FOREIGN KEY (verkaeufer_id) REFERENCES benutzer(benutzer_id)
);

CREATE TABLE abgeschlossene_kaeufe (
    kauf_id INT AUTO_INCREMENT PRIMARY KEY,
    kaeufer_id INT NOT NULL,
    artikel_id INT NOT NULL,
    versanddaten TEXT,
    kaufpreis DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (kaeufer_id) REFERENCES benutzer(benutzer_id),
    FOREIGN KEY (artikel_id) REFERENCES artikel(artikel_id)
);

CREATE TABLE warenkorb (
    warenkorb_id INT AUTO_INCREMENT PRIMARY KEY,
    kaeufer_id INT NOT NULL,
    FOREIGN KEY (kaeufer_id) REFERENCES benutzer(benutzer_id)
);

CREATE TABLE warenkorb_artikel (
    warenkorb_id INT NOT NULL,
    artikel_id INT NOT NULL,
    anzahl INT NOT NULL,
    PRIMARY KEY (warenkorb_id, artikel_id),
    FOREIGN KEY (warenkorb_id) REFERENCES warenkorb(warenkorb_id),
    FOREIGN KEY (artikel_id) REFERENCES artikel(artikel_id)
);

CREATE TABLE bewertung (
    bewertung_id INT AUTO_INCREMENT PRIMARY KEY,
    bewerter_id INT NOT NULL,
    bewerteter_id INT NOT NULL,
    kommentar TEXT,
    rolle_des_bewerteten ENUM('käufer', 'verkäufer') NOT NULL,
	sterne INT NOT NULL,
    FOREIGN KEY (bewerter_id) REFERENCES benutzer(benutzer_id),
    FOREIGN KEY (bewerteter_id) REFERENCES benutzer(benutzer_id)
);

CREATE TABLE aufrufe (
    aufrufer_id INT AUTO_INCREMENT PRIMARY KEY,
    artikel_id INT NOT NULL,
    anzahl INT,
    FOREIGN KEY (artikel_id) REFERENCES artikel(artikel_id)
);



--
-- Tabellenstruktur für Tabelle `taco_stack_test`
--

CREATE TABLE taco_stack_test (
  id int AUTO_INCREMENT PRIMARY KEY,
  name varchar(255) DEFAULT NULL
);

--
-- Daten für Tabelle `taco_stack_test`
--

INSERT INTO taco_stack_test (id, name) VALUES
(1, 'Mit der Datenbank ist alles Taco!');

---------------------------------------------

# Rechte für `taco`@`%`

GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, FILE, INDEX, ALTER, CREATE TEMPORARY TABLES, EXECUTE, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, EVENT, TRIGGER ON *.* TO `taco`@`%` IDENTIFIED BY PASSWORD '*7CA0A190BED49E7D08519F51A8F873A9E2FDEB08';

GRANT ALL PRIVILEGES ON `taco`.* TO `taco`@`%`;
