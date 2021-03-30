--
-- PostgreSQL database dump
--

-- Dumped from database version 13.0
-- Dumped by pg_dump version 13.0

-- Started on 2020-10-08 10:31:24

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 200 (class 1259 OID 16437)
-- Name: fingerprints; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fingerprints (
                                     id integer NOT NULL,
                                     hashe character varying,
                                     id_music integer
);


ALTER TABLE public.fingerprints OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 16443)
-- Name: music; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.music (
                              id integer NOT NULL,
                              titre character varying,
                              idvideo character varying

);


ALTER TABLE public.music OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 16449)
-- Name: music_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.music_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.music_id_seq OWNER TO postgres;

--
-- TOC entry 2995 (class 0 OID 0)
-- Dependencies: 202
-- Name: music_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.music_id_seq OWNED BY public.music.id;


--
-- TOC entry 2856 (class 2604 OID 16454)
-- Name: music id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.music ALTER COLUMN id SET DEFAULT nextval('public.music_id_seq'::regclass);


--
-- TOC entry 2858 (class 2606 OID 16456)
-- Name: music music_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.music
    ADD CONSTRAINT music_pk PRIMARY KEY (id);


--
-- TOC entry 2859 (class 2606 OID 16457)
-- Name: fingerprints fingerprints_music_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fingerprints
    ADD CONSTRAINT fingerprints_music_id_fk FOREIGN KEY (id_music) REFERENCES public.music(id);


ALTER TABLE ONLY public.fingerprints
    ADD CONSTRAINT fingerprints_pk PRIMARY KEY (id);

-- Completed on 2020-10-08 10:31:25

--
-- PostgreSQL database dump complete
--

CREATE INDEX hashe_index ON public.fingerprints (hashe);

-- Table: public.buffer

-- DROP TABLE public.buffer;

CREATE TABLE public.buffer
(
    hashe character varying COLLATE pg_catalog."default",
    id_user integer
)

    TABLESPACE pg_default;

ALTER TABLE public.buffer
    OWNER to postgres;
-- Index: buffer_hashe_hashe1_idx

-- DROP INDEX public.buffer_hashe_hashe1_idx;

CREATE INDEX buffer_hashe_hashe1_idx
    ON public.buffer USING btree
    (hashe COLLATE pg_catalog."default" ASC NULLS LAST)
    INCLUDE(hashe)
    TABLESPACE pg_default;