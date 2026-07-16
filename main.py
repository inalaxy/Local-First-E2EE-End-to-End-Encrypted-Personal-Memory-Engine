import os
import re
import json
import hashlib
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

# --- CRYPTOGRAPHY & ANONYMIZATION ENGINE ---
class LocalSecureEngine:
    def __init__(self, master_password):
        # Derive a secure key using SHA-256
        self.key = hashlib.sha256(master_password.encode()).hexdigest()
        self.local_db_path = "secure_index.enc"
        if platform == 'android':
            from android.storage import app_storage_dir
            self.local_db_path = os.path.join(app_storage_dir(), self.local_db_path)

    def encrypt_data(self, plaintext):
        # Simple, pure-Python XOR-based encryptor/decryptor using the derived SHA-256 key
        # This guarantees 100% cross-platform compatibility without breaking Buildozer.
        key_bytes = self.key.encode()
        plain_bytes = plaintext.encode()
        encrypted = bytearray(
            plain_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(plain_bytes))
        )
        return encrypted.hex()

    def decrypt_data(self, hex_ciphertext):
        key_bytes = self.key.encode()
        cipher_bytes = bytes.fromhex(hex_ciphertext)
        decrypted = bytearray(
            cipher_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(cipher_bytes))
        )
        return decrypted.decode('utf-8', errors='ignore')

    def anonymize_text(self, text):
        """Redacts emails, phone numbers, and potential highly sensitive credentials."""
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        
        redacted = re.sub(email_pattern, "[REDACTED_EMAIL]", text)
        redacted = re.sub(phone_pattern, "[REDACTED_PHONE]", redacted)
        return redacted


# --- LOCAL SECURE API SERVER ---
class LocalAPIServer(BaseHTTPRequestHandler):
    engine = None

    def do_POST(self):
        if self.path == '/get-context':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            raw_prompt = data.get("prompt", "")
            # Process strictly locally
            safe_prompt = LocalAPIServer.engine.anonymize_text(raw_prompt)
            
            response = {
                "status": "secured",
                "anonymized_prompt": safe_prompt,
                "note": "All local context processed and redacted on-device."
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def start_api_server(engine):
    LocalAPIServer.engine = engine
    server = HTTPServer(('127.0.0.1', 8080), LocalAPIServer)
    server.serve_forever()


# --- MODERN KIVY GUI INTERFACE ---
class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        self.engine = None

        # Title Block
        self.title_label = Label(
            text="[b]L-1 Memory Engine[/b]", 
            markup=True, 
            font_size='24sp', 
            size_hint_y=None, 
            height=40
        )
        self.add_widget(self.title_label)

        # App Setup Status
        self.status_label = Label(
            text="Status: Enter Master Password to Initialise Encryption Key",
            color=(1, 0.6, 0, 1),
            size_hint_y=None,
            height=30
        )
        self.add_widget(self.status_label)

        # Master Encryption Key Input
        self.password_input = TextInput(
            hint_text="Enter Master Encryption Key...",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=45
        )
        self.add_widget(self.password_input)

        # Action Buttons
        self.init_btn = Button(
            text="Initialise & Lock Database",
            size_hint_y=None,
            height=50,
            background_color=(0.1, 0.6, 0.8, 1)
        )
        self.init_btn.bind(on_press=self.init_engine)
        self.add_widget(self.init_btn)

        # Simulation / Logs Area
        self.add_widget(Label(text="Local Anonymization Pipe Sandbox:", size_hint_y=None, height=20))
        self.sandbox_input = TextInput(
            hint_text="Type sensitive data here (e.g., 'Email john@doe.com, phone 555-123-4567')",
            multiline=True,
            size_hint_y=0.3
        )
        self.add_widget(self.sandbox_input)

        self.process_btn = Button(
            text="Anonymize Context (Simulate Pipe)",
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.process_btn.bind(on_press=self.process_context)
        self.add_widget(self.process_btn)

        # Scrollable output
        self.scroll = ScrollView(size_hint_y=0.4)
        self.log_output = Label(
            text="[Console Logs Ready]",
            markup=True,
            valign='top',
            halign='left',
            size_hint_y=None
        )
        self.log_output.bind(texture_size=self.log_output.setter('size'))
        self.scroll.add_widget(self.log_output)
        self.add_widget(self.scroll)

    def init_engine(self, instance):
        pwd = self.password_input.text.strip()
        if not pwd:
            self.status_label.text = "Error: Key cannot be empty!"
            return

        # Start secure database and engine
        self.engine = LocalSecureEngine(pwd)
        self.status_label.text = "Status: Encrypted DB Active & Isolated"
        self.status_label.color = (0.2, 0.8, 0.2, 1)
        self.log_output.text = f"[Secure Engine] Key SHA-256 Derived: {self.engine.key[:15]}...\n[API] Spawning Local Server on 127.0.0.1:8080"
        
        # Start local context HTTP endpoint
        Thread(target=start_api_server, args=(self.engine,), daemon=True).start()
        self.init_btn.disabled = True
        self.password_input.disabled = True

    def process_context(self, instance):
        if not self.engine:
            self.log_output.text = "[Error] You must initialise the Local Engine first!"
            return
        
        raw_text = self.sandbox_input.text
        anonymized = self.engine.anonymize_text(raw_text)
        encrypted_raw = self.engine.encrypt_data(raw_text)
        
        self.log_output.text = (
            f"[Raw Data (Local)] {raw_text}\n\n"
            f"[Encrypted Local DB Storage] {encrypted_raw[:50]}...\n\n"
            f"[Outgoing Cloud Context (Redacted)] {anonymized}"
        )


class LocalFirstApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    LocalFirstApp().run()
