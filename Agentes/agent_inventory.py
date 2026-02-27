import os
import sqlite3
import logging
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from prompts import get_inventory_sql_prompt, get_inventory_system_prompt
from Agentes.seed_data import INVENTORY_SEED

load_dotenv()
logger = logging.getLogger(__name__)

class InventoryAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
        self.deployment = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")
        
        # Configuración DB
        self.db_path = os.path.join(os.path.dirname(__file__), 'inventory.db')
        self._init_db()

    def _init_db(self):
        """Inicializar la BD de SQLite y poblar con datos dummy"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Crear tabla
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    modelo TEXT,
                    marca TEXT,
                    id_number TEXT UNIQUE,
                    asignado_a TEXT,
                    costo_total REAL,
                    estado TEXT,
                    departamento TEXT
                )
            ''')
            
            # Poblar BD si está vacía (se ejecuta automáticamente en Render y en local)
            cursor.execute("SELECT COUNT(*) FROM inventario")
            if cursor.fetchone()[0] == 0:
                cursor.executemany('''
                    INSERT INTO inventario (modelo, marca, id_number, asignado_a, costo_total, estado, departamento)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', INVENTORY_SEED)
                conn.commit()
                logger.info(f"[Inventory] BD inicializada con {len(INVENTORY_SEED)} registros.")
                
            conn.close()
        except Exception as e:
            logger.error(f"[Inventory] Error inicializando DB: {e}")


    def get_connection(self):
        try:
            return sqlite3.connect(self.db_path)
        except Exception as e:
            logger.error(f"[Inventory] Error conectando DB: {e}")
            return None

    def query_db(self, query):
        conn = self.get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            if cursor.description:
                columns = [column[0] for column in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                return results
            conn.commit()
            return []
        except Exception as e:
            logger.error(f"[Inventory] SQL Error: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_response(self, user_msg, history=None, memory=None):
        """
        memory: dict con {last_sql, last_context, last_results} de la consulta anterior.
        Permite que preguntas de seguimiento como "muéstramelos" o "¿cuánto cuesta?"
        funcionen correctamente sin perder el hilo de la conversación.
        """
        memory = memory or {}

        # 1. Construir historial de texto para el prompt SQL
        hist_parts = []
        if memory.get('last_sql'):
            hist_parts.append(f"[CONSULTA ANTERIOR] SQL ejecutado: {memory['last_sql']}")
        if memory.get('last_context'):
            hist_parts.append(f"[DATOS ANTERIORES]: {memory['last_context'][:800]}")
        if history:
            hist_parts.append("\n".join([
                f"{msg['role'].upper()}: {msg['content']}" for msg in history[-6:]
            ]))
        hist_text = "\n".join(hist_parts)

        prompt = get_inventory_sql_prompt(user_msg, hist_text)

        # 2. Generar SQL
        try:
            logger.info(f"[INV-SQL] Generando SQL para: '{user_msg}'")
            res_sql = self.client.chat.completions.create(
                model=self.deployment,
                messages=[{"role": "user", "content": prompt}],
                temperature=0, max_tokens=300
            )
            sql_query = res_sql.choices[0].message.content.strip().replace("```sql", "").replace("```", "").strip()
            logger.info(f"[INV-SQL] SQL Generado: {sql_query}")
        except Exception as e:
            logger.error(f"[INV-SQL] Error Generando SQL: {e}")
            return {"success": False, "error": f"Error generando SQL: {e}"}

        # 3. Ejecutar SQL
        context = ""
        new_memory = dict(memory)  # preservar memoria previa por defecto
        
        if sql_query:
            results = self.query_db(sql_query)
            if results is None:
                context = "Error ejecutando la consulta en la base de datos."
                logger.error("[INV-DB] Error ejecutando query.")
            elif not results:
                context = f"La consulta devolvió 0 resultados. SQL: {sql_query}"
                logger.warning("[INV-DB] 0 Resultados.")
            else:
                logger.info(f"[INV-DB] {len(results)} registros encontrados.")
                if len(results) == 1 and len(results[0]) == 1:
                    val = list(results[0].values())[0]
                    context = f"Resultado (Dato Único): {val}"
                else:
                    context = f"Resultados ({len(results)} registros):\n{json.dumps(results[:20], default=str, indent=2)}"
                # Actualizar memoria con la consulta actual
                new_memory = {
                    "last_sql": sql_query,
                    "last_context": context,
                }
        else:
            context = "No se pudo generar una consulta SQL válida."

        # Si la consulta falló o no aportó datos, usar contexto anterior como fallback
        if not context or "0 resultados" in context or "No se pudo" in context:
            if memory.get('last_context'):
                context = (
                    f"[Contexto de consulta anterior que puede ser relevante]:\n{memory['last_context']}\n\n"
                    f"[Consulta actual]: {context}"
                )

        # 4. Respuesta Final
        try:
            sys_prompt = get_inventory_system_prompt(context)
            messages = [{"role": "system", "content": sys_prompt}]

            if history:
                for msg in history[-8:]:
                    messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})

            messages.append({"role": "user", "content": user_msg})

            res_chat = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                temperature=0.3
            )
            return {
                "success": True,
                "respuesta": res_chat.choices[0].message.content,
                "memory": new_memory,  # app.py lo extrae y guarda
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

inventory_agent = InventoryAgent()

