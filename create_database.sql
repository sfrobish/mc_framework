--
-- PostgreSQL database dump
--

-- Dumped from database version 11.5 (Ubuntu 11.5-3.pgdg18.04+1)
-- Dumped by pg_dump version 11.5 (Ubuntu 11.5-3.pgdg18.04+1)

-- Started on 2019-10-24 10:20:51 CDT

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
-- TOC entry 7 (class 2615 OID 16489)
-- Name: mc_demo; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA mc_demo;


ALTER SCHEMA mc_demo OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 204 (class 1259 OID 16547)
-- Name: classification; Type: TABLE; Schema: mc_demo; Owner: postgres
--

CREATE TABLE mc_demo.classification (
    classification_id integer NOT NULL,
    classification_version integer NOT NULL,
    domain_id integer,
    source_id integer,
    usage_id integer,
    geo_id integer,
    rights_id integer,
    data_element_class_id integer,
    controls_recipe_id integer NOT NULL,
    classification_label character varying(60) NOT NULL,
    create_tstmp timestamp without time zone NOT NULL
);


ALTER TABLE mc_demo.classification OWNER TO postgres;

--
-- TOC entry 199 (class 1259 OID 16517)
-- Name: control; Type: TABLE; Schema: mc_demo; Owner: postgres
--

CREATE TABLE mc_demo.control (
    control_id integer NOT NULL,
    control_name character varying(60) NOT NULL,
    control_description character varying(1000)
);


ALTER TABLE mc_demo.control OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 16515)
-- Name: control2_control_id_seq; Type: SEQUENCE; Schema: mc_demo; Owner: postgres
--

CREATE SEQUENCE mc_demo.control2_control_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mc_demo.control2_control_id_seq OWNER TO postgres;

--
-- TOC entry 3030 (class 0 OID 0)
-- Dependencies: 198
-- Name: control2_control_id_seq; Type: SEQUENCE OWNED BY; Schema: mc_demo; Owner: postgres
--

ALTER SEQUENCE mc_demo.control2_control_id_seq OWNED BY mc_demo.control.control_id;


--
-- TOC entry 203 (class 1259 OID 16539)
-- Name: control_recipe; Type: TABLE; Schema: mc_demo; Owner: postgres
--

CREATE TABLE mc_demo.control_recipe (
    control_recipe_id integer NOT NULL,
    control_id integer NOT NULL,
    recipe_id integer NOT NULL
);


ALTER TABLE mc_demo.control_recipe OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 16537)
-- Name: control_recipe_control_recipe_id_seq; Type: SEQUENCE; Schema: mc_demo; Owner: postgres
--

CREATE SEQUENCE mc_demo.control_recipe_control_recipe_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mc_demo.control_recipe_control_recipe_id_seq OWNER TO postgres;

--
-- TOC entry 3031 (class 0 OID 0)
-- Dependencies: 202
-- Name: control_recipe_control_recipe_id_seq; Type: SEQUENCE OWNED BY; Schema: mc_demo; Owner: postgres
--

ALTER SEQUENCE mc_demo.control_recipe_control_recipe_id_seq OWNED BY mc_demo.control_recipe.control_recipe_id;


--
-- TOC entry 208 (class 1259 OID 16565)
-- Name: domain_dim; Type: TABLE; Schema: mc_demo; Owner: postgres
--

CREATE TABLE mc_demo.domain_dim (
    domain_id integer NOT NULL,
    domain_name character varying(60) NOT NULL,
    domain_descr character varying(1000),
    parent_domain_id integer,
    similarity_score smallint NOT NULL
);


ALTER TABLE mc_demo.domain_dim OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 16563)
-- Name: domain_dim_domain_id_seq; Type: SEQUENCE; Schema: mc_demo; Owner: postgres
--

CREATE SEQUENCE mc_demo.domain_dim_domain_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mc_demo.domain_dim_domain_id_seq OWNER TO postgres;

--
-- TOC entry 3032 (class 0 OID 0)
-- Dependencies: 207
-- Name: domain_dim_domain_id_seq; Type: SEQUENCE OWNED BY; Schema: mc_demo; Owner: postgres
--

ALTER SEQUENCE mc_demo.domain_dim_domain_id_seq OWNED BY mc_demo.domain_dim.domain_id;


--
-- TOC entry 218 (class 1259 OID 16621)
-- Name: field_class_rules; Type: TABLE; Schema: mc_demo; Owner: postgres
--

