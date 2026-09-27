--
-- PostgreSQL database dump
--

\restrict WEacGtuzfJTDTBRhJVzRar1YgEnW2Rns9UBJ8rbHDpQSnx8SrnulkipmGfDSVhs

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

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
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: estado_asignacion; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.estado_asignacion AS ENUM (
    'ACTIVA',
    'FINALIZADA',
    'CANCELADA'
);


ALTER TYPE public.estado_asignacion OWNER TO postgres;

--
-- Name: intensidad; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.intensidad AS ENUM (
    'BAJA',
    'MEDIA',
    'ALTA'
);


ALTER TYPE public.intensidad OWNER TO postgres;

--
-- Name: nivel_rutina; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.nivel_rutina AS ENUM (
    'BASICO',
    'INTERMEDIO',
    'AVANZADO'
);


ALTER TYPE public.nivel_rutina OWNER TO postgres;

--
-- Name: tipo_usuario; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tipo_usuario AS ENUM (
    'cliente',
    'administrador'
);


ALTER TYPE public.tipo_usuario OWNER TO postgres;

--
-- Name: sincronizar_hash_contrasena(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sincronizar_hash_contrasena() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.sincronizar_hash_contrasena() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: asignacion_rutina_ejercicios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.asignacion_rutina_ejercicios (
    id_asignacion_ejercicio integer NOT NULL,
    id_asignacion integer NOT NULL,
    id_ejercicio integer NOT NULL,
    orden_ejercicio integer NOT NULL,
    veces_planificadas integer DEFAULT 1 NOT NULL,
    activo boolean DEFAULT true NOT NULL,
    fecha_agregado date DEFAULT CURRENT_DATE NOT NULL,
    CONSTRAINT chk_asignacion_ejercicio_orden CHECK ((orden_ejercicio > 0)),
    CONSTRAINT chk_asignacion_ejercicio_veces CHECK ((veces_planificadas > 0))
);


ALTER TABLE public.asignacion_rutina_ejercicios OWNER TO postgres;

--
-- Name: asignacion_rutina_ejercicios_id_asignacion_ejercicio_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.asignacion_rutina_ejercicios_id_asignacion_ejercicio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.asignacion_rutina_ejercicios_id_asignacion_ejercicio_seq OWNER TO postgres;

--
-- Name: asignacion_rutina_ejercicios_id_asignacion_ejercicio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.asignacion_rutina_ejercicios_id_asignacion_ejercicio_seq OWNED BY public.asignacion_rutina_ejercicios.id_asignacion_ejercicio;


--
-- Name: asignaciones_rutina; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.asignaciones_rutina (
    id_asignacion integer NOT NULL,
    id_cliente integer NOT NULL,
    id_rutina integer NOT NULL,
    fecha_asignacion date DEFAULT CURRENT_DATE NOT NULL,
    fecha_finalizacion date,
    estado public.estado_asignacion DEFAULT 'ACTIVA'::public.estado_asignacion NOT NULL,
    observaciones text,
    CONSTRAINT chk_fechas CHECK (((fecha_finalizacion IS NULL) OR (fecha_finalizacion >= fecha_asignacion)))
);


ALTER TABLE public.asignaciones_rutina OWNER TO postgres;

--
-- Name: TABLE asignaciones_rutina; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.asignaciones_rutina IS 'Historial de asignaciones (Clase AsignacionRutina)';


--
-- Name: CONSTRAINT chk_fechas ON asignaciones_rutina; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON CONSTRAINT chk_fechas ON public.asignaciones_rutina IS 'La fecha de finalización debe ser posterior a la asignación';


--
-- Name: asignaciones_rutina_id_asignacion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.asignaciones_rutina_id_asignacion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.asignaciones_rutina_id_asignacion_seq OWNER TO postgres;

--
-- Name: asignaciones_rutina_id_asignacion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.asignaciones_rutina_id_asignacion_seq OWNED BY public.asignaciones_rutina.id_asignacion;


--
-- Name: clientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clientes (
    id_usuario integer NOT NULL,
    peso numeric(5,2) NOT NULL,
    altura numeric(5,2) NOT NULL,
    objetivo character varying(255) NOT NULL,
    fecha_ingreso date DEFAULT CURRENT_DATE NOT NULL,
    peso_objetivo numeric(6,2),
    genero character varying(30),
    CONSTRAINT clientes_altura_check CHECK ((altura > (0)::numeric)),
    CONSTRAINT clientes_peso_check CHECK ((peso > (0)::numeric))
);


ALTER TABLE public.clientes OWNER TO postgres;

--
-- Name: TABLE clientes; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.clientes IS 'Especialización de Usuario: Cliente (hereda de Usuario)';


--
-- Name: COLUMN clientes.objetivo; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.clientes.objetivo IS 'Ej: Bajar de peso, Mejorar resistencia, Mantener condición';


--
-- Name: ejercicios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ejercicios (
    id_ejercicio integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    tipo character varying(50) NOT NULL,
    duracion_minutos integer NOT NULL,
    intensidad public.intensidad NOT NULL,
    calorias_estimadas numeric(6,2) NOT NULL,
    creado_por integer,
    CONSTRAINT ejercicios_calorias_estimadas_check CHECK ((calorias_estimadas >= (0)::numeric)),
    CONSTRAINT ejercicios_duracion_minutos_check CHECK ((duracion_minutos > 0))
);


ALTER TABLE public.ejercicios OWNER TO postgres;

--
-- Name: TABLE ejercicios; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.ejercicios IS 'Catálogo de ejercicios (Clase EjercicioCardio)';


--
-- Name: COLUMN ejercicios.creado_por; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ejercicios.creado_por IS 'Administrador que creó el ejercicio (asociación)';


--
-- Name: ejercicios_id_ejercicio_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ejercicios_id_ejercicio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ejercicios_id_ejercicio_seq OWNER TO postgres;

--
-- Name: ejercicios_id_ejercicio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ejercicios_id_ejercicio_seq OWNED BY public.ejercicios.id_ejercicio;


--
-- Name: progreso_mensual; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.progreso_mensual (
    id_progreso integer NOT NULL,
    id_cliente integer NOT NULL,
    mes date NOT NULL,
    peso numeric(5,2) NOT NULL,
    sesiones_completadas integer DEFAULT 0 NOT NULL,
    sesiones_planificadas integer DEFAULT 0 NOT NULL,
    porcentaje_cumplimiento numeric(5,2) DEFAULT 0.0 NOT NULL,
    CONSTRAINT progreso_mensual_peso_check CHECK ((peso > (0)::numeric)),
    CONSTRAINT progreso_mensual_porcentaje_cumplimiento_check CHECK (((porcentaje_cumplimiento >= (0)::numeric) AND (porcentaje_cumplimiento <= (100)::numeric))),
    CONSTRAINT progreso_mensual_sesiones_completadas_check CHECK ((sesiones_completadas >= 0)),
    CONSTRAINT progreso_mensual_sesiones_planificadas_check CHECK ((sesiones_planificadas >= 0))
);


ALTER TABLE public.progreso_mensual OWNER TO postgres;

--
-- Name: TABLE progreso_mensual; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.progreso_mensual IS 'Resumen mensual de progreso (Clase ProgresoMensual)';


--
-- Name: COLUMN progreso_mensual.mes; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.progreso_mensual.mes IS 'Primer día del mes (ej. 2026-08-01)';


--
-- Name: progreso_mensual_id_progreso_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.progreso_mensual_id_progreso_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.progreso_mensual_id_progreso_seq OWNER TO postgres;

--
-- Name: progreso_mensual_id_progreso_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.progreso_mensual_id_progreso_seq OWNED BY public.progreso_mensual.id_progreso;


--
-- Name: rutina_ejercicios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rutina_ejercicios (
    id_rutina integer NOT NULL,
    id_ejercicio integer NOT NULL,
    orden_ejercicio integer NOT NULL,
    CONSTRAINT rutina_ejercicios_orden_ejercicio_check CHECK ((orden_ejercicio > 0))
);


ALTER TABLE public.rutina_ejercicios OWNER TO postgres;

--
-- Name: TABLE rutina_ejercicios; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.rutina_ejercicios IS 'Relación N:M: una rutina contiene varios ejercicios (agregación)';


--
-- Name: rutinas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rutinas (
    id_rutina integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    objetivo character varying(255) NOT NULL,
    nivel public.nivel_rutina NOT NULL,
    duracion_semanas integer NOT NULL,
    creado_por integer,
    fecha_creacion date DEFAULT CURRENT_DATE NOT NULL,
    CONSTRAINT rutinas_duracion_semanas_check CHECK ((duracion_semanas > 0))
);


ALTER TABLE public.rutinas OWNER TO postgres;

--
-- Name: TABLE rutinas; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.rutinas IS 'Planes de entrenamiento (Clase Rutina)';


--
-- Name: COLUMN rutinas.creado_por; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.rutinas.creado_por IS 'Administrador que gestiona/crea la rutina (asociación)';


--
-- Name: rutinas_id_rutina_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rutinas_id_rutina_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rutinas_id_rutina_seq OWNER TO postgres;

--
-- Name: rutinas_id_rutina_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rutinas_id_rutina_seq OWNED BY public.rutinas.id_rutina;


--
-- Name: sesiones_entrenamiento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sesiones_entrenamiento (
    id_sesion integer NOT NULL,
    id_cliente integer NOT NULL,
    fecha date DEFAULT CURRENT_DATE NOT NULL,
    duracion_real integer NOT NULL,
    intensidad_real public.intensidad NOT NULL,
    calorias_quemadas numeric(10,2) NOT NULL,
    observaciones text,
    completada boolean DEFAULT false NOT NULL,
    id_rutina integer,
    nombre_ejercicio character varying(100) DEFAULT ''::character varying,
    veces_planificadas integer DEFAULT 1 NOT NULL,
    veces_realizadas integer DEFAULT 0 NOT NULL,
    id_asignacion integer,
    id_asignacion_ejercicio integer,
    CONSTRAINT sesiones_entrenamiento_calorias_quemadas_check CHECK ((calorias_quemadas >= (0)::numeric)),
    CONSTRAINT sesiones_entrenamiento_duracion_real_check CHECK ((duracion_real > 0)),
    CONSTRAINT sesiones_veces_planificadas_check CHECK ((veces_planificadas > 0)),
    CONSTRAINT sesiones_veces_realizadas_check CHECK ((veces_realizadas >= 0)),
    CONSTRAINT sesiones_veces_realizadas_max_check CHECK ((veces_realizadas <= veces_planificadas))
);


ALTER TABLE public.sesiones_entrenamiento OWNER TO postgres;

--
-- Name: TABLE sesiones_entrenamiento; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.sesiones_entrenamiento IS 'Registro de entrenamientos (Clase SesionEntrenamiento)';


--
-- Name: sesiones_entrenamiento_id_sesion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sesiones_entrenamiento_id_sesion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sesiones_entrenamiento_id_sesion_seq OWNER TO postgres;

--
-- Name: sesiones_entrenamiento_id_sesion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sesiones_entrenamiento_id_sesion_seq OWNED BY public.sesiones_entrenamiento.id_sesion;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id_usuario integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido character varying(100) NOT NULL,
    correo_electronico character varying(150) NOT NULL,
    contrasenia_hash character varying(255) CONSTRAINT "usuarios_contraseña_hash_not_null" NOT NULL,
    edad integer NOT NULL,
    tipo_usuario public.tipo_usuario DEFAULT 'cliente'::public.tipo_usuario NOT NULL,
    fecha_registro date DEFAULT CURRENT_DATE NOT NULL,
    "contraseña_hash" character varying(255),
    CONSTRAINT usuarios_edad_check CHECK ((edad > 0))
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: TABLE usuarios; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.usuarios IS 'Base de la herencia: Usuario (abstracta en Python)';


--
-- Name: COLUMN usuarios.contrasenia_hash; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.usuarios.contrasenia_hash IS 'Almacena el hash de la contraseña, no el texto plano';


--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_usuario_seq OWNER TO postgres;

--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_usuario_seq OWNED BY public.usuarios.id_usuario;


--
-- Name: vw_clientes_completo; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vw_clientes_completo AS
 SELECT u.id_usuario,
    u.nombre,
    u.apellido,
    u.correo_electronico,
    u.edad,
    u.fecha_registro,
    c.peso,
    c.altura,
    c.objetivo,
    c.fecha_ingreso
   FROM (public.usuarios u
     JOIN public.clientes c ON ((u.id_usuario = c.id_usuario)))
  WHERE (u.tipo_usuario = 'cliente'::public.tipo_usuario);


ALTER VIEW public.vw_clientes_completo OWNER TO postgres;

--
-- Name: VIEW vw_clientes_completo; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW public.vw_clientes_completo IS 'Vista para obtener todos los datos de un cliente en una sola consulta';


--
-- Name: vw_rutina_activa_cliente; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vw_rutina_activa_cliente AS
 SELECT a.id_cliente,
    a.id_asignacion,
    r.id_rutina,
    r.nombre AS nombre_rutina,
    r.objetivo,
    r.nivel,
    r.duracion_semanas,
    a.fecha_asignacion,
    a.fecha_finalizacion,
    a.observaciones
   FROM (public.asignaciones_rutina a
     JOIN public.rutinas r ON ((a.id_rutina = r.id_rutina)))
  WHERE (a.estado = 'ACTIVA'::public.estado_asignacion);


ALTER VIEW public.vw_rutina_activa_cliente OWNER TO postgres;

--
-- Name: VIEW vw_rutina_activa_cliente; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW public.vw_rutina_activa_cliente IS 'Vista para obtener la rutina activa de un cliente (filtro por id_cliente)';


--
-- Name: asignacion_rutina_ejercicios id_asignacion_ejercicio; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignacion_rutina_ejercicios ALTER COLUMN id_asignacion_ejercicio SET DEFAULT nextval('public.asignacion_rutina_ejercicios_id_asignacion_ejercicio_seq'::regclass);


--
-- Name: asignaciones_rutina id_asignacion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignaciones_rutina ALTER COLUMN id_asignacion SET DEFAULT nextval('public.asignaciones_rutina_id_asignacion_seq'::regclass);


--
-- Name: ejercicios id_ejercicio; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ejercicios ALTER COLUMN id_ejercicio SET DEFAULT nextval('public.ejercicios_id_ejercicio_seq'::regclass);


--
-- Name: progreso_mensual id_progreso; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progreso_mensual ALTER COLUMN id_progreso SET DEFAULT nextval('public.progreso_mensual_id_progreso_seq'::regclass);


--
-- Name: rutinas id_rutina; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutinas ALTER COLUMN id_rutina SET DEFAULT nextval('public.rutinas_id_rutina_seq'::regclass);


--
-- Name: sesiones_entrenamiento id_sesion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesiones_entrenamiento ALTER COLUMN id_sesion SET DEFAULT nextval('public.sesiones_entrenamiento_id_sesion_seq'::regclass);


--
-- Name: usuarios id_usuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuarios_id_usuario_seq'::regclass);


--
-- Data for Name: asignacion_rutina_ejercicios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.asignacion_rutina_ejercicios (id_asignacion_ejercicio, id_asignacion, id_ejercicio, orden_ejercicio, veces_planificadas, activo, fecha_agregado) FROM stdin;
1	384	24	1	1	t	2026-09-25
2	384	27	2	1	t	2026-09-25
3	384	888	3	1	t	2026-09-25
4	255	635	1	1	t	2026-09-25
5	303	635	1	1	t	2026-09-25
6	255	30	2	1	t	2026-09-25
7	303	30	2	1	t	2026-09-25
8	255	29	3	1	t	2026-09-25
9	303	29	3	1	t	2026-09-25
10	475	25	1	1	t	2026-09-26
11	475	26	2	1	t	2026-09-26
12	475	27	3	1	t	2026-09-26
13	475	635	4	1	t	2026-09-26
18	476	761	4	5	t	2026-09-25
14	476	24	1	10	t	2026-09-26
15	476	27	2	10	t	2026-09-26
16	476	888	3	10	t	2026-09-26
19	476	26	5	10	t	2026-09-26
20	476	29	6	10	t	2026-09-26
21	476	30	7	10	t	2026-09-26
\.


--
-- Data for Name: asignaciones_rutina; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.asignaciones_rutina (id_asignacion, id_cliente, id_rutina, fecha_asignacion, fecha_finalizacion, estado, observaciones) FROM stdin;
384	3884	895	2026-09-24	\N	ACTIVA	Asignación desde prueba de integración
303	3370	643	2026-09-23	\N	ACTIVA	ninguna
255	3152	643	2026-09-22	2026-09-25	FINALIZADA	ninguna
475	3152	42	2026-09-25	2026-09-25	CANCELADA	
476	3152	895	2026-09-25	\N	ACTIVA	Rutina reemplazada por un administrador.
\.


--
-- Data for Name: clientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clientes (id_usuario, peso, altura, objetivo, fecha_ingreso, peso_objetivo, genero) FROM stdin;
3369	34.00	1.76	Subir de peso	2026-09-23	60.00	HOMBRE
3370	56.00	1.80	Subir de peso	2026-09-23	70.00	HOMBRE
3884	75.50	1.75	Mejorar resistencia	2026-09-24	\N	\N
3152	78.00	1.80	Mantener peso	2026-09-22	78.00	HOMBRE
\.


--
-- Data for Name: ejercicios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ejercicios (id_ejercicio, nombre, descripcion, tipo, duracion_minutos, intensidad, calorias_estimadas, creado_por) FROM stdin;
761	saltar	salta	HIIT	12	MEDIA	120.00	\N
27	Sentadillas	Sentadillas sin pes	Fuerza	10	BAJA	40.00	448
22	Press de banca	Press de banca con barra	Fuerza	15	MEDIA	80.00	\N
23	Cinta caminando	Caminata moderada	Cardio	10	BAJA	50.00	\N
24	Press de banca	Press de banca con barra	Fuerza	15	MEDIA	80.00	\N
25	Cinta caminando	Caminata moderada	Cardio	10	BAJA	50.00	448
26	Elíptica	Ejercicio de baja impacto	Cardio	10	BAJA	60.00	448
28	Press de banca	Press de banca con barra	Fuerza	15	MEDIA	80.00	448
29	Peso muerto	Peso muerto rumano	Fuerza	15	MEDIA	90.00	448
30	Dominadas	Dominadas asistidas	Fuerza	15	MEDIA	70.00	448
635	Caminata	Camina	LISS	6	MEDIA	30.00	\N
21	Cinta caminando	Caminata moderada	Cardio	10	BAJA	40.00	\N
888	Mancuernas	levantar	Fuerza	12	MEDIA	120.00	\N
\.


--
-- Data for Name: progreso_mensual; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.progreso_mensual (id_progreso, id_cliente, mes, peso, sesiones_completadas, sesiones_planificadas, porcentaje_cumplimiento) FROM stdin;
160	3152	2026-09-01	78.00	10	34	29.41
\.


--
-- Data for Name: rutina_ejercicios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rutina_ejercicios (id_rutina, id_ejercicio, orden_ejercicio) FROM stdin;
895	24	1
895	27	2
895	888	3
42	25	1
42	26	2
42	27	3
43	28	1
43	29	2
643	635	1
643	30	2
643	29	3
42	635	4
42	22	5
643	26	4
\.


--
-- Data for Name: rutinas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rutinas (id_rutina, nombre, descripcion, objetivo, nivel, duracion_semanas, creado_por, fecha_creacion) FROM stdin;
895	Rutina Test Integración	Rutina creada para pruebas de integración	Mejorar resistencia	INTERMEDIO	4	\N	2026-09-24
42	Cardio Básico	Rutina de cardio para principiantes	Perder peso	BASICO	4	448	2026-09-13
43	Fuerza Intermedio	ganar musculo	Ganar masa muscular	INTERMEDIO	6	448	2026-09-13
1204	Cardio Básico	Rutina de cardio para principiantes	Perder peso	BASICO	4	448	2026-09-26
1205	asda	das	sad	INTERMEDIO	2	448	2026-09-26
643	Cardio Mantenimiento	Intervalos de alta intensidad, pero con volumen moderado	Mantener capacidad cardiovascular	AVANZADO	6	448	2026-09-22
\.


--
-- Data for Name: sesiones_entrenamiento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sesiones_entrenamiento (id_sesion, id_cliente, fecha, duracion_real, intensidad_real, calorias_quemadas, observaciones, completada, id_rutina, nombre_ejercicio, veces_planificadas, veces_realizadas, id_asignacion, id_asignacion_ejercicio) FROM stdin;
15429	3152	2026-09-22	12	MEDIA	30.00	Ninguna	f	643	Caminata	1	0	\N	\N
15430	3152	2026-09-22	8	MEDIA	20.00	Ninguna	f	643	Caminata	1	0	\N	\N
15431	3152	2026-09-22	20	MEDIA	50.00	ninguna	f	643	Caminata	3	2	\N	\N
15432	3152	2026-09-22	12	MEDIA	23.00	Ninguna	f	643	Caminata	3	2	\N	\N
15433	3152	2026-09-22	13	MEDIA	22.00	Ninguna	f	643	Caminata	2	2	\N	\N
15460	3152	2026-09-23	6	MEDIA	120.00	ninguna	f	643	trotar	3	1	\N	\N
15466	3152	2026-09-23	12	MEDIA	120.00	ninguna	f	643	pesas	4	2	\N	\N
16134	3884	2026-09-24	45	ALTA	450.50	Sesión de prueba de integración	t	\N		1	0	\N	\N
16205	3152	2026-09-25	30	MEDIA	150.00		t	643	Caminata	1	1	255	4
16206	3152	2026-09-25	20	MEDIA	120.00		t	643	Dominadas	1	1	255	6
16207	3152	2026-09-25	25	ALTA	180.00		t	643	Peso muerto	1	1	255	8
16219	3152	2026-09-25	10	BAJA	120.00		f	42	Caminata	3	2	\N	\N
16220	3152	2026-09-25	10	BAJA	120.00		t	42	Caminata	1	1	\N	\N
16221	3152	2026-09-25	10	MEDIA	120.00		t	42	Caminata	1	1	475	13
16222	3152	2026-09-25	12	MEDIA	120.00		t	42	Sentadillas	1	1	475	12
16223	3152	2026-09-25	120	MEDIA	120.00		t	895	Mancuernas	1	1	476	16
16224	3152	2026-09-25	12	MEDIA	120.00	top	t	895	Press de banca	1	1	476	14
16230	3152	2026-09-26	13	MEDIA	97.60		t	895	Sentadillas	1	1	476	15
16231	3152	2026-09-26	12	ALTA	131.04		f	895	Mancuernas	3	1	476	16
16232	3152	2026-09-26	12	BAJA	57.33		f	895	Mancuernas	2	1	476	16
16233	3152	2026-09-26	10	ALTA	109.20		f	895	saltar	5	1	476	18
16234	3152	2026-09-26	10	ALTA	109.20		t	895	Mancuernas	1	1	476	16
16235	3152	2026-09-26	10	ALTA	81.90		f	895	Press de banca	9	1	476	14
16236	3152	2026-09-26	10	ALTA	81.90		f	895	Sentadillas	9	1	476	15
16237	3152	2026-09-26	10	ALTA	122.85		f	895	Mancuernas	6	1	476	16
16238	3152	2026-09-26	10	ALTA	81.90		f	895	Sentadillas	8	1	476	15
16239	3152	2026-09-26	10	ALTA	81.90		f	895	Mancuernas	5	1	476	16
16240	3152	2026-09-26	10	MEDIA	95.55		f	895	saltar	4	1	476	18
16241	3152	2026-09-26	10	MEDIA	61.43		f	895	Mancuernas	4	1	476	16
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id_usuario, nombre, apellido, correo_electronico, contrasenia_hash, edad, tipo_usuario, fecha_registro, "contraseña_hash") FROM stdin;
448	Admin	Sistema	admin@cardio.com	$2b$12$.pYQF7KD5Dtwx828I.5dKOnOd4GliD5WYTKCUYmWivH6ShA1V5FkO	30	administrador	2026-09-13	\N
3369	Jose	Corzo	jose123@gmail.com	$2b$12$Ovr/vcnnBafNrYOo43blqedNv2xKFr52/g9jEsClBcNJrN9fTeEYW	19	cliente	2026-09-23	$2b$12$Ovr/vcnnBafNrYOo43blqedNv2xKFr52/g9jEsClBcNJrN9fTeEYW
3152	Juan	Perea	juan123@gmail.com	$2b$12$vBU22G8lPS2.Kt2ekiOFLuA1XiO4ypyFT6Ephfg6xas7hnkoLMA/6	20	cliente	2026-09-22	\N
3884	Test	Integracion	test.integracion@wellness.com	a109e36947ad56de1dca1cc49f0ef8ac9ad9a7b1aa0df41fb3c4cb73c1ff01ea	25	cliente	2026-09-24	a109e36947ad56de1dca1cc49f0ef8ac9ad9a7b1aa0df41fb3c4cb73c1ff01ea
3370	Pedro	Torres	pedro123@gmail.com	$2b$12$E.sXYndXKf7RGDP54DVq3eXnZoKx187MZ//8ZE1txumszxtmJ/xDq	23	cliente	2026-09-23	$2b$12$OJj.VO4ZJ8W7qOzsXmAHze4I1dCf/.iPr4s98xbCzgivjnuJmkFKO
4637	Jhon	Paredes	jhon123@cardio.com	$2b$12$Lu8o1zchZVSl8RfRPXCQd.8fOI1mC2UWHLQjEw119UJ8er3gLuct.	12	administrador	2026-09-26	\N
\.


