--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: scissordb_spvj_user
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO scissordb_spvj_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: scissordb_spvj_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO scissordb_spvj_user;

--
-- Name: custom_url; Type: TABLE; Schema: public; Owner: scissordb_spvj_user
--

CREATE TABLE public.custom_url (
    id integer NOT NULL,
    original_url character varying(500) NOT NULL,
    custom_short_url character varying(120) NOT NULL,
    user_id integer NOT NULL,
    date_created timestamp without time zone DEFAULT now(),
    click_count integer
);


ALTER TABLE public.custom_url OWNER TO scissordb_spvj_user;

--
-- Name: custom_url_id_seq; Type: SEQUENCE; Schema: public; Owner: scissordb_spvj_user
--

CREATE SEQUENCE public.custom_url_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.custom_url_id_seq OWNER TO scissordb_spvj_user;

--
-- Name: custom_url_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: scissordb_spvj_user
--

ALTER SEQUENCE public.custom_url_id_seq OWNED BY public.custom_url.id;


--
-- Name: password_history; Type: TABLE; Schema: public; Owner: scissordb_spvj_user
--

CREATE TABLE public.password_history (
    id integer NOT NULL,
    user_id integer NOT NULL,
    password_hash character varying(256) NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now()
);


ALTER TABLE public.password_history OWNER TO scissordb_spvj_user;

--
-- Name: password_history_id_seq; Type: SEQUENCE; Schema: public; Owner: scissordb_spvj_user
--

CREATE SEQUENCE public.password_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.password_history_id_seq OWNER TO scissordb_spvj_user;

--
-- Name: password_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: scissordb_spvj_user
--

ALTER SEQUENCE public.password_history_id_seq OWNED BY public.password_history.id;


--
-- Name: url; Type: TABLE; Schema: public; Owner: scissordb_spvj_user
--

CREATE TABLE public.url (
    id integer NOT NULL,
    original_url character varying(500) NOT NULL,
    short_url character varying(120) NOT NULL,
    user_id integer NOT NULL,
    date_created timestamp without time zone DEFAULT now(),
    click_count integer
);


ALTER TABLE public.url OWNER TO scissordb_spvj_user;

--
-- Name: url_id_seq; Type: SEQUENCE; Schema: public; Owner: scissordb_spvj_user
--

CREATE SEQUENCE public.url_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.url_id_seq OWNER TO scissordb_spvj_user;

--
-- Name: url_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: scissordb_spvj_user
--

ALTER SEQUENCE public.url_id_seq OWNED BY public.url.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: scissordb_spvj_user
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    email character varying(150),
    username character varying(150),
    password character varying(150),
    is_admin boolean
);


ALTER TABLE public."user" OWNER TO scissordb_spvj_user;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: scissordb_spvj_user
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO scissordb_spvj_user;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: scissordb_spvj_user
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: custom_url id; Type: DEFAULT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public.custom_url ALTER COLUMN id SET DEFAULT nextval('public.custom_url_id_seq'::regclass);


--
-- Name: password_history id; Type: DEFAULT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public.password_history ALTER COLUMN id SET DEFAULT nextval('public.password_history_id_seq'::regclass);


