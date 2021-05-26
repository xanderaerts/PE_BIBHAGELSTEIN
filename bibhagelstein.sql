-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: dbbibhagelstein
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `boeken`
--

DROP TABLE IF EXISTS `boeken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `boeken` (
  `BoekID` int NOT NULL AUTO_INCREMENT,
  `Titel` varchar(150) DEFAULT NULL,
  `isbn` varchar(30) DEFAULT NULL,
  `auteur` varchar(50) DEFAULT NULL,
  `afkorting_auteur` varchar(5) DEFAULT NULL,
  `categorie` varchar(15) DEFAULT NULL,
  `nummer_jaartal_volgnummer` varchar(15) DEFAULT NULL,
  `LeenID` int DEFAULT NULL,
  PRIMARY KEY (`BoekID`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boeken`
--

LOCK TABLES `boeken` WRITE;
/*!40000 ALTER TABLE `boeken` DISABLE KEYS */;
INSERT INTO `boeken` VALUES (1,'4 vrienden, 1 spijkerbroek','90-245-4514-5','Brashares, Anne','BRAS','groen','2020/001',NULL),(2,'Het goddelijke monster','90-5333-571-4','Lanoye, Tom','LANO','rood','2020/002',NULL),(3,'Groenten uit Balen','90-223-0814-3','van den Broeck, Walter','BROE','blauw','2020/003',NULL),(4,'Op zoek naar violet park','Boektoppers','Valentine, Jeanny','VALE','groen','2020/004',NULL),(5,'Spijt!','90-30-17535-x','Slee, Carry','SLEE','groen','2020/005',NULL),(6,'Giftig','978-90-223-2320-5','Van Renterghem, Vera','RENT','groen','2020/006',NULL),(7,'Eva\'s oog','Boektoppers','Fossum, Karin','FOSS','rood','2020/007',NULL),(8,'Vrouwland','Boektoppers','Lamrebet, Trachida','LAMR','rood','2020/008',NULL),(9,'Vluchten','90-317-1546-8','Bowler, Tim','BOWL','blauw','2020/009',NULL),(10,'Kus me','90-317-0915-8','Moeyaert, Bart','MOEY','blauw','2020/010',NULL),(100,'test','test','test','test','test','test',NULL);
/*!40000 ALTER TABLE `boeken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leerlingen`
--

DROP TABLE IF EXISTS `leerlingen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leerlingen` (
  `LeerlingID` int NOT NULL AUTO_INCREMENT,
  `klas` varchar(10) DEFAULT NULL,
  `klas_nr` int DEFAULT NULL,
  `naam` varchar(50) DEFAULT NULL,
  `voornaam` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`LeerlingID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leerlingen`
--

LOCK TABLES `leerlingen` WRITE;
/*!40000 ALTER TABLE `leerlingen` DISABLE KEYS */;
INSERT INTO `leerlingen` VALUES (1,'6BI',1,'Aerts','Xander'),(2,'3C',1,'Berre','jef'),(3,'6BI',1,'Van Den Abeele','Sofie'),(4,'4BE',1,'TEST','TEST'),(5,'test',1,'terst','test');
/*!40000 ALTER TABLE `leerlingen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lenen`
--

DROP TABLE IF EXISTS `lenen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lenen` (
  `LeenID` int NOT NULL AUTO_INCREMENT,
  `datum` datetime DEFAULT NULL,
  `UserID` int DEFAULT NULL,
  `BoekID` int DEFAULT NULL,
  `LeerlingID` int DEFAULT NULL,
  PRIMARY KEY (`LeenID`),
  UNIQUE KEY `BoekID_UNIQUE` (`BoekID`),
  KEY `LeenUser_idx` (`UserID`),
  KEY `LeenBoek_idx` (`BoekID`),
  KEY `LeenLeerling_idx` (`LeerlingID`),
  CONSTRAINT `LeenBoek` FOREIGN KEY (`BoekID`) REFERENCES `boeken` (`BoekID`),
  CONSTRAINT `LeenLeerling` FOREIGN KEY (`LeerlingID`) REFERENCES `leerlingen` (`LeerlingID`),
  CONSTRAINT `LeenUser` FOREIGN KEY (`UserID`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lenen`
--

LOCK TABLES `lenen` WRITE;
/*!40000 ALTER TABLE `lenen` DISABLE KEYS */;
/*!40000 ALTER TABLE `lenen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(30) DEFAULT NULL,
  `password` varchar(150) DEFAULT NULL,
  `naam` varchar(50) DEFAULT NULL,
  `voornaam` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','pbkdf2:sha256:150000$5r5wiKnd$5bf298164baf90f051bbc5252f684086326be6075a37643395bd43992b8bba28','admin','admin');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-26 13:03:34