CREATE TABLE mc_demo.field_class_rules (
    fcr_id bigint NOT NULL,
    fcr_name character varying(60) NOT NULL,
    fcr_descr character varying(1000),
    seq integer NOT NULL,
    expr character varying(1000) NOT NULL
);


ALTER TABLE mc_demo.field_class_rules OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16619)
-- Name: field_classification_rules_fcr_id_seq; Type: SEQUENCE; Schema: mc_demo; Owner: postgres
--

CREATE SEQUENCE mc_demo.field_classification_rules_fcr_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mc_demo.field_classification_rules_fcr_id_seq OWNER TO postgres;

--
-- TOC entry 3033 (class 0 OID 0)
-- Dependencies: 217
-- Name: field_classification_rules_fcr_id_seq; Type: SEQUENCE OWNED BY; Schema: mc_demo; Owner: postgres
--

ALTER SEQUENCE mc_demo.field_classification_rules_fcr_id_seq OWNED BY mc_demo.field_class_rules.fcr_id;


--
-- TOC entry 210 (class 1259 OID 16576)
-- Name: geo_dim; Type: TABLE; Schema: mc_demo; Owner: postgres
--

CREATE TABLE mc_demo.geo_dim (
    geo_id integer NOT NULL,
    geo_name character varying(60) NOT NULL,
    geo_descr character varying(1000),
    parent_geo_id integer,
    similarity_score smallint NOT NULL
);


ALTER TABLE mc_demo.geo_dim OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16574)
-- Name: geo_dim_geo_id_seq; Type: SEQUENCE; Schema: mc_demo; Owner: postgres
--

CREATE SEQUENCE mc_demo.geo_dim_geo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mc_demo.geo_dim_geo_id_seq OWNER TO postgres;

--
-- TOC entry 3034 (class 0 OID 0)
-- Dependencies: 209
-- Name: geo_dim_geo_id_seq; Type: SEQUENCE OWNED BY; Schema: mc_demo; Owner: postgres
--

ALTER SEQUENCE mc_demo.geo_dim_geo_id_seq OWNED BY mc_demo.geo_dim.geo_id;


--
-- TOC entry 201 (class 1259 OID 16528)
-- Name: recipe; Type: TABLE; Schema: mc_demo; Owner: postgres
--

CREATE TABLE mc_demo.recipe (
    recipe_id integer NOT NULL,
    recipe_name character varying NOT NULL,
    recipe_description character varying
);


ALTER TABLE mc_demo.recipe OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 16526)
-- Name: recipe_recipe_id_seq; Type: SEQUENCE; Schema: mc_demo; Owner: postgres
--

CREATE SEQUENCE mc_demo.recipe_recipe_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mc_demo.recipe_recipe_id_seq OWNER TO postgres;

--
-- TOC entry 3035 (class 0 OID 0)
-- Dependencies: 200
-- Name: recipe_recipe_id_seq; Type: SEQUENCE OWNED BY; Schema: mc_demo; Owner: postgres
--

ALTER SEQUENCE mc_demo.recipe_recipe_id_seq OWNED BY mc_demo.recipe.recipe_id;


--
-- TOC entry 214 (class 1259 OID 16599)
-- Name: rights_dim; Type: TABLE; Schema: mc_demo; Owner: postgres
--

CREATE TABLE mc_demo.rights_dim (
    rights_id integer NOT NULL,
    rights_name character varying(60) NOT NULL,
    rights_descr character varying(1000),
    parent_rights_id integer,
    similarity_score smallint NOT NULL
);


ALTER TABLE mc_demo.rights_dim OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 16597)
-- Name: rights_dim_rights_id_seq; Type: SEQUENCE; Schema: mc_demo; Owner: postgres
--

CREATE SEQUENCE mc_demo.rights_dim_rights_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mc_demo.rights_dim_rights_id_seq OWNER TO postgres;

--
-- TOC entry 3036 (class 0 OID 0)
-- Dependencies: 213
-- Name: rights_dim_rights_id_seq; Type: SEQUENCE OWNED BY; Schema: mc_demo; Owner: postgres
--

ALTER SEQUENCE mc_demo.rights_dim_rights_id_seq OWNED BY mc_demo.rights_dim.rights_id;


--
-- TOC entry 216 (class 1259 OID 16610)
-- Name: sensitive_data_fields; Type: TABLE; Schema: mc_demo; Owner: postgres
--

CREATE TABLE mc_demo.sensitive_data_fields (
    sdf_id integer NOT NULL,
    sdf_name character varying(60) NOT NULL,
    sdf_descr character varying(1000),
    sdf_regex character varying(1000)
);