--
-- Name: asignacion_rutina_ejercicios_id_asignacion_ejercicio_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.asignacion_rutina_ejercicios_id_asignacion_ejercicio_seq', 21, true);


--
-- Name: asignaciones_rutina_id_asignacion_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.asignaciones_rutina_id_asignacion_seq', 480, true);


--
-- Name: ejercicios_id_ejercicio_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ejercicios_id_ejercicio_seq', 1163, true);


--
-- Name: progreso_mensual_id_progreso_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.progreso_mensual_id_progreso_seq', 346, true);


--
-- Name: rutinas_id_rutina_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rutinas_id_rutina_seq', 1205, true);


--
-- Name: sesiones_entrenamiento_id_sesion_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sesiones_entrenamiento_id_sesion_seq', 16241, true);


--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_usuario_seq', 4637, true);


--
-- Name: asignacion_rutina_ejercicios asignacion_rutina_ejercicios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignacion_rutina_ejercicios
    ADD CONSTRAINT asignacion_rutina_ejercicios_pkey PRIMARY KEY (id_asignacion_ejercicio);


--
-- Name: asignaciones_rutina asignaciones_rutina_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignaciones_rutina
    ADD CONSTRAINT asignaciones_rutina_pkey PRIMARY KEY (id_asignacion);


