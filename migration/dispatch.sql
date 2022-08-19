-- MySQL dump 10.13  Distrib 8.0.27, for Linux (x86_64)
--
-- Host: localhost    Database: dispatch
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dispatch_ack_method`
--

DROP TABLE IF EXISTS `dispatch_ack_method`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatch_ack_method` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `description` varchar(64) DEFAULT NULL,
  `need_text` tinyint(1) DEFAULT NULL,
  `need_photo` tinyint(1) DEFAULT NULL,
  `need_video` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_dispatch_ack_method_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispatch_ack_method`
--

LOCK TABLES `dispatch_ack_method` WRITE;
/*!40000 ALTER TABLE `dispatch_ack_method` DISABLE KEYS */;
INSERT INTO `dispatch_ack_method` VALUES (1,'simple_ack','just need reply only',0,0,0),(2,'need_text_only','need text only',1,0,0),(3,'need_text_photo','need text and photo',1,1,0),(4,'need_all','need text, photo and video',1,1,1);
/*!40000 ALTER TABLE `dispatch_ack_method` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dispatch_confirm`
--

DROP TABLE IF EXISTS `dispatch_confirm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatch_confirm` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dispatch_task_id` int DEFAULT NULL,
  `provider_name` varchar(64) DEFAULT NULL,
  `status` enum('fail','success','other') DEFAULT NULL,
  `description` text,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `dispatch_task_id` (`dispatch_task_id`),
  KEY `ix_dispatch_confirm_id` (`id`),
  CONSTRAINT `dispatch_confirm_ibfk_1` FOREIGN KEY (`dispatch_task_id`) REFERENCES `dispatch_task` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispatch_confirm`
--

