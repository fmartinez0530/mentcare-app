-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: cs490_GP
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

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
-- Table structure for table `chats`
--

DROP TABLE IF EXISTS `chats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chats` (
  `chatID` int NOT NULL AUTO_INCREMENT,
  `patientID` int DEFAULT NULL,
  `therapistID` int DEFAULT NULL,
  `content` json DEFAULT NULL,
  `startTime` datetime DEFAULT NULL,
  `endTime` datetime DEFAULT NULL,
  PRIMARY KEY (`chatID`),
  KEY `patientID` (`patientID`),
  KEY `therapistID` (`therapistID`),
  CONSTRAINT `chats_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `patients` (`patientID`),
  CONSTRAINT `chats_ibfk_2` FOREIGN KEY (`therapistID`) REFERENCES `therapists` (`therapistID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chats`
--

LOCK TABLES `chats` WRITE;
/*!40000 ALTER TABLE `chats` DISABLE KEYS */;
INSERT INTO `chats` VALUES (1,1,1,'{\"chats\": [{\"msg\": \"Hellofasdf?\", \"sender\": \"P\"}, {\"msg\": \"Hello!\", \"sender\": \"T\"}, {\"msg\": \"I am sad\", \"sender\": \"P\"}, {\"msg\": \"Have you tried the antidepressant drugs\", \"sender\": \"T\"}, {\"msg\": \"Those scare me\", \"sender\": \"P\"}, {\"msg\": \"Theyll help trust me.\", \"sender\": \"T\"}, {\"msg\": \"Okay thank you\", \"sender\": \"P\"}]}','2023-10-01 09:00:00','2023-10-01 09:30:00'),(2,2,1,'{\"chats\": [{\"msg\": \"Hellohaha...\", \"sender\": \"P\"}, {\"msg\": \"Hello!\", \"sender\": \"T\"}, {\"msg\": \"I am sad\", \"sender\": \"P\"}, {\"msg\": \"Have you tried the antidepressant drugs\", \"sender\": \"T\"}, {\"msg\": \"Those scare me\", \"sender\": \"P\"}, {\"msg\": \"Theyll help trust me.\", \"sender\": \"T\"}, {\"msg\": \"Okay thank you\", \"sender\": \"P\"}]}','2023-10-02 10:00:00','2023-10-02 10:30:00'),(3,3,1,'{\"chats\": [{\"msg\": \"Hellovff!\", \"sender\": \"P\"}, {\"msg\": \"Hello!\", \"sender\": \"T\"}, {\"msg\": \"I am sad\", \"sender\": \"P\"}, {\"msg\": \"Have you tried the antidepressant drugs\", \"sender\": \"T\"}, {\"msg\": \"Those scare me\", \"sender\": \"P\"}, {\"msg\": \"Theyll help trust me.\", \"sender\": \"T\"}, {\"msg\": \"Okay thank you\", \"sender\": \"P\"}]}','2023-10-03 11:00:00','2023-10-03 11:30:00'),(4,4,1,'{\"chats\": [{\"msg\": \"Hellocdd!!\", \"sender\": \"P\"}, {\"msg\": \"Hello!\", \"sender\": \"T\"}, {\"msg\": \"I am sad\", \"sender\": \"P\"}, {\"msg\": \"Have you tried the antidepressant drugs\", \"sender\": \"T\"}, {\"msg\": \"Those scare me\", \"sender\": \"P\"}, {\"msg\": \"Theyll help trust me.\", \"sender\": \"T\"}, {\"msg\": \"Okay thank you\", \"sender\": \"P\"}]}','2023-10-04 12:00:00','2023-10-04 12:30:00'),(5,5,1,'{\"chats\": [{\"msg\": \"Helooerrg\", \"sender\": \"P\"}, {\"msg\": \"Hello!\", \"sender\": \"T\"}, {\"msg\": \"I am sad\", \"sender\": \"P\"}, {\"msg\": \"Have you tried the antidepressant drugs\", \"sender\": \"T\"}, {\"msg\": \"Those scare me\", \"sender\": \"P\"}, {\"msg\": \"Theyll help trust me.\", \"sender\": \"T\"}, {\"msg\": \"Okay thank you\", \"sender\": \"P\"}]}','2023-10-04 12:00:00','2023-10-04 12:30:00'),(6,6,1,'{\"chats\": [{\"msg\": \"Hey!cdvd\", \"sender\": \"P\"}, {\"msg\": \"Hello!\", \"sender\": \"T\"}, {\"msg\": \"I am sad\", \"sender\": \"P\"}, {\"msg\": \"Have you tried the antidepressant drugs\", \"sender\": \"T\"}, {\"msg\": \"Those scare me\", \"sender\": \"P\"}, {\"msg\": \"Theyll help trust me.\", \"sender\": \"T\"}, {\"msg\": \"Okay thank you\", \"sender\": \"P\"}]}','2023-10-05 13:00:00','2023-10-05 13:30:00');
/*!40000 ALTER TABLE `chats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question` text NOT NULL,
  `answer` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
INSERT INTO `company` VALUES (1,'What is MentCare, and how does it work?','MentCare is a mental health care organization that connects patients with top therapists worldwide.'),(2,'How can I find a therapist that’s right for me?','MentCare uses a detailed matching process to connect you with a therapist suited to your unique needs.'),(3,'Is my information secure with MentCare?','Yes, MentCare is committed to maintaining the privacy and confidentiality of all users.');
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `completedDailySurveys`
--

DROP TABLE IF EXISTS `completedDailySurveys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `completedDailySurveys` (
  `completionID` int NOT NULL AUTO_INCREMENT,
  `dailySurveyID` int DEFAULT NULL,
  `patientID` int DEFAULT NULL,
  `weight` int DEFAULT NULL,
  `height` float DEFAULT NULL,
  `calories` int DEFAULT NULL,
  `water` int DEFAULT NULL,
  `exercise` int DEFAULT NULL,
  `sleep` int DEFAULT NULL,
  `energy` int DEFAULT NULL,
  `stress` int DEFAULT NULL,
  PRIMARY KEY (`completionID`),
  KEY `patientID` (`patientID`),
  KEY `dailySurveyID` (`dailySurveyID`),
  CONSTRAINT `completedDailySurveys_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `patients` (`patientID`),
  CONSTRAINT `completedDailySurveys_ibfk_2` FOREIGN KEY (`dailySurveyID`) REFERENCES `dailySurveys` (`dailySurveyID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `completedDailySurveys`
--

LOCK TABLES `completedDailySurveys` WRITE;
/*!40000 ALTER TABLE `completedDailySurveys` DISABLE KEYS */;
INSERT INTO `completedDailySurveys` VALUES (1,1,1,150,70,500,1,2,8,5,9),(2,2,1,100,60,600,2,3,6,7,8);
/*!40000 ALTER TABLE `completedDailySurveys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `completedSurveys`
--

DROP TABLE IF EXISTS `completedSurveys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `completedSurveys` (
  `completionID` int NOT NULL AUTO_INCREMENT,
  `patientID` int DEFAULT NULL,
  `therapistID` int DEFAULT NULL,
  `questions` json DEFAULT NULL,
  `answers` json DEFAULT NULL,
  `dateDone` date DEFAULT NULL,
  PRIMARY KEY (`completionID`),
  KEY `patientID` (`patientID`),
  KEY `therapistID` (`therapistID`),
  CONSTRAINT `completedSurveys_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `patients` (`patientID`),
  CONSTRAINT `completedSurveys_ibfk_2` FOREIGN KEY (`therapistID`) REFERENCES `therapists` (`therapistID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `completedSurveys`
--

LOCK TABLES `completedSurveys` WRITE;
/*!40000 ALTER TABLE `completedSurveys` DISABLE KEYS */;
INSERT INTO `completedSurveys` VALUES (1,1,1,'{\"survey\": [{\"question\": \"How was your day?\", \"questionType\": \"string\"}, {\"question\": \"How much do you weigh in pounds?\", \"questionType\": \"number\"}, {\"question\": \"Did you eat today\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','{\"answers\": [{\"q1\": \"Great!\"}, {\"q2\": 150}, {\"q3\": true}, {\"q4\": 9}]}','2023-10-06'),(2,1,1,'{\"survey\": [{\"question\": \"How was your day?\", \"questionType\": \"string\"}, {\"question\": \"How much do you weigh in pounds?\", \"questionType\": \"number\"}, {\"question\": \"Did you eat today\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','{\"answers\": [{\"q1\": \"Great!\"}, {\"q2\": 150}, {\"q3\": true}, {\"q4\": 9}]}','2023-10-06'),(3,2,1,'{\"survey\": [{\"question\": \"How was your day?\", \"questionType\": \"string\"}, {\"question\": \"How much do you weigh in pounds?\", \"questionType\": \"number\"}, {\"question\": \"Did you eat today\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','{\"answers\": [{\"q1\": \"Alright.\"}, {\"q2\": 160}, {\"q3\": false}, {\"q4\": 6}]}','2023-10-07'),(4,3,2,'{\"survey\": [{\"question\": \"How was your day?\", \"questionType\": \"string\"}, {\"question\": \"How much do you weigh in pounds?\", \"questionType\": \"number\"}, {\"question\": \"Did you eat today\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','{\"answers\": [{\"q1\": \"Okay.\"}, {\"q2\": 72}, {\"q3\": true}, {\"q4\": 5}]}','2023-10-08'),(5,4,2,'{\"survey\": [{\"question\": \"How was your day?\", \"questionType\": \"string\"}, {\"question\": \"How much do you weigh in pounds?\", \"questionType\": \"number\"}, {\"question\": \"Did you eat today\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','{\"answers\": [{\"q1\": \"Meh.\"}, {\"q2\": 71}, {\"q3\": true}, {\"q4\": 4}]}','2023-10-09'),(6,5,3,'{\"survey\": [{\"question\": \"How was your day?\", \"questionType\": \"string\"}, {\"question\": \"How much do you weigh in pounds?\", \"questionType\": \"number\"}, {\"question\": \"Did you eat today\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','{\"answers\": [{\"q1\": \"Sad...\"}, {\"q2\": 1750}, {\"q3\": true}, {\"q4\": 2}]}','2023-10-10'),(7,6,4,'{\"survey\": [{\"question\": \"How was your day?\", \"questionType\": \"string\"}, {\"question\": \"How much do you weigh in pounds?\", \"questionType\": \"number\"}, {\"question\": \"Did you eat today\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','{\"answers\": [{\"q1\": \"Terrible!\"}, {\"q2\": 2500}, {\"q3\": true}, {\"q4\": 1}]}','2023-10-11');
/*!40000 ALTER TABLE `completedSurveys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dailySurveys`
--

DROP TABLE IF EXISTS `dailySurveys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dailySurveys` (
  `dailySurveyID` int NOT NULL AUTO_INCREMENT,
  `dateCreated` datetime DEFAULT NULL,
  PRIMARY KEY (`dailySurveyID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dailySurveys`
--

LOCK TABLES `dailySurveys` WRITE;
/*!40000 ALTER TABLE `dailySurveys` DISABLE KEYS */;
INSERT INTO `dailySurveys` VALUES (1,'2024-11-10 00:00:00'),(2,'2024-11-11 00:00:00'),(3,'2024-11-12 00:00:00');
/*!40000 ALTER TABLE `dailySurveys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `details`
--

DROP TABLE IF EXISTS `details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `details` (
  `detailsID` int NOT NULL AUTO_INCREMENT,
  `patientID` int DEFAULT NULL,
  `cardNum` int DEFAULT NULL,
  `cvc` int DEFAULT NULL,
  `expDate` date DEFAULT NULL,
  `firstName` varchar(25) DEFAULT NULL,
  `lastName` varchar(25) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `billingAddress` varchar(100) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `zip` int DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`detailsID`),
  KEY `patientID` (`patientID`),
  CONSTRAINT `details_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `patients` (`patientID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `details`
--

LOCK TABLES `details` WRITE;
/*!40000 ALTER TABLE `details` DISABLE KEYS */;
/*!40000 ALTER TABLE `details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `feedbackID` int NOT NULL AUTO_INCREMENT,
  `therapistID` int DEFAULT NULL,
  `patientID` int DEFAULT NULL,
  `feedbackDate` date DEFAULT NULL,
  `feedback` text,
  PRIMARY KEY (`feedbackID`),
  KEY `patientID` (`patientID`),
  KEY `therapistID` (`therapistID`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `patients` (`patientID`),
  CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`therapistID`) REFERENCES `therapists` (`therapistID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (1,1,1,'2023-10-02','Keep on exercising!'),(2,1,1,'2023-10-02','Keep on exercising 2!'),(3,1,2,'2023-10-03','Jog for an hour.'),(4,2,3,'2023-10-04','Stay hydrated!'),(5,2,4,'2023-10-05','Try not to do too much exercise!'),(6,3,5,'2023-10-06','Stop smoking.'),(7,4,6,'2023-10-07','Walk the dog!');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoices`
--

DROP TABLE IF EXISTS `invoices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoices` (
  `invoiceID` int NOT NULL AUTO_INCREMENT,
  `patientID` int DEFAULT NULL,
  `therapistID` int DEFAULT NULL,
  `amountDue` float DEFAULT NULL,
  `dateCreated` datetime DEFAULT NULL,
  PRIMARY KEY (`invoiceID`),
  KEY `patientID` (`patientID`),
  KEY `therapistID` (`therapistID`),
  CONSTRAINT `invoices_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `patients` (`patientID`),
  CONSTRAINT `invoices_ibfk_2` FOREIGN KEY (`therapistID`) REFERENCES `therapists` (`therapistID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoices`
--

LOCK TABLES `invoices` WRITE;
/*!40000 ALTER TABLE `invoices` DISABLE KEYS */;
INSERT INTO `invoices` VALUES (1,1,1,20,'2024-11-12 00:00:00'),(2,1,1,30,'2024-11-11 00:00:00'),(3,1,1,10,'2024-11-10 00:00:00');
/*!40000 ALTER TABLE `invoices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `journals`
--

DROP TABLE IF EXISTS `journals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `journals` (
  `journalID` int NOT NULL AUTO_INCREMENT,
  `patientID` int DEFAULT NULL,
  `journalEntry` text,
  `timeDone` datetime DEFAULT NULL,
  PRIMARY KEY (`journalID`),
  KEY `patientID` (`patientID`),
  CONSTRAINT `journals_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `patients` (`patientID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `journals`
--

LOCK TABLES `journals` WRITE;
/*!40000 ALTER TABLE `journals` DISABLE KEYS */;
INSERT INTO `journals` VALUES (1,1,'Feeling good today','2023-10-01 00:00:00'),(2,2,'Struggled with anxiety','2023-10-02 00:00:00'),(3,3,'No significant issues today','2023-10-03 00:00:00'),(4,6,'Had a minor asthma attack','2023-10-04 00:00:00'),(5,4,'Mood swings were tough','2023-10-05 00:00:00'),(6,5,'Ate a salad','2023-10-06 00:00:00');
/*!40000 ALTER TABLE `journals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mission`
--

DROP TABLE IF EXISTS `mission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `statement` text,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `stage1` text,
  `stage2` text,
  `stage3` text,
  `stage4` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mission`
--

LOCK TABLES `mission` WRITE;
/*!40000 ALTER TABLE `mission` DISABLE KEYS */;
INSERT INTO `mission` VALUES (1,'MentCare is a mental-health care organization dedicated to helping people access some of the best therapists around the world. These therapists conduct mental diagnostic tests and provide personalized health-care tools, resources, and treatment to patients.','123-1234-1234','mentcareabc@gmail.com','Access to Care: This initial phase involves recognizing the need for mental health services and overcoming barriers to obtain them.','Assessment and Diagnosis: Mental health professionals conduct thorough evaluations to understand an individual\'s psychological state, leading to accurate diagnoses.','Treatment Planning and Implementation: Based on the assessment, a personalized treatment plan is developed, includes mental therapy, and healthy lifestyle changes.','Monitoring and Evaluation: Continuous monitoring of the individual\'s progress allows for adjustments to the treatment plan as needed.');
/*!40000 ALTER TABLE `mission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `notificationID` int NOT NULL AUTO_INCREMENT,
  `userID` int DEFAULT NULL,
  `message` text,
  `redirectLocation` text,
  PRIMARY KEY (`notificationID`),
  KEY `userID` (`userID`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (1,1,'Therapist started a chat!','/chat'),(2,1,'Therapist has retired!',NULL),(3,1,'Therapist sent you feedback!','/dashboard'),(4,1,'Testing Notification!',NULL);
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `patientID` int NOT NULL AUTO_INCREMENT,
  `userID` int DEFAULT NULL,
  `insuranceCompany` varchar(128) DEFAULT NULL,
  `insuranceID` varchar(32) DEFAULT NULL,
  `insuranceTier` varchar(32) DEFAULT NULL,
  `mainTherapistID` int DEFAULT NULL,
  `allRecordsViewable` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`patientID`),
  UNIQUE KEY `userID` (`userID`),
  CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (1,1,'Blue Cross Blue Shield','ABCDE-12345','Basic',1,0),(2,2,'Aetna','11223344','Basic',1,0),(3,3,'SafeInsure','abcdefg123','Premium',2,0),(4,6,'Farmers','123-123-1234','HealthPlan D',2,0),(5,8,'Liberty Mutual','zyxwvwxyz','HealthPlan E',3,0),(6,10,'Progressive','INS111999','HomeHealthAndAuto',4,0);
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `paymentID` int NOT NULL AUTO_INCREMENT,
  `patientID` int DEFAULT NULL,
  `amount` decimal(5,2) DEFAULT NULL,
  `datePaid` date DEFAULT NULL,
  `cardNum` varchar(16) DEFAULT NULL,
  `cvc` varchar(3) DEFAULT NULL,
  `expDate` date DEFAULT NULL,
  `firstName` varchar(40) DEFAULT NULL,
  `lastName` varchar(40) DEFAULT NULL,
  `city` varchar(40) DEFAULT NULL,
  `billingAddress` varchar(40) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `country` varchar(40) DEFAULT NULL,
  `zip` varchar(10) DEFAULT NULL,
  `phone` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`paymentID`),
  KEY `patientID` (`patientID`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `patients` (`patientID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
INSERT INTO `payments` VALUES (1,1,200.00,'2023-10-01','111122224444','000','2029-12-06',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,2,250.00,'2023-10-02','111122223333','111','2028-12-05',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,3,150.00,'2023-10-03','555522223333','222','2029-04-04',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,4,100.00,'2023-10-04','111155553333','333','2028-01-03',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,5,300.00,'2023-10-05','111122225555','444','2029-12-02',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(6,6,300.00,'2023-10-05','000022223333','555','2083-11-01',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `reviewID` int NOT NULL AUTO_INCREMENT,
  `therapistID` int DEFAULT NULL,
  `patientID` int DEFAULT NULL,
  `content` text,
  `stars` tinyint DEFAULT NULL,
  `dateDone` datetime DEFAULT NULL,
  PRIMARY KEY (`reviewID`),
  KEY `patientID` (`patientID`),
  KEY `therapistID` (`therapistID`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `patients` (`patientID`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`therapistID`) REFERENCES `therapists` (`therapistID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,1,1,'I love linda white',3,'2024-12-01 00:00:00'),(2,1,2,'I love linda white!',4,'2024-12-01 00:00:00'),(3,1,3,'I love linda white!!',5,'2024-12-01 00:00:00'),(4,1,1,'I HATE linda white',1,'2024-12-01 00:00:00');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `surveys`
--

DROP TABLE IF EXISTS `surveys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `surveys` (
  `surveyID` int NOT NULL AUTO_INCREMENT,
  `therapistID` int DEFAULT NULL,
  `patientID` int DEFAULT NULL,
  `content` json DEFAULT NULL,
  `dateCreated` datetime DEFAULT NULL,
  PRIMARY KEY (`surveyID`),
  KEY `therapistID` (`therapistID`),
  KEY `patientID` (`patientID`),
  CONSTRAINT `surveys_ibfk_1` FOREIGN KEY (`therapistID`) REFERENCES `therapists` (`therapistID`),
  CONSTRAINT `surveys_ibfk_2` FOREIGN KEY (`patientID`) REFERENCES `patients` (`patientID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surveys`
--

LOCK TABLES `surveys` WRITE;
/*!40000 ALTER TABLE `surveys` DISABLE KEYS */;
INSERT INTO `surveys` VALUES (1,1,1,'{\"survey\": [{\"question\": \"How was your day?\", \"questionType\": \"string\"}, {\"question\": \"How much do you weigh in pounds?\", \"questionType\": \"number\"}, {\"question\": \"Did you eat today\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','2024-11-17 00:00:00'),(2,1,2,'{\"survey\": [{\"question\": \"How was your day?\", \"questionType\": \"string\"}, {\"question\": \"How tall are you in inches?\", \"questionType\": \"number\"}, {\"question\": \"Did you feel sad today\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','2024-11-16 00:00:00'),(3,2,3,'{\"survey\": [{\"question\": \"How was your day?\", \"questionType\": \"string\"}, {\"question\": \"How many calories did you intake?\", \"questionType\": \"number\"}, {\"question\": \"Did you eat a salad?\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','2024-11-15 00:00:00'),(4,3,4,'{\"survey\": [{\"question\": \"Was today good?\", \"questionType\": \"string\"}, {\"question\": \"What was your caloric intake?\", \"questionType\": \"number\"}, {\"question\": \"Did you drink water?\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','2024-11-14 00:00:00');
/*!40000 ALTER TABLE `surveys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `testimonials`
--

DROP TABLE IF EXISTS `testimonials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `testimonials` (
  `testimonialID` int NOT NULL AUTO_INCREMENT,
  `userID` int DEFAULT NULL,
  `content` varchar(512) DEFAULT NULL,
  `datePosted` datetime DEFAULT NULL,
  PRIMARY KEY (`testimonialID`),
  KEY `userID` (`userID`),
  CONSTRAINT `testimonials_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `testimonials`
--

LOCK TABLES `testimonials` WRITE;
/*!40000 ALTER TABLE `testimonials` DISABLE KEYS */;
INSERT INTO `testimonials` VALUES (1,1,'The convenience of virtual sessions and personalized tools make it easy for me to stay on track.','2024-12-15 01:07:36'),(2,2,'MentCare transformed my mental health journey. The personalized tools and supportive therapists have made all the difference in my progress.','2024-12-15 01:07:36'),(3,3,'MentCare has been a game-changer in my life.','2024-12-15 01:07:36'),(4,4,'Thanks to MentCare, I was matched with a therapist who understands me. The insights and tools provided have been life-changing.','2024-12-15 01:07:36'),(5,5,'Using MentCare has been an incredible experience. The resources, tools, and therapist support have improved my well-being immensely.','2024-12-15 01:07:36');
/*!40000 ALTER TABLE `testimonials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `therapistPatientsList`
--

DROP TABLE IF EXISTS `therapistPatientsList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `therapistPatientsList` (
  `pairingID` int NOT NULL AUTO_INCREMENT,
  `therapistID` int DEFAULT NULL,
  `patientID` int DEFAULT NULL,
  `status` enum('Active','Inactive') DEFAULT NULL,
  `chatStatus` enum('Active','Inactive') DEFAULT NULL,
  `requestStatus` enum('Active','Inactive') DEFAULT NULL,
  PRIMARY KEY (`pairingID`),
  KEY `patientID` (`patientID`),
  KEY `therapistID` (`therapistID`),
  CONSTRAINT `therapistPatientsList_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `patients` (`patientID`),
  CONSTRAINT `therapistPatientsList_ibfk_2` FOREIGN KEY (`therapistID`) REFERENCES `therapists` (`therapistID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `therapistPatientsList`
--

LOCK TABLES `therapistPatientsList` WRITE;
/*!40000 ALTER TABLE `therapistPatientsList` DISABLE KEYS */;
INSERT INTO `therapistPatientsList` VALUES (1,1,1,'Active','Inactive','Inactive'),(2,1,2,'Active','Inactive','Inactive'),(3,1,3,'Active','Inactive','Inactive'),(4,1,4,'Active','Inactive','Inactive'),(5,1,5,'Active','Inactive','Inactive'),(6,1,6,'Active','Inactive','Inactive');
/*!40000 ALTER TABLE `therapistPatientsList` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `therapists`
--

DROP TABLE IF EXISTS `therapists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `therapists` (
  `therapistID` int NOT NULL AUTO_INCREMENT,
  `userID` int DEFAULT NULL,
  `licenseNumber` int DEFAULT NULL,
  `specializations` set('Relationship','Depression','Addiction','Anxiety','PTSD','Family Therapy','Anger Mgmt.','Confidence') DEFAULT NULL,
  `acceptingPatients` tinyint(1) DEFAULT NULL,
  `content` json DEFAULT NULL,
  `DaysHours` text,
  `Price` text,
  `Intro` text,
  `Education` text,
  `chargingPrice` int DEFAULT NULL,
  `isActive` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`therapistID`),
  UNIQUE KEY `userID` (`userID`),
  CONSTRAINT `therapists_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `therapists`
--

LOCK TABLES `therapists` WRITE;
/*!40000 ALTER TABLE `therapists` DISABLE KEYS */;
INSERT INTO `therapists` VALUES (1,4,123456,'Relationship,Anxiety',1,'{\"survey\": [{\"question\": \"How was your day?\", \"questionType\": \"string\"}, {\"question\": \"How much do you weigh in pounds?\", \"questionType\": \"number\"}, {\"question\": \"Did you eat today\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','Monday -> Friday, 9am -> 5pm','Price can vary','Hello everyone! I am new to the MentCare website!','MS in Psychology',20,1),(2,5,1654321,'Depression,PTSD',1,'{\"survey\": [{\"question\": \"How was your day?\", \"questionType\": \"string\"}, {\"question\": \"How much do you weigh in pounds?\", \"questionType\": \"number\"}, {\"question\": \"Did you eat today\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','Monday -> Friday, 9am -> 5pm','Price can vary','Hello everyone! I am new to the MentCare website!','MS in Psychology',20,1),(3,7,123343,'Family Therapy,Confidence',1,'{\"survey\": [{\"question\": \"How was your day?\", \"questionType\": \"string\"}, {\"question\": \"How much do you weigh in pounds?\", \"questionType\": \"number\"}, {\"question\": \"Did you eat today\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','Monday -> Friday, 9am -> 5pm','Price can vary','Hello everyone! I am new to the MentCare website!','MS in Psychology',20,1),(4,9,801208,'Anger Mgmt.',1,'{\"survey\": [{\"question\": \"How was your day?\", \"questionType\": \"string\"}, {\"question\": \"How much do you weigh in pounds?\", \"questionType\": \"number\"}, {\"question\": \"Did you eat today\", \"questionType\": \"boolean\"}, {\"question\": \"How much do you look forward to tomorrow?\", \"questionType\": \"range10\"}]}','Monday -> Friday, 9am -> 5pm','Price can vary','Hello everyone! I am new to the MentCare website!','MS in Psychology',20,1);
/*!40000 ALTER TABLE `therapists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userID` int NOT NULL AUTO_INCREMENT,
  `userName` varchar(50) DEFAULT NULL,
  `email` varchar(320) DEFAULT NULL,
  `pass` varchar(128) DEFAULT NULL,
  `userType` enum('Patient','Therapist','Admin') DEFAULT NULL,
  `gender` enum('Male','Female','Other') DEFAULT NULL,
  `profileImg` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'John Smith','john.smith@example.com','password123','Patient','Male',NULL),(2,'Emily Jones','emily.jones@example.com','password123','Patient','Female',NULL),(3,'Michael Brown','michael.brown@example.com','password123','Patient','Male',NULL),(4,'Linda White','linda.white@example.com','password123','Therapist','Female',NULL),(5,'James Johnson','james.johnson@example.com','password123','Therapist','Male',NULL),(6,'Patricia Williams','patricia.williams@example.com','password123','Patient','Female',NULL),(7,'David Miller','david.miller@example.com','password123','Therapist','Male',NULL),(8,'Jennifer Taylor','jennifer.taylor@example.com','password123','Patient','Female',NULL),(9,'Robert Harris','robert.harris@example.com','password123','Therapist','Male',NULL),(10,'Maria Robinson','maria.robinson@example.com','password123','Patient','Female',NULL);
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

-- Dump completed on 2024-12-15  1:08:08
