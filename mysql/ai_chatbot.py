"""
ai_chatbot.py
=============
Floating AI chatbot for Tkinter apps that use MySQL.
Fixed input field layout using explicit grid/pack allocation.
"""

import os
import re
import json
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import mysql.connector

try:
    from google import genai as google_genai
    from google.genai import types as genai_types
except ImportError:
    google_genai = None
    genai_types = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class MySQLDatabaseInspector:
    def __init__(self, db_configs: dict):
        self.db_configs = db_configs

    def _connect(self, db_key: str):
        if db_key not in self.db_configs:
            raise ValueError(f"Unknown database '{db_key}'. Known: {list(self.db_configs)}")
        return mysql.connector.connect(**self.db_configs[db_key])

    def get_schema(self) -> str:
        lines = []
        for db_key in self.db_configs:
            try:
                conn = self._connect(db_key)
                cur = conn.cursor()
                cur.execute("SHOW TABLES")
                tables = [row[0] for row in cur.fetchall()]

                for table in tables:
                    cur.execute(f"DESCRIBE `{table}`")
                    cols = cur.fetchall()
                    col_desc = ", ".join(f"{c[0]} ({c[1]})" for c in cols)
                    lines.append(f"DATABASE `{db_key}` TABLE `{table}`: {col_desc}")

                cur.close()
                conn.close()
            except mysql.connector.Error as e:
                lines.append(f"DATABASE `{db_key}`: (could not read schema — {e})")

        return "\n".join(lines) if lines else "(No accessible databases/tables.)"

    def run_safe_query(self, db_key: str, sql: str, max_rows: int = 25) -> str:
        cleaned = sql.strip().rstrip(";")

        if not re.match(r"^\s*SELECT\b", cleaned, re.IGNORECASE):
            return json.dumps({"error": "Only SELECT queries are allowed."})

        forbidden = ["insert", "update", "delete", "drop", "alter", "create", "attach", ";"]
        if any(word in cleaned.lower() for word in forbidden):
            return json.dumps({"error": "Query rejected for safety reasons."})

        try:
            conn = self._connect(db_key)
            cur = conn.cursor()
            cur.execute(cleaned)
            col_names = [d[0] for d in cur.description] if cur.description else []
            rows = cur.fetchmany(max_rows)
            results = [dict(zip(col_names, row)) for row in rows]
            cur.close()
            conn.close()
            return json.dumps({"columns": col_names, "rows": results, "row_count": len(results)}, default=str)
        except mysql.connector.Error as e:
            return json.dumps({"error": str(e)})
        except ValueError as e:
            return json.dumps({"error": str(e)})