ALTER TABLE mc_demo.sensitive_data_fields OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16608)
-- Name: sensitive_data_fields_sdf_id_seq; Type: SEQUENCE; Schema: mc_demo; Owner: postgres
--

CREATE SEQUENCE mc_demo.sensitive_data_fields_sdf_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mc_demo.sensitive_data_fields_sdf_id_seq OWNER TO postgres;

--
-- TOC entry 3037 (class 0 OID 0)
-- Dependencies: 215
-- Name: sensitive_data_fields_sdf_id_seq; Type: SEQUENCE OWNED BY; Schema: mc_demo; Owner: postgres
--

ALTER SEQUENCE mc_demo.sensitive_data_fields_sdf_id_seq OWNED BY mc_demo.sensitive_data_fields.sdf_id;


--
-- TOC entry 206 (class 1259 OID 16554)
-- Name: source_dim; Type: TABLE; Schema: mc_demo; Owner: postgres
--

CREATE TABLE mc_demo.source_dim (
    source_id integer NOT NULL,
    source_name character varying(60) NOT NULL,
    source_descr character varying(1000),
    parent_source_id integer,
    similarity_score smallint NOT NULL
);


ALTER TABLE mc_demo.source_dim OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 16552)
-- Name: source_dim_source_id_seq; Type: SEQUENCE; Schema: mc_demo; Owner: postgres
--

CREATE SEQUENCE mc_demo.source_dim_source_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mc_demo.source_dim_source_id_seq OWNER TO postgres;

--
-- TOC entry 3038 (class 0 OID 0)
-- Dependencies: 205
-- Name: source_dim_source_id_seq; Type: SEQUENCE OWNED BY; Schema: mc_demo; Owner: postgres
--

ALTER SEQUENCE mc_demo.source_dim_source_id_seq OWNED BY mc_demo.source_dim.source_id;


--
-- TOC entry 212 (class 1259 OID 16587)
-- Name: usage; Type: TABLE; Schema: mc_demo; Owner: postgres
--

CREATE TABLE mc_demo.usage (
    usage_id bigint NOT NULL,
    usage_name character varying(60) NOT NULL,
    usage_descr character varying(1000),
    parent_usage_id integer,
    similarity_score smallint NOT NULL
);


ALTER TABLE mc_demo.usage OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 16585)
-- Name: usage_usage_id_seq; Type: SEQUENCE; Schema: mc_demo; Owner: postgres
--

CREATE SEQUENCE mc_demo.usage_usage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mc_demo.usage_usage_id_seq OWNER TO postgres;

--
-- TOC entry 3039 (class 0 OID 0)
-- Dependencies: 211
-- Name: usage_usage_id_seq; Type: SEQUENCE OWNED BY; Schema: mc_demo; Owner: postgres
--

ALTER SEQUENCE mc_demo.usage_usage_id_seq OWNED BY mc_demo.usage.usage_id;


--
-- TOC entry 2870 (class 2604 OID 16520)
-- Name: control control_id; Type: DEFAULT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.control ALTER COLUMN control_id SET DEFAULT nextval('mc_demo.control2_control_id_seq'::regclass);


--
-- TOC entry 2872 (class 2604 OID 16542)
-- Name: control_recipe control_recipe_id; Type: DEFAULT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.control_recipe ALTER COLUMN control_recipe_id SET DEFAULT nextval('mc_demo.control_recipe_control_recipe_id_seq'::regclass);


--
-- TOC entry 2874 (class 2604 OID 16568)
-- Name: domain_dim domain_id; Type: DEFAULT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.domain_dim ALTER COLUMN domain_id SET DEFAULT nextval('mc_demo.domain_dim_domain_id_seq'::regclass);


--
-- TOC entry 2879 (class 2604 OID 16624)
-- Name: field_class_rules fcr_id; Type: DEFAULT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.field_class_rules ALTER COLUMN fcr_id SET DEFAULT nextval('mc_demo.field_classification_rules_fcr_id_seq'::regclass);


--
-- TOC entry 2875 (class 2604 OID 16579)
-- Name: geo_dim geo_id; Type: DEFAULT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.geo_dim ALTER COLUMN geo_id SET DEFAULT nextval('mc_demo.geo_dim_geo_id_seq'::regclass);


