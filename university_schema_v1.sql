CREATE DATABASE  IF NOT EXISTS `universityrecordsystem` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `universityrecordsystem`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: universityrecordsystem
-- ------------------------------------------------------
-- Server version	8.0.44

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  PRIMARY KEY (`lecturer_id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `lecturers_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-10 22:39:59
