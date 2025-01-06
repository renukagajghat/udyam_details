-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 06, 2025 at 10:23 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 7.4.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `udyam_details_schema`
--

-- --------------------------------------------------------

--
-- Table structure for table `enterprises`
--

CREATE TABLE `enterprises` (
  `id` int(11) NOT NULL,
  `enterprise_name` varchar(255) NOT NULL,
  `organisation_type` varchar(255) NOT NULL,
  `date_of_incorporation` date NOT NULL,
  `date_of_udyam_registration` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `enterprises`
--

INSERT INTO `enterprises` (`id`, `enterprise_name`, `organisation_type`, `date_of_incorporation`, `date_of_udyam_registration`) VALUES
(1, 'M/S MIST IT SERVICES PRIVATE LIMITED', 'Private Limited Company', '0000-00-00', '0000-00-00'),
(2, 'M/S MIST IT SERVICES PRIVATE LIMITED', 'Private Limited Company', '2014-07-28', '2022-01-15'),
(3, 'M/S MIST IT SERVICES PRIVATE LIMITED', 'Private Limited Company', '2014-07-28', '2022-01-15'),
(4, 'M/S MIST IT SERVICES PRIVATE LIMITED', 'Private Limited Company', '2014-07-28', '2022-01-15'),
(5, 'M/S MIST IT SERVICES PRIVATE LIMITED', 'Private Limited Company', '2014-07-28', '2022-01-15');

-- --------------------------------------------------------

--
-- Table structure for table `enterprise_classifications`
--

CREATE TABLE `enterprise_classifications` (
  `id` int(11) NOT NULL,
  `enterprise_id` int(11) DEFAULT NULL,
  `classification_year` varchar(20) NOT NULL,
  `enterprise_type` varchar(50) NOT NULL,
  `classification_date` date NOT NULL,
  `s_no` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `enterprise_classifications`
--

INSERT INTO `enterprise_classifications` (`id`, `enterprise_id`, `classification_year`, `enterprise_type`, `classification_date`, `s_no`) VALUES
(1, 1, '2024-25', 'Small', '0000-00-00', 1),
(2, 1, '2023-24', 'Small', '0000-00-00', 2),
(3, 1, '2022-23', 'Micro', '0000-00-00', 3),
(4, 1, '2021-22', 'Micro', '0000-00-00', 4),
(5, 2, '2024-25', 'Small', '2024-04-27', 1),
(6, 2, '2023-24', 'Small', '2023-05-09', 2),
(7, 2, '2022-23', 'Micro', '2022-06-26', 3),
(8, 2, '2021-22', 'Micro', '2022-01-15', 4),
(9, 3, '2024-25', 'Small', '2024-04-27', 1),
(10, 3, '2023-24', 'Small', '2023-05-09', 2),
(11, 3, '2022-23', 'Micro', '2022-06-26', 3),
(12, 3, '2021-22', 'Micro', '2022-01-15', 4),
(13, 4, '2024-25', 'Small', '2024-04-27', 1),
(14, 4, '2023-24', 'Small', '2023-05-09', 2),
(15, 4, '2022-23', 'Micro', '2022-06-26', 3),
(16, 4, '2021-22', 'Micro', '2022-01-15', 4),
(17, 5, '2024-25', 'Small', '2024-04-27', 1),
(18, 5, '2023-24', 'Small', '2023-05-09', 2),
(19, 5, '2022-23', 'Micro', '2022-06-26', 3),
(20, 5, '2021-22', 'Micro', '2022-01-15', 4);

-- --------------------------------------------------------

--
-- Table structure for table `unit_locations`
--

CREATE TABLE `unit_locations` (
  `id` int(11) NOT NULL,
  `enterprise_id` int(11) DEFAULT NULL,
  `unit_name` varchar(255) NOT NULL,
  `flat` varchar(255) DEFAULT NULL,
  `building` varchar(255) DEFAULT NULL,
  `village_town` varchar(255) DEFAULT NULL,
  `block` varchar(255) DEFAULT NULL,
  `road` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `pin` varchar(10) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `district` varchar(255) DEFAULT NULL,
  `sn` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `unit_locations`
--

INSERT INTO `unit_locations` (`id`, `enterprise_id`, `unit_name`, `flat`, `building`, `village_town`, `block`, `road`, `city`, `pin`, `state`, `district`, `sn`) VALUES
(1, 1, 'MIST IT SERVICES PRIVATE LIMITED Vashi', '2046-2049', 'Akshar Business Park', 'Vashi', '“O” Wing, Plot No.03', 'Sec. 25', 'Navi Mumbai', '400703', 'MAHARASHTRA', 'THANE', 1),
(2, 1, 'MIST IT SERVICES PRIVATE LIMITED', 'OFFICE NO 902-903', 'ELLORA FIESTA', 'OPP JUINAGAR STATION', 'PLOT NO 8', 'SANPADA SECTOR 11', 'NAVI MUMBAI', '400614', 'MAHARASHTRA', 'MUMBAI', 2),
(3, 1, 'MIST IT Services Private Limited', 'I-185', 'GARHWALI MOHAL', 'LAXMI NAGAR', '', 'Block I', 'Delhi', '110092', 'DELHI', 'EAST', 3),
(4, 2, 'MIST IT SERVICES PRIVATE LIMITED Vashi', '2046-2049', 'Akshar Business Park', 'Vashi', '“O” Wing, Plot No.03', 'Sec. 25', 'Navi Mumbai', '400703', 'MAHARASHTRA', 'THANE', 1),
(5, 2, 'MIST IT SERVICES PRIVATE LIMITED', 'OFFICE NO 902-903', 'ELLORA FIESTA', 'OPP JUINAGAR STATION', 'PLOT NO 8', 'SANPADA SECTOR 11', 'NAVI MUMBAI', '400614', 'MAHARASHTRA', 'MUMBAI', 2),
(6, 2, 'MIST IT Services Private Limited', 'I-185', 'GARHWALI MOHAL', 'LAXMI NAGAR', '', 'Block I', 'Delhi', '110092', 'DELHI', 'EAST', 3),
(7, 3, 'MIST IT SERVICES PRIVATE LIMITED Vashi', '2046-2049', 'Akshar Business Park', 'Vashi', '“O” Wing, Plot No.03', 'Sec. 25', 'Navi Mumbai', '400703', 'MAHARASHTRA', 'THANE', 1),
(8, 3, 'MIST IT SERVICES PRIVATE LIMITED', 'OFFICE NO 902-903', 'ELLORA FIESTA', 'OPP JUINAGAR STATION', 'PLOT NO 8', 'SANPADA SECTOR 11', 'NAVI MUMBAI', '400614', 'MAHARASHTRA', 'MUMBAI', 2),
(9, 3, 'MIST IT Services Private Limited', 'I-185', 'GARHWALI MOHAL', 'LAXMI NAGAR', '', 'Block I', 'Delhi', '110092', 'DELHI', 'EAST', 3),
(10, 4, 'MIST IT SERVICES PRIVATE LIMITED Vashi', '2046-2049', 'Akshar Business Park', 'Vashi', '“O” Wing, Plot No.03', 'Sec. 25', 'Navi Mumbai', '400703', 'MAHARASHTRA', 'THANE', 1),
(11, 4, 'MIST IT SERVICES PRIVATE LIMITED', 'OFFICE NO 902-903', 'ELLORA FIESTA', 'OPP JUINAGAR STATION', 'PLOT NO 8', 'SANPADA SECTOR 11', 'NAVI MUMBAI', '400614', 'MAHARASHTRA', 'MUMBAI', 2),
(12, 4, 'MIST IT Services Private Limited', 'I-185', 'GARHWALI MOHAL', 'LAXMI NAGAR', '', 'Block I', 'Delhi', '110092', 'DELHI', 'EAST', 3),
(13, 5, 'MIST IT SERVICES PRIVATE LIMITED Vashi', '2046-2049', 'Akshar Business Park', 'Vashi', '“O” Wing, Plot No.03', 'Sec. 25', 'Navi Mumbai', '400703', 'MAHARASHTRA', 'THANE', 1),
(14, 5, 'MIST IT SERVICES PRIVATE LIMITED', 'OFFICE NO 902-903', 'ELLORA FIESTA', 'OPP JUINAGAR STATION', 'PLOT NO 8', 'SANPADA SECTOR 11', 'NAVI MUMBAI', '400614', 'MAHARASHTRA', 'MUMBAI', 2),
(15, 5, 'MIST IT Services Private Limited', 'I-185', 'GARHWALI MOHAL', 'LAXMI NAGAR', '', 'Block I', 'Delhi', '110092', 'DELHI', 'EAST', 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `enterprises`
--
ALTER TABLE `enterprises`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `enterprise_classifications`
--
ALTER TABLE `enterprise_classifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `enterprise_id` (`enterprise_id`);

--
-- Indexes for table `unit_locations`
--
ALTER TABLE `unit_locations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `enterprise_id` (`enterprise_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `enterprises`
--
ALTER TABLE `enterprises`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `enterprise_classifications`
--
ALTER TABLE `enterprise_classifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `unit_locations`
--
ALTER TABLE `unit_locations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `enterprise_classifications`
--
ALTER TABLE `enterprise_classifications`
  ADD CONSTRAINT `enterprise_classifications_ibfk_1` FOREIGN KEY (`enterprise_id`) REFERENCES `enterprises` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `unit_locations`
--
ALTER TABLE `unit_locations`
  ADD CONSTRAINT `unit_locations_ibfk_1` FOREIGN KEY (`enterprise_id`) REFERENCES `enterprises` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