--
-- Name: clientes clientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY (id_usuario);


--
-- Name: ejercicios ejercicios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ejercicios
    ADD CONSTRAINT ejercicios_pkey PRIMARY KEY (id_ejercicio);


--
-- Name: progreso_mensual progreso_mensual_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progreso_mensual
    ADD CONSTRAINT progreso_mensual_pkey PRIMARY KEY (id_progreso);


--
-- Name: rutina_ejercicios rutina_ejercicios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutina_ejercicios
    ADD CONSTRAINT rutina_ejercicios_pkey PRIMARY KEY (id_rutina, id_ejercicio);


--
-- Name: rutinas rutinas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutinas
    ADD CONSTRAINT rutinas_pkey PRIMARY KEY (id_rutina);


--
-- Name: sesiones_entrenamiento sesiones_entrenamiento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesiones_entrenamiento
    ADD CONSTRAINT sesiones_entrenamiento_pkey PRIMARY KEY (id_sesion);


--
-- Name: progreso_mensual unq_cliente_mes; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progreso_mensual
    ADD CONSTRAINT unq_cliente_mes UNIQUE (id_cliente, mes);


--
-- Name: asignacion_rutina_ejercicios uq_asignacion_ejercicio; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignacion_rutina_ejercicios
    ADD CONSTRAINT uq_asignacion_ejercicio UNIQUE (id_asignacion, id_ejercicio);


