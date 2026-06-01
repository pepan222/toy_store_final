-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Июн 01 2026 г., 18:25
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `toys2026`
--

-- --------------------------------------------------------

--
-- Структура таблицы `categories`
--

CREATE TABLE `categories` (
  `category_id` int UNSIGNED NOT NULL,
  `name` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `categories`
--

INSERT INTO `categories` (`category_id`, `name`) VALUES
(3, 'Детский музыкальный инструмент'),
(1, 'Игровой набор'),
(2, 'Конструктор'),
(4, 'Машинка');

-- --------------------------------------------------------

--
-- Структура таблицы `manufacturers`
--

CREATE TABLE `manufacturers` (
  `manufacturer_id` int UNSIGNED NOT NULL,
  `name` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `manufacturers`
--

INSERT INTO `manufacturers` (`manufacturer_id`, `name`) VALUES
(1, 'ABSпластик'),
(2, 'BambiniFelici'),
(3, 'Junion');

-- --------------------------------------------------------

--
-- Структура таблицы `orders`
--

CREATE TABLE `orders` (
  `order_id` int UNSIGNED NOT NULL,
  `order_number` int UNSIGNED NOT NULL,
  `article_text` varchar(255) NOT NULL,
  `order_date` date DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `pickup_point_id` int UNSIGNED NOT NULL,
  `client_user_id` int UNSIGNED DEFAULT NULL,
  `pickup_code` int UNSIGNED NOT NULL,
  `status_id` tinyint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `orders`
--

INSERT INTO `orders` (`order_id`, `order_number`, `article_text`, `order_date`, `delivery_date`, `pickup_point_id`, `client_user_id`, `pickup_code`, `status_id`) VALUES
(42, 1, 'PMEZMH, 2, BPV4MM, 2', '2025-02-27', '2025-04-20', 1, 7, 901, 1),
(43, 2, 'JVL42J, 1, F895RB, 1', '2024-09-28', '2025-04-21', 11, 1, 902, 1),
(44, 3, '3XBOTN, 10, 3L7RCZ, 10', '2025-03-21', '2025-04-22', 2, 2, 903, 1),
(45, 4, 'S72AM3, 5, 2G3280, 4', '2025-02-20', '2025-04-23', 11, 10, 904, 1),
(46, 5, 'MIO8YV, 2, UER2QD, 2', '2025-03-17', '2025-04-24', 2, 7, 905, 1),
(47, 6, 'PMEZMH, 2, BPV4MM, 2', '2025-03-01', '2025-04-25', 15, 8, 906, 1),
(48, 7, 'JVL42J, 1, F895RB, 1', NULL, '2025-04-26', 3, 2, 907, 1),
(49, 8, '3XBOTN, 10, 3L7RCZ, 10', '2025-03-31', '2025-04-27', 19, 10, 908, 2),
(50, 9, 'S72AM3, 5, 2G3280, 4', '2025-04-02', '2025-04-28', 5, 2, 909, 2),
(51, 10, 'MIO8YV, 2, UER2QD, 2', '2025-04-03', '2025-04-29', 19, 10, 910, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `orders_import_raw`
--

CREATE TABLE `orders_import_raw` (
  `raw_id` int UNSIGNED NOT NULL,
  `order_number_text` varchar(40) DEFAULT NULL,
  `articles_text` varchar(255) DEFAULT NULL,
  `order_date_text` varchar(40) DEFAULT NULL,
  `delivery_date_text` varchar(40) DEFAULT NULL,
  `pickup_point_text` varchar(40) DEFAULT NULL,
  `client_fio_text` varchar(200) DEFAULT NULL,
  `pickup_code_text` varchar(40) DEFAULT NULL,
  `status_text` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `orders_import_raw`
--

INSERT INTO `orders_import_raw` (`raw_id`, `order_number_text`, `articles_text`, `order_date_text`, `delivery_date_text`, `pickup_point_text`, `client_fio_text`, `pickup_code_text`, `status_text`) VALUES
(1, '1', 'PMEZMH, 2, BPV4MM, 2', '27.02.2025', '20.04.2025', '1', 'Степанов Михаил Артёмович', '901', 'Завершен'),
(2, '2', 'JVL42J, 1, F895RB, 1', '28.09.2024', '21.04.2025', '11', 'Ворсин Петр Евгеньевич', '902', 'Завершен'),
(3, '3', '3XBOTN, 10, 3L7RCZ, 10', '21.03.2025', '22.04.2025', '2', 'Старикова Елена Павловна', '903', 'Завершен'),
(4, '4', 'S72AM3, 5, 2G3280, 4', '20.02.2025', '23.04.2025', '11', 'Сазонов Руслан Германович', '904', 'Завершен'),
(5, '5', 'MIO8YV, 2, UER2QD, 2', '17.03.2025', '24.04.2025', '2', 'Степанов Михаил Артёмович', '905', 'Завершен'),
(6, '6', 'PMEZMH, 2, BPV4MM, 2', '01.03.2025', '25.04.2025', '15', 'Ворсин Петр Евгеньевич', '906', 'Завершен'),
(7, '7', 'JVL42J, 1, F895RB, 1', NULL, '26.04.2025', '3', 'Старикова Елена Павловна', '907', 'Завершен'),
(8, '8', '3XBOTN, 10, 3L7RCZ, 10', '31.03.2025', '27.04.2025', '19', 'Сазонов Руслан Германович', '908', 'Новый'),
(9, '9', 'S72AM3, 5, 2G3280, 4', '02.04.2025', '28.04.2025', '5', 'Старикова Елена Павловна', '909', 'Новый'),
(10, '10', 'MIO8YV, 2, UER2QD, 2', '03.04.2025', '29.04.2025', '19', 'Сазонов Руслан Германович', '910', 'Новый');

-- --------------------------------------------------------

--
-- Структура таблицы `order_items`
--

CREATE TABLE `order_items` (
  `order_item_id` int UNSIGNED NOT NULL,
  `order_id` int UNSIGNED NOT NULL,
  `product_id` int UNSIGNED NOT NULL,
  `quantity` int NOT NULL
) ;

--
-- Дамп данных таблицы `order_items`
--

INSERT INTO `order_items` (`order_item_id`, `order_id`, `product_id`, `quantity`) VALUES
(1, 42, 1, 2),
(2, 43, 3, 1),
(3, 44, 5, 10),
(4, 45, 7, 5),
(5, 46, 9, 2),
(6, 47, 1, 2),
(7, 48, 3, 1),
(8, 49, 5, 10),
(9, 50, 7, 5),
(10, 51, 9, 2),
(11, 42, 2, 2),
(12, 43, 4, 1),
(13, 44, 6, 10),
(14, 45, 8, 4),
(15, 46, 10, 2),
(16, 47, 2, 2),
(17, 48, 4, 1),
(18, 49, 6, 10),
(19, 50, 8, 4),
(20, 51, 10, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `order_statuses`
--

CREATE TABLE `order_statuses` (
  `status_id` tinyint UNSIGNED NOT NULL,
  `status_name` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `order_statuses`
--

INSERT INTO `order_statuses` (`status_id`, `status_name`) VALUES
(1, 'Завершен'),
(2, 'Новый');

-- --------------------------------------------------------

--
-- Структура таблицы `pickup_points`
--

CREATE TABLE `pickup_points` (
  `pickup_point_id` int UNSIGNED NOT NULL,
  `address_text` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `pickup_points`
--

INSERT INTO `pickup_points` (`pickup_point_id`, `address_text`) VALUES
(2, '125061, г. Лесной, ул. Подгорная, 8'),
(29, '125703, г. Лесной, ул. Партизанская, 49'),
(28, '125837, г. Лесной, ул. Шоссейная, 40'),
(36, '190949, г. Лесной, ул. Мичурина, 26'),
(24, '344288, г. Лесной, ул. Чехова, 1'),
(16, '394060, г.Лесной, ул. Фрунзе, 43'),
(26, '394242, г. Лесной, ул. Коммунистическая, 43'),
(21, '394782, г. Лесной, ул. Чехова, 3'),
(4, '400562, г. Лесной, ул. Зеленая, 32'),
(11, '410172, г. Лесной, ул. Северная, 13'),
(6, '410542, г. Лесной, ул. Светлая, 46'),
(17, '410661, г. Лесной, ул. Школьная, 50'),
(1, '420151, г. Лесной, ул. Вишневая, 32'),
(32, '426030, г. Лесной, ул. Маяковского, 44'),
(8, '443890, г. Лесной, ул. Коммунистическая, 1'),
(33, '450375, г. Лесной ул. Клубная, 44'),
(23, '450558, г. Лесной, ул. Набережная, 30'),
(20, '450983, г.Лесной, ул. Комсомольская, 26'),
(13, '454311, г.Лесной, ул. Новая, 19'),
(22, '603002, г. Лесной, ул. Дзержинского, 28'),
(15, '603036, г. Лесной, ул. Садовая, 4'),
(9, '603379, г. Лесной, ул. Спортивная, 46'),
(10, '603721, г. Лесной, ул. Гоголя, 41'),
(25, '614164, г.Лесной,  ул. Степная, 30'),
(5, '614510, г. Лесной, ул. Маяковского, 47'),
(12, '614611, г. Лесной, ул. Молодежная, 50'),
(31, '614753, г. Лесной, ул. Полевая, 35'),
(7, '620839, г. Лесной, ул. Цветочная, 8'),
(30, '625283, г. Лесной, ул. Победы, 46'),
(34, '625560, г. Лесной, ул. Некрасова, 12'),
(18, '625590, г. Лесной, ул. Коммунистическая, 20'),
(19, '625683, г. Лесной, ул. 8 Марта'),
(35, '630201, г. Лесной, ул. Комсомольская, 17'),
(3, '630370, г. Лесной, ул. Шоссейная, 24'),
(14, '660007, г.Лесной, ул. Октябрьская, 19'),
(27, '660540, г. Лесной, ул. Солнечная, 25');

-- --------------------------------------------------------

--
-- Структура таблицы `pickup_points_import_raw`
--

CREATE TABLE `pickup_points_import_raw` (
  `raw_id` int UNSIGNED NOT NULL,
  `address_text` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `pickup_points_import_raw`
--

INSERT INTO `pickup_points_import_raw` (`raw_id`, `address_text`) VALUES
(1, '420151, г. Лесной, ул. Вишневая, 32'),
(2, '125061, г. Лесной, ул. Подгорная, 8'),
(3, '630370, г. Лесной, ул. Шоссейная, 24'),
(4, '400562, г. Лесной, ул. Зеленая, 32'),
(5, '614510, г. Лесной, ул. Маяковского, 47'),
(6, '410542, г. Лесной, ул. Светлая, 46'),
(7, '620839, г. Лесной, ул. Цветочная, 8'),
(8, '443890, г. Лесной, ул. Коммунистическая, 1'),
(9, '603379, г. Лесной, ул. Спортивная, 46'),
(10, '603721, г. Лесной, ул. Гоголя, 41'),
(11, '410172, г. Лесной, ул. Северная, 13'),
(12, '614611, г. Лесной, ул. Молодежная, 50'),
(13, '454311, г.Лесной, ул. Новая, 19'),
(14, '660007, г.Лесной, ул. Октябрьская, 19'),
(15, '603036, г. Лесной, ул. Садовая, 4'),
(16, '394060, г.Лесной, ул. Фрунзе, 43'),
(17, '410661, г. Лесной, ул. Школьная, 50'),
(18, '625590, г. Лесной, ул. Коммунистическая, 20'),
(19, '625683, г. Лесной, ул. 8 Марта'),
(20, '450983, г.Лесной, ул. Комсомольская, 26'),
(21, '394782, г. Лесной, ул. Чехова, 3'),
(22, '603002, г. Лесной, ул. Дзержинского, 28'),
(23, '450558, г. Лесной, ул. Набережная, 30'),
(24, '344288, г. Лесной, ул. Чехова, 1'),
(25, '614164, г.Лесной,  ул. Степная, 30'),
(26, '394242, г. Лесной, ул. Коммунистическая, 43'),
(27, '660540, г. Лесной, ул. Солнечная, 25'),
(28, '125837, г. Лесной, ул. Шоссейная, 40'),
(29, '125703, г. Лесной, ул. Партизанская, 49'),
(30, '625283, г. Лесной, ул. Победы, 46'),
(31, '614753, г. Лесной, ул. Полевая, 35'),
(32, '426030, г. Лесной, ул. Маяковского, 44'),
(33, '450375, г. Лесной ул. Клубная, 44'),
(34, '625560, г. Лесной, ул. Некрасова, 12'),
(35, '630201, г. Лесной, ул. Комсомольская, 17'),
(36, '190949, г. Лесной, ул. Мичурина, 26');

-- --------------------------------------------------------

--
-- Структура таблицы `products`
--

CREATE TABLE `products` (
  `product_id` int UNSIGNED NOT NULL,
  `article` varchar(50) NOT NULL,
  `name` varchar(200) NOT NULL,
  `unit_name` varchar(20) NOT NULL,
  `price` decimal(12,2) NOT NULL,
  `supplier_id` int UNSIGNED NOT NULL,
  `manufacturer_id` int UNSIGNED NOT NULL,
  `category_id` int UNSIGNED NOT NULL,
  `discount_percent` decimal(5,2) NOT NULL,
  `stock_quantity` int NOT NULL,
  `description_text` text,
  `photo_file` varchar(255) DEFAULT NULL
) ;

--
-- Дамп данных таблицы `products`
--

INSERT INTO `products` (`product_id`, `article`, `name`, `unit_name`, `price`, `supplier_id`, `manufacturer_id`, `category_id`, `discount_percent`, `stock_quantity`, `description_text`, `photo_file`) VALUES
(1, 'PMEZMH', 'Детский игровой набор машинок Щенячий патруль / Dogs mini . 9 героев + 9 инерфионных машинок', 'шт.', '1.00', 1, 1, 1, '22.00', 50, 'Детский набор машинок с героями мультсериала «Щенячий патруль» подойдет как для мальчиков, так и для девочек. В детский набор входит 9 фигурок щенков спасателей.', '1.jpg'),
(2, 'BPV4MM', 'Конструктор Гарри Поттер Сова Букля 630 деталей совместим с lego harry potter, лего совместимый)', 'шт.', '771.00', 2, 1, 2, '15.00', 26, 'Коллекционная модель Букля состоит из множества потрясающих элементов, а также специального механизма внутри. С его помощью можно плавно поднимать-опускать крылья птицы.', '2.jpg'),
(3, 'JVL42J', 'Музыкальные инструменты для детей, ксилофон, барабаны, развивающие игрушки, игрушки для детей', 'шт.', '2750.00', 2, 2, 3, '15.00', 0, 'Откройте мир музыки для вашего ребенка с этой уникальной игрушкой! Это многофункциональное музыкальное чудо объединяет в себе всё, что нужно для творческого развития.', '3.jpg'),
(4, 'F895RB', 'Машинка игрушка диско шар светящаяся музыкальная', 'шт.', '368.00', 3, 1, 4, '6.00', 7, 'Светящаяся музыкальная машина с диско шаром переливается разными цветами, играет ритмичные мелодии, объезжает препятствия и крутится, поэтому с ней точно не будет скучно.', '4.jpg'),
(5, '3XBOTN', 'Игровой набор Hot Wheels Action Loop Cyclone Challenge Track, с машинкой и удобным хранением, HTK16', 'шт.', '3426.00', 3, 2, 1, '10.00', 21, 'Игровой набор Hot Wheels Action Loop Cyclone Challenge Track - это уникальная игра, которая позволит вам испытать себя и своих друзей в скорости и ловкости. Этот набор состоит из металлической дорожки с циклоном, которая создает потрясающий эффект и добавляет дополнительную сложность в игру.', '5.jpg'),
(6, '3L7RCZ', 'Игровой набор с деревянными машинками Стройплощадка Кран-Паркс, Junion', 'шт.', '7400.00', 3, 3, 1, '15.00', 0, 'Игровой набор «Стройплощадка Кран-Паркс Junion» — это большая игрушечная парковка с деревянными машинками и настоящим подъёмным краном, придуманная в Яндексе настоящими родителями.', '6.jpg'),
(7, 'S72AM3', 'Синтезатор детский с микрофоном 61 клавиша', 'шт.', '1749.00', 4, 3, 3, '10.00', 35, 'Откройте для ребенка дверь в мир музыки с детским синтезатором! Этот компактный инструмент с микрофоном станет верным другом для юных музыкантов, помогая им развивать творческий потенциал и получать удовольствие от игры.', '7.jpg'),
(8, '2G3280', 'Деревянный игровой набор JUNION Стройплощадка \"Кран-Паркс\" с подъёмным, строительным краном и машинками, 18 предметов, подвижные элементы', 'шт.', '1624.00', 5, 3, 1, '9.00', 20, 'Игровой набор «Стройплощадка Кран-Паркс Junion» — это большая игрушечная парковка с деревянными машинками и настоящим подъёмным краном, придуманная в Яндексе настоящими родителями.', '8.jpg'),
(9, 'MIO8YV', 'Музыкальная игрушка интерактивная Пульт, детский прорезыватель для малышей', 'шт.', '305.00', 5, 2, 3, '9.00', 31, 'Музыкальная игрушка интерактивная Пульт, детский прорезыватель для малышей', '9.jpg'),
(10, 'UER2QD', 'Большой набор опытов и экспериментов для детей 14 в 1', 'шт.', '2506.00', 5, 2, 1, '8.00', 27, 'Большой набор опытов и экспериментов для детей 14 в 1', '10.jpg');

-- --------------------------------------------------------

--
-- Структура таблицы `products_import_raw`
--

CREATE TABLE `products_import_raw` (
  `article_text` varchar(60) DEFAULT NULL,
  `name_text` varchar(200) DEFAULT NULL,
  `unit_text` varchar(20) DEFAULT NULL,
  `price_text` varchar(40) DEFAULT NULL,
  `supplier_text` varchar(120) DEFAULT NULL,
  `manufacturer_text` varchar(120) DEFAULT NULL,
  `category_text` varchar(120) DEFAULT NULL,
  `discount_text` varchar(40) DEFAULT NULL,
  `stock_text` varchar(40) DEFAULT NULL,
  `description_text` text,
  `photo_text` varchar(120) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `products_import_raw`
--

INSERT INTO `products_import_raw` (`article_text`, `name_text`, `unit_text`, `price_text`, `supplier_text`, `manufacturer_text`, `category_text`, `discount_text`, `stock_text`, `description_text`, `photo_text`) VALUES
('PMEZMH', 'Детский игровой набор машинок Щенячий патруль / Dogs mini . 9 героев + 9 инерфионных машинок', 'шт.', '1 414', 'Pikeshop', 'ABSпластик', 'Игровой набор', '22', '50', 'Детский набор машинок с героями мультсериала «Щенячий патруль» подойдет как для мальчиков, так и для девочек. В детский набор входит 9 фигурок щенков спасателей. ', '1.jpg'),
('BPV4MM', 'Конструктор Гарри Поттер Сова Букля 630 деталей совместим с lego harry potter, лего совместимый)', 'шт.', '771', 'Playbig', 'ABSпластик', 'Конструктор', '15', '26', 'Коллекционная модель Букля состоит из множества потрясающих элементов, а также специального механизма внутри. С его помощью можно плавно поднимать-опускать крылья птицы.', '2.jpg'),
('JVL42J', 'Музыкальные инструменты для детей, ксилофон, барабаны, развивающие игрушки, игрушки для детей', 'шт.', '2750', 'Playbig', 'BambiniFelici', 'Детский музыкальный инструмент', '15', '0', 'Откройте мир музыки для вашего ребенка с этой уникальной игрушкой! Это многофункциональное музыкальное чудо объединяет в себе всё, что нужно для творческого развития.', '3.jpg'),
('F895RB', 'Машинка игрушка диско шар светящаяся музыкальная', 'шт.', '368', 'Knauf', 'ABSпластик', 'Машинка', '6', '7', 'Светящаяся музыкальная машина с диско шаром переливается разными цветами, играет ритмичные мелодии, объезжает препятствия и крутится, поэтому с ней точно не будет скучно.', '4.jpg'),
('3XBOTN', 'Игровой набор Hot Wheels Action Loop Cyclone Challenge Track, с машинкой и удобным хранением, HTK16', 'шт.', '3426', 'Knauf', 'BambiniFelici', 'Игровой набор', '10', '21', 'Игровой набор Hot Wheels Action Loop Cyclone Challenge Track - это уникальная игра, которая позволит вам испытать себя и своих друзей в скорости и ловкости. Этот набор состоит из металлической дорожки с циклоном, которая создает потрясающий эффект и добавляет дополнительную сложность в игру.', '5.jpg'),
('3L7RCZ', 'Игровой набор с деревянными машинками Стройплощадка Кран-Паркс, Junion', 'шт.', '7400', 'Knauf', 'Junion', 'Игровой набор', '15', '0', 'Игровой набор «Стройплощадка Кран-Паркс Junion» — это большая игрушечная парковка с деревянными машинками и настоящим подъёмным краном, придуманная в Яндексе настоящими родителями.', '6.jpg'),
('S72AM3', 'Синтезатор детский с микрофоном 61 клавиша', 'шт.', '1749', 'CHILITOY', 'Junion', 'Детский музыкальный инструмент', '10', '35', 'Откройте для ребенка дверь в мир музыки с детским синтезатором! Этот компактный инструмент с микрофоном станет верным другом для юных музыкантов, помогая им развивать творческий потенциал и получать удовольствие от игры.', '7.jpg'),
('2G3280', 'Деревянный игровой набор JUNION Стройплощадка \"Кран-Паркс\" с подъёмным, строительным краном и машинками, 18 предметов, подвижные элементы', 'шт.', '1624', 'Vinylon', 'Junion', 'Игровой набор', '9', '20', 'Игровой набор «Стройплощадка Кран-Паркс Junion» — это большая игрушечная парковка с деревянными машинками и настоящим подъёмным краном, придуманная в Яндексе настоящими родителями.', '8.jpg'),
('MIO8YV', 'Музыкальная игрушка интерактивная Пульт, детский прорезыватель для малышей', 'шт.', '305', 'Vinylon', 'BambiniFelici', 'Детский музыкальный инструмент', '9', '31', 'Музыкальная игрушка интерактивная Пульт, детский прорезыватель для малышей', '9.jpg'),
('UER2QD', 'Большой набор опытов и экспериментов для детей 14 в 1', 'шт.', '2506', 'Vinylon', 'BambiniFelici', 'Игровой набор', '8', '27', 'Большой набор опытов и экспериментов для детей 14 в 1', '10.jpg');

-- --------------------------------------------------------

--
-- Структура таблицы `roles`
--

CREATE TABLE `roles` (
  `role_id` tinyint UNSIGNED NOT NULL,
  `role_name` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `roles`
--

INSERT INTO `roles` (`role_id`, `role_name`) VALUES
(2, 'Авторизированный клиент'),
(4, 'Администратор'),
(1, 'Гость'),
(3, 'Менеджер');

-- --------------------------------------------------------

--
-- Структура таблицы `suppliers`
--

CREATE TABLE `suppliers` (
  `supplier_id` int UNSIGNED NOT NULL,
  `name` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `suppliers`
--

INSERT INTO `suppliers` (`supplier_id`, `name`) VALUES
(4, 'CHILITOY'),
(3, 'Knauf'),
(1, 'Pikeshop'),
(2, 'Playbig'),
(5, 'Vinylon');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `user_id` int UNSIGNED NOT NULL,
  `role_id` tinyint UNSIGNED NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `login` varchar(120) NOT NULL,
  `password_plain` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`user_id`, `role_id`, `full_name`, `login`, `password_plain`) VALUES
(1, 4, 'Ворсин Петр Евгеньевич', '94d5ous@gmail.com', 'uzWC67'),
(2, 4, 'Старикова Елена Павловна', 'uth4iz@mail.com', '2L6KZG'),
(3, 4, 'Одинцов Серафим Артёмович', 'yzls62@outlook.com', 'JlFRCZ'),
(4, 3, 'Михайлюк Анна Вячеславовна', '1diph5e@tutanota.com', '8ntwUp'),
(5, 3, 'Ситдикова Елена Анатольевна', 'tjde7c@yahoo.com', 'YOyhfR'),
(6, 3, 'Никифорова Весения Николаевна', 'wpmrc3do@tutanota.com', 'RSbvHv'),
(7, 2, 'Степанов Михаил Артёмович', '5d4zbu@tutanota.com', 'rwVDh9'),
(8, 2, 'Ворсин Петр Евгеньевич', 'ptec8ym@yahoo.com', 'LdNyos'),
(9, 2, 'Старикова Елена Павловна', '1qz4kw@mail.com', 'gynQMT'),
(10, 2, 'Сазонов Руслан Германович', '4np6se@mail.com', 'AtnDjr');

-- --------------------------------------------------------

--
-- Структура таблицы `users_import_raw`
--

CREATE TABLE `users_import_raw` (
  `role_name` varchar(100) DEFAULT NULL,
  `full_name` varchar(200) DEFAULT NULL,
  `login_text` varchar(120) DEFAULT NULL,
  `password_text` varchar(120) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `users_import_raw`
--

INSERT INTO `users_import_raw` (`role_name`, `full_name`, `login_text`, `password_text`) VALUES
('Администратор', 'Ворсин Петр Евгеньевич', '94d5ous@gmail.com', 'uzWC67'),
('Администратор', 'Старикова Елена Павловна', 'uth4iz@mail.com', '2L6KZG'),
('Администратор', 'Одинцов Серафим Артёмович', 'yzls62@outlook.com', 'JlFRCZ'),
('Менеджер', 'Михайлюк Анна Вячеславовна', '1diph5e@tutanota.com', '8ntwUp'),
('Менеджер', 'Ситдикова Елена Анатольевна', 'tjde7c@yahoo.com', 'YOyhfR'),
('Менеджер', 'Никифорова Весения Николаевна', 'wpmrc3do@tutanota.com', 'RSbvHv'),
('Авторизированный клиент', 'Степанов Михаил Артёмович', '5d4zbu@tutanota.com', 'rwVDh9'),
('Авторизированный клиент', 'Ворсин Петр Евгеньевич', 'ptec8ym@yahoo.com', 'LdNyos'),
('Авторизированный клиент', 'Старикова Елена Павловна', '1qz4kw@mail.com', 'gynQMT'),
('Авторизированный клиент', 'Сазонов Руслан Германович', '4np6se@mail.com', 'AtnDjr');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `manufacturers`
--
ALTER TABLE `manufacturers`
  ADD PRIMARY KEY (`manufacturer_id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD UNIQUE KEY `order_number` (`order_number`),
  ADD KEY `fk_orders_pickup_points` (`pickup_point_id`),
  ADD KEY `fk_orders_users` (`client_user_id`),
  ADD KEY `idx_orders_status` (`status_id`);

--
-- Индексы таблицы `orders_import_raw`
--
ALTER TABLE `orders_import_raw`
  ADD PRIMARY KEY (`raw_id`);

--
-- Индексы таблицы `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`order_item_id`),
  ADD UNIQUE KEY `uk_order_product` (`order_id`,`product_id`),
  ADD KEY `idx_order_items_product` (`product_id`);

--
-- Индексы таблицы `order_statuses`
--
ALTER TABLE `order_statuses`
  ADD PRIMARY KEY (`status_id`),
  ADD UNIQUE KEY `status_name` (`status_name`);

--
-- Индексы таблицы `pickup_points`
--
ALTER TABLE `pickup_points`
  ADD PRIMARY KEY (`pickup_point_id`),
  ADD UNIQUE KEY `address_text` (`address_text`);

--
-- Индексы таблицы `pickup_points_import_raw`
--
ALTER TABLE `pickup_points_import_raw`
  ADD PRIMARY KEY (`raw_id`);

--
-- Индексы таблицы `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`),
  ADD UNIQUE KEY `article` (`article`),
  ADD KEY `fk_products_manufacturers` (`manufacturer_id`),
  ADD KEY `idx_products_supplier` (`supplier_id`),
  ADD KEY `idx_products_category` (`category_id`);

--
-- Индексы таблицы `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`role_id`),
  ADD UNIQUE KEY `role_name` (`role_name`);

--
-- Индексы таблицы `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`supplier_id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `login` (`login`),
  ADD KEY `fk_users_roles` (`role_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `categories`
--
ALTER TABLE `categories`
  MODIFY `category_id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `manufacturers`
--
ALTER TABLE `manufacturers`
  MODIFY `manufacturer_id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT для таблицы `orders_import_raw`
--
ALTER TABLE `orders_import_raw`
  MODIFY `raw_id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `order_items`
--
ALTER TABLE `order_items`
  MODIFY `order_item_id` int UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `order_statuses`
--
ALTER TABLE `order_statuses`
  MODIFY `status_id` tinyint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `pickup_points_import_raw`
--
ALTER TABLE `pickup_points_import_raw`
  MODIFY `raw_id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT для таблицы `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `supplier_id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `fk_orders_pickup_points` FOREIGN KEY (`pickup_point_id`) REFERENCES `pickup_points` (`pickup_point_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_orders_statuses` FOREIGN KEY (`status_id`) REFERENCES `order_statuses` (`status_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_orders_users` FOREIGN KEY (`client_user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `fk_order_items_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_order_items_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `fk_products_categories` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_products_manufacturers` FOREIGN KEY (`manufacturer_id`) REFERENCES `manufacturers` (`manufacturer_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_products_suppliers` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`supplier_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `fk_users_roles` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`) ON DELETE RESTRICT ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
