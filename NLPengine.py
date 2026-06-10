import re

class NLPEngine:
    """
    Natural Language Processing Engine untuk Ciput Community Chatbot
    Digunakan untuk parsing pesanan dan deteksi intent
    """
    
    def __init__(self):
        """
        Inisialisasi NLP Engine dengan data menu, sinonim, dan regex patterns
        """
        # Database Menu / Jasa Fotografi Ciput Community
        self.menu_data = {
            "studio": {
                "price": 150000,
                "emoji": "📸",
                "desc": "Sewa Studio Indoor (per jam)"
            },
            "outdoor": {
                "price": 250000,
                "emoji": "🌳",
                "desc": "Sesi Foto Outdoor (per jam)"
            },
            "event": {
                "price": 500000,
                "emoji": "🎉",
                "desc": "Dokumentasi Event (per jam)"
            },
            "editing": {
                "price": 50000,
                "emoji": "🖥️",
                "desc": "Editing Premium (per foto)"
            },
            "lighting": {
                "price": 100000,
                "emoji": "💡",
                "desc": "Lighting Setup Pro (flat)"
            },
            "model": {
                "price": 200000,
                "emoji": "👤",
                "desc": "Talent/Model Tambahan (flat)"
            }
        }

        # Sinonim item untuk berbagai bahasa
        self.item_synonyms = {
            "studio": ["studio", "indoor", "dalam ruangan", "studio indoor"],
            "outdoor": ["outdoor", "hunting", "luar ruangan", "out door"],
            "event": ["event", "acara", "wedding", "nikah", "dokumentasi", "pernikahan"],
            "editing": ["editing", "edit", "retouch", "retouching", "foto edit", "edit foto"],
            "lighting": ["lighting", "lampu", "light", "pencahayaan", "lighting setup"],
            "model": ["model", "talent", "peraga", "model tambahan", "figuran"]
        }

        # Regex Patterns
        self.re_number = r"\b(\d+)\b"  # Mencari angka: \d+ = satu atau lebih digit
        self.re_split = r"[,.]|\bdan\b|\b&\b|\band\b|\bwith\b|\blan\b|\bsarta\b|\s+"  # Pemisah kalimat

        # Regex untuk intent detection
        self.intent_patterns = {
            "why_ciput": r"(kenapa ciput|kenapa pilih ciput|mengapa ciput|alasan memilih ciput|why ciput|kelebihan ciput|keunggulan ciput|kenapa harus ciput)",
            "info": r"(info|tentang|komunitas|ciput|profil|about|community|sejarah|babagan)",
            "pricelist": r"(pricelist|harga|biaya|tarif|sewa|paket|daftar harga|price|cost|rate|fee|rent|packages)",
            "contact": r"(kontak|hubungi|telp|whatsapp|wa|instagram|ig|email|alamat|contact|call|phone|address)",
            "register": r"(daftar|register|member|pendaftaran|registrasi|gabung|join|signup|enroll|melu|ndaftar)",
            "booking": r"(booking|pesan|sewa jasa|order|reservasi|book|reserve|rent|pesen)",
            "checkout": r"\b(selesai|bayar|checkout|cukup|deal|lanjut|pay|finish|done|settle|rampung|wis)\b",
            "yes": r"\b(ya|yes|oke|betul|siap|baik|ok|bisa|sure|yeah|yup|okay|fine|correct|iyo|nggih|yo|bener|setuju|njh)\b",
            "no": r"\b(tidak|enggak|batal|no|salah|gak|nope|wrong|not|ora|mboten|durung)\b"
        }

    def _parse_single_segment(self, text):
        """
        Memproses satu potongan kalimat (private method)
        
        Args:
            text (str): Satu potongan kalimat, misal: "studio 2 jam"
            
        Returns:
            dict: Dictionary berisi item, qty, price, emoji, desc
            None: Jika tidak ada item yang dikenali
        """
        text = text.lower().strip()

        # 1. Cari Item berdasarkan sinonim
        matched_key = None
        for canonical_key, synonyms in self.item_synonyms.items():
            for synonym in synonyms:
                if re.search(rf"\b{re.escape(synonym)}\b", text):
                    matched_key = canonical_key
                    break
            if matched_key:
                break

        if not matched_key:
            return None

        # 2. Cari Jumlah / Durasi (Default 1)
        qty_match = re.search(self.re_number, text)
        qty = int(qty_match.group(1)) if qty_match else 1

        return {
            "item": matched_key,
            "qty": qty,
            "price": self.menu_data[matched_key]["price"],
            "emoji": self.menu_data[matched_key]["emoji"],
            "desc": self.menu_data[matched_key]["desc"]
        }

    def parse_orders(self, full_text):
        """
        Memecah kalimat majemuk menjadi list orders.
        Contoh: "booking studio 2 jam, 1 lighting, dan 5 editing"
        
        Args:
            full_text (str): Kalimat lengkap dari user
            
        Returns:
            list: List of dictionaries berisi order-item
        """
        # Hapus kata kunci booking di awal
        clean_text = full_text.lower()
        for keyword in ['booking', 'pesan', 'order', 'book', 'sewa', 'pesen']:
            clean_text = clean_text.replace(keyword, '')
        
        # Pecah kalimat berdasarkan pemisah
        segments = re.split(self.re_split, clean_text)
        found_orders = []

        for segment in segments:
            segment = segment.strip()
            if segment:
                order = self._parse_single_segment(segment)
                if order:
                    found_orders.append(order)

        return found_orders

    def detect_intent(self, text):
        """
        Mendeteksi intent dari input user menggunakan regex patterns
        
        Args:
            text (str): Input dari user
            
        Returns:
            str: Intent yang terdeteksi (WHY_CIPUT, INFO, PRICELIST, dll)
        """
        text = text.lower().strip()

        # Reset system
        if re.search(r"\b(reset|ulang|start over|new session)\b", text):
            return "RESET_SYSTEM"

        # Kenapa Ciput
        if re.search(self.intent_patterns["why_ciput"], text):
            return "WHY_CIPUT"

        # Pricelist / Harga
        if re.search(self.intent_patterns["pricelist"], text):
            return "ASK_PRICELIST"

        # Info komunitas
        if re.search(self.intent_patterns["info"], text):
            return "ASK_INFO"

        # Kontak
        if re.search(self.intent_patterns["contact"], text):
            return "ASK_CONTACT"

        # Registrasi member
        if re.search(self.intent_patterns["register"], text):
            return "REGISTER"

        # Booking
        if re.search(self.intent_patterns["booking"], text):
            return "BOOKING"

        # Checkout / selesai
        if re.search(self.intent_patterns["checkout"], text):
            return "CHECKOUT"

        # Yes / konfirmasi
        if re.search(self.intent_patterns["yes"], text):
            return "YES"

        # No / batal
        if re.search(self.intent_patterns["no"], text):
            return "NO"

        return "UNKNOWN"

    def print_menu(self):
        """
        Menampilkan daftar menu layanan Ciput Community
        
        Returns:
            str: String berisi daftar menu lengkap dengan harga
        """
        menu_text = "\n" + "=" * 50 + "\n"
        menu_text += "📋 **DAFTAR LAYANAN CIPUT COMMUNITY**\n"
        menu_text += "=" * 50 + "\n\n"
        
        for key, item in self.menu_data.items():
            menu_text += f"  {item['emoji']} {item['desc']:<35} Rp {item['price']:>10,}\n"
        
        menu_text += "\n" + "-" * 50 + "\n"
        menu_text += "💡 Cara pemesanan:\n"
        menu_text += "   • Ketik 'booking <item> <jumlah>'\n"
        menu_text += "   • Contoh: 'booking studio 2 jam'\n"
        menu_text += "   • Contoh: 'outdoor 3 jam, 1 lighting'\n"
        menu_text += "=" * 50 + "\n"
        
        return menu_text

    def extract_booking_info(self, text):
        """
        Extract booking information from text (wrapper for parse_orders)
        
        Args:
            text (str): Input dari user
            
        Returns:
            dict: Dictionary dengan keys success, orders, total, message
        """
        orders = self.parse_orders(text)
        
        if orders:
            total = sum(order['price'] * order['qty'] for order in orders)
            return {
                "success": True,
                "orders": orders,
                "total": total,
                "message": f"Ditemukan {len(orders)} item pesanan"
            }
        
        return {
            "success": False,
            "orders": [],
            "total": 0,
            "message": "Tidak ada item pesanan yang dikenali"
        }

    def detect_language(self, text):
        """
        Mendeteksi bahasa input: 'id' (Indonesia), 'en' (Inggris), 'jv' (Jawa)
        
        Args:
            text (str): Input dari user
            
        Returns:
            str: Kode bahasa ('id', 'en', 'jv')
        """
        text = text.lower()
        
        # Kata kunci per bahasa
        en_words = [
            r"\b(price|pricelist|cost|rent|packages)\b",
            r"\b(info|about|community|what is)\b",
            r"\b(contact|call|phone|address)\b",
            r"\b(register|join|signup|member)\b",
            r"\b(booking|book|reserve|order)\b",
            r"\b(yes|no|cancel|done)\b"
        ]
        
        jv_words = [
            r"\b(sugeng|rawuh|rego|piye|pira)\b",
            r"\b(daftar|gabung|melu|pesen|sewa)\b",
            r"\b(iyo|nggih|yo|ora|mboten)\b"
        ]

        en_score = sum(1 for pattern in en_words if re.search(pattern, text))
        jv_score = sum(1 for pattern in jv_words if re.search(pattern, text))

        if en_score > jv_score and en_score > 0:
            return "en"
        elif jv_score > en_score and jv_score > 0:
            return "jv"
        return "id"