LOCK TABLES `dispatch_confirm` WRITE;
/*!40000 ALTER TABLE `dispatch_confirm` DISABLE KEYS */;
/*!40000 ALTER TABLE `dispatch_confirm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dispatch_level`
--

DROP TABLE IF EXISTS `dispatch_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatch_level` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `description` varchar(64) DEFAULT NULL,
  `color_code` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_dispatch_level_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispatch_level`
--

LOCK TABLES `dispatch_level` WRITE;
/*!40000 ALTER TABLE `dispatch_level` DISABLE KEYS */;
INSERT INTO `dispatch_level` VALUES (1,'low','level low','[\"#ffffff\", \"#000000\"]'),(2,'medium','level medium','[\"#ffffff\", \"#000000\"]'),(3,'high','level high','[\"#ffffff\", \"#000000\"]');
/*!40000 ALTER TABLE `dispatch_level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dispatch_reply`
--

DROP TABLE IF EXISTS `dispatch_reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatch_reply` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dispatch_task_id` int DEFAULT NULL,
  `worker_name` varchar(64) DEFAULT NULL,
  `status` enum('fail','success','other') DEFAULT NULL,
  `description` text,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `dispatch_task_id` (`dispatch_task_id`),
  KEY `ix_dispatch_reply_id` (`id`),
  CONSTRAINT `dispatch_reply_ibfk_1` FOREIGN KEY (`dispatch_task_id`) REFERENCES `dispatch_task` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispatch_reply`
--

LOCK TABLES `dispatch_reply` WRITE;
/*!40000 ALTER TABLE `dispatch_reply` DISABLE KEYS */;
/*!40000 ALTER TABLE `dispatch_reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dispatch_reply_file`
--

DROP TABLE IF EXISTS `dispatch_reply_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatch_reply_file` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dispatch_reply_id` int DEFAULT NULL,
  `filename` varchar(64) DEFAULT NULL,
  `file_type` enum('photo','video') DEFAULT NULL,
  `content_type` varchar(64) DEFAULT NULL,
  `path` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `dispatch_reply_id` (`dispatch_reply_id`),
  KEY `ix_dispatch_reply_file_id` (`id`),
  CONSTRAINT `dispatch_reply_file_ibfk_1` FOREIGN KEY (`dispatch_reply_id`) REFERENCES `dispatch_reply` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispatch_reply_file`
--

LOCK TABLES `dispatch_reply_file` WRITE;
/*!40000 ALTER TABLE `dispatch_reply_file` DISABLE KEYS */;
/*!40000 ALTER TABLE `dispatch_reply_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dispatch_status`
--

DROP TABLE IF EXISTS `dispatch_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatch_status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `description` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_dispatch_status_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispatch_status`
--

LOCK TABLES `dispatch_status` WRITE;
/*!40000 ALTER TABLE `dispatch_status` DISABLE KEYS */;
INSERT INTO `dispatch_status` VALUES (1,'pending','waiting for workers to take'),(2,'in_progress','people are working'),(3,'reply_fail','worker reply failure'),(4,'reply_success','worker reply success'),(5,'reply_other','worker reply other'),(6,'confirm_fail','dispatcher confirm failure'),(7,'confirm_success','dispatcher confirm success'),(8,'confirm_other','dispatcher confirm other');
/*!40000 ALTER TABLE `dispatch_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dispatch_task`
--

DROP TABLE IF EXISTS `dispatch_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatch_task` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dispatch_event_id` varchar(64) DEFAULT NULL,
  `bind_event_id` varchar(64) DEFAULT NULL,
  `category` varchar(64) DEFAULT NULL,
  `level_id` int DEFAULT NULL,
  `provider` varchar(64) DEFAULT NULL,
  `job` varchar(64) DEFAULT NULL,
  `location` varchar(64) DEFAULT NULL,
  `assign_account` json DEFAULT NULL,
  `assign_account_role` json DEFAULT NULL,
  `assign_account_group` json DEFAULT NULL,
  `people_limit` int DEFAULT NULL,
  `order_taker` json DEFAULT NULL,
  `deadline` datetime DEFAULT NULL,
  `ack_method_id` int DEFAULT NULL,
  `status_id` int DEFAULT NULL,
  `isActive` tinyint(1) NOT NULL,
  `start_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dispatch_event_id` (`dispatch_event_id`),
  KEY `level_id` (`level_id`),
  KEY `ack_method_id` (`ack_method_id`),
  KEY `status_id` (`status_id`),
  KEY `ix_dispatch_task_id` (`id`),
  CONSTRAINT `dispatch_task_ibfk_1` FOREIGN KEY (`level_id`) REFERENCES `dispatch_level` (`id`),
  CONSTRAINT `dispatch_task_ibfk_2` FOREIGN KEY (`ack_method_id`) REFERENCES `dispatch_ack_method` (`id`),
  CONSTRAINT `dispatch_task_ibfk_3` FOREIGN KEY (`status_id`) REFERENCES `dispatch_status` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispatch_task`
--

LOCK TABLES `dispatch_task` WRITE;
/*!40000 ALTER TABLE `dispatch_task` DISABLE KEYS */;
/*!40000 ALTER TABLE `dispatch_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dispatch_template`
--

DROP TABLE IF EXISTS `dispatch_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatch_template` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dependence` varchar(64) DEFAULT NULL,
  `category` varchar(64) DEFAULT NULL,
  `level_id` int DEFAULT NULL,
  `job` varchar(64) DEFAULT NULL,
  `location` varchar(64) DEFAULT NULL,
  `assign_account_role` json DEFAULT NULL,
  `assign_account_group` json DEFAULT NULL,
  `people_limit` int DEFAULT NULL,
  `time_limit` datetime DEFAULT NULL,
  `ack_method_id` int DEFAULT NULL,
  `modify_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `level_id` (`level_id`),
  KEY `ack_method_id` (`ack_method_id`),
  KEY `ix_dispatch_template_id` (`id`),
  CONSTRAINT `dispatch_template_ibfk_1` FOREIGN KEY (`level_id`) REFERENCES `dispatch_level` (`id`),
  CONSTRAINT `dispatch_template_ibfk_2` FOREIGN KEY (`ack_method_id`) REFERENCES `dispatch_ack_method` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispatch_template`
--

LOCK TABLES `dispatch_template` WRITE;
/*!40000 ALTER TABLE `dispatch_template` DISABLE KEYS */;
/*!40000 ALTER TABLE `dispatch_template` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-17  1:54:44
