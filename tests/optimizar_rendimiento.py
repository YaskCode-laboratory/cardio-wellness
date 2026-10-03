#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OPTIMIZADOR DE RENDIMIENTO - CARDIO-WELLNESS
Aplica índices optimizados a la base de datos PostgreSQL.
"""

import argparse
import os
from datetime import datetime

import psycopg2


def parse_args():
    """Procesa argumentos y configuración de conexión."""

    parser = argparse.ArgumentParser(
        description="Optimizador de Rendimiento"
    )

    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("DB_HOST", "localhost"),
        help="Host de la BD; usa DB_HOST o --host.",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("DB_PORT", "5432")),
        help="Puerto de la BD; usa DB_PORT o --port.",
    )

    parser.add_argument(
        "--db",
        type=str,
        default=os.getenv("DB_NAME", "cardio_wellness"),
        help="Nombre de la BD; usa DB_NAME o --db.",
    )

    parser.add_argument(
        "--user",
        type=str,
        default=os.getenv("DB_USER", "postgres"),
        help="Usuario de la BD; usa DB_USER o --user.",
    )

    parser.add_argument(
        "--password",
        type=str,
        default=os.getenv("DB_PASSWORD"),
        help="Contraseña de la BD; usa DB_PASSWORD o --password.",
    )

    args = parser.parse_args()

    if not args.password:
        parser.error(
            "Debes proporcionar --password o definir "
            "la variable de entorno DB_PASSWORD."
        )

    return args


def crear_indices(conn):
    """Crea índices optimizados en la BD."""

    print("\n" + "=" * 80)
    print("CREANDO ÍNDICES OPTIMIZADOS")
    print("=" * 80)

    indices = [
        (
            "idx_clientes_id_usuario",
            "CREATE INDEX IF NOT EXISTS "
            "idx_clientes_id_usuario ON clientes(id_usuario)",
        ),
        (
            "idx_sesiones_id_cliente_fecha",
            "CREATE INDEX IF NOT EXISTS "
            "idx_sesiones_id_cliente_fecha "
            "ON sesiones_entrenamiento(id_cliente, fecha)",
        ),
        (
            "idx_sesiones_id_cliente_completada",
            "CREATE INDEX IF NOT EXISTS "
            "idx_sesiones_id_cliente_completada "
            "ON sesiones_entrenamiento(id_cliente, completada)",
        ),
        (
            "idx_asignaciones_estado",
            "CREATE INDEX IF NOT EXISTS "
            "idx_asignaciones_estado ON asignaciones_rutina(estado)",
        ),
        (
            "idx_asignaciones_id_cliente",
            "CREATE INDEX IF NOT EXISTS "
            "idx_asignaciones_id_cliente "
            "ON asignaciones_rutina(id_cliente, estado)",
        ),
        (
            "idx_progreso_id_cliente",
            "CREATE INDEX IF NOT EXISTS "
            "idx_progreso_id_cliente ON progreso_mensual(id_cliente)",
        ),
        (
            "idx_progreso_id_cliente_mes",
            "CREATE INDEX IF NOT EXISTS "
            "idx_progreso_id_cliente_mes "
            "ON progreso_mensual(id_cliente, mes)",
        ),
        (
            "idx_rutinas_creado_por",
            "CREATE INDEX IF NOT EXISTS "
            "idx_rutinas_creado_por ON rutinas(creado_por)",
        ),
        (
            "idx_ejercicios_creado_por",
            "CREATE INDEX IF NOT EXISTS "
            "idx_ejercicios_creado_por ON ejercicios(creado_por)",
        ),
        (
            "idx_rutina_ejercicios_orden",
            "CREATE INDEX IF NOT EXISTS "
            "idx_rutina_ejercicios_orden "
            "ON rutina_ejercicios(id_rutina, orden_ejercicio)",
        ),
        (
            "idx_usuarios_correo",
            "CREATE INDEX IF NOT EXISTS "
            "idx_usuarios_correo ON usuarios(correo_electronico)",
        ),
    ]

    with conn.cursor() as cur:
        for nombre, sql in indices:
            try:
                print(f"  Creando índice: {nombre}...")
                cur.execute(sql)
                conn.commit()
                print(f"  ✅ {nombre} creado")
            except Exception as error:
                print(f"  ⚠️  {nombre}: {error}")
                conn.rollback()

    print("\n✅ Índices creados")


def analizar_tablas(conn):
    """Analiza tablas para optimizar consultas."""

    print("\n" + "=" * 80)
    print("ANALIZANDO TABLAS (VACUUM ANALYZE)")
    print("=" * 80)

    tablas = [
        "clientes",
        "sesiones_entrenamiento",
        "asignaciones_rutina",
        "progreso_mensual",
        "rutinas",
        "ejercicios",
        "rutina_ejercicios",
        "usuarios",
    ]

    conn.commit()

    for tabla in tablas:
        try:
            print(f"  Analizando tabla: {tabla}...")

            conn_temp = psycopg2.connect(
                host=conn.info.host,
                port=conn.info.port,
                database=conn.info.dbname,
                user=conn.info.user,
                password=conn.info.password,
            )

            conn_temp.autocommit = True

            with conn_temp.cursor() as cur:
                cur.execute(f"VACUUM ANALYZE {tabla}")

            conn_temp.close()

            print(f"  ✅ {tabla} analizada")

        except Exception as error:
            print(f"  ⚠️  {tabla}: {error}")

    print("\n✅ Tablas analizadas")


def verificar_rendimiento(conn):
    """Muestra información general de rendimiento de la BD."""

    print("\n" + "=" * 80)
    print("VERIFICANDO RENDIMIENTO")
    print("=" * 80)

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM pg_indexes
            WHERE schemaname = 'public'
            """
        )
        total_indices = cur.fetchone()[0]
        print(f"  📊 Total de índices: {total_indices}")

        cur.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'public'
            """
        )
        total_tablas = cur.fetchone()[0]
        print(f"  📊 Total de tablas: {total_tablas}")

        cur.execute(
            """
            SELECT pg_size_pretty(pg_database_size(current_database()))
            """
        )
        tamano = cur.fetchone()[0]
        print(f"  📊 Tamaño de BD: {tamano}")

    print("\n✅ Estadísticas obtenidas")


def main():
    """Ejecuta la optimización de la base de datos."""

    args = parse_args()

    print("=" * 80)
    print("OPTIMIZADOR DE RENDIMIENTO - CARDIO-WELLNESS")
    print("=" * 80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"BD: {args.db}@{args.host}:{args.port}")
    print("=" * 80)

    conn = None

    try:
        print("\n[1/4] Conectando a la base de datos...")

        conn = psycopg2.connect(
            host=args.host,
            port=args.port,
            database=args.db,
            user=args.user,
            password=args.password,
        )

        print("✅ Conexión establecida")

        print("\n[2/4] Creando índices optimizados...")
        crear_indices(conn)

        print("\n[3/4] Analizando tablas...")
        analizar_tablas(conn)

        print("\n[4/4] Verificando rendimiento...")
        verificar_rendimiento(conn)

        print("\n" + "=" * 80)
        print("✅ OPTIMIZACIÓN COMPLETADA")
        print("=" * 80)

        print("\nAhora ejecuta el stress test:")
        print(
            "  python tests/stress_test_postgresql.py "
            "--usuarios 100 --duracion 300 --clientes 500"
        )

        print("\nDeberías ver:")
        print("  - Menos fallos (<1%)")
        print("  - Menor latencia máxima (<2s)")
        print("  - Mejor throughput (>300 ops/segundo)")

        return 0

    except Exception as error:
        print(f"\n❌ ERROR: {error}")
        return 1

    finally:
        if conn is not None:
            conn.close()
            print("\nConexión cerrada.")


if __name__ == "__main__":
    raise SystemExit(main())