--
-- Name: asignacion_rutina_ejercicios uq_asignacion_orden; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignacion_rutina_ejercicios
    ADD CONSTRAINT uq_asignacion_orden UNIQUE (id_asignacion, orden_ejercicio);


--
-- Name: progreso_mensual uq_progreso_cliente_mes; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progreso_mensual
    ADD CONSTRAINT uq_progreso_cliente_mes UNIQUE (id_cliente, mes);


--
-- Name: usuarios usuarios_correo_electronico_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_correo_electronico_key UNIQUE (correo_electronico);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);


--
-- Name: idx_asignacion_rutina_ejercicios_activo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_asignacion_rutina_ejercicios_activo ON public.asignacion_rutina_ejercicios USING btree (id_asignacion, activo);


--
-- Name: idx_asignacion_rutina_ejercicios_asignacion; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_asignacion_rutina_ejercicios_asignacion ON public.asignacion_rutina_ejercicios USING btree (id_asignacion);


--
-- Name: idx_asignacion_rutina_ejercicios_ejercicio; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_asignacion_rutina_ejercicios_ejercicio ON public.asignacion_rutina_ejercicios USING btree (id_ejercicio);


--
-- Name: idx_asignaciones_activa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_asignaciones_activa ON public.asignaciones_rutina USING btree (id_cliente) WHERE (estado = 'ACTIVA'::public.estado_asignacion);