--
-- TOC entry 2871 (class 2604 OID 16531)
-- Name: recipe recipe_id; Type: DEFAULT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.recipe ALTER COLUMN recipe_id SET DEFAULT nextval('mc_demo.recipe_recipe_id_seq'::regclass);


--
-- TOC entry 2877 (class 2604 OID 16602)
-- Name: rights_dim rights_id; Type: DEFAULT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.rights_dim ALTER COLUMN rights_id SET DEFAULT nextval('mc_demo.rights_dim_rights_id_seq'::regclass);


--
-- TOC entry 2878 (class 2604 OID 16613)
-- Name: sensitive_data_fields sdf_id; Type: DEFAULT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.sensitive_data_fields ALTER COLUMN sdf_id SET DEFAULT nextval('mc_demo.sensitive_data_fields_sdf_id_seq'::regclass);


--
-- TOC entry 2873 (class 2604 OID 16557)
-- Name: source_dim source_id; Type: DEFAULT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.source_dim ALTER COLUMN source_id SET DEFAULT nextval('mc_demo.source_dim_source_id_seq'::regclass);


--
-- TOC entry 2876 (class 2604 OID 16590)
-- Name: usage usage_id; Type: DEFAULT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.usage ALTER COLUMN usage_id SET DEFAULT nextval('mc_demo.usage_usage_id_seq'::regclass);


--
-- TOC entry 2889 (class 2606 OID 16551)
-- Name: classification classification_pkey; Type: CONSTRAINT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.classification
    ADD CONSTRAINT classification_pkey PRIMARY KEY (classification_id, classification_version);


--
-- TOC entry 2881 (class 2606 OID 16525)
-- Name: control control2_pkey; Type: CONSTRAINT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.control
    ADD CONSTRAINT control2_pkey PRIMARY KEY (control_id);


--
-- TOC entry 2885 (class 2606 OID 16546)
-- Name: control_recipe control_id_recipe_id_unique; Type: CONSTRAINT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.control_recipe
    ADD CONSTRAINT control_id_recipe_id_unique UNIQUE (control_id, recipe_id);


--
-- TOC entry 2887 (class 2606 OID 16544)
-- Name: control_recipe control_recipe_pkey; Type: CONSTRAINT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.control_recipe
    ADD CONSTRAINT control_recipe_pkey PRIMARY KEY (control_recipe_id);


--
-- TOC entry 2893 (class 2606 OID 16573)
-- Name: domain_dim domain_dim_pkey; Type: CONSTRAINT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.domain_dim
    ADD CONSTRAINT domain_dim_pkey PRIMARY KEY (domain_id);


--
-- TOC entry 2903 (class 2606 OID 16629)
-- Name: field_class_rules field_classification_rules_pkey; Type: CONSTRAINT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.field_class_rules
    ADD CONSTRAINT field_classification_rules_pkey PRIMARY KEY (fcr_id);


--
-- TOC entry 2895 (class 2606 OID 16584)
-- Name: geo_dim geo_dim_pkey; Type: CONSTRAINT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.geo_dim
    ADD CONSTRAINT geo_dim_pkey PRIMARY KEY (geo_id);


--
-- TOC entry 2883 (class 2606 OID 16536)
-- Name: recipe recipe_pkey; Type: CONSTRAINT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.recipe
    ADD CONSTRAINT recipe_pkey PRIMARY KEY (recipe_id);


--
-- TOC entry 2899 (class 2606 OID 16607)
-- Name: rights_dim rights_dim_pkey; Type: CONSTRAINT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.rights_dim
    ADD CONSTRAINT rights_dim_pkey PRIMARY KEY (rights_id);


--
-- TOC entry 2901 (class 2606 OID 16618)
-- Name: sensitive_data_fields sensitive_data_fields_pkey; Type: CONSTRAINT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.sensitive_data_fields
    ADD CONSTRAINT sensitive_data_fields_pkey PRIMARY KEY (sdf_id);


--
-- TOC entry 2891 (class 2606 OID 16562)
-- Name: source_dim source_dim_pkey; Type: CONSTRAINT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.source_dim
    ADD CONSTRAINT source_dim_pkey PRIMARY KEY (source_id);


--
-- TOC entry 2897 (class 2606 OID 16595)
-- Name: usage usage_pkey; Type: CONSTRAINT; Schema: mc_demo; Owner: postgres
--

ALTER TABLE ONLY mc_demo.usage
    ADD CONSTRAINT usage_pkey PRIMARY KEY (usage_id);


-- Completed on 2019-10-24 10:20:51 CDT

--
-- PostgreSQL database dump complete
--
