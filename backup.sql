--
-- PostgreSQL database dump
--


-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_app_furnizor; Type: TABLE DATA; Schema: django; Owner: aris
--

INSERT INTO django.magazin_app_furnizor (name, email, is_active, furnizor_id) VALUES ('MyProtein', 'myprotein@myprotein.com', true, 1);
INSERT INTO django.magazin_app_furnizor (name, email, is_active, furnizor_id) VALUES ('GymBeam', 'gymbeam@gymbeam.com', true, 2);
INSERT INTO django.magazin_app_furnizor (name, email, is_active, furnizor_id) VALUES ('FitNutrition', 'fitnutrition@fitnutrition.com', true, 3);


--
-- Name: magazin_app_furnizor_furnizor_id_seq; Type: SEQUENCE SET; Schema: django; Owner: aris
--

SELECT pg_catalog.setval('django.magazin_app_furnizor_furnizor_id_seq', 3, true);


--
-- PostgreSQL database dump complete
--


--
-- PostgreSQL database dump
--


-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_app_categorie; Type: TABLE DATA; Schema: django; Owner: aris
--

INSERT INTO django.magazin_app_categorie (name, description, status, categorie_id, icon, culoare) VALUES ('Creatine', 'creatine', 'activ', 6, 'fa-solid fa-bolt', 'yellow');
INSERT INTO django.magazin_app_categorie (name, description, status, categorie_id, icon, culoare) VALUES ('Pre-workout', 'pre-workout', 'activ', 5, 'fa-solid fa-fire-flame-simple', 'orange');
INSERT INTO django.magazin_app_categorie (name, description, status, categorie_id, icon, culoare) VALUES ('Aminoacizi', 'aminoacizi', 'activ', 4, 'fa-solid fa-dna', 'purple');
INSERT INTO django.magazin_app_categorie (name, description, status, categorie_id, icon, culoare) VALUES ('Minerale', 'idk', 'activ', 3, 'fa-solid fa-gem', 'blue');
INSERT INTO django.magazin_app_categorie (name, description, status, categorie_id, icon, culoare) VALUES ('Proteine', 'bla bla', 'activ', 2, 'fa-solid fa-dumbbell', 'grey');
INSERT INTO django.magazin_app_categorie (name, description, status, categorie_id, icon, culoare) VALUES ('Vitamine', 'bla bla', 'activ', 1, 'fa-solid fa-apple-whole', 'red');


--
-- Name: magazin_app_categorie_categorie_id_seq; Type: SEQUENCE SET; Schema: django; Owner: aris
--

SELECT pg_catalog.setval('django.magazin_app_categorie_categorie_id_seq', 6, true);


--
-- PostgreSQL database dump complete
--


--
-- PostgreSQL database dump
--


-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_app_produs; Type: TABLE DATA; Schema: django; Owner: aris
--

INSERT INTO django.magazin_app_produs (name, price, stock_quantity, is_active, weight, categorie_id, furnizor_id, produs_id) VALUES ('Electrolyte Hydration Tabs', 59.90, 50, true, 100, 3, 2, 2);
INSERT INTO django.magazin_app_produs (name, price, stock_quantity, is_active, weight, categorie_id, furnizor_id, produs_id) VALUES ('ZMA Recovery Formula', 89.50, 22, true, 180, 3, 1, 3);
INSERT INTO django.magazin_app_produs (name, price, stock_quantity, is_active, weight, categorie_id, furnizor_id, produs_id) VALUES ('Mass Gainer XXL 6000', 239.00, 8, true, 5000, 2, 1, 4);
INSERT INTO django.magazin_app_produs (name, price, stock_quantity, is_active, weight, categorie_id, furnizor_id, produs_id) VALUES ('Glutamine Pure Micronized', 109.00, 15, true, 600, 4, 2, 5);
INSERT INTO django.magazin_app_produs (name, price, stock_quantity, is_active, weight, categorie_id, furnizor_id, produs_id) VALUES ('BCAA 2:1:1 Instant Powder', 150.00, 20, true, 400, 4, 1, 6);
INSERT INTO django.magazin_app_produs (name, price, stock_quantity, is_active, weight, categorie_id, furnizor_id, produs_id) VALUES ('Pre-Workout Nitro Surge', 159.00, 12, true, 250, 5, 3, 7);
INSERT INTO django.magazin_app_produs (name, price, stock_quantity, is_active, weight, categorie_id, furnizor_id, produs_id) VALUES ('Vitamins Pack Daily Formula', 99.99, 25, true, 200, 1, 3, 8);
INSERT INTO django.magazin_app_produs (name, price, stock_quantity, is_active, weight, categorie_id, furnizor_id, produs_id) VALUES ('Creatină Xplode 5000', 129.99, 15, true, 500, 6, 3, 9);
INSERT INTO django.magazin_app_produs (name, price, stock_quantity, is_active, weight, categorie_id, furnizor_id, produs_id) VALUES ('Omega 3 Fish Oil 1000mg', 89.99, 30, true, 300, 1, 1, 10);
INSERT INTO django.magazin_app_produs (name, price, stock_quantity, is_active, weight, categorie_id, furnizor_id, produs_id) VALUES ('Proteina Whey Gold', 199.99, 5, true, 300, 2, 1, 1);
INSERT INTO django.magazin_app_produs (name, price, stock_quantity, is_active, weight, categorie_id, furnizor_id, produs_id) VALUES ('Creatina Xplode 1000', 220.00, 20, false, 300, 6, 1, 13);