--
-- Name: url id; Type: DEFAULT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public.url ALTER COLUMN id SET DEFAULT nextval('public.url_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: scissordb_spvj_user
--

COPY public.alembic_version (version_num) FROM stdin;
4fc674490774
\.


--
-- Data for Name: custom_url; Type: TABLE DATA; Schema: public; Owner: scissordb_spvj_user
--

COPY public.custom_url (id, original_url, custom_short_url, user_id, date_created, click_count) FROM stdin;
4	https://drive.google.com/drive/u/0/mobile/folders/100HZt_cPM8EhFjSlQE3HgRXG_QVAuV-e?usp=sharing&pli=1	www.custom.com/pasfhf	3	2023-06-30 11:50:32.32471	0
11	https://garbageuniversity.io	dwq	7	2023-07-22 22:24:45.330853	0
12	https://garbageuniversity.io	Dwq	1	2023-07-22 22:25:23.203541	0
\.


--
-- Data for Name: password_history; Type: TABLE DATA; Schema: public; Owner: scissordb_spvj_user
--

COPY public.password_history (id, user_id, password_hash, "timestamp") FROM stdin;
1	1	pbkdf2:sha256:260000$bGb0fTPJ0awtZsV3$29b5d2cc6ef7745de2105c03f5228bd442fd17714c50ca52abec5648eb6e5033	2023-06-29 21:12:29.085378
2	1	pbkdf2:sha256:260000$Bs3LnQwZ1wQNT0Zp$ebc0bbd497ca7385be88b9286dad34b9a0e9e2712a58a6c6ddbfd166f4deb939	2023-06-30 10:28:57.005119
3	1	pbkdf2:sha256:260000$eRy25p8u7QtG6zNd$e17c8056c2ce89c0c1e5205e7d351770eb019eb85f8deeb51d6ceb0a50283bbd	2023-07-20 11:53:54.146765
4	1	pbkdf2:sha256:260000$G4XTWjyVE1errwZ7$770b4b4309a6310167ff60b1f4598a036f33774feef3c09f173b79b0f851006d	2023-07-20 12:02:44.463366
\.


--
-- Data for Name: url; Type: TABLE DATA; Schema: public; Owner: scissordb_spvj_user
--

COPY public.url (id, original_url, short_url, user_id, date_created, click_count) FROM stdin;
6	https://marketingexamples.com/	kWKDmB	4	2023-06-30 15:07:50.406587	0
14	https://garbageuniversity.io	3lxWXT	1	2023-07-22 22:25:02.202439	0
12	https://twitter.com	moxbSH	7	2023-07-22 21:50:46.043282	1
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: scissordb_spvj_user
--

COPY public."user" (id, email, username, password, is_admin) FROM stdin;
2	predovicalexandria138@gmail.com	katrin81	pbkdf2:sha256:260000$awiPIoXscefOy8N3$5667b4275c826d6f3b63cad3c222f6c986cb7187aa3488fcc2b6893ac64b000b	\N
3	priscilla@gmail.com	priscilla	pbkdf2:sha256:260000$s6RrpkfLa9yV9hw5$9500efeab301c5dcde5ed4c80125c31d4916c6d9af2c772d95e797d777e075d9	\N
4	veektaw@gmail.com	veektaw	pbkdf2:sha256:260000$vzf1JxZ3ueHJc5CB$94aafa0a156427712b4c94e1182543051120592cf6d3600e473c02604233581a	\N
5	mathilde.roussel89@gmxxail.com	mathilde.roussel89@gmxxail.com	pbkdf2:sha256:260000$Wn6MwyDquhC2GDDc$e47dfbb7fe8c67babd978e391136f6e6af1a9810ad622111971183431675ec90	\N
6	jayne.harris20@webmai.co	jayne.harris20@webmai.co	pbkdf2:sha256:260000$gwukgydAzL8BO9Wn$a260b1f29ca45428743df469167b321cc22d7e88cafdb65bddbac40fde59deb3	\N
1	emmypresh777@gmail.com	iamprecieee	pbkdf2:sha256:260000$G4XTWjyVE1errwZ7$770b4b4309a6310167ff60b1f4598a036f33774feef3c09f173b79b0f851006d	\N
7	goldenjaguar747@gmail.com	iamprecieee2	pbkdf2:sha256:260000$SpqryDvN3ruHKh2k$0f6f90103c08df4831cb146c1662f6e24c7ac614083c97a60daa4a550d9de07f	\N
8	scssr.tech@gmail.com	iamprecieee747	prec1ou57475	t
\.


--
-- Name: custom_url_id_seq; Type: SEQUENCE SET; Schema: public; Owner: scissordb_spvj_user
--

SELECT pg_catalog.setval('public.custom_url_id_seq', 15, true);


--
-- Name: password_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: scissordb_spvj_user
--

SELECT pg_catalog.setval('public.password_history_id_seq', 4, true);


--
-- Name: url_id_seq; Type: SEQUENCE SET; Schema: public; Owner: scissordb_spvj_user
--

SELECT pg_catalog.setval('public.url_id_seq', 14, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: scissordb_spvj_user
--

SELECT pg_catalog.setval('public.user_id_seq', 8, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: custom_url custom_url_custom_short_url_key; Type: CONSTRAINT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public.custom_url
    ADD CONSTRAINT custom_url_custom_short_url_key UNIQUE (custom_short_url);


--
-- Name: custom_url custom_url_pkey; Type: CONSTRAINT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public.custom_url
    ADD CONSTRAINT custom_url_pkey PRIMARY KEY (id);


--
-- Name: password_history password_history_pkey; Type: CONSTRAINT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public.password_history
    ADD CONSTRAINT password_history_pkey PRIMARY KEY (id);


--
-- Name: url url_pkey; Type: CONSTRAINT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public.url
    ADD CONSTRAINT url_pkey PRIMARY KEY (id);


--
-- Name: url url_short_url_key; Type: CONSTRAINT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public.url
    ADD CONSTRAINT url_short_url_key UNIQUE (short_url);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: custom_url custom_url_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public.custom_url
    ADD CONSTRAINT custom_url_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: password_history password_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public.password_history
    ADD CONSTRAINT password_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: url url_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: scissordb_spvj_user
--

ALTER TABLE ONLY public.url
    ADD CONSTRAINT url_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON SEQUENCES  TO scissordb_spvj_user;


--
-- Name: DEFAULT PRIVILEGES FOR TYPES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TYPES  TO scissordb_spvj_user;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON FUNCTIONS  TO scissordb_spvj_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES  TO scissordb_spvj_user;


--
-- PostgreSQL database dump complete
--

