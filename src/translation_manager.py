"""
Translation Manager for multi-language support
Converted from C# TranslationManager class
"""

class TranslationManager:
    """Manages translations for all supported languages"""
    
    # Dictionary to store translations for all languages
    _translations = {
        "English": {},  # Default, no translations needed
        
        "Spain": {
            "window_title": "Mira Stealer - Panel de Control",
            "language_selector_title": "Seleccionar Idioma",
            "choose_language": "Elegir idioma:",
            "continue": "Continuar",
            "label1": "Registro total",
            "label3": "Durante todo este tiempo",
            "label6": "Última semana",
            "label4": "Durante toda la semana",
            "label9": "Últimos 30 días",
            "label7": "Durante todo el mes",
            "label12": "Contraseñas totales",
            "label10": "Durante todo el tiempo",
            "label85": "Constructor",
            "label88": "Todas las funciones están activadas automáticamente.",
            "label39": "Escuchar en el puerto elegido",
            "label37": "Estado",
            "simpleButton13": "Construir",
            "simpleButton2": "Guardar todos los registros en disco",
            "simpleButton3": "Verificador de registros",
            "simpleButton4": "Buscar *Metamask en disco",
            "simpleButton5": "Buscar *Todas las carteras en disco",
            "simpleButton6": "Borrar todos los registros",
            "simpleButton7": "Eliminar todos los registros",
            "simpleButton1": "Iniciar el servidor ZeroTrace en el puerto elegido",
            "simpleButton12": "Buscar *Billetera Metamask",
            "simpleButton11": "Buscar *Billetera Exodus",
            "simpleButton10": "Borrar lista de contraseñas",
            "simpleButton9": "Buscar *Sitio web específico",
            "simpleButton8": "Buscar *Contraseñas en disco",
            "accordionControlElement1": "Panel de control",
            "accordionControlElement2": "Registros",
            "accordionControlElement3": "Configuración del Stealer",
            "accordionControlElement4": "Acerca de",
            "accordionControlElement5": "Constructor",
            "accordionControlElement6": "Construir ZeroTrace",
            "accordionControlElement7": "Acerca de",
            "accordionControlElement8": "Salir del software",
            "accordionControlElement9": "Salir",
        },
        
        "Italian": {
            "window_title": "Mira Stealer - Pannello di Controllo",
            "language_selector_title": "Seleziona Lingua",
            "choose_language": "Scegli lingua:",
            "continue": "Continua",
            "label1": "Log totale",
            "label3": "Durante tutto questo tempo",
            "label6": "Ultima settimana",
            "label4": "Durante tutta la settimana",
            "label9": "Ultimi 30 giorni",
            "label7": "Durante tutto il mese",
            "label12": "Password totali",
            "label10": "Durante tutto il tempo",
            "label85": "Builder",
            "label88": "Tutte le funzionalità sono attivate automaticamente.",
            "label39": "Ascolta sulla porta scelta",
            "label37": "Stato",
            "simpleButton13": "Costruisci",
            "simpleButton2": "Salva tutti i log su disco",
            "simpleButton3": "Controllore dei log",
            "simpleButton4": "Cerca *Metamask su disco",
            "simpleButton5": "Cerca *Tutti i portafogli su disco",
            "simpleButton6": "Cancella tutti i log",
            "simpleButton7": "Elimina tutti i log",
            "simpleButton1": "Avvia il server ZeroTrace sulla porta scelta",
            "simpleButton12": "Cerca *Portafoglio Metamask",
            "simpleButton11": "Cerca *Portafoglio Exodus",
            "simpleButton10": "Cancella lista password",
            "simpleButton9": "Cerca *Sito web specifico",
            "simpleButton8": "Cerca *Password su disco",
            "accordionControlElement1": "Dashboard",
            "accordionControlElement2": "Log",
            "accordionControlElement3": "Impostazioni Stealer",
            "accordionControlElement4": "Informazioni",
            "accordionControlElement5": "Builder",
            "accordionControlElement6": "Costruisci ZeroTrace",
            "accordionControlElement7": "Informazioni",
            "accordionControlElement8": "Esci dal software",
            "accordionControlElement9": "Esci",
        },
        
        "France": {
            "window_title": "Mira Stealer - Panneau de Contrôle",
            "language_selector_title": "Sélectionner la Langue",
            "choose_language": "Choisir la langue:",
            "continue": "Continuer",
            "label1": "Journal total",
            "label3": "Pendant tout ce temps",
            "label6": "Semaine dernière",
            "label4": "Pendant toute la semaine",
            "label9": "30 derniers jours",
            "label7": "Pendant tout le mois",
            "label12": "Mots de passe totaux",
            "label10": "Pendant tout le temps",
            "label85": "Constructeur",
            "label88": "Toutes les fonctionnalités sont automatiquement activées.",
            "label39": "Écouter sur le port choisi",
            "label37": "Statut",
            "simpleButton13": "Construire",
            "simpleButton2": "Enregistrer tous les journaux sur le disque",
            "simpleButton3": "Vérificateur de journaux",
            "simpleButton4": "Rechercher *Metamask sur le disque",
            "simpleButton5": "Rechercher *Tous les portefeuilles sur le disque",
            "simpleButton6": "Effacer tous les journaux",
            "simpleButton7": "Supprimer tous les journaux",
            "simpleButton1": "Démarrer le serveur ZeroTrace sur le port choisi",
            "simpleButton12": "Rechercher *Portefeuille Metamask",
            "simpleButton11": "Rechercher *Portefeuille Exodus",
            "simpleButton10": "Effacer la liste des mots de passe",
            "simpleButton9": "Rechercher *Site web spécifique",
            "simpleButton8": "Rechercher *Mots de passe sur le disque",
            "accordionControlElement1": "Tableau de bord",
            "accordionControlElement2": "Journaux",
            "accordionControlElement3": "Paramètres du Stealer",
            "accordionControlElement4": "À propos",
            "accordionControlElement5": "Constructeur",
            "accordionControlElement6": "Construire ZeroTrace",
            "accordionControlElement7": "À propos",
            "accordionControlElement8": "Quitter le logiciel",
            "accordionControlElement9": "Quitter",
        },
        
        "Chinese": {
            "window_title": "Mira Stealer - 控制面板",
            "language_selector_title": "选择语言",
            "choose_language": "选择语言:",
            "continue": "继续",
            "label1": "总日志",
            "label3": "在此期间",
            "label6": "上周",
            "label4": "整周期间",
            "label9": "最近30天",
            "label7": "整月期间",
            "label12": "密码总数",
            "label10": "所有时间内",
            "label85": "构建器",
            "label88": "所有功能自动开启。",
            "label39": "监听所选端口",
            "label37": "状态",
            "simpleButton13": "构建",
            "simpleButton2": "将所有日志保存到磁盘",
            "simpleButton3": "日志检查器",
            "simpleButton4": "查找磁盘上的*Metamask",
            "simpleButton5": "查找磁盘上的*所有钱包",
            "simpleButton6": "清除所有日志",
            "simpleButton7": "删除所有日志",
            "simpleButton1": "在所选端口上启动ZeroTrace服务器",
            "simpleButton12": "查找*Metamask钱包",
            "simpleButton11": "查找*Exodus钱包",
            "simpleButton10": "清除所有密码列表",
            "simpleButton9": "查找*特定网站",
            "simpleButton8": "查找磁盘上的*密码",
            "accordionControlElement1": "仪表板",
            "accordionControlElement2": "日志",
            "accordionControlElement3": "Stealer设置",
            "accordionControlElement4": "关于",
            "accordionControlElement5": "构建器",
            "accordionControlElement6": "构建ZeroTrace",
            "accordionControlElement7": "关于",
            "accordionControlElement8": "退出软件",
            "accordionControlElement9": "退出",
        },
        
        "Deutsche": {
            "window_title": "Mira Stealer - Kontrollpanel",
            "language_selector_title": "Sprache auswählen",
            "choose_language": "Sprache wählen:",
            "continue": "Fortfahren",
            "label1": "Gesamtprotokoll",
            "label3": "Während dieser ganzen Zeit",
            "label6": "Letzte Woche",
            "label4": "Während der ganzen Woche",
            "label9": "Letzte 30 Tage",
            "label7": "Während des ganzen Monats",
            "label12": "Gesamtpasswörter",
            "label10": "Während der gesamten Zeit",
            "label85": "Builder",
            "label88": "Alle Funktionen sind automatisch aktiviert.",
            "label39": "Auf gewähltem Port hören",
            "label37": "Status",
            "simpleButton13": "Erstellen",
            "simpleButton2": "Alle Logs auf Festplatte speichern",
            "simpleButton3": "Log-Prüfer",
            "simpleButton4": "Suche *Metamask auf Festplatte",
            "simpleButton5": "Suche *Alle Wallets auf Festplatte",
            "simpleButton6": "Alle Logs löschen",
            "simpleButton7": "Alle Logs löschen",
            "simpleButton1": "ZeroTrace-Server auf gewähltem Port starten",
            "simpleButton12": "Suche *Metamask Wallet",
            "simpleButton11": "Suche *Exodus Wallet",
            "simpleButton10": "Passwortliste löschen",
            "simpleButton9": "Suche *Spezifische Website",
            "simpleButton8": "Suche *Passwörter auf Festplatte",
            "accordionControlElement1": "Dashboard",
            "accordionControlElement2": "Logs",
            "accordionControlElement3": "Stealer-Einstellungen",
            "accordionControlElement4": "Über",
            "accordionControlElement5": "Builder",
            "accordionControlElement6": "ZeroTrace erstellen",
            "accordionControlElement7": "Über",
            "accordionControlElement8": "Software beenden",
            "accordionControlElement9": "Beenden",
        }
    }
    
    @classmethod
    def get_translation(cls, language_name, key):
        """
        Get translation for a specific key and language
        
        Args:
            language_name (str): Name of the language
            key (str): Translation key
            
        Returns:
            str: Translated text or None if not found
        """
        if language_name == "English" or language_name not in cls._translations:
            return None  # Return None for English or unknown languages
            
        language_dict = cls._translations[language_name]
        return language_dict.get(key, None)
    
    @classmethod
    def get_supported_languages(cls):
        """Get list of supported languages"""
        return list(cls._translations.keys())
    
    @classmethod
    def translate_text(cls, text, language):
        """
        Helper method to translate text or return original if no translation
        
        Args:
            text (str): Original text
            language (str): Target language
            
        Returns:
            str: Translated text or original if no translation found
        """
        if language == "English":
            return text
            
        # For other languages, we'll need to implement reverse lookup
        # This is a simplified approach - in a real app you'd have better key mapping
        return text  # Return original text if no translation found