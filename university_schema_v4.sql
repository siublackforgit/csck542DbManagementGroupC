CREATE DATABASE  IF NOT EXISTS `universityrecordsystem` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `universityrecordsystem`;
-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: universityrecordsystem
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `assessments`
--

DROP TABLE IF EXISTS `assessments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assessments` (
  `assessment_id` int NOT NULL AUTO_INCREMENT,
  `assessment_name` varchar(150) NOT NULL,
  `assessment_grade` int NOT NULL,
  `enrolment_id` int NOT NULL,
  PRIMARY KEY (`assessment_id`),
  KEY `enrolment_id` (`enrolment_id`),
  CONSTRAINT `assessments_ibfk_1` FOREIGN KEY (`enrolment_id`) REFERENCES `enrolment` (`enrolment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessments`
--

LOCK TABLES `assessments` WRITE;
/*!40000 ALTER TABLE `assessments` DISABLE KEYS */;
INSERT INTO `assessments` VALUES (1,'Coursework 1',68,1),(2,'Midterm Exam',74,2),(3,'Final Exam',81,3),(4,'Project Report',77,4),(5,'Quiz 1',65,5),(6,'Coursework 2',72,6),(7,'Presentation',69,7),(8,'Lab Assessment',84,8),(9,'Midterm Exam',71,9),(10,'Final Exam',88,10),(11,'Project Report',73,11),(12,'Quiz 2',67,12),(13,'Coursework 1',79,13),(14,'Presentation',75,14),(15,'Lab Assessment',82,15),(16,'Midterm Exam',64,16),(17,'Final Exam',86,17),(18,'Project Report',70,18),(19,'Quiz 1',63,19),(20,'Coursework 2',78,20),(21,'Presentation',74,21),(22,'Lab Assessment',80,22),(23,'Midterm Exam',69,23),(24,'Final Exam',85,24),(25,'Project Report',76,25),(26,'Quiz 2',66,26),(27,'Coursework 1',72,27),(28,'Presentation',83,28),(29,'Lab Assessment',71,29),(30,'Final Exam',89,30),(31,'Coursework 2',68,31),(32,'Midterm Exam',73,32),(33,'Project Report',77,33),(34,'Quiz 1',62,34),(35,'Presentation',81,35),(36,'Lab Assessment',75,36),(37,'Final Exam',87,37),(38,'Coursework 1',70,38),(39,'Midterm Exam',66,39),(40,'Project Report',79,40),(41,'Quiz 2',64,41),(42,'Presentation',74,42),(43,'Lab Assessment',82,43),(44,'Final Exam',90,44),(45,'Coursework 2',71,45),(46,'Midterm Exam',68,46),(47,'Project Report',84,47),(48,'Quiz 1',65,48),(49,'Presentation',78,49),(50,'Lab Assessment',73,50);
/*!40000 ALTER TABLE `assessments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `committeemembers`
--

DROP TABLE IF EXISTS `committeemembers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `committeemembers` (
  `member_id` int NOT NULL AUTO_INCREMENT,
  `lecturer_id` int NOT NULL,
  `committee_id` int NOT NULL,
  PRIMARY KEY (`member_id`),
  UNIQUE KEY `lecturer_id` (`lecturer_id`,`committee_id`),
  KEY `committee_id` (`committee_id`),
  CONSTRAINT `committeemembers_ibfk_1` FOREIGN KEY (`lecturer_id`) REFERENCES `lecturers` (`lecturer_id`),
  CONSTRAINT `committeemembers_ibfk_2` FOREIGN KEY (`committee_id`) REFERENCES `committees` (`committee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `committeemembers`
--

LOCK TABLES `committeemembers` WRITE;
/*!40000 ALTER TABLE `committeemembers` DISABLE KEYS */;
INSERT INTO `committeemembers` VALUES (10,2,1),(6,5,1),(11,5,2),(4,5,3),(3,6,4),(7,7,2),(1,8,3),(14,8,4),(12,10,1),(15,11,3),(9,12,1),(2,13,2),(8,19,2),(13,20,1);
/*!40000 ALTER TABLE `committeemembers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `committees`
--

DROP TABLE IF EXISTS `committees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `committees` (
  `committee_id` int NOT NULL AUTO_INCREMENT,
  `committee_name` varchar(150) NOT NULL,
  `meeting_frequency` varchar(50) NOT NULL,
  `department_id` int NOT NULL,
  PRIMARY KEY (`committee_id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `committees_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `committees`
--

LOCK TABLES `committees` WRITE;
/*!40000 ALTER TABLE `committees` DISABLE KEYS */;
INSERT INTO `committees` VALUES (1,'Academic Board','Bi-monthly',5),(2,'Research Committee','Monthly',5),(3,'Ethics Committee','Monthly',4),(4,'Curriculum Review Committee','Quarterly',3),(5,'Student Welfare Committee','Monthly',4);
/*!40000 ALTER TABLE `committees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courselecturers`
--

DROP TABLE IF EXISTS `courselecturers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courselecturers` (
  `assignment_id` int NOT NULL AUTO_INCREMENT,
  `lecturer_id` int NOT NULL,
  `course_code` varchar(20) NOT NULL,
  `role` varchar(50) NOT NULL,
  PRIMARY KEY (`assignment_id`),
  UNIQUE KEY `lecturer_id` (`lecturer_id`,`course_code`),
  KEY `course_code` (`course_code`),
  CONSTRAINT `courselecturers_ibfk_1` FOREIGN KEY (`lecturer_id`) REFERENCES `lecturers` (`lecturer_id`),
  CONSTRAINT `courselecturers_ibfk_2` FOREIGN KEY (`course_code`) REFERENCES `courses` (`course_code`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courselecturers`
--

LOCK TABLES `courselecturers` WRITE;
/*!40000 ALTER TABLE `courselecturers` DISABLE KEYS */;
INSERT INTO `courselecturers` VALUES (1,8,'SE203','Course Coodinator'),(2,15,'MA203','Lab Instructor'),(3,19,'EE201','Module Leader'),(4,15,'MA201','Module Leader'),(5,12,'EE102','Course Coodinator'),(6,9,'MA202','Lab Instructor'),(7,4,'CS202','Module Leader'),(8,3,'SE202','Course Coodinator'),(9,7,'SE202','Course Coodinator'),(11,17,'MG101','Course Coodinator'),(12,4,'SE101','Lab Instructor'),(13,2,'SE103','Course Coodinator'),(14,2,'SE203','Lab Instructor'),(15,8,'CS101','Lecturer'),(16,1,'EE101','Lab Instructor'),(17,10,'CS203','Module Leader'),(18,17,'CS203','Lab Instructor'),(19,14,'MA102','Course Coodinator'),(20,17,'SE201','Lecturer');
/*!40000 ALTER TABLE `courselecturers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseprerequisites`
--

DROP TABLE IF EXISTS `courseprerequisites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courseprerequisites` (
  `prerequisite_id` int NOT NULL AUTO_INCREMENT,
  `course_code` varchar(20) NOT NULL,
  `prerequisite_course_code` varchar(20) NOT NULL,
  PRIMARY KEY (`prerequisite_id`),
  KEY `course_code` (`course_code`),
  KEY `prerequisite_course_code` (`prerequisite_course_code`),
  CONSTRAINT `courseprerequisites_ibfk_1` FOREIGN KEY (`course_code`) REFERENCES `courses` (`course_code`),
  CONSTRAINT `courseprerequisites_ibfk_2` FOREIGN KEY (`prerequisite_course_code`) REFERENCES `courses` (`course_code`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseprerequisites`
--

LOCK TABLES `courseprerequisites` WRITE;
/*!40000 ALTER TABLE `courseprerequisites` DISABLE KEYS */;
INSERT INTO `courseprerequisites` VALUES (1,'MA203','MA201'),(2,'MA103','MA203'),(3,'SE103','MG103'),(4,'SE102','MA203'),(5,'MA202','CS101'),(6,'MG201','CS101'),(7,'MA202','CS201'),(8,'SE202','MG202'),(9,'EE101','MA101'),(10,'SE103','CS102'),(11,'MA201','EE103'),(12,'MA201','EE203'),(13,'MG101','MG203'),(14,'MA203','MA103'),(15,'MG102','SE202'),(16,'MA102','EE101'),(17,'CS203','CS202'),(18,'SE102','MA201'),(19,'EE203','MG203'),(20,'SE202','EE202'),(21,'MG201','SE103'),(22,'CS201','SE201'),(23,'EE101','EE203'),(24,'CS103','EE201'),(25,'MA103','MA102'),(26,'MA102','MA103'),(27,'SE201','EE103'),(28,'CS201','SE201'),(29,'EE101','CS101'),(30,'MG203','MA203');
/*!40000 ALTER TABLE `courseprerequisites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `course_code` varchar(20) NOT NULL,
  `course_name` varchar(150) NOT NULL,
  `course_description` text,
  `course_level` varchar(50) NOT NULL,
  `course_credits` int NOT NULL,
  `course_schedule` varchar(100) DEFAULT NULL,
  `course_materials` varchar(50) DEFAULT NULL,
  `department_id` int NOT NULL,
  PRIMARY KEY (`course_code`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES ('CS101','Introduction to Programming','Fundamental programming concepts using structured problem solving','Undergraduate',20,'Monday 09:00-11:00','Lecture slides and lab sheets',1),('CS102','Database Systems','Relational database design SQL and data modelling principles','Undergraduate',20,'Tuesday 10:00-12:00','Lecture slides and SQL exercises',1),('CS103','Data Structures and Algorithms','Core data structures algorithm design and complexity analysis','Undergraduate',20,'Wednesday 11:00-13:00','Lecture notes and programming tasks',1),('CS201','Machine Learning Foundations','Introduction to supervised and unsupervised learning methods','Postgraduate',20,'Thursday 14:00-16:00','Research papers and Python notebooks',1),('CS202','Artificial Intelligence Applications','Study of AI techniques and practical applications in industry','Postgraduate',20,'Friday 09:00-11:00','Lecture slides and case studies',1),('CS203','Operating Systems','Concepts of process management memory and file systems','Undergraduate',20,'Monday 13:00-15:00','Lecture slides and lab manual',1),('EE101','Digital Signal Processing','Analysis and processing of digital signals and systems','Undergraduate',20,'Friday 09:00-11:00','Lecture slides and lab sheets',5),('EE102','Embedded Systems','Design and programming of embedded computing devices','Undergraduate',20,'Monday 15:00-17:00','Lab manual and microcontroller notes',5),('EE103','Robotics Fundamentals','Introduction to robotic systems sensors and control','Postgraduate',20,'Tuesday 10:00-12:00','Lecture slides and practical tasks',5),('EE201','Internet of Things','Connected devices communication protocols and applications','Postgraduate',20,'Wednesday 15:00-17:00','Technical articles and lab exercises',5),('EE202','Control Systems','Modelling and analysis of feedback control systems','Undergraduate',20,'Thursday 14:00-16:00','Lecture notes and problem sheets',5),('EE203','Advanced Robotics','Advanced methods in autonomous systems and robotic control','Postgraduate',20,'Friday 13:00-15:00','Research papers and simulation files',5),('MA101','Calculus for Engineers','Differential and integral calculus for engineering analysis','Undergraduate',20,'Tuesday 09:00-11:00','Workbook and tutorial sheets',2),('MA102','Linear Algebra','Matrix methods vector spaces and linear transformations','Undergraduate',20,'Wednesday 14:00-16:00','Lecture notes and problem sets',2),('MA103','Statistical Methods','Probability distributions estimation and hypothesis testing','Undergraduate',20,'Thursday 10:00-12:00','Lecture slides and exercises',2),('MA201','Numerical Analysis','Computational methods for solving mathematical problems','Postgraduate',20,'Friday 11:00-13:00','Lab sheets and software tutorials',2),('MA202','Discrete Mathematics','Logic sets combinatorics and graph theory','Undergraduate',20,'Monday 10:00-12:00','Lecture notes and tutorial questions',2),('MA203','Applied Probability','Application of probability models in real world scenarios','Postgraduate',20,'Tuesday 14:00-16:00','Research articles and worksheets',2),('MG101','Research Methods','Approaches to academic research design and analysis','Postgraduate',20,'Thursday 09:00-11:00','Methodology handbook and journal articles',4),('MG102','Project Management','Planning scheduling risk and resource management in projects','Undergraduate',20,'Friday 14:00-16:00','Lecture slides and case studies',4),('MG103','Professional Ethics','Ethical principles and professional standards in organisations','Undergraduate',20,'Monday 11:00-13:00','Policy documents and seminar readings',4),('MG201','Innovation Management','Management of innovation processes and strategic change','Postgraduate',20,'Tuesday 13:00-15:00','Research papers and case materials',4),('MG202','Business Analytics','Use of data analysis to support organisational decision making','Postgraduate',20,'Wednesday 10:00-12:00','Lecture slides and analytics exercises',4),('MG203','Leadership in Organisations','Leadership theories and management practice in organisations','Undergraduate',20,'Thursday 11:00-13:00','Textbook chapters and discussion notes',4),('SE101','Software Engineering Principles','Methods for software development testing and maintenance','Undergraduate',20,'Wednesday 09:00-11:00','Lecture slides and project brief',3),('SE102','Web Development','Design and implementation of interactive web applications','Undergraduate',20,'Thursday 13:00-15:00','Coding examples and lab tasks',3),('SE103','Computer Networks','Network architectures protocols and communication systems','Undergraduate',20,'Friday 10:00-12:00','Lecture slides and lab manual',3),('SE201','Cyber Security Fundamentals','Principles of information security threats and controls','Postgraduate',20,'Monday 14:00-16:00','Case studies and security labs',3),('SE202','Human Computer Interaction','User centred design usability and interface evaluation','Undergraduate',20,'Tuesday 11:00-13:00','Lecture notes and design exercises',3),('SE203','Cloud Computing','Virtualisation distributed systems and cloud service models','Postgraduate',20,'Wednesday 13:00-15:00','Lecture slides and technical articles',3);
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `department_id` int NOT NULL AUTO_INCREMENT,
  `department_name` varchar(100) NOT NULL,
  `faculty` varchar(100) NOT NULL,
  PRIMARY KEY (`department_id`),
  UNIQUE KEY `department_name` (`department_name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'Department of Computer Science','Faculty of Science'),(2,'Department of Psychology','Faculty of Health'),(3,'Department of Physics','Faculty of Science'),(4,'Department of Biology','Faculty of Biology'),(5,'Department of Economics','Faculty of Engineering');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `disciplinaryrecords`
--

DROP TABLE IF EXISTS `disciplinaryrecords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `disciplinaryrecords` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `incident_date` date NOT NULL,
  `description` text NOT NULL,
  `student_id` int NOT NULL,
  PRIMARY KEY (`record_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `disciplinaryrecords_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `disciplinaryrecords`
--

LOCK TABLES `disciplinaryrecords` WRITE;
/*!40000 ALTER TABLE `disciplinaryrecords` DISABLE KEYS */;
INSERT INTO `disciplinaryrecords` VALUES (1,'2025-02-19','Disruptive behaviour',81),(2,'2026-02-16','Unauthorized collaboration',55),(3,'2025-12-07','Unauthorized recording',85),(4,'2023-06-16','Unauthorized collaboration',92),(5,'2025-06-19','Unauthorized collaboration',12),(6,'2025-07-15','Plagiarism',23),(7,'2024-04-21','Unauthorized recording',8),(8,'2025-04-17','Unauthorized collaboration',98),(9,'2023-05-11','Plagiarism',52),(10,'2025-08-08','Plagiarism',45),(11,'2026-03-07','Plagiarism',84),(12,'2026-01-09','Unauthorized collaboration',77),(13,'2023-10-21','Unauthorized collaboration',100),(14,'2025-12-13','Unauthorized collaboration',66),(15,'2024-02-23','Plagiarism',90),(16,'2023-05-20','Unauthorized collaboration',65),(17,'2023-06-19','Unauthorized recording',95),(18,'2024-11-06','Unauthorized recording',44),(19,'2024-04-29','Unauthorized collaboration',94),(20,'2025-01-06','Unauthorized recording',34);
/*!40000 ALTER TABLE `disciplinaryrecords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrolment`
--

DROP TABLE IF EXISTS `enrolment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enrolment` (
  `enrolment_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `course_code` varchar(20) NOT NULL,
  PRIMARY KEY (`enrolment_id`),
  UNIQUE KEY `student_id` (`student_id`,`course_code`),
  KEY `course_code` (`course_code`),
  CONSTRAINT `enrolment_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `enrolment_ibfk_2` FOREIGN KEY (`course_code`) REFERENCES `courses` (`course_code`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrolment`
--

LOCK TABLES `enrolment` WRITE;
/*!40000 ALTER TABLE `enrolment` DISABLE KEYS */;
INSERT INTO `enrolment` VALUES (77,2,'SE203'),(8,3,'MA203'),(53,3,'SE202'),(29,4,'EE101'),(62,5,'EE201'),(12,6,'CS101'),(80,6,'MA201'),(7,6,'SE101'),(2,8,'CS101'),(90,8,'EE102'),(23,10,'SE202'),(76,11,'SE102'),(89,12,'EE203'),(41,15,'CS201'),(60,15,'MG102'),(4,15,'MG203'),(30,18,'CS103'),(67,20,'MA103'),(5,20,'MG102'),(87,24,'SE201'),(73,25,'MA202'),(44,26,'MG201'),(17,26,'SE101'),(78,27,'CS103'),(66,27,'MG203'),(58,28,'MA202'),(79,30,'MA103'),(10,30,'SE203'),(14,31,'CS103'),(50,33,'MA102'),(85,34,'EE203'),(88,36,'CS203'),(54,36,'EE102'),(22,36,'MA203'),(33,38,'EE103'),(55,38,'MG203'),(39,39,'CS201'),(46,40,'MA103'),(16,43,'SE103'),(83,45,'SE103'),(47,48,'CS103'),(31,48,'EE201'),(48,48,'MA103'),(57,49,'EE101'),(3,49,'MA203'),(72,50,'MA102'),(28,50,'MG203'),(35,52,'SE203'),(86,54,'EE203'),(64,54,'MG101'),(9,54,'SE203'),(75,55,'MG101'),(63,56,'CS203'),(6,56,'EE102'),(82,56,'EE203'),(11,57,'MA101'),(25,58,'MA101'),(21,58,'SE103'),(24,59,'CS102'),(15,60,'CS201'),(45,61,'CS203'),(65,61,'SE202'),(18,61,'SE203'),(26,63,'EE102'),(38,64,'MA102'),(74,64,'SE102'),(56,65,'CS101'),(59,65,'MA103'),(49,67,'SE203'),(61,68,'MA101'),(69,70,'MG202'),(84,72,'CS203'),(13,73,'SE101'),(51,75,'CS103'),(1,75,'MA201'),(27,76,'EE202'),(20,79,'CS201'),(81,81,'MA103'),(43,82,'SE103'),(68,87,'MG103'),(71,87,'SE202'),(34,89,'MA103'),(42,90,'CS201'),(70,92,'EE202'),(32,92,'SE101'),(37,94,'MG202'),(52,95,'MA101'),(36,97,'SE201'),(40,98,'EE203'),(19,98,'SE201');
/*!40000 ALTER TABLE `enrolment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lecturerexpertise`
--

DROP TABLE IF EXISTS `lecturerexpertise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lecturerexpertise` (
  `expertise_id` int NOT NULL AUTO_INCREMENT,
  `lecturer_id` int NOT NULL,
  `area_name` varchar(150) NOT NULL,
  PRIMARY KEY (`expertise_id`),
  KEY `lecturer_id` (`lecturer_id`),
  CONSTRAINT `lecturerexpertise_ibfk_1` FOREIGN KEY (`lecturer_id`) REFERENCES `lecturers` (`lecturer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lecturerexpertise`
--

LOCK TABLES `lecturerexpertise` WRITE;
/*!40000 ALTER TABLE `lecturerexpertise` DISABLE KEYS */;
INSERT INTO `lecturerexpertise` VALUES (1,19,'Database Systems'),(2,4,'Software Engineering'),(3,19,'Data Analytics'),(4,1,'Cyber Security'),(5,5,'Database Systems'),(6,9,'Machine Learning'),(7,18,'Machine Learning'),(8,11,'Cyber Security'),(9,8,'Machine Learning'),(10,14,'Database Systems'),(11,4,'Software Engineering'),(12,12,'Database Systems'),(13,4,'Machine Learning'),(14,16,'Cyber Security'),(15,12,'Machine Learning'),(16,15,'Database Systems'),(17,20,'Cyber Security'),(18,1,'Software Engineering'),(19,6,'Software Engineering'),(20,15,'Cyber Security');
/*!40000 ALTER TABLE `lecturerexpertise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lecturerqualifications`
--

DROP TABLE IF EXISTS `lecturerqualifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lecturerqualifications` (
  `qualification_id` int NOT NULL AUTO_INCREMENT,
  `lecturer_id` int NOT NULL,
  `qualification_name` varchar(150) NOT NULL,
  `qualification_level` varchar(50) NOT NULL,
  PRIMARY KEY (`qualification_id`),
  KEY `lecturer_id` (`lecturer_id`),
  CONSTRAINT `lecturerqualifications_ibfk_1` FOREIGN KEY (`lecturer_id`) REFERENCES `lecturers` (`lecturer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lecturerqualifications`
--

LOCK TABLES `lecturerqualifications` WRITE;
/*!40000 ALTER TABLE `lecturerqualifications` DISABLE KEYS */;
INSERT INTO `lecturerqualifications` VALUES (1,3,'Data Science','Master'),(2,19,'Software Engineering','Postgraduate'),(3,18,'Information Systems','Professional Certification'),(4,18,'Data Science','Postgraduate'),(5,14,'Data Science','Doctorate'),(6,1,'Data Science','Postgraduate'),(7,12,'Software Engineering','Doctorate'),(8,13,'Computer Science','Bachelor'),(9,5,'Cyber Security','Professional Certification'),(10,18,'Information Systems','Professional Certification'),(11,6,'Information Systems','Bachelor'),(12,1,'Data Science','Master'),(13,8,'Data Science','Professional Certification'),(14,13,'Information Systems','Master'),(15,12,'Computer Science','Doctorate'),(16,13,'Data Science','Master'),(17,6,'Computer Science','Master'),(18,18,'Cyber Security','Bachelor'),(19,2,'Information Systems','Professional Certification'),(20,13,'Data Science','Postgraduate');
/*!40000 ALTER TABLE `lecturerqualifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lecturers`
--

DROP TABLE IF EXISTS `lecturers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lecturers` (
  `lecturer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `course_load` varchar(50) NOT NULL,
  `department_id` int NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` varchar(25) NOT NULL,
  PRIMARY KEY (`lecturer_id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `lecturers_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lecturers`
--

LOCK TABLES `lecturers` WRITE;
/*!40000 ALTER TABLE `lecturers` DISABLE KEYS */;
INSERT INTO `lecturers` VALUES (1,'Dr. Cherlyn Bamber','Very High',2,'cherlyn.bamber@universityrecords.local','831 842 2978'),(2,'Dr. August Hebner','High',1,'august.hebner@universityrecords.local','249 191 7639'),(3,'Prof. Clayson Di Meo','Light',2,'clayson.dimeo@universityrecords.local','652 402 8187'),(4,'Dr. Normy Mantle','Light',3,'normy.mantle@universityrecords.local','389 110 4609'),(5,'Prof. Carolyn Spirritt','Very Light',5,'carolyn.spirritt@universityrecords.local','947 184 4830'),(6,'Dr. Carling Piperley','Very High',5,'carling.piperley@universityrecords.local','562 683 1628'),(7,'Prof. Lucinda Ashman','Very Light',2,'lucinda.ashman@universityrecords.local','733 735 3643'),(8,'Dr. Rosa Stubbs','Very Light',5,'rosa.stubbs@universityrecords.local','372 868 6776'),(9,'Prof. Katharine Joselson','Very Light',4,'katharine.joselson@universityrecords.local','768 835 8413'),(10,'Dr. Lizzie Rundall','Very High',3,'lizzie.rundall@universityrecords.local','162 220 4147'),(11,'Dr. Codie O\'Hannen','Very Light',4,'codie.ohannen@universityrecords.local','815 797 5190'),(12,'Prof. Buffy Haquard','Very High',4,'buffy.haquard@universityrecords.local','445 147 4962'),(13,'Dr. Marcelia Hazell','Light',1,'marcelia.hazell@universityrecords.local','587 993 4682'),(14,'Dr. Bary Pigrome','Very High',3,'bary.pigrome@universityrecords.local','304 493 0464'),(15,'Prof. Paula Collier','Light',5,'paula.collier@universityrecords.local','646 843 9082'),(16,'Dr. Blanch Lodeke','High',4,'blanch.lodeke@universityrecords.local','448 250 5064'),(17,'Prof. Adan Grier','Very High',3,'adan.grier@universityrecords.local','822 704 1546'),(18,'Dr. Laughton Reames','Very Light',4,'laughton.reames@universityrecords.local','801 870 2997'),(19,'Dr. Maurise Clowser','Light',1,'maurise.clowser@universityrecords.local','656 974 2844'),(20,'Prof. Cornelle Rosina','Very Light',4,'cornelle.rosina@universityrecords.local','742 893 4545');
/*!40000 ALTER TABLE `lecturers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nonacademicstaff`
--

DROP TABLE IF EXISTS `nonacademicstaff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nonacademicstaff` (
  `staff_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `job_title` varchar(100) NOT NULL,
  `employment_type` varchar(50) NOT NULL,
  `contract_details` varchar(255) DEFAULT NULL,
  `salary_info` decimal(10,2) NOT NULL,
  `emergency_contact` int DEFAULT NULL,
  `department_id` int NOT NULL,
  PRIMARY KEY (`staff_id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `nonacademicstaff_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nonacademicstaff`
--

LOCK TABLES `nonacademicstaff` WRITE;
/*!40000 ALTER TABLE `nonacademicstaff` DISABLE KEYS */;
INSERT INTO `nonacademicstaff` VALUES (1,'Hervey Daville','Accountant I','Temporary','Renewable annual contract',3200.00,1157684436,5),(2,'Jillian Dagworthy','Librarian','Full-time','Permanent contract',3200.00,1206658039,2),(3,'Elli Shirley','Web Designer III','Full-time','Renewable annual contract',2800.00,1929614964,5),(4,'Rickard Jenno','Statistician II','Temporary','Permanent contract',2400.00,73974924,1),(5,'Delphinia Poyle','Staff Scientist','Full-time','Renewable annual contract',2700.00,8482456,1),(6,'Suzi Bartocci','Tax Accountant','Full-time','Permanent contract',2600.00,77222541,4),(7,'Halley Darnbrough','Community Outreach Specialist','Temporary','12-month fixed-term contract',3000.00,88517697,4),(8,'Dolf Fruen','Nurse','Full-time','Renewable annual contract',2600.00,65466020,4),(9,'Cletis Christofol','Administrative Officer','Contract','Renewable annual contract',2600.00,34985893,5),(10,'Tynan Androsik','Statistician I','Full-time','Renewable annual contract',2800.00,47648677,4),(11,'Rivkah Hanton','Quality Engineer','Full-time','Permanent contract',2400.00,90293433,2),(12,'Gibby Tabner','VP Sales','Part-time','12-month fixed-term contract',2500.00,29575743,1),(13,'Zebadiah Shelborne','Human Resources Assistant IV','Part-time','Permanent contract',3100.00,60004890,5),(14,'Lynsey Blasdale','Web Developer IV','Full-time','12-month fixed-term contract',2800.00,49714761,2),(15,'Marji Boothby','General Manager','Part-time','Permanent contract',2400.00,82367140,3),(16,'Ibbie Bottini','Product Engineer','Full-time','Permanent contract',2700.00,62782732,4),(17,'Mathe Samper','Environmental Specialist','Temporary','Renewable annual contract',2300.00,47927340,5),(18,'Roderich Antonignetti','Human Resources Assistant I','Permanent','Renewable annual contract',2200.00,92136006,3),(19,'Tamas Waymont','Accountant II','Permanent','Renewable annual contract',2700.00,27579690,1),(20,'Hildegaard Treby','Structural Engineer','Permanent','Permanent contract',3200.00,48592386,2),(21,'Sileas Tottle','Systems Administrator II','Part-time','12-month fixed-term contract',3200.00,52730346,1),(22,'Laurent Francello','Data Coordinator','Part-time','Renewable annual contract',2600.00,34031718,5),(23,'Cathe Robard','Professor','Full-time','Renewable annual contract',2600.00,44862770,3),(24,'Ginelle Tarr','Teacher','Part-time','12-month fixed-term contract',2800.00,38079656,1),(25,'Elyse Cato','Geological Engineer','Contract','12-month fixed-term contract',2400.00,69649131,3),(26,'Beth Tomkiss','Systems Administrator II','Permanent','12-month fixed-term contract',2700.00,31093450,5),(27,'Trula Braycotton','Structural Engineer','Temporary','12-month fixed-term contract',2400.00,25808607,4),(28,'Lennie Cookney','VP Accounting','Contract','Permanent contract',2500.00,53066126,5),(29,'Rebecca Belone','Senior Sales Associate','Contract','Renewable annual contract',2400.00,85022506,4),(30,'Shea Moreman','Sales Representative','Full-time','Renewable annual contract',2300.00,55317583,5);
/*!40000 ALTER TABLE `nonacademicstaff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organisationmemberships`
--

DROP TABLE IF EXISTS `organisationmemberships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organisationmemberships` (
  `membership_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `organisation_id` int NOT NULL,
  `join_date` date NOT NULL,
  `role` varchar(100) NOT NULL,
  PRIMARY KEY (`membership_id`),
  UNIQUE KEY `student_id` (`student_id`,`organisation_id`),
  KEY `organisation_id` (`organisation_id`),
  CONSTRAINT `organisationmemberships_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `organisationmemberships_ibfk_2` FOREIGN KEY (`organisation_id`) REFERENCES `studentorganisations` (`organisation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organisationmemberships`
--

LOCK TABLES `organisationmemberships` WRITE;
/*!40000 ALTER TABLE `organisationmemberships` DISABLE KEYS */;
INSERT INTO `organisationmemberships` VALUES (121,47,6,'2023-06-10','Member'),(122,39,5,'2026-01-16','Member'),(123,87,10,'2025-03-31','Member'),(124,70,6,'2025-02-22','Member'),(125,34,6,'2025-07-27','Member'),(126,76,10,'2024-06-12','Member'),(127,45,4,'2023-11-29','Member'),(128,80,10,'2025-03-20','Member'),(129,59,10,'2024-01-03','Member'),(130,51,9,'2025-09-27','President'),(131,81,7,'2023-07-26','Member'),(132,85,1,'2025-06-19','Member'),(133,90,4,'2025-07-31','Member'),(134,52,1,'2025-09-20','Member'),(135,54,3,'2025-03-11','Treasurer'),(136,95,8,'2026-02-05','Member'),(137,67,2,'2024-05-24','Member'),(138,42,4,'2023-12-01','Member'),(139,3,7,'2024-03-10','Member'),(140,9,2,'2024-01-25','Member'),(141,91,3,'2023-06-14','Member'),(142,27,6,'2025-06-23','Member'),(143,8,8,'2023-09-21','Member'),(144,54,4,'2023-10-06','Member'),(145,38,6,'2025-03-14','Member'),(146,37,1,'2024-07-11','Member'),(147,98,2,'2025-07-02','Member'),(148,50,3,'2025-09-03','Vice-President'),(149,11,9,'2025-07-06','Member'),(150,95,3,'2024-04-28','Member');
/*!40000 ALTER TABLE `organisationmemberships` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programmerequirements`
--

DROP TABLE IF EXISTS `programmerequirements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programmerequirements` (
  `requirement_id` int NOT NULL AUTO_INCREMENT,
  `programme_id` int NOT NULL,
  `course_code` varchar(20) NOT NULL,
  `is_mandatory` tinyint(1) NOT NULL,
  PRIMARY KEY (`requirement_id`),
  KEY `programme_id` (`programme_id`),
  KEY `course_code` (`course_code`),
  CONSTRAINT `programmerequirements_ibfk_1` FOREIGN KEY (`programme_id`) REFERENCES `programmes` (`programme_id`),
  CONSTRAINT `programmerequirements_ibfk_2` FOREIGN KEY (`course_code`) REFERENCES `courses` (`course_code`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programmerequirements`
--

LOCK TABLES `programmerequirements` WRITE;
/*!40000 ALTER TABLE `programmerequirements` DISABLE KEYS */;
INSERT INTO `programmerequirements` VALUES (1,9,'EE202',0),(2,10,'EE103',1),(3,2,'SE103',1),(4,4,'MA201',1),(5,10,'EE103',0),(6,5,'EE101',1),(7,8,'CS101',0),(8,1,'SE202',0),(9,4,'MA202',1),(10,7,'CS101',1);
/*!40000 ALTER TABLE `programmerequirements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programmes`
--

DROP TABLE IF EXISTS `programmes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programmes` (
  `programme_id` int NOT NULL AUTO_INCREMENT,
  `programme_name` varchar(100) NOT NULL,
  `degree_awarded` varchar(50) NOT NULL,
  `duration` int NOT NULL,
  `department_id` int NOT NULL,
  PRIMARY KEY (`programme_id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `programmes_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programmes`
--

LOCK TABLES `programmes` WRITE;
/*!40000 ALTER TABLE `programmes` DISABLE KEYS */;
INSERT INTO `programmes` VALUES (1,'Economics','MSc',4,5),(2,'Civil Engineering','BEng',1,3),(3,'Architecture','MA',4,3),(4,'Civil Engineering','MSc',1,3),(5,'Economics','BA',1,5),(6,'Data Science','MA',2,1),(7,'Mechanical Engineering','BSc',2,3),(8,'Mechanical Engineering','BEng',4,3),(9,'Biomedical Science','MA',1,4),(10,'Data Science','BSc',4,2);
/*!40000 ALTER TABLE `programmes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projectteams`
--

DROP TABLE IF EXISTS `projectteams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projectteams` (
  `team_id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `role` varchar(100) NOT NULL,
  PRIMARY KEY (`team_id`),
  UNIQUE KEY `project_id` (`project_id`,`staff_id`),
  KEY `staff_id` (`staff_id`),
  CONSTRAINT `projectteams_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `researchprojects` (`project_id`),
  CONSTRAINT `projectteams_ibfk_2` FOREIGN KEY (`staff_id`) REFERENCES `nonacademicstaff` (`staff_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projectteams`
--

LOCK TABLES `projectteams` WRITE;
/*!40000 ALTER TABLE `projectteams` DISABLE KEYS */;
INSERT INTO `projectteams` VALUES (1,1,1,'Administrative Support'),(2,2,3,'Project Coordinator'),(3,1,11,'Administrative Support'),(4,2,20,'Administrative Support'),(5,4,17,'Administrative Support'),(6,1,16,'Administrative Support'),(7,1,2,'Project Manager'),(8,1,14,'Project Manager'),(9,2,8,'Administrative Support'),(10,4,4,'Administrative Support');
/*!40000 ALTER TABLE `projectteams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `publications`
--

DROP TABLE IF EXISTS `publications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `publications` (
  `publication_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `publication_date` date NOT NULL,
  `lecturer_id` int NOT NULL,
  `project_id` int NOT NULL,
  PRIMARY KEY (`publication_id`),
  KEY `lecturer_id` (`lecturer_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `publications_ibfk_1` FOREIGN KEY (`lecturer_id`) REFERENCES `lecturers` (`lecturer_id`),
  CONSTRAINT `publications_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `researchprojects` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `publications`
--

LOCK TABLES `publications` WRITE;
/*!40000 ALTER TABLE `publications` DISABLE KEYS */;
INSERT INTO `publications` VALUES (1,'Predictive Modelling of Student Performance Using Machine Learning','2025-12-13',1,4),(2,'A Secure Framework for Cloud-Based Academic Data Management','2025-09-04',8,3),(3,'Intelligent Robotic Assistance in Independent Living Environments','2024-07-27',19,2),(4,'Data-Driven Approaches to University Resource Allocation','2023-06-09',14,3),(5,'Detecting Cyber Security Threats in Higher Education Networks','2023-11-29',17,3);
/*!40000 ALTER TABLE `publications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `researchgroups`
--

DROP TABLE IF EXISTS `researchgroups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `researchgroups` (
  `group_id` int NOT NULL AUTO_INCREMENT,
  `group_name` varchar(150) NOT NULL,
  `head_lecturer_id` int NOT NULL,
  PRIMARY KEY (`group_id`),
  UNIQUE KEY `head_lecturer_id` (`head_lecturer_id`),
  CONSTRAINT `researchgroups_ibfk_1` FOREIGN KEY (`head_lecturer_id`) REFERENCES `lecturers` (`lecturer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `researchgroups`
--

LOCK TABLES `researchgroups` WRITE;
/*!40000 ALTER TABLE `researchgroups` DISABLE KEYS */;
INSERT INTO `researchgroups` VALUES (1,'Artificial Intelligence Research Group',10),(2,'Data Science and Analytics Group',15),(3,'Cyber Security Research Group',19),(4,'Software Engineering Research Group',2),(5,'Robotics and Autonomous Systems Group',8);
/*!40000 ALTER TABLE `researchgroups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `researchprojects`
--

DROP TABLE IF EXISTS `researchprojects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `researchprojects` (
  `project_id` int NOT NULL AUTO_INCREMENT,
  `project_title` varchar(200) NOT NULL,
  `principal_investigator_id` int NOT NULL,
  `funding_source` varchar(50) NOT NULL,
  PRIMARY KEY (`project_id`),
  KEY `principal_investigator_id` (`principal_investigator_id`),
  CONSTRAINT `researchprojects_ibfk_1` FOREIGN KEY (`principal_investigator_id`) REFERENCES `lecturers` (`lecturer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `researchprojects`
--

LOCK TABLES `researchprojects` WRITE;
/*!40000 ALTER TABLE `researchprojects` DISABLE KEYS */;
INSERT INTO `researchprojects` VALUES (1,'AI-Based Student Performance Prediction',13,'UK Research and Innovation'),(2,'Secure Cloud Data Management Framework',1,'European Research Council'),(3,'Intelligent Robotics',15,'Industry Partnership Grant'),(4,'Cyber Security Risk Detection in Academic NetworksData',14,'UK Research and Innovation'),(5,'Analytics for University Resource Planning for Assisted Living',4,'European Research Council');
/*!40000 ALTER TABLE `researchprojects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentorganisations`
--

DROP TABLE IF EXISTS `studentorganisations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studentorganisations` (
  `organisation_id` int NOT NULL AUTO_INCREMENT,
  `organisation_name` varchar(100) NOT NULL,
  `organisation_type` varchar(50) NOT NULL,
  PRIMARY KEY (`organisation_id`),
  UNIQUE KEY `organisation_name` (`organisation_name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentorganisations`
--

LOCK TABLES `studentorganisations` WRITE;
/*!40000 ALTER TABLE `studentorganisations` DISABLE KEYS */;
INSERT INTO `studentorganisations` VALUES (1,'Computer Science Society','Academic'),(2,'Engineering Students Association','Academic'),(3,'International Students Club','Cultural'),(4,'Debate and Public Speaking Society','Academic'),(5,'Entrepreneurship and Innovation Club','Professional'),(6,'Women in STEM Network','Professional'),(7,'Environmental Sustainability Club','Social'),(8,'University Football Club','Sports'),(9,'Photography and Media Society','Creative'),(10,'Volunteer and Community Service Group','Social');
/*!40000 ALTER TABLE `studentorganisations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `date_of_birth` date NOT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `year_of_study` int NOT NULL,
  `graduation_status` varchar(50) NOT NULL,
  `programme_id` int NOT NULL,
  `advisor_id` int NOT NULL,
  PRIMARY KEY (`student_id`),
  KEY `programme_id` (`programme_id`),
  KEY `advisor_id` (`advisor_id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`programme_id`) REFERENCES `programmes` (`programme_id`),
  CONSTRAINT `students_ibfk_2` FOREIGN KEY (`advisor_id`) REFERENCES `lecturers` (`lecturer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'Toinette Wilby','2001-02-19','+86 281 316 1877','twilby0@npr.org',4,'Graduated',1,20),(2,'Gladi Danilyak','1995-10-28','+420 216 901 9044','gdanilyak1@studiopress.com',3,'Enrolled',7,6),(3,'Dominick McCurtain','2000-10-03','+381 546 365 1319','dmccurtain2@histats.com',6,'Paused',2,13),(4,'Phoebe Clapson','1997-07-10','+62 244 603 9383','pclapson3@reverbnation.com',8,'Enrolled',9,3),(5,'Winthrop Ferry','1994-09-28','+62 417 926 6649','wferry4@networkadvertising.org',6,'Enrolled',9,11),(6,'Weber O\'Finan','1996-10-20','+7 422 513 3593','wofinan5@studiopress.com',10,'Paused',3,19),(7,'Rosy Braunthal','2005-07-26','+33 922 469 6147','rbraunthal6@mail.ru',1,'Enrolled',2,4),(8,'Darb Amoore','1999-05-27','+82 379 966 0058','damoore7@tripod.com',7,'Enrolled',3,12),(9,'Dedra Staden','2002-03-26','+30 380 917 5574','dstaden8@vk.com',3,'Enrolled',5,11),(10,'Novelia Kydde','2006-01-21','+86 895 864 5087','nkydde9@squarespace.com',4,'Enrolled',2,3),(11,'Vevay McCrea','1999-05-03','+260 897 299 8134','vmccreaa@hud.gov',2,'Enrolled',6,13),(12,'Wendy Pettus','1995-03-25','+351 111 352 2635','wpettusb@arizona.edu',8,'Enrolled',6,18),(13,'Silvanus Guittet','1998-02-15','+358 480 548 8697','sguittetc@amazon.de',4,'Enrolled',8,16),(14,'Cymbre Peffer','1996-11-03','+86 273 950 8236','cpefferd@fc2.com',10,'Enrolled',3,1),(15,'Tracie McGorman','2005-12-18','+46 579 755 4993','tmcgormane@nih.gov',1,'Paused',9,14),(16,'Hagan Phipard-Shears','1990-09-12','+52 870 452 4113','hphipardshearsf@360.cn',4,'Enrolled',2,18),(17,'Adrianne Farra','2003-03-15','+880 679 371 8139','afarrag@fc2.com',4,'Enrolled',9,10),(18,'Marga Chesterton','1995-07-27','+62 120 261 0521','mchestertonh@netlog.com',5,'Enrolled',5,20),(19,'Drugi Kerin','2000-01-20','+86 598 971 1711','dkerini@amazon.co.uk',9,'Enrolled',4,9),(20,'Benn Frankum','2004-01-27','+82 230 793 9604','bfrankumj@paginegialle.it',3,'Enrolled',2,3),(21,'Portie Scarffe','1993-05-15','+86 644 589 1147','pscarffek@chron.com',5,'Enrolled',10,5),(22,'Noreen Furzer','2000-02-11','+66 929 181 9539','nfurzerl@etsy.com',10,'Enrolled',7,8),(23,'Yvor Sigmund','1990-06-20','+46 929 217 2679','ysigmundm@imdb.com',6,'Enrolled',4,8),(24,'Torrence Hoffner','1997-03-03','+86 919 838 0280','thoffnern@fc2.com',9,'Graduated',5,8),(25,'Carmon McGinny','2000-02-06','+63 146 919 0443','cmcginnyo@dailymotion.com',8,'Enrolled',7,11),(26,'Tadeas Cavey','1999-11-11','+994 471 469 5256','tcaveyp@nasa.gov',2,'Enrolled',4,12),(27,'Leslie Rulton','1992-03-23','+216 613 930 3041','lrultonq@nasa.gov',3,'Enrolled',9,7),(28,'Demetri Ewenson','1992-10-22','+976 372 222 7851','dewensonr@pinterest.com',10,'Enrolled',9,9),(29,'Harvey O\'Flaherty','2002-02-26','+375 500 208 3538','hoflahertys@salon.com',2,'Enrolled',9,5),(30,'Gilbertine Bowkley','2001-12-09','+66 630 287 1025','gbowkleyt@dell.com',5,'Enrolled',8,16),(31,'Ava Spivey','2001-10-05','+66 112 374 8085','aspiveyu@com.com',1,'Enrolled',10,19),(32,'Melania Wetwood','1990-10-10','+49 749 422 0152','mwetwoodv@nba.com',7,'Paused',7,6),(33,'Rafaelita Nussii','1996-07-26','+55 874 380 3881','rnussiiw@cdbaby.com',3,'Enrolled',6,3),(34,'Lisha McPaike','1997-09-09','+355 646 979 1951','lmcpaikex@irs.gov',9,'Graduated',8,8),(35,'Aloisia Wipfler','1994-08-29','+60 272 946 2483','awipflery@mozilla.org',5,'Paused',10,7),(36,'Yurik Wroe','1991-03-25','+380 619 826 6799','ywroez@github.io',3,'Enrolled',6,7),(37,'Barrie Jukes','1997-06-24','+93 398 637 3399','bjukes10@w3.org',5,'Enrolled',10,1),(38,'Candide Rivilis','1998-10-14','+62 601 660 5318','crivilis11@prnewswire.com',7,'Enrolled',1,13),(39,'Saudra Ivantyev','1996-03-28','+66 802 315 0788','sivantyev12@tinyurl.com',3,'Enrolled',1,16),(40,'Holden Veschambre','2004-08-14','+351 513 866 9812','hveschambre13@howstuffworks.com',4,'Enrolled',7,14),(41,'Sheela Donan','2001-11-16','+66 456 267 4547','sdonan14@scribd.com',6,'Enrolled',10,10),(42,'Vale Winsley','2004-07-18','+52 731 833 6507','vwinsley15@washingtonpost.com',3,'Enrolled',10,16),(43,'Gustavus Gouda','1996-02-26','+250 661 181 1207','ggouda16@wordpress.com',1,'Enrolled',8,13),(44,'Bertie Strelitzer','1996-12-02','+420 427 531 7582','bstrelitzer17@theguardian.com',3,'Enrolled',1,4),(45,'Brooks Hunnicot','1991-01-26','+255 772 884 0340','bhunnicot18@nytimes.com',10,'Enrolled',1,6),(46,'Claiborne Persitt','2003-11-03','+1 915 471 1215','cpersitt19@phoca.cz',2,'Enrolled',7,9),(47,'Rafaello Cattach','1995-01-16','+46 933 256 6106','rcattach1a@imdb.com',7,'Paused',3,14),(48,'Cherye Giron','1993-06-28','+62 528 984 2755','cgiron1b@marriott.com',2,'Graduated',9,20),(49,'Valentia Guinn','1990-08-19','+7 482 373 9807','vguinn1c@marketwatch.com',3,'Paused',3,8),(50,'Adamo Cattemull','2002-02-28','+48 952 310 4303','acattemull1d@microsoft.com',6,'Enrolled',4,16),(51,'Ban Hambleton','1994-06-13','+7 292 282 5655','bhambleton1e@ehow.com',8,'Enrolled',5,12),(52,'Jenna Woodman','1998-10-11','+86 548 777 2785','jwoodman1f@51.la',6,'Dropped',1,20),(53,'Aubrette Oke','1992-05-19','+86 545 714 4596','aoke1g@utexas.edu',3,'Enrolled',6,17),(54,'Gerianne Fadden','1990-09-21','+98 191 984 9567','gfadden1h@alibaba.com',1,'Graduated',4,20),(55,'Rikki Gilliat','2003-02-13','+54 989 298 8302','rgilliat1i@nymag.com',9,'Graduated',5,9),(56,'Maurise McGeever','2001-12-23','+62 962 832 8092','mmcgeever1j@pbs.org',10,'Dropped',4,18),(57,'Olivette Broadway','1992-11-28','+351 498 729 1233','obroadway1k@topsy.com',9,'Paused',5,2),(58,'Selina Steljes','2004-09-11','+86 955 215 4611','ssteljes1l@biblegateway.com',9,'Enrolled',6,8),(59,'Emelda Kervin','1991-05-12','+55 334 992 1303','ekervin1m@com.com',7,'Enrolled',8,4),(60,'North Yeoland','2004-12-29','+48 204 506 5496','nyeoland1n@gmpg.org',3,'Enrolled',7,20),(61,'Norris Reece','1996-05-07','+374 745 606 8453','nreece1o@jiathis.com',7,'Dropped',1,4),(62,'Duky Wilson','2006-02-07','+54 751 990 9847','dwilson1p@scientificamerican.com',6,'Enrolled',8,16),(63,'Albrecht Ivanchikov','2005-12-05','+57 417 841 5498','aivanchikov1q@infoseek.co.jp',10,'Enrolled',6,20),(64,'Suzie Mapes','1998-05-24','+92 338 465 8063','smapes1r@china.com.cn',7,'Enrolled',7,12),(65,'Normie Maynard','2005-01-17','+33 982 564 7297','nmaynard1s@domainmarket.com',6,'Enrolled',2,17),(66,'Braden Clarae','2000-07-11','+1 650 641 8076','bclarae1t@mashable.com',5,'Enrolled',7,11),(67,'Jenine Clough','1997-12-27','+46 568 810 3266','jclough1u@de.vu',7,'Enrolled',2,20),(68,'Carlen Ruppele','1998-07-22','+86 802 165 6882','cruppele1v@squarespace.com',8,'Dropped',5,10),(69,'Melinde Segeswoeth','1996-09-21','+86 988 999 0843','msegeswoeth1w@joomla.org',1,'Paused',3,2),(70,'Rand Orwin','1990-11-22','+57 653 769 9678','rorwin1x@sakura.ne.jp',10,'Graduated',10,1),(71,'Avigdor Polk','2003-05-13','+48 570 832 0714','apolk1y@ucla.edu',9,'Paused',9,15),(72,'Jacqueline Luebbert','2004-03-18','+7 536 968 0853','jluebbert1z@theguardian.com',5,'Enrolled',2,6),(73,'Leanor Yousef','2002-01-23','+82 736 229 1113','lyousef20@google.de',3,'Enrolled',8,7),(74,'Tamara D\'Elias','1991-05-02','+62 963 474 5214','tdelias21@wiley.com',4,'Enrolled',2,7),(75,'Maye Wadworth','1995-02-27','+63 139 179 9609','mwadworth22@myspace.com',5,'Enrolled',7,20),(76,'Trish Basilone','2000-02-19','+55 153 530 0797','tbasilone23@google.com.au',2,'Enrolled',6,1),(77,'Esther Issakov','2004-07-16','+57 588 927 6158','eissakov24@squidoo.com',9,'Dropped',1,6),(78,'Cloris Watkiss','1992-04-23','+62 982 258 8388','cwatkiss25@opera.com',10,'Graduated',1,16),(79,'Lanna Piers','2000-04-24','+33 483 668 8843','lpiers26@google.nl',9,'Enrolled',2,11),(80,'Connie Klejin','1990-05-08','+86 467 939 5119','cklejin27@example.com',5,'Enrolled',2,9),(81,'Marta Gary','1996-10-15','+51 239 727 2176','mgary28@godaddy.com',10,'Enrolled',5,11),(82,'Obadiah Syer','1999-08-12','+66 353 325 3234','osyer29@seesaa.net',7,'Graduated',3,1),(83,'Fannie Harnor','1996-03-05','+86 942 500 5342','fharnor2a@miibeian.gov.cn',6,'Enrolled',2,13),(84,'Pris Warnock','2001-02-22','+7 823 103 1939','pwarnock2b@yahoo.co.jp',2,'Enrolled',3,4),(85,'Sansone Iston','1991-06-08','+355 828 996 6152','siston2c@slashdot.org',5,'Enrolled',4,7),(86,'Josselyn Wilprecht','2001-11-20','+63 343 611 1863','jwilprecht2d@admin.ch',4,'Enrolled',9,10),(87,'Wendell Brickner','1994-02-14','+86 138 727 8536','wbrickner2e@ow.ly',5,'Enrolled',9,8),(88,'Jo Clemenza','1990-09-26','+86 512 505 9337','jclemenza2f@pen.io',1,'Enrolled',10,4),(89,'Iris Caveau','1997-09-10','+86 154 217 4323','icaveau2g@pcworld.com',2,'Enrolled',7,19),(90,'Demetre Frankcom','2001-01-31','+1 281 781 1464','dfrankcom2h@ucoz.com',3,'Enrolled',2,18),(91,'Damita Churchin','1993-03-30','+57 107 518 3988','dchurchin2i@chicagotribune.com',2,'Paused',10,6),(92,'Mella Gurwood','1990-06-30','+86 502 867 0099','mgurwood2j@jiathis.com',8,'Enrolled',10,10),(93,'Onfroi Adin','1992-01-20','+62 984 195 2349','oadin2k@creativecommons.org',10,'Paused',8,7),(94,'Carlyle de Voiels','1991-10-01','+7 298 915 7484','cde2l@elegantthemes.com',5,'Graduated',5,9),(95,'Karyl Wemyss','1990-08-17','+33 662 387 7818','kwemyss2m@arizona.edu',2,'Paused',3,4),(96,'Isobel Brunner','1995-02-28','+54 905 270 9964','ibrunner2n@sciencedirect.com',7,'Paused',4,2),(97,'Gwenni Kersey','2002-01-02','+62 663 969 4715','gkersey2o@quantcast.com',7,'Enrolled',10,4),(98,'Sigrid Joutapaitis','2001-04-03','+86 784 309 8652','sjoutapaitis2p@yellowpages.com',5,'Paused',7,19),(99,'Keith Josilevich','1990-11-20','+54 895 974 7184','kjosilevich2q@telegraph.co.uk',1,'Paused',6,16),(100,'Amalie Garritley','1996-11-28','+7 202 718 9534','agarritley2r@cornell.edu',1,'Enrolled',3,15);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-15 14:27:11