# Contoh penggunaan jika dijalankan langsung
if __name__ == "__main__":
    # Test NLPEngine
    nlp = NLPEngine()
    
    print("=" * 60)
    print("TESTING NLP ENGINE")
    print("=" * 60)
    
    # Test print_menu
    print("\n1. TEST PRINT MENU:")
    print(nlp.print_menu())
    
    # Test detect_intent
    print("\n2. TEST DETECT INTENT:")
    test_inputs = [
        "info tentang komunitas",
        "berapa harga sewa studio",
        "saya mau booking studio 2 jam",
        "kenapa harus pilih ciput",
        "kontak wa",
        "daftar member",
        "ya",
        "tidak",
        "selesai"
    ]
    
    for inp in test_inputs:
        intent = nlp.detect_intent(inp)
        print(f"  Input: '{inp}' → Intent: {intent}")
    
    # Test parse_orders
    print("\n3. TEST PARSE ORDERS:")
    test_orders = [
        "studio 2 jam",
        "outdoor 3 jam, 1 lighting",
        "booking 5 editing dan 1 model",
        "studio 2 jam, 1 lighting, 5 editing"
    ]
    
    for order in test_orders:
        result = nlp.parse_orders(order)
        print(f"  Input: '{order}'")
        for r in result:
            print(f"    → {r['emoji']} {r['desc']}: {r['qty']}x = Rp {r['price'] * r['qty']:,}")
    
    # Test extract_booking_info
    print("\n4. TEST EXTRACT BOOKING INFO:")
    result = nlp.extract_booking_info("studio 2 jam dan 1 lighting")
    print(f"  Success: {result['success']}")
    print(f"  Total: Rp {result['total']:,}")
    print(f"  Message: {result['message']}")
    
    # Test detect_language
    print("\n5. TEST DETECT LANGUAGE:")
    lang_tests = [
        ("Harga sewa studio berapa?", "id"),
        ("How much for studio rental?", "en"),
        ("Regane studio piro?", "jv")
    ]
    
    for inp, expected in lang_tests:
        detected = nlp.detect_language(inp)
        print(f"  Input: '{inp}' → Detected: {detected} (Expected: {expected}) {'✅' if detected == expected else '❌'}")
    
    print("\n" + "=" * 60)
    print("TESTING SELESAI")
    print("=" * 60)