--
-- Name: idx_asignaciones_cliente; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_asignaciones_cliente ON public.asignaciones_rutina USING btree (id_cliente);


--
-- Name: idx_asignaciones_estado; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_asignaciones_estado ON public.asignaciones_rutina USING btree (estado);


--
-- Name: idx_asignaciones_fechas; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_asignaciones_fechas ON public.asignaciones_rutina USING btree (fecha_asignacion, fecha_finalizacion);


--
-- Name: idx_asignaciones_id_cliente; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_asignaciones_id_cliente ON public.asignaciones_rutina USING btree (id_cliente, estado);


--
-- Name: idx_clientes_id_usuario; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_clientes_id_usuario ON public.clientes USING btree (id_usuario);


--
-- Name: idx_clientes_ingreso; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_clientes_ingreso ON public.clientes USING btree (fecha_ingreso);


--
-- Name: idx_ejercicios_creado_por; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ejercicios_creado_por ON public.ejercicios USING btree (creado_por);


--
-- Name: idx_ejercicios_intensidad; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ejercicios_intensidad ON public.ejercicios USING btree (intensidad);


--
-- Name: idx_ejercicios_nombre; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ejercicios_nombre ON public.ejercicios USING btree (nombre);


--
-- Name: idx_ejercicios_tipo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ejercicios_tipo ON public.ejercicios USING btree (tipo);


