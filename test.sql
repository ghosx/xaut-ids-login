-- phpMyAdmin SQL Dump
-- version 4.4.15.10
-- https://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2017-08-06 13:26:22
-- 服务器版本： 5.5.54-log
-- PHP Version: 5.4.45

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test`
--

-- --------------------------------------------------------

--
-- 表的结构 `lib_his`
--

CREATE TABLE IF NOT EXISTS `lib_his` (
  `id` int(9) NOT NULL,
  `bar_code` varchar(30) NOT NULL,
  `title` varchar(30) NOT NULL,
  `author` varchar(30) NOT NULL,
  `borrow_date` varchar(30) NOT NULL,
  `return_date` varchar(30) NOT NULL,
  `place` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `lib_info`
--

CREATE TABLE IF NOT EXISTS `lib_info` (
  `id` int(9) NOT NULL,
  `student_id` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  `sex` varchar(30) NOT NULL,
  `reader_id` varchar(30) NOT NULL,
  `reader_type` varchar(30) NOT NULL,
  `college` varchar(30) NOT NULL,
  `major` varchar(30) NOT NULL,
  `zhicheng` varchar(30) NOT NULL,
  `position` varchar(30) NOT NULL,
  `effective_date` varchar(30) NOT NULL,
  `expiry_date` varchar(30) NOT NULL,
  `cash_pledge` varchar(30) NOT NULL,
  `service_charge` varchar(30) NOT NULL,
  `total_book` varchar(30) NOT NULL,
  `dark_room` varchar(30) NOT NULL,
  `debt_status` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `lib_his`
--
ALTER TABLE `lib_his`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `lib_info`
--
ALTER TABLE `lib_info`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `lib_info`
--
ALTER TABLE `lib_info`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