--
-- Name: magazin_app_produs_produs_id_seq; Type: SEQUENCE SET; Schema: django; Owner: aris
--

SELECT pg_catalog.setval('django.magazin_app_produs_produs_id_seq', 14, true);


--
-- PostgreSQL database dump complete
--


--
-- PostgreSQL database dump
--


-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_app_inventar; Type: TABLE DATA; Schema: django; Owner: aris
--

INSERT INTO django.magazin_app_inventar (cantitate, modif, date_modif, produs_id, inventar_id) VALUES (5, 'buy', '2025-10-29 21:15:22.462897+02', 1, 1);
INSERT INTO django.magazin_app_inventar (cantitate, modif, date_modif, produs_id, inventar_id) VALUES (30, 'buy', '2025-10-29 23:10:24.47495+02', 10, 2);


--
-- Name: magazin_app_inventar_inventar_id_seq; Type: SEQUENCE SET; Schema: django; Owner: aris
--

SELECT pg_catalog.setval('django.magazin_app_inventar_inventar_id_seq', 2, true);


--
-- PostgreSQL database dump complete
--


--
-- PostgreSQL database dump
--


-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_app_promotie; Type: TABLE DATA; Schema: django; Owner: aris
--

INSERT INTO django.magazin_app_promotie (name, discount_percentage, start_date, end_date, promotie_id) VALUES ('Pachet An Nou - Detox & Energie', 15.00, '2026-01-01', '2026-01-07', 2);
INSERT INTO django.magazin_app_promotie (name, discount_percentage, start_date, end_date, promotie_id) VALUES ('Black Friday', 25.00, '2025-11-22', '2025-11-30', 1);


--
-- Name: magazin_app_promotie_promotie_id_seq; Type: SEQUENCE SET; Schema: django; Owner: aris
--

SELECT pg_catalog.setval('django.magazin_app_promotie_promotie_id_seq', 2, true);


--
-- PostgreSQL database dump complete
--


--
-- PostgreSQL database dump
--


-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_app_ingredient; Type: TABLE DATA; Schema: django; Owner: aris
--

INSERT INTO django.magazin_app_ingredient (name, benefit, protein_per_100g, country_from, ingredient_id) VALUES ('Vitamina B12', 'Ajuta la cresterea masei musculare', 89.00, 'Olanda', 1);
INSERT INTO django.magazin_app_ingredient (name, benefit, protein_per_100g, country_from, ingredient_id) VALUES ('Lapte', 'Contribuie la creșterea masei musculare și la refacerea rapidă după antrenament', 90.00, 'Romania', 2);


--
-- Name: magazin_app_ingredient_ingredient_id_seq; Type: SEQUENCE SET; Schema: django; Owner: aris
--

SELECT pg_catalog.setval('django.magazin_app_ingredient_ingredient_id_seq', 2, true);


--
-- PostgreSQL database dump complete
--


--
-- PostgreSQL database dump
--


-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_app_organizator; Type: TABLE DATA; Schema: django; Owner: aris
--



--
-- Name: magazin_app_organizator_organizator_id_seq; Type: SEQUENCE SET; Schema: django; Owner: aris
--

SELECT pg_catalog.setval('django.magazin_app_organizator_organizator_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--


--
-- PostgreSQL database dump
--


-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_app_locatie; Type: TABLE DATA; Schema: django; Owner: aris
--



--
-- Name: magazin_app_locatie_locatie_id_seq; Type: SEQUENCE SET; Schema: django; Owner: aris
--

SELECT pg_catalog.setval('django.magazin_app_locatie_locatie_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--