--
-- Name: idx_progreso_cliente; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_progreso_cliente ON public.progreso_mensual USING btree (id_cliente);


--
-- Name: idx_progreso_id_cliente; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_progreso_id_cliente ON public.progreso_mensual USING btree (id_cliente);


--
-- Name: idx_progreso_id_cliente_mes; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_progreso_id_cliente_mes ON public.progreso_mensual USING btree (id_cliente, mes);


--
-- Name: idx_progreso_mes; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_progreso_mes ON public.progreso_mensual USING btree (mes);


--
-- Name: idx_rutina_ejercicios_ejercicio; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_rutina_ejercicios_ejercicio ON public.rutina_ejercicios USING btree (id_ejercicio);


--
-- Name: idx_rutina_ejercicios_orden; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_rutina_ejercicios_orden ON public.rutina_ejercicios USING btree (id_rutina, orden_ejercicio);


--
-- Name: idx_rutina_ejercicios_rutina; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_rutina_ejercicios_rutina ON public.rutina_ejercicios USING btree (id_rutina);


--
-- Name: idx_rutinas_creado_por; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_rutinas_creado_por ON public.rutinas USING btree (creado_por);


--
-- Name: idx_rutinas_nivel; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_rutinas_nivel ON public.rutinas USING btree (nivel);


