-- MySQL dump 10.13  Distrib 5.7.26, for Linux (x86_64)
--
-- Host: localhost    Database: cardinal
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `access_point_groups`
--

DROP TABLE IF EXISTS `access_point_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `access_point_groups` (
  `ap_group_id` int(11) NOT NULL AUTO_INCREMENT,
  `ap_group_name` text NOT NULL,
  PRIMARY KEY (`ap_group_id`),
  UNIQUE KEY `access_point_groups` (`ap_group_name`(255))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COMMENT='For Cardinal Access Point Groups';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `access_points`
--

DROP TABLE IF EXISTS `access_points`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `access_points` (
  `ap_id` int(11) NOT NULL AUTO_INCREMENT,
  `ap_group_id` int(11) NOT NULL,
  `ap_name` text NOT NULL,
  `ap_ip` text NOT NULL,
  `ap_ssh_username` text NOT NULL,
  `ap_ssh_password` text NOT NULL,
  `ap_snmp` text NOT NULL,
  `ap_total_clients` varchar(255) DEFAULT '0',
  `ap_bandwidth` varchar(255) DEFAULT NULL,
  `ap_mac_addr` varchar(255) DEFAULT NULL,
  `ap_model` varchar(255) DEFAULT NULL,
  `ap_serial` varchar(255) DEFAULT NULL,
  `ap_location` varchar(255) DEFAULT NULL,
  `ap_ios_info` varchar(255) DEFAULT NULL,
  `ap_ping_ms` varchar(255) DEFAULT NULL,
  `ap_uptime` varchar(255) DEFAULT NULL,
  `ap_all_id` int(11) DEFAULT '2',
  PRIMARY KEY (`ap_id`),
  UNIQUE KEY `ap_name` (`ap_name`(255)),
  UNIQUE KEY `ap_ip` (`ap_ip`(15))
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1 COMMENT='For Cardinal Individual Access Points';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `settings` (
  `settings_id` int(11) NOT NULL,
  `cardinal_home` text NOT NULL COMMENT 'Directory where Cardinal core resides',
  `scout_dir` text NOT NULL COMMENT 'Directory where Scout resides',
  `cardinal_tftp` text NOT NULL COMMENT 'Directory where Cardinal TFTP data is stored',
  `poll_schedule` int(11) NOT NULL COMMENT 'Amount (in minutes) when Cardinal fetches information',
  PRIMARY KEY (`settings_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ssids_24ghz`
--

DROP TABLE IF EXISTS `ssids_24ghz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ssids_24ghz` (
  `ap_ssid_id` int(11) NOT NULL AUTO_INCREMENT,
  `ap_ssid_name` text NOT NULL,
  `ap_ssid_vlan` int(11) NOT NULL,
  `ap_ssid_wpa2` text,
  `ap_ssid_bridge_id` int(11) NOT NULL,
  `ap_ssid_radio_id` int(11) NOT NULL,
  `ap_ssid_ethernet_id` int(11) NOT NULL,
  PRIMARY KEY (`ap_ssid_id`),
  UNIQUE KEY `ap_ssid_name` (`ap_ssid_name`(255))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COMMENT='For Cardinal SSIDs on 2.4GHz radio';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ssids_24ghz_deployed`
--

DROP TABLE IF EXISTS `ssids_24ghz_deployed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ssids_24ghz_deployed` (
  `ap_ssid_assoc_id` int(11) NOT NULL AUTO_INCREMENT,
  `ap_id` int(11) NOT NULL,
  `ssid_id` int(11) NOT NULL,
  PRIMARY KEY (`ap_ssid_assoc_id`),
  UNIQUE KEY `ap_id` (`ap_id`,`ssid_id`),
  KEY `ssid_id` (`ssid_id`),
  CONSTRAINT `ssids_24ghz_deployed_ibfk_1` FOREIGN KEY (`ssid_id`) REFERENCES `ssids_24ghz` (`ap_ssid_id`),
  CONSTRAINT `ssids_24ghz_deployed_ibfk_2` FOREIGN KEY (`ap_id`) REFERENCES `access_points` (`ap_id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ssids_24ghz_radius`
--

DROP TABLE IF EXISTS `ssids_24ghz_radius`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ssids_24ghz_radius` (
  `ap_ssid_id` int(11) NOT NULL AUTO_INCREMENT,
  `ap_ssid_name` text NOT NULL,
  `ap_ssid_vlan` int(11) NOT NULL,
  `ap_ssid_bridge_id` int(11) NOT NULL,
  `ap_ssid_radio_id` int(11) NOT NULL,
  `ap_ssid_ethernet_id` int(11) NOT NULL,
  `ap_ssid_radius_server` text NOT NULL,
  `ap_ssid_radius_secret` text,
  `ap_ssid_authorization_port` int(11) NOT NULL,
  `ap_ssid_accounting_port` int(11) NOT NULL,
  `ap_ssid_radius_timeout` int(11) NOT NULL,
  `ap_ssid_radius_group` text,
  `ap_ssid_radius_method_list` text,
  PRIMARY KEY (`ap_ssid_id`),
  UNIQUE KEY `ap_ssid_name` (`ap_ssid_name`(255))
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='For Cardinal RADIUS 2.4GHz SSIDs';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ssids_5ghz`
--

DROP TABLE IF EXISTS `ssids_5ghz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ssids_5ghz` (
  `ap_ssid_id` int(11) NOT NULL AUTO_INCREMENT,
  `ap_ssid_name` text NOT NULL,
  `ap_ssid_vlan` int(11) NOT NULL,
  `ap_ssid_wpa2` text NOT NULL,
  `ap_ssid_bridge_id` int(11) NOT NULL,
  `ap_ssid_radio_id` int(11) NOT NULL,
  `ap_ssid_ethernet_id` int(11) NOT NULL,
  PRIMARY KEY (`ap_ssid_id`),
  UNIQUE KEY `ap_ssid_name` (`ap_ssid_name`(255))
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='For Cardinal SSIDs on 5GHz radio';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ssids_5ghz_radius`
--

DROP TABLE IF EXISTS `ssids_5ghz_radius`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ssids_5ghz_radius` (
  `ap_ssid_id` int(11) NOT NULL AUTO_INCREMENT,
  `ap_ssid_name` text NOT NULL,
  `ap_ssid_vlan` int(11) NOT NULL,
  `ap_ssid_bridge_id` int(11) NOT NULL,
  `ap_ssid_radio_id` int(11) NOT NULL,
  `ap_ssid_ethernet_id` int(11) NOT NULL,
  `ap_ssid_radius_server` text NOT NULL,
  `ap_ssid_radius_secret` text,
  `ap_ssid_authorization_port` int(11) NOT NULL,
  `ap_ssid_accounting_port` int(11) NOT NULL,
  `ap_ssid_radius_timeout` int(11) NOT NULL,
  `ap_ssid_radius_group` text,
  `ap_ssid_radius_method_list` text,
  PRIMARY KEY (`ap_ssid_id`),
  UNIQUE KEY `ap_ssid_name` (`ap_ssid_name`(255))
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='For Cardinal RADIUS 5GHz SSIDs';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` char(102) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1 COMMENT='For Cardinal User Management';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-08-10  1:18:51