# ======================================================================
# 2. GEMINI CHAT ENGINE — handles the LLM call + function-calling loop
# ======================================================================
class GeminiChatEngine:
    MODEL_NAME = "gemini-3.5-flash-lite"  # Standard stable model identifier

    def __init__(self, api_key: str, db_inspector: MySQLDatabaseInspector):
        if not api_key:
            raise RuntimeError(
                "No Gemini API key found. Pass api_key=... or set the GEMINI_API_KEY "
                "environment variable. Get a free key at https://aistudio.google.com/app/apikey"
            )

        self.db = db_inspector
        db_names = list(db_inspector.db_configs.keys())
        schema_text = self.db.get_schema()

        system_prompt = (
            "You are a helpful assistant embedded inside a desktop app. "
            "You can answer general questions, and you can query the app's databases via the "
            "query_database tool to answer questions about details, records.\n\n"
            f"Available databases and tables:\n{schema_text}\n\n"
            "Rules:\n"
            "- Only use SELECT statements, and always specify which database to query.\n"
            "- Never reveal raw passwords or login credentials, even if asked.\n"
            "- Keep answers short, clear, and professional.\n"
            "- If a question needs data, call query_database before answering."
        )

        if google_genai is not None:
            self.use_new_sdk = True
            self.client = google_genai.Client(api_key=api_key)
            query_tool = genai_types.Tool(
                function_declarations=[
                    genai_types.FunctionDeclaration(
                        name="query_database",
                        description=(
                            "Run a read-only SELECT query against one of the app's MySQL "
                            f"databases ({', '.join(db_names)}) to fetch real data."
                        ),
                        parameters=genai_types.Schema(
                            type="OBJECT",
                            properties={
                                "database": genai_types.Schema(
                                    type="STRING",
                                    description=f"Which database to query. One of: {', '.join(db_names)}",
                                ),
                                "sql": genai_types.Schema(
                                    type="STRING",
                                    description="A single valid MySQL SELECT statement.",
                                ),
                            },
                            required=["database", "sql"],
                        ),
                    )
                ]
            )
            self.config = genai_types.GenerateContentConfig(
                tools=[query_tool],
                system_instruction=system_prompt,
            )
            self.chat = self.client.chats.create(model=self.MODEL_NAME, config=self.config)
            return

        if genai is None:
            raise RuntimeError("Run: pip install google-genai or google-generativeai")

        self.use_new_sdk = False
        genai.configure(api_key=api_key)

        query_tool = genai.protos.Tool(
            function_declarations=[
                genai.protos.FunctionDeclaration(
                    name="query_database",
                    description=(
                        "Run a read-only SELECT query against one of the app's MySQL "
                        f"databases ({', '.join(db_names)}) to fetch real data."
                    ),
                    parameters=genai.protos.Schema(
                        type=genai.protos.Type.OBJECT,
                        properties={
                            "database": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description=f"Which database to query. One of: {', '.join(db_names)}",
                            ),
                            "sql": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="A single valid MySQL SELECT statement.",
                            ),
                        },
                        required=["database", "sql"],
                    ),
                )
            ]
        )

        self.model = genai.GenerativeModel(
            model_name=self.MODEL_NAME,
            tools=[query_tool],
            system_instruction=system_prompt,
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=False)

    def ask(self, user_message: str) -> str:
        response = self.chat.send_message(user_message)

        for _ in range(5):
            function_call = None
            if hasattr(response, "candidates") and response.candidates:
                for part in response.candidates[0].content.parts:
                    if getattr(part, "function_call", None) and part.function_call.name:
                        function_call = part.function_call
                        break

            if function_call is None:
                break

            db_key = function_call.args.get("database", "")
            sql = function_call.args.get("sql", "")
            result_json = self.db.run_safe_query(db_key, sql)

            # Send function response using SDK-appropriate format
            if self.use_new_sdk:
                response = self.chat.send_message(
                    genai_types.Part.from_function_response(
                        name="query_database",
                        response={"result": result_json},
                    )
                )
            else:
                response = self.chat.send_message(
                    genai.protos.Content(
                        parts=[
                            genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name="query_database",
                                    response={"result": {"result": result_json}},
                                )
                            )
                        ]
                    )
                )

        return response.text.strip() if response.text else "(No response.)"