--
-- Name: idx_rutinas_nombre; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_rutinas_nombre ON public.rutinas USING btree (nombre);


--
-- Name: idx_rutinas_objetivo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_rutinas_objetivo ON public.rutinas USING btree (objetivo);


--
-- Name: idx_sesiones_asignacion; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sesiones_asignacion ON public.sesiones_entrenamiento USING btree (id_asignacion);


--
-- Name: idx_sesiones_asignacion_ejercicio; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sesiones_asignacion_ejercicio ON public.sesiones_entrenamiento USING btree (id_asignacion_ejercicio);


--
-- Name: idx_sesiones_cliente; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sesiones_cliente ON public.sesiones_entrenamiento USING btree (id_cliente);


--
-- Name: idx_sesiones_completada; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sesiones_completada ON public.sesiones_entrenamiento USING btree (completada);


--
-- Name: idx_sesiones_fecha; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sesiones_fecha ON public.sesiones_entrenamiento USING btree (fecha);


--
-- Name: idx_sesiones_id_cliente; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sesiones_id_cliente ON public.sesiones_entrenamiento USING btree (id_cliente);


--
-- Name: idx_sesiones_id_cliente_completada; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sesiones_id_cliente_completada ON public.sesiones_entrenamiento USING btree (id_cliente, completada);


