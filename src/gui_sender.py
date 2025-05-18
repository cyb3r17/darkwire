import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, StringVar
import threading
import time
import serial
import serial.tools.list_ports
from bitcoinlib.wallets import Wallet, wallet_exists, WalletError
import re

class CyberpunkWalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("darkwire v1.0")
        self.root.geometry("900x700")
        self.root.configure(bg="#0a0a0a")
        
       #color var
        self.colors = {
            'dark': "#0a0a0a",
            'darker': "#000000",
            'light': "#00ff41",
            'light_dim': "#11a836",
            'light_dimmer': "#0d7a28",
            'mid_gray': "#111",
            'light_gray': "#333",
            'accent': "#ff003c",
            'accent_dim': "#aa0029",
            'accent2': "#00b4d8",
            'terminal_bg': "#000a02"
        }
        
        # Set fonts
        self.font_normal = ("Courier New", 10)
        self.font_bold = ("Courier New", 11, "bold")
        self.font_large = ("Courier New", 14, "bold")
        self.font_title = ("Courier New", 22, "bold")
        
    
        self.wallet_name = StringVar(value="shunya_test_wallet")
        self.destination_address = StringVar(value="tb1qlj64u6fqutr0xue85kl55fx0gt4m4urun25p7q")
        self.amount = StringVar(value="4000")
        self.selected_port = StringVar()
        self.status_text = StringVar(value="SYSTEM READY")
        self.transaction_hex = ""

        self.ser = None
        self.ports_list = []
        self.mode = StringVar(value="bitcoin")
        self.message_text = StringVar()
     
        self.create_ui()
        self.update_mode()
        
       
        self.refresh_ports()
        
    def create_ui(self):
        """Create the cyberpunk-styled UI"""
      
        style = ttk.Style()
        style.theme_use('default')
        
      
        style.configure('TFrame', background=self.colors['dark'])
        style.configure('TLabel', 
                        background=self.colors['dark'], 
                        foreground=self.colors['light'],
                        font=self.font_normal)
        style.configure('TButton', 
                        background=self.colors['accent_dim'],
                        foreground="white",
                        borderwidth=1,
                        focusthickness=3,
                        focuscolor=self.colors['accent'])
        style.map('TButton',
                background=[('active', self.colors['accent'])],
                foreground=[('active', 'white')])
        style.configure('Terminal.TFrame', 
                        background=self.colors['terminal_bg'],
                        borderwidth=1,
                        relief="solid")
        
     
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
      
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(header, 
                              text="darkwire",
                              font=self.font_title,
                              fg=self.colors['light'],
                              bg=self.colors['dark'])
        title_label.pack(pady=10)
        
        subtitle = tk.Label(header,
                           text="< The internet is optional. Freedom isn't. >",
                           font=self.font_normal,
                           fg=self.colors['light'],
                           bg=self.colors['dark'])
        subtitle.pack()
        
       
        columns_frame = ttk.Frame(main_frame)
        columns_frame.pack(fill=tk.BOTH, expand=True)
        
        left_frame = ttk.Frame(columns_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.left_frame = left_frame 
        right_frame = ttk.Frame(columns_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        

        mode_frame = ttk.Frame(header)
        mode_frame.pack(pady=10)

        mode_label = tk.Label(mode_frame, 
                            text="MODE:",
                            font=self.font_bold,
                            fg=self.colors['light'],
                            bg=self.colors['dark'])
        mode_label.pack(side=tk.LEFT, padx=(0, 10))

      
        bitcoin_radio = tk.Radiobutton(mode_frame,
                                    text="BITCOIN",
                                    variable=self.mode,
                                    value="bitcoin",
                                    command=self.update_mode,
                                    selectcolor=self.colors['dark'],
                                    bg=self.colors['dark'],
                                    fg=self.colors['light'],
                                    activebackground=self.colors['dark'],
                                    activeforeground=self.colors['accent'],
                                    font=self.font_bold)
        bitcoin_radio.pack(side=tk.LEFT, padx=10)

      
        message_radio = tk.Radiobutton(mode_frame,
                                    text="MESSAGES",
                                    variable=self.mode,
                                    value="messages",
                                    command=self.update_mode,
                                    selectcolor=self.colors['dark'],
                                    bg=self.colors['dark'],
                                    fg=self.colors['light'],
                                    activebackground=self.colors['dark'],
                                    activeforeground=self.colors['accent'],
                                    font=self.font_bold)
        message_radio.pack(side=tk.LEFT, padx=10)

      
        wallet_frame = self.create_section(left_frame, "WALLET CONFIG")
        
     
        ttk.Label(wallet_frame, text="WALLET ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        wallet_entry = tk.Entry(wallet_frame, 
                              textvariable=self.wallet_name,
                              bg=self.colors['mid_gray'],
                              fg=self.colors['light'],
                              insertbackground=self.colors['light'],
                              relief=tk.FLAT,
                              highlightthickness=1,
                              highlightcolor=self.colors['light_dim'],
                              highlightbackground=self.colors['light_dimmer'],
                              font=self.font_normal)
        wallet_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        

        self.wallet_entry = wallet_entry

      
        balance_frame = ttk.Frame(wallet_frame)
        balance_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Label(balance_frame, text="BTC BALANCE:").pack(side=tk.LEFT)
        self.balance_label = tk.Label(balance_frame, 
                                    text="-- NOT LOADED --", 
                                    font=self.font_bold,
                                    bg=self.colors['dark'],
                                    fg=self.colors['accent2'])
        self.balance_label.pack(side=tk.LEFT, padx=10)
        

        wallet_btn_frame = ttk.Frame(wallet_frame)
        wallet_btn_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=5)
        
        self.load_wallet_btn = self.create_button(wallet_btn_frame, "LOAD WALLET", self.load_wallet)
        self.load_wallet_btn.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
       
        tx_frame = self.create_section(left_frame, "TRANSACTION DETAILS")
        
       
        ttk.Label(tx_frame, text="DESTINATION:").grid(row=0, column=0, sticky=tk.W, pady=5)
        dest_entry = tk.Entry(tx_frame, 
                            textvariable=self.destination_address,
                            bg=self.colors['mid_gray'],
                            fg=self.colors['light'],
                            insertbackground=self.colors['light'],
                            relief=tk.FLAT,
                            highlightthickness=1,
                            highlightcolor=self.colors['light_dim'],
                            highlightbackground=self.colors['light_dimmer'],
                            font=self.font_normal,
                            width=40)
        dest_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        self.dest_entry = dest_entry

       
        ttk.Label(tx_frame, text="AMOUNT (SATS):").grid(row=1, column=0, sticky=tk.W, pady=5)
        amount_entry = tk.Entry(tx_frame, 
                              textvariable=self.amount,
                              bg=self.colors['mid_gray'],
                              fg=self.colors['light'],
                              insertbackground=self.colors['light'],
                              relief=tk.FLAT,
                              highlightthickness=1,
                              highlightcolor=self.colors['light_dim'],
                              highlightbackground=self.colors['light_dimmer'],
                              font=self.font_normal)
        amount_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        self.amount_entry = amount_entry
        
        fee_info_label = tk.Label(tx_frame, 
                               text="* NETWORK FEES CALCULATED AUTOMATICALLY", 
                               fg=self.colors['light_dim'],
                               bg=self.colors['dark'],
                               font=("Courier New", 8))
        fee_info_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
   
        self.create_tx_btn = self.create_button(tx_frame, "GENERATE TRANSACTION", self.create_transaction)
        self.create_tx_btn.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
       
        arduino_frame = self.create_section(right_frame, "HARDWARE INTERFACE")
        
       
        ttk.Label(arduino_frame, text="COM PORT:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
     
        port_frame = ttk.Frame(arduino_frame)
        port_frame.grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        self.port_combo = ttk.Combobox(port_frame, 
                                     textvariable=self.selected_port,
                                     state="readonly",
                                     font=self.font_normal,
                                     width=15)
        self.port_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        refresh_btn = self.create_button(port_frame, "↻", self.refresh_ports)
        refresh_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
     
        self.connect_btn = self.create_button(arduino_frame, "CONNECT", self.toggle_connection)
        self.connect_btn.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=5)
        
    
        self.send_tx_btn = self.create_button(arduino_frame, "TRANSMIT TO DEVICE", self.send_transaction)
        self.send_tx_btn.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=5)
        self.send_tx_btn.config(state=tk.DISABLED)
        
       
        terminal_frame = self.create_section(right_frame, "TERMINAL OUTPUT")
        
        self.terminal = scrolledtext.ScrolledText(terminal_frame, 
                                              bg=self.colors['terminal_bg'],
                                              fg=self.colors['light'],
                                              font=("Courier New", 9),
                                              height=15,
                                              relief=tk.FLAT,
                                              borderwidth=1,
                                              highlightthickness=1,
                                              highlightcolor=self.colors['light_dim'],
                                              highlightbackground=self.colors['light_dimmer'])
        self.terminal.grid(row=0, column=0, sticky=tk.NSEW, pady=5)
        self.terminal.insert(tk.END, "[ SYSTEM INITIALIZED ]\n")
        self.terminal.configure(state='disabled')
        
     
        terminal_frame.grid_rowconfigure(0, weight=1)
        terminal_frame.grid_columnconfigure(0, weight=1)
        
      
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(20, 0))
        
        status_prefix = tk.Label(status_frame, text="STATUS:", 
                               bg=self.colors['dark'],
                               fg=self.colors['light_dim'],
                               font=self.font_normal)
        status_prefix.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(status_frame, 
                                    textvariable=self.status_text,
                                    bg=self.colors['dark'],
                                    fg=self.colors['light'],
                                    font=self.font_bold)
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        
        for frame in [wallet_frame, tx_frame, arduino_frame]:
            frame.grid_columnconfigure(1, weight=1)
            
    def create_section(self, parent, title):
        """Create a section with a title and a frame"""
        section = ttk.Frame(parent)
        section.pack(fill=tk.BOTH, expand=True, pady=10)
        
      
        title_frame = ttk.Frame(section)
        title_frame.pack(fill=tk.X)
        
        title_prefix = tk.Label(title_frame, text="<", 
                              font=self.font_bold,
                              bg=self.colors['dark'],
                              fg=self.colors['accent'])
        title_prefix.pack(side=tk.LEFT)
        
        title_label = tk.Label(title_frame, text=title, 
                             font=self.font_bold,
                             bg=self.colors['dark'],
                             fg=self.colors['light'])
        title_label.pack(side=tk.LEFT)
        
        title_suffix = tk.Label(title_frame, text=">", 
                              font=self.font_bold,
                              bg=self.colors['dark'],
                              fg=self.colors['accent'])
        title_suffix.pack(side=tk.LEFT)
        
        # Separator line
        separator = ttk.Frame(section, height=1, style="Terminal.TFrame")
        separator.pack(fill=tk.X, pady=5)
        
        # Content frame
        content = ttk.Frame(section)
        content.pack(fill=tk.BOTH, expand=True, pady=5)
        
        return content
    
    def create_button(self, parent, text, command):
        """Create a custom styled button"""
        btn = tk.Button(parent, 
                      text=text,
                      command=command,
                      bg=self.colors['accent_dim'],
                      fg="white",
                      activebackground=self.colors['accent'],
                      activeforeground="white",
                      relief=tk.FLAT,
                      borderwidth=0,
                      highlightthickness=1,
                      highlightcolor=self.colors['accent'],
                      highlightbackground=self.colors['accent_dim'],
                      font=self.font_bold,
                      padx=10,
                      pady=5,
                      cursor="hand2")
        return btn
    

    def update_mode(self):
        """Update UI based on selected mode"""
        mode = self.mode.get()
        
        if mode == "bitcoin":
           
            for widget in [self.wallet_entry, self.load_wallet_btn, 
                        self.dest_entry, self.amount_entry, 
                        self.create_tx_btn]:
                widget.config(state=tk.NORMAL)
            
          
            if hasattr(self, 'message_frame'):
                self.message_frame.pack_forget()
        else:
            
            for widget in [self.wallet_entry, self.load_wallet_btn, 
                        self.dest_entry, self.amount_entry, 
                        self.create_tx_btn]:
                widget.config(state=tk.DISABLED)
            
           
            if hasattr(self, 'message_frame'):
                self.message_frame.pack(fill=tk.BOTH, expand=True, pady=5)
            else:
                self.create_message_ui()

    
    def create_message_ui(self):
        """Create UI for the messages mode"""
        self.message_frame = ttk.Frame(self.left_frame)
        self.message_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        message_section = self.create_section(self.message_frame, "MESSAGE")
        
       
        ttk.Label(message_section, text="MESSAGE:").grid(row=0, column=0, sticky=tk.NW, pady=5)
        
        self.message_input = scrolledtext.ScrolledText(message_section, 
                                                    bg=self.colors['mid_gray'],
                                                    fg=self.colors['light'],
                                                    height=5,
                                                    width=30,
                                                    insertbackground=self.colors['light'],
                                                    relief=tk.FLAT,
                                                    highlightthickness=1,
                                                    highlightcolor=self.colors['light_dim'],
                                                    highlightbackground=self.colors['light_dimmer'],
                                                    font=self.font_normal)
        self.message_input.grid(row=0, column=1, sticky=tk.NSEW, pady=5)
        
       
        counter_frame = ttk.Frame(message_section)
        counter_frame.grid(row=1, column=0, columnspan=2, sticky=tk.E, pady=5)
        
        self.byte_counter = tk.Label(counter_frame,
                                text="0/400 bytes",
                                bg=self.colors['dark'],
                                fg=self.colors['light_dim'],
                                font=self.font_normal)
        self.byte_counter.pack(side=tk.RIGHT)
        
      
        self.message_input.bind("<KeyRelease>", self.update_byte_counter)
        
       
        self.send_msg_btn = self.create_button(message_section, "SEND MESSAGE", self.send_message)
        self.send_msg_btn.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        message_section.grid_columnconfigure(1, weight=1)

  
    def update_byte_counter(self, event=None):
        """Update the byte counter for the message input"""
        message = self.message_input.get("1.0", tk.END)
        bytes_length = len(message.encode('utf-8')) - 1  
        
        if bytes_length > 400:
            
            self.byte_counter.config(fg=self.colors['accent'])
        else:
            self.byte_counter.config(fg=self.colors['light_dim'])
            
        self.byte_counter.config(text=f"{bytes_length}/400 bytes")

    def send_message(self):
        """Send message to Arduino"""
        if not self.ser or not self.ser.is_open:
            self.log("Not connected to device", "ERROR")
            return
            
        message = self.message_input.get("1.0", tk.END).strip()
        bytes_length = len(message.encode('utf-8'))
        
        if bytes_length > 400:
            self.log(f"Message too large: {bytes_length} bytes (max 400)", "ERROR")
            return
            
        if not message:
            self.log("Message is empty", "ERROR")
            return
            
        self.log(f"Sending message ({bytes_length} bytes)...")
        self.set_status("SENDING MESSAGE...")
        
        # Run in a thread to keep UI responsive
        threading.Thread(target=self._send_message_thread, args=(message,), daemon=True).start()

    def _send_message_thread(self, message):
        """Background thread for sending message to Arduino"""
        try:
            # Add explicit newline to ensure proper transmission
            if not message.endswith('\n'):
                message += '\n'
            
            self.ser.write(message.encode('utf-8'))
            self.ser.flush()  # Ensure data is sent immediately
            
            # Wait for response with timeout
            self.root.after(0, lambda: self.log("Message sent", "SUCCESS"))
            
            # Read response from Arduino with timeout
            timeout_start = time.time()
            max_wait_time = 5  # 5 seconds max wait time
            
            while time.time() - timeout_start < max_wait_time:
                if self.ser and self.ser.is_open and self.ser.in_waiting > 0:
                    try:
                        response = self.ser.readline().decode('utf-8').strip()
                        if response:
                            self.root.after(0, lambda r=response: self.log(f"Device: {r}", "DEVICE"))
                    except UnicodeDecodeError:
                        # Handle potential binary data
                        self.root.after(0, lambda: self.log("Received non-text data from device", "DEVICE"))
                
                # Small pause between checks
                time.sleep(0.1)
                    
            self.root.after(0, lambda: self.set_status("MESSAGE SENT"))
            
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Error sending message: {str(e)}", "ERROR"))
            self.root.after(0, lambda: self.set_status("TRANSMISSION FAILED"))


    def log(self, message, level="INFO"):
        """Add a message to the terminal"""
        self.terminal.configure(state='normal')
        
        timestamp = time.strftime('%H:%M:%S')
        
        if level == "INFO":
            prefix = f"[{timestamp}] > "
            color = self.colors['light']
        elif level == "ERROR":
            prefix = f"[{timestamp}] ERROR: "
            color = self.colors['accent']
        elif level == "SUCCESS":
            prefix = f"[{timestamp}] SUCCESS: "
            color = self.colors['light_dim']
        else:
            prefix = f"[{timestamp}] {level}: "
            color = self.colors['accent2']
        
        self.terminal.insert(tk.END, prefix + message + "\n")
        
        # Auto-scroll to the end
        self.terminal.see(tk.END)
        self.terminal.configure(state='disabled')
        
    def set_status(self, message):
        """Update status bar message"""
        self.status_text.set(message)
        
    def refresh_ports(self):
        """Refresh available COM ports"""
        self.ports_list = [port.device for port in serial.tools.list_ports.comports()]
        
        if not self.ports_list:
            self.ports_list = ["No ports available"]
            
        self.port_combo['values'] = self.ports_list
        
        if self.ports_list and self.ports_list[0] != "No ports available":
            self.port_combo.current(0)
            self.log(f"Found {len(self.ports_list)} COM ports")
        else:
            self.log("No COM ports detected", "ERROR")
            
    def toggle_connection(self):
        """Connect or disconnect from the selected serial port"""
        if self.ser and self.ser.is_open:
            # Disconnect
            try:
                self.ser.close()
                self.log("Disconnected from device")
                self.connect_btn.config(text="CONNECT")
                self.set_status("DISCONNECTED")
                self.send_tx_btn.config(state=tk.DISABLED)
            except Exception as e:
                self.log(f"Error disconnecting: {str(e)}", "ERROR")
        else:
            # Connect
            port = self.selected_port.get()
            if not port or port == "No ports available":
                self.log("No valid port selected", "ERROR")
                return
            
            try:
                self.ser = serial.Serial(port, 9600, timeout=1)
                time.sleep(2)  # Give time for Arduino to reset
                self.log(f"Connected to {port}")
                self.connect_btn.config(text="DISCONNECT")
                self.set_status(f"CONNECTED TO {port}")
                
                # Enable send button if transaction exists
                if self.transaction_hex:
                    self.send_tx_btn.config(state=tk.NORMAL)
            except Exception as e:
                self.log(f"Connection error: {str(e)}", "ERROR")
                self.set_status("CONNECTION FAILED")
                
    def load_wallet(self):
        """Load the Bitcoin wallet and display balance"""
        wallet_name = self.wallet_name.get().strip()
        
        if not wallet_name:
            self.log("Please enter a wallet name", "ERROR")
            return
        
        self.log(f"Loading wallet: {wallet_name}...")
        self.set_status("LOADING WALLET...")
        
        # Run in a thread to keep UI responsive
        threading.Thread(target=self._load_wallet_thread, args=(wallet_name,), daemon=True).start()
            
    def _load_wallet_thread(self, wallet_name):
        """Background thread for wallet loading"""
        try:
            if not wallet_exists(wallet_name):
                self.log(f"Wallet '{wallet_name}' does not exist", "ERROR")
                self.set_status("WALLET NOT FOUND")
                return
                
            wallet = Wallet(wallet_name)
            wallet.utxos_update()  # Update UTXOs
            balance = wallet.balance() / 100000000  # Convert sats to BTC
            
            # Update UI in main thread
            self.root.after(0, lambda: self._update_wallet_ui(balance))
            
        except WalletError as e:
            self.root.after(0, lambda: self.log(f"Wallet error: {str(e)}", "ERROR"))
            self.root.after(0, lambda: self.set_status("WALLET ERROR"))
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Error loading wallet: {str(e)}", "ERROR"))
            self.root.after(0, lambda: self.set_status("ERROR"))
            
    def _update_wallet_ui(self, balance):
        """Update UI with wallet information"""
        self.balance_label.config(text=f"{balance:.8f} BTC")
        self.log(f"Wallet loaded successfully. Balance: {balance:.8f} BTC", "SUCCESS")
        self.set_status("WALLET LOADED")
        
    def create_transaction(self):
        """Create Bitcoin transaction"""
        wallet_name = self.wallet_name.get().strip()
        address = self.destination_address.get().strip()
        
        # Validate inputs
        try:
            amount = int(self.amount.get().strip())
        except ValueError:
            self.log("Amount must be an integer (in satoshis)", "ERROR")
            return
            
        if not re.match(r'^[a-zA-Z0-9]{25,}$', address):
            self.log("Invalid Bitcoin address format", "ERROR")
            return
            
        self.log(f"Creating transaction: {amount} satoshis to {address}")
        self.set_status("GENERATING TRANSACTION...")
        
        # Run in a thread to keep UI responsive
        threading.Thread(target=self._create_tx_thread, 
                         args=(wallet_name, address, amount), 
                         daemon=True).start()
            
    def _create_tx_thread(self, wallet_name, address, amount):
        """Background thread for transaction creation"""
        try:
            if not wallet_exists(wallet_name):
                self.root.after(0, lambda: self.log(f"Wallet '{wallet_name}' does not exist", "ERROR"))
                self.root.after(0, lambda: self.set_status("WALLET NOT FOUND"))
                return
                
            wallet = Wallet(wallet_name)
            
            # Let bitcoinlib calculate the appropriate fee
            transaction = wallet.send([(address, amount)], fee=None, broadcast=False)
            raw_tx = transaction.raw_hex()
            
            # Update UI in main thread
            self.root.after(0, lambda: self._update_transaction_ui(raw_tx, address, amount, transaction.fee))
            
        except WalletError as e:
            self.root.after(0, lambda: self.log(f"Wallet error: {str(e)}", "ERROR"))
            self.root.after(0, lambda: self.set_status("TRANSACTION FAILED"))
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Error creating transaction: {str(e)}", "ERROR"))
            self.root.after(0, lambda: self.set_status("ERROR"))
            
    def _update_transaction_ui(self, tx_hex, address, amount, fee):
        """Update UI with transaction information"""
        # Store the transaction hex
        self.transaction_hex = tx_hex
        
        # Log transaction details
        self.log(f"Transaction created successfully:", "SUCCESS")
        self.log(f"Destination: {address}", "TX")
        self.log(f"Amount: {amount} satoshis ({amount/100000000:.8f} BTC)", "TX")
        self.log(f"Network Fee: {fee} satoshis ({fee/100000000:.8f} BTC)", "TX")
        
        # Truncated transaction hex for display
        truncated_hex = tx_hex
        self.log(f"Transaction hex: {truncated_hex}", "TX")
        
        self.set_status("TRANSACTION READY")
        
        # Enable send button if connected
        if self.ser and self.ser.is_open:
            self.send_tx_btn.config(state=tk.NORMAL)
            
    

    def send_transaction(self):
        """Send transaction to Arduino"""
       
        if self.mode.get() == "messages":
            self.send_message()
            return
            
       
        if not self.transaction_hex:
            self.log("No transaction available to send", "ERROR")
            return
            
        if not self.ser or not self.ser.is_open:
            self.log("Not connected to device", "ERROR")
            return
            
        self.log("Sending transaction to device...")
        self.set_status("TRANSMITTING...")
        
       
        threading.Thread(target=self._send_tx_thread, daemon=True).start()
            
    def _send_tx_thread(self):
        """Background thread for sending data to Arduino"""
        try:
            tx_data = self.transaction_hex
            
            
            self.root.after(0, lambda: self.log(f"Transaction length: {len(tx_data)} bytes"))
            
           
            if not tx_data.endswith('\n'):
                tx_data += '\n'
            
         
            chunk_size = 256  # Smaller chunk size
            
            for i in range(0, len(tx_data), chunk_size):
                chunk = tx_data[i:i+chunk_size]
                self.ser.write(chunk.encode('utf-8'))
                self.ser.flush()  
                
               
                if i % 1024 == 0:
                    percent = min(100, int((i / len(tx_data)) * 100))
                    self.root.after(0, lambda p=percent: self.log(f"Sent {p}% of transaction..."))
                
                
                time.sleep(0.1)  
            
            
            self.ser.write(b'\n')
            self.ser.flush()
                
           
            self.root.after(0, lambda: self.log("Transaction sent to device", "SUCCESS"))
            
           
            timeout_start = time.time()
            max_wait_time = 10  
            
         
            while time.time() - timeout_start < max_wait_time:
                if self.ser and self.ser.is_open and self.ser.in_waiting > 0:
                    try:
                        response = self.ser.readline().decode('utf-8').strip()
                        if response:
                            self.root.after(0, lambda r=response: self.log(f"Device: {r}", "DEVICE"))
                            
                            timeout_start = time.time()
                    except UnicodeDecodeError:
                        
                        self.root.after(0, lambda: self.log("Received non-text data from device", "DEVICE"))
                
              
                time.sleep(0.1)
                    
            self.root.after(0, lambda: self.set_status("TRANSMISSION COMPLETE"))
            
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Error sending data: {str(e)}", "ERROR"))
            self.root.after(0, lambda: self.set_status("TRANSMISSION FAILED"))

def main():
    root = tk.Tk()
    app = CyberpunkWalletApp(root)
    photo = tk.PhotoImage(file = 'darkwire.png')
    root.wm_iconphoto(False, photo)
    
    
    root.mainloop()

if __name__ == "__main__":
    main()