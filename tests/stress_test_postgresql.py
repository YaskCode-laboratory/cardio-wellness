#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prueba de estrés para PostgreSQL - Cardio-Wellness.

Crea clientes temporales, ejecuta operaciones concurrentes y limpia
los datos creados al finalizar.

Por seguridad, solo puede ejecutarse contra:
cardio_wellness_prueba_limpieza
"""

import argparse
import os
import random
import threading
import time
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import psycopg2
from psycopg2 import pool


SAFE_TEST_DATABASE = "cardio_wellness_prueba_limpieza"


class StressTesterPostgreSQL:
    """Ejecuta pruebas de estrés concurrentes sobre PostgreSQL."""

    def __init__(
        self,
        host: str = os.getenv("DB_HOST", "localhost"),
        port: int = int(os.getenv("DB_PORT", "5432")),
        database: str = os.getenv("DB_NAME", SAFE_TEST_DATABASE),
        user: str = os.getenv("DB_USER", "postgres"),
        password: str | None = None,
        num_usuarios: int = 20,
        duracion: int = 30,
        num_clientes_prueba: int = 100,
    ):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.num_usuarios = num_usuarios
        self.duracion = duracion
        self.num_clientes_prueba = num_clientes_prueba

        self.running = True
        self.ops_exitosas = 0
        self.ops_fallidas = 0
        self.response_times = []

        self.lock = threading.Lock()
        self.connection_pool = None

        self.id_usuarios_prueba = []
        self.id_clientes_prueba = []

    def _init_pool(self):
        """Inicializa el pool de conexiones."""

        max_conexiones = max(1, min(self.num_usuarios, 100))

        self.connection_pool = pool.SimpleConnectionPool(
            1,
            max_conexiones,
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
        )

        print(
            "✅ Pool de conexiones inicializado "
            f"(1-{max_conexiones} conexiones)"
        )

    def _get_connection(self):
        """Obtiene una conexión desde el pool."""

        return self.connection_pool.getconn()

    def _release_connection(self, conn):
        """Devuelve una conexión al pool."""

        if conn is not None and self.connection_pool is not None:
            self.connection_pool.putconn(conn)

    def _crear_clientes_prueba(self):
        """Crea usuarios y clientes temporales para el test."""

        print(
            f"\n📝 Creando "
            f"{self.num_clientes_prueba} clientes de prueba..."
        )

        conn = self._get_connection()

        try:
            with conn.cursor() as cursor:
                for indice in range(self.num_clientes_prueba):
                    correo = f"stress.{uuid4().hex[:12]}@test.com"
                    hash_temporal = "hash_temporal_stress_test"

                    cursor.execute(
                        """
                        INSERT INTO usuarios (
                            nombre,
                            apellido,
                            correo_electronico,
                            contrasenia_hash,
                            edad,
                            tipo_usuario
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING id_usuario
                        """,
                        (
                            f"Stress{indice}",
                            "Test",
                            correo,
                            hash_temporal,
                            random.randint(20, 50),
                            "cliente",
                        ),
                    )

                    id_usuario = cursor.fetchone()[0]

                    cursor.execute(
                        """
                        INSERT INTO clientes (
                            id_usuario,
                            peso,
                            altura,
                            objetivo
                        )
                        VALUES (%s, %s, %s, %s)
                        RETURNING id_usuario
                        """,
                        (
                            id_usuario,
                            random.uniform(50, 120),
                            random.uniform(1.50, 2.00),
                            "Pruebas de estrés",
                        ),
                    )

                    id_cliente = cursor.fetchone()[0]

                    self.id_usuarios_prueba.append(id_usuario)
                    self.id_clientes_prueba.append(id_cliente)

            conn.commit()

            print(
                f"✅ {len(self.id_clientes_prueba)} "
                f"clientes de prueba creados"
            )

        except Exception:
            conn.rollback()
            raise

        finally:
            self._release_connection(conn)

    def _limpiar_clientes_prueba(self):
        """Elimina sesiones, clientes y usuarios temporales."""

        print(
            f"\n🧹 Limpiando "
            f"{len(self.id_clientes_prueba)} clientes de prueba..."
        )

        if not self.id_clientes_prueba:
            return

        conn = self._get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM sesiones_entrenamiento
                    WHERE id_cliente = ANY(%s)
                    """,
                    (self.id_clientes_prueba,),
                )

                cursor.execute(
                    """
                    DELETE FROM clientes
                    WHERE id_usuario = ANY(%s)
                    """,
                    (self.id_clientes_prueba,),
                )

                cursor.execute(
                    """
                    DELETE FROM usuarios
                    WHERE id_usuario = ANY(%s)
                    """,
                    (self.id_usuarios_prueba,),
                )

            conn.commit()
            print("✅ Clientes de prueba eliminados")

        except Exception as error:
            conn.rollback()

            print(
                "⚠️ Error al limpiar clientes de prueba: "
                f"{error}"
            )

        finally:
            self._release_connection(conn)

    def _registrar_exito(self, response_time):
        """Registra una operación ejecutada correctamente."""

        with self.lock:
            self.ops_exitosas += 1
            self.response_times.append(response_time)

    def _registrar_fallo(self):
        """Registra una operación fallida."""

        with self.lock:
            self.ops_fallidas += 1

    def _simulate_user_behavior(self, user_id: int):
        """Simula operaciones de un usuario concurrente."""

        while self.running:
            start_op = time.time()
            conn = None

            try:
                conn = self._get_connection()
                conn.autocommit = False

                operacion = random.choices(
                    ["SELECT", "INSERT", "UPDATE", "DELETE"],
                    weights=[92, 7, 0.5, 0.5],
                )[0]

                if operacion == "INSERT":
                    self._insert_sesion(conn, user_id)

                elif operacion == "SELECT":
                    self._select_sesiones(conn)

                elif operacion == "UPDATE":
                    self._update_sesion(conn, user_id)

                else:
                    self._delete_sesion(conn, user_id)

                conn.commit()

                response_time = (time.time() - start_op) * 1000
                self._registrar_exito(response_time)

            except (
                psycopg2.errors.DeadlockDetected,
                psycopg2.errors.LockNotAvailable,
                psycopg2.errors.SerializationFailure,
                psycopg2.errors.UniqueViolation,
            ):
                if conn is not None:
                    conn.rollback()

                self._registrar_fallo()
                time.sleep(random.uniform(0.05, 0.2))

            except Exception as error:
                if conn is not None:
                    conn.rollback()

                self._registrar_fallo()

                with self.lock:
                    print(
                        f"⚠️ Error en usuario {user_id}: "
                        f"{type(error).__name__}: {error}"
                    )

            finally:
                self._release_connection(conn)

            time.sleep(random.uniform(0.02, 0.15))

    def _insert_sesion(self, conn, user_id: int):
        """Inserta una sesión para un cliente temporal."""

        id_cliente = random.choice(self.id_clientes_prueba)

        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO sesiones_entrenamiento (
                    id_cliente,
                    fecha,
                    duracion_real,
                    intensidad_real,
                    calorias_quemadas,
                    observaciones,
                    completada
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    id_cliente,
                    datetime.now().date()
                    - timedelta(days=random.randint(0, 30)),
                    random.randint(15, 90),
                    random.choice(
                        [
                            "BAJA",
                            "MEDIA",
                            "ALTA",
                        ]
                    ),
                    Decimal(str(random.uniform(100, 800))),
                    f"Sesión estrés {user_id}",
                    True,
                ),
            )

    def _select_sesiones(self, conn):
        """Consulta sesiones de un cliente temporal."""

        id_cliente = random.choice(self.id_clientes_prueba)

        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id_sesion,
                    id_cliente,
                    fecha,
                    duracion_real,
                    calorias_quemadas
                FROM sesiones_entrenamiento
                WHERE id_cliente = %s
                ORDER BY fecha DESC
                LIMIT 10
                """,
                (id_cliente,),
            )

            cursor.fetchall()

    def _update_sesion(self, conn, user_id: int):
        """Actualiza una sesión creada por el usuario simulado."""

        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE sesiones_entrenamiento
                SET duracion_real = %s
                WHERE ctid IN (
                    SELECT ctid
                    FROM sesiones_entrenamiento
                    WHERE observaciones LIKE %s
                      AND completada = TRUE
                    LIMIT 1
                )
                """,
                (
                    random.randint(15, 90),
                    f"%estrés {user_id}%",
                ),
            )

    def _delete_sesion(self, conn, user_id: int):
        """Elimina una sesión creada por el usuario simulado."""

        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM sesiones_entrenamiento
                WHERE ctid IN (
                    SELECT ctid
                    FROM sesiones_entrenamiento
                    WHERE observaciones LIKE %s
                    LIMIT 1
                )
                """,
                (f"%estrés {user_id}%",),
            )

    def run(self):
        """Ejecuta la prueba de estrés."""

        self._init_pool()

        try:
            self._crear_clientes_prueba()

            print(f"\n{'=' * 60}")
            print(
                "PRUEBA DE ESTRÉS - CARDIO-WELLNESS "
                "(PostgreSQL)"
            )
            print(f"{'=' * 60}")
            print(
                f"Base de datos: "
                f"{self.database}@{self.host}:{self.port}"
            )
            print(f"Usuarios concurrentes: {self.num_usuarios}")
            print(
                f"Clientes de prueba: "
                f"{len(self.id_clientes_prueba)}"
            )
            print(f"Duración: {self.duracion} segundos")
            print(f"{'=' * 60}\n")

            start_time = time.time()

            print(
                f"[{datetime.now().strftime('%H:%M:%S')}] "
                f"Iniciando {self.num_usuarios} "
                f"usuarios concurrentes...\n"
            )

            threads = []

            for indice in range(self.num_usuarios):
                thread = threading.Thread(
                    target=self._simulate_user_behavior,
                    args=(indice + 1,),
                    daemon=True,
                )

                thread.start()
                threads.append(thread)

            time.sleep(self.duracion)
            self.running = False

            for thread in threads:
                thread.join(timeout=2)

            total_time = time.time() - start_time
            total_ops = self.ops_exitosas + self.ops_fallidas

            tasa_exito = (
                self.ops_exitosas / total_ops * 100
                if total_ops > 0
                else 0
            )

            ops_por_segundo = (
                total_ops / total_time
                if total_time > 0
                else 0
            )

            avg_response = (
                sum(self.response_times)
                / len(self.response_times)
                if self.response_times
                else 0
            )

            max_response = (
                max(self.response_times)
                if self.response_times
                else 0
            )

            min_response = (
                min(self.response_times)
                if self.response_times
                else 0
            )

            print(f"\n{'=' * 60}")
            print("RESULTADOS DE LA PRUEBA DE ESTRÉS")
            print(f"{'=' * 60}")
            print(f"Tiempo total: {total_time:.2f} segundos")
            print(f"Operaciones totales: {total_ops}")
            print(f"Exitosas: {self.ops_exitosas}")
            print(f"Fallidas: {self.ops_fallidas}")
            print(f"Tasa de éxito: {tasa_exito:.2f}%")
            print("\nRendimiento:")
            print(f"  - Ops/segundo: {ops_por_segundo:.2f}")
            print(f"  - Avg response: {avg_response:.2f} ms")
            print(f"  - Max response: {max_response:.2f} ms")
            print(f"  - Min response: {min_response:.2f} ms")
            print(f"{'=' * 60}\n")

            if tasa_exito >= 99 and ops_por_segundo >= 300:
                print(
                    "✅ RESULTADO: EXITOSO - "
                    "Se cumplen los objetivos de estabilidad "
                    "y rendimiento."
                )

            elif tasa_exito >= 95 and ops_por_segundo >= 10:
                print(
                    "⚠️ RESULTADO: ACEPTABLE - "
                    "La concurrencia funciona, pero se recomiendan "
                    "optimizaciones adicionales."
                )

            else:
                print(
                    "❌ RESULTADO: CRÍTICO - "
                    "Se requieren optimizaciones antes de usar "
                    "esta configuración bajo carga."
                )

        finally:
            self.running = False
            self._limpiar_clientes_prueba()

            if self.connection_pool is not None:
                self.connection_pool.closeall()


def main():
    """Procesa argumentos y ejecuta la prueba."""

    parser = argparse.ArgumentParser(
        description="Prueba de estrés para PostgreSQL"
    )

    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("DB_HOST", "localhost"),
        help="Host de PostgreSQL; usa DB_HOST o --host.",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("DB_PORT", "5432")),
        help="Puerto de PostgreSQL; usa DB_PORT o --port.",
    )

    parser.add_argument(
        "--db",
        type=str,
        default=os.getenv("DB_NAME", SAFE_TEST_DATABASE),
        help="Base de datos de prueba; usa DB_NAME o --db.",
    )

    parser.add_argument(
        "--user",
        type=str,
        default=os.getenv("DB_USER", "postgres"),
        help="Usuario de PostgreSQL; usa DB_USER o --user.",
    )

    parser.add_argument(
        "--password",
        type=str,
        default=os.getenv("DB_PASSWORD"),
        help="Contraseña de PostgreSQL; usa DB_PASSWORD o --password.",
    )

    parser.add_argument(
        "--usuarios",
        type=int,
        default=20,
        help="Cantidad de usuarios concurrentes.",
    )

    parser.add_argument(
        "--duracion",
        type=int,
        default=30,
        help="Duración de la prueba en segundos.",
    )

    parser.add_argument(
        "--clientes",
        type=int,
        default=100,
        help="Clientes temporales a crear.",
    )

    args = parser.parse_args()

    if not args.password:
        parser.error(
            "Debes proporcionar --password o definir "
            "la variable de entorno DB_PASSWORD."
        )

    if args.db != SAFE_TEST_DATABASE:
        parser.error(
            "Por seguridad, el stress test solo puede ejecutarse "
            f"contra '{SAFE_TEST_DATABASE}'. "
            f"Base solicitada: '{args.db}'."
        )

    if args.usuarios < 1:
        parser.error("--usuarios debe ser mayor o igual a 1.")

    if args.duracion < 1:
        parser.error("--duracion debe ser mayor o igual a 1.")

    if args.clientes < 1:
        parser.error("--clientes debe ser mayor o igual a 1.")

    tester = StressTesterPostgreSQL(
        host=args.host,
        port=args.port,
        database=args.db,
        user=args.user,
        password=args.password,
        num_usuarios=args.usuarios,
        duracion=args.duracion,
        num_clientes_prueba=args.clientes,
    )

    try:
        tester.run()
        return 0

    except KeyboardInterrupt:
        print(
            "\n⚠️ Prueba interrumpida por el usuario. "
            "Los datos temporales se limpiaron antes de salir."
        )
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
