
CREATE DATABASE IF NOT EXISTS allestacoDB
    CHARACTER SET utf16
    COLLATE utf16_german2_ci;

USE allestacoDB;

CREATE TABLE benutzer (
    benutzer_id INT AUTO_INCREMENT PRIMARY KEY,
    vorname VARCHAR(255) NOT NULL,
    nachname VARCHAR(255) NOT NULL,
    benutzername VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    rolle ENUM('käufer', 'verkäufer') NOT NULL
);

CREATE TABLE artikel (
    artikel_id INT AUTO_INCREMENT PRIMARY KEY,
	tiel VARCHAR(255),
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
    FOREIGN KEY (bewerter_id) REFERENCES benutzer(benutzer_id),
    FOREIGN KEY (bewerteter_id) REFERENCES benutzer(benutzer_id)
);

CREATE TABLE aufrufe (
    aufrufer_id INT AUTO_INCREMENT PRIMARY KEY,
    artikel_id INT NOT NULL,
    anzahl INT,
    FOREIGN KEY (artikel_id) REFERENCES artikel(artikel_id)
);