--
-- Name: idx_sesiones_id_cliente_fecha; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sesiones_id_cliente_fecha ON public.sesiones_entrenamiento USING btree (id_cliente, fecha);


--
-- Name: idx_usuarios_correo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_usuarios_correo ON public.usuarios USING btree (correo_electronico);


--
-- Name: idx_usuarios_tipo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_usuarios_tipo ON public.usuarios USING btree (tipo_usuario);


--
-- Name: uq_asignacion_activa_por_cliente; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX uq_asignacion_activa_por_cliente ON public.asignaciones_rutina USING btree (id_cliente) WHERE ((estado = 'ACTIVA'::public.estado_asignacion) AND (fecha_finalizacion IS NULL));


--
-- Name: usuarios trigger_sincronizar_hash_contrasena; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_sincronizar_hash_contrasena BEFORE INSERT OR UPDATE ON public.usuarios FOR EACH ROW EXECUTE FUNCTION public.sincronizar_hash_contrasena();


--
-- Name: asignaciones_rutina asignaciones_rutina_id_cliente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignaciones_rutina
    ADD CONSTRAINT asignaciones_rutina_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES public.clientes(id_usuario) ON DELETE CASCADE;


--
-- Name: asignaciones_rutina asignaciones_rutina_id_rutina_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignaciones_rutina
    ADD CONSTRAINT asignaciones_rutina_id_rutina_fkey FOREIGN KEY (id_rutina) REFERENCES public.rutinas(id_rutina) ON DELETE RESTRICT;


--
-- Name: clientes clientes_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario) ON DELETE CASCADE;


--
-- Name: ejercicios ejercicios_creado_por_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ejercicios
    ADD CONSTRAINT ejercicios_creado_por_fkey FOREIGN KEY (creado_por) REFERENCES public.usuarios(id_usuario) ON DELETE SET NULL;


--
-- Name: asignacion_rutina_ejercicios fk_asignacion_ejercicio_asignacion; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignacion_rutina_ejercicios
    ADD CONSTRAINT fk_asignacion_ejercicio_asignacion FOREIGN KEY (id_asignacion) REFERENCES public.asignaciones_rutina(id_asignacion) ON DELETE CASCADE;


--
-- Name: asignacion_rutina_ejercicios fk_asignacion_ejercicio_ejercicio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignacion_rutina_ejercicios
    ADD CONSTRAINT fk_asignacion_ejercicio_ejercicio FOREIGN KEY (id_ejercicio) REFERENCES public.ejercicios(id_ejercicio) ON DELETE RESTRICT;


--
-- Name: sesiones_entrenamiento fk_sesion_asignacion; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesiones_entrenamiento
    ADD CONSTRAINT fk_sesion_asignacion FOREIGN KEY (id_asignacion) REFERENCES public.asignaciones_rutina(id_asignacion) ON DELETE RESTRICT;


--
-- Name: sesiones_entrenamiento fk_sesion_asignacion_ejercicio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesiones_entrenamiento
    ADD CONSTRAINT fk_sesion_asignacion_ejercicio FOREIGN KEY (id_asignacion_ejercicio) REFERENCES public.asignacion_rutina_ejercicios(id_asignacion_ejercicio) ON DELETE RESTRICT;


--
-- Name: sesiones_entrenamiento fk_sesion_rutina; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesiones_entrenamiento
    ADD CONSTRAINT fk_sesion_rutina FOREIGN KEY (id_rutina) REFERENCES public.rutinas(id_rutina);


--
-- Name: progreso_mensual progreso_mensual_id_cliente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progreso_mensual
    ADD CONSTRAINT progreso_mensual_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES public.clientes(id_usuario) ON DELETE CASCADE;


--
-- Name: rutina_ejercicios rutina_ejercicios_id_ejercicio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutina_ejercicios
    ADD CONSTRAINT rutina_ejercicios_id_ejercicio_fkey FOREIGN KEY (id_ejercicio) REFERENCES public.ejercicios(id_ejercicio) ON DELETE CASCADE;


--
-- Name: rutina_ejercicios rutina_ejercicios_id_rutina_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutina_ejercicios
    ADD CONSTRAINT rutina_ejercicios_id_rutina_fkey FOREIGN KEY (id_rutina) REFERENCES public.rutinas(id_rutina) ON DELETE CASCADE;


--
-- Name: rutinas rutinas_creado_por_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutinas
    ADD CONSTRAINT rutinas_creado_por_fkey FOREIGN KEY (creado_por) REFERENCES public.usuarios(id_usuario) ON DELETE SET NULL;


--
-- Name: sesiones_entrenamiento sesiones_entrenamiento_id_cliente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesiones_entrenamiento
    ADD CONSTRAINT sesiones_entrenamiento_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES public.clientes(id_usuario) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict WEacGtuzfJTDTBRhJVzRar1YgEnW2Rns9UBJ8rbHDpQSnx8SrnulkipmGfDSVhs