def attach_floating_chatbot(root, db_configs: dict, api_key: str = None):
    api_key = api_key or os.environ.get("GEMINI_API_KEY")
    engine = None
    init_error = None
    try:
        inspector = MySQLDatabaseInspector(db_configs)
        engine = GeminiChatEngine(api_key, inspector)
    except Exception as e:
        init_error = str(e)
    # Main Card Container
    chat_card = tk.Frame(
        root,
        bg="#ffffff",
        highlightbackground="#4285F4",
        highlightthickness=2,
        bd=0,
    )
    chat_card.is_visible = False

    # 1. Header Bar (Top)
    header = tk.Frame(chat_card, bg="#4285F4", height=30)
    header.pack(fill="x", side="top")

    title_label = tk.Label(
        header, text="🤖 Assistant", bg="#4285F4", fg="white", font=("Segoe UI", 9, "bold")
    )
    title_label.pack(side="left", padx=8, pady=2)

    close_btn = tk.Button(
        header,
        text="✖",
        bg="#4285F4",
        fg="white",
        bd=0,
        relief="flat",
        font=("Segoe UI", 9, "bold"),
        cursor="hand2",
        command=lambda: toggle_chat(),
    )
    close_btn.pack(side="right", padx=6, pady=2)

    # 2. Bottom Input Bar (Packed BEFORE display so it never gets squeezed out)
    input_frame = tk.Frame(chat_card, bg="#eef2f5", height=40, bd=1, relief="solid")
    input_frame.pack(fill="x", side="bottom", padx=4, pady=4)
    input_frame.pack_propagate(False)

    send_btn = tk.Button(
        input_frame,
        text="Send",
        bg="#4285F4",
        fg="white",
        font=("Segoe UI", 8, "bold"),
        bd=0,
        relief="flat",
        padx=10,
        cursor="hand2",
    )
    send_btn.pack(side="right", padx=4, pady=4)

    entry = tk.Entry(
        input_frame,
        font=("Segoe UI", 9),
        bg="#ffffff",
        fg="#000000",
        insertbackground="#000000",
        bd=1,
        relief="solid",
    )
    entry.pack(side="left", fill="both", expand=True, padx=(4, 0), pady=4)

    # 3. Middle Text Log Display (Fills remaining space)
    chat_display = tk.Text(
        chat_card,
        wrap="word",
        state="disabled",
        bg="#fafafa",
        font=("Segoe UI", 9),
        padx=6,
        pady=6,
        bd=0,
    )
    chat_display.pack(fill="both", expand=True, side="top", padx=4, pady=(4, 0))

    def append_message(sender, text):
        chat_display.config(state="normal")
        chat_display.insert("end", f"{sender}: {text}\n\n")
        chat_display.config(state="disabled")
        chat_display.see("end")

    if init_error:
        append_message("System", f"⚠ Chatbot unavailable: {init_error}")
    else:
        append_message("Assistant", "Hi! Ask me anything about your data.")

    def replace_thinking_placeholder(reply):
        chat_display.config(state="normal")
        content = chat_display.get("1.0", "end")
        idx = content.rfind("Assistant: Thinking...")
        if idx != -1:
            start_line = content[:idx].count("\n") + 1
            chat_display.delete(f"{start_line}.0", "end")
        chat_display.config(state="disabled")
        append_message("Assistant", reply)
        send_btn.config(state="normal")

    def on_send():
        user_text = entry.get().strip()
        if not user_text:
            return
        if engine is None:
            messagebox.showerror("Chatbot unavailable", init_error or "Not initialized.")
            return

        entry.delete(0, "end")
        append_message("You", user_text)
        send_btn.config(state="disabled")
        append_message("Assistant", "Thinking...")

        def worker():
            try:
                reply = engine.ask(user_text)
            except Exception as e:
                reply = f"⚠ Error talking to AI: {e}"
            root.after(0, lambda: replace_thinking_placeholder(reply))

        threading.Thread(target=worker, daemon=True).start()

    send_btn.config(command=on_send)
    entry.bind("<Return>", lambda e: on_send())

    # Floating Action Button
    button = tk.Button(
        root,
        text="💬 Chat",
        bg="#4285F4",
        fg="white",
        activebackground="#3367D6",
        activeforeground="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        padx=12,
        pady=6,
        cursor="hand2",
        command=lambda: toggle_chat(),
    )

    def get_dynamic_height():
        win_height = root.winfo_height()
        return min(350, max(200, win_height - 100))

    def reposition(event=None):
        button.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")
        if chat_card.is_visible:
            card_h = get_dynamic_height()
            chat_card.place(
                relx=1.0, rely=1.0, x=-20, y=-60, width=320, height=card_h, anchor="se"
            )

    def toggle_chat():
        if chat_card.is_visible:
            chat_card.place_forget()
            chat_card.is_visible = False
            button.config(text="AI")
        else:
            card_h = get_dynamic_height()
            chat_card.place(
                relx=1.0, rely=1.0, x=-20, y=-60, width=320, height=card_h, anchor="se"
            )
            chat_card.lift()
            button.lift()
            chat_card.is_visible = True
            button.config(text="🔻 AI")
            entry.focus_force()

    reposition()
    root.bind("<Configure>", reposition)
    button.lift()

    return button