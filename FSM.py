from enum import Enum
import re
from datetime import datetime
from NLPengine import NLPEngine  

# State definition for FSM
class State(Enum):
    IDLE = "idle"
    ORDERING = "ordering"
    REG_NAME = "reg_name"
    REG_EMAIL = "reg_email"
    REG_PHONE = "reg_phone"
    REG_CONFIRM = "reg_confirm"
    CONFIRMATION = "confirmation"
    PAYMENT = "payment"


class CiputFSM:
    def __init__(self):
        self.state = State.IDLE
        self.language = "id"  # id, en, jv
        self.registration_data = {
            'name': '',
            'email': '',
            'phone': ''
        }
        self.cart = []
        self.last_response = ""
        self.nlp = NLPEngine()  # PERBAIKAN 2: Inisialisasi NLPEngine
        self.current_booking = {}
    
    # ==================== GREETING ====================
    def get_greeting(self):
        greetings = {
            'id': "Halo! Selamat datang di Ciput Community! 👋\n\nSaya Cici asisten virtual Ciput. Ada yang bisa saya bantu?\n\n• Ketik 'info' - Tentang komunitas\n• Ketik 'pricelist' - Daftar harga\n• Ketik 'kontak' - Hubungi kami\n• Ketik 'daftar' - Daftar member\n• Ketik 'booking' - Booking jasa\n• Ketik 'kenapa ciput' - Alasan memilih Ciput",
            'en': "Hello! Welcome to Ciput Community! 👋\n\nI'm Cici your virtual assistant. How can I help you?\n\n• Type 'info' - About community\n• Type 'pricelist' - Price list\n• Type 'contact' - Contact us\n• Type 'register' - Become a member\n• Type 'booking' - Book service\n• Type 'why ciput' - Why choose Ciput",
            'jv': "Halo! Sugeng rawuh ing Ciput Community! 👋\n\nKula asisten virtual Ciput. Menapa ingkang saget kula bantos?\n\n• Ketik 'info' - Babagan komunitas\n• Ketik 'pricelist' - Daftar rega\n• Ketik 'kontak' - Hubungi kita\n• Ketik 'daftar' - Daftar member\n• Ketik 'booking' - Booking jasa\n• Ketik 'kenapa ciput' - Alasan milih Ciput"
        }
        return greetings.get(self.language, greetings['id'])
    
    # ==================== INFO KOMUNITAS ====================
    def get_info_text(self):
        texts = {
            'id': "📸 **Tentang Ciput Community**\n\nCiput Community adalah komunitas fotografi yang berbasis di Yogyakarta. Kami menggabungkan keindahan fotografi modern dengan kearifan lokal batik Nusantara.\n\n**Kami menyediakan:**\n• Studio foto lengkap dengan dekorasi batik\n• Workshop fotografi\n• Hunting bareng\n• Pameran foto\n• Kolaborasi kreatif\n\nBergabunglah bersama kami untuk mengembangkan passion fotografi Anda!",
            'en': "📸 **About Ciput Community**\n\nCiput Community is a photography community based in Yogyakarta. We combine the beauty of modern photography with the local wisdom of Indonesian batik.\n\n**We provide:**\n• Complete photo studio with batik decoration\n• Photography workshops\n• Group hunting\n• Photo exhibitions\n• Creative collaboration\n\nJoin us to develop your photography passion!",
            'jv': "📸 **Babagan Ciput Community**\n\nCiput Community punika komunitas fotografi ingkang mapan ing Yogyakarta. Kawulo nyediakaken:\n\n• Studio foto jangkep\n• Workshop fotografi\n• Hunting bareng\n• Pameran foto\n• Kolaborasi kreatif\n\nGabung kaliyan kita kangge ngembangaken passion fotografi panjenengan!"
        }
        return texts.get(self.language, texts['id'])
    
    # ==================== ALASAN MEMILIH CIPUT ====================
    def get_why_ciput_text(self):
        texts = {
            'id': """🎯 **5 Alasan Memilih Ciput Community**

**1. Kolaborasi Batik & Fotografi** ✨
Kami menggabungkan estetika batik Nusantara dengan teknik fotografi modern, menciptakan karya yang tidak hanya indah tapi juga bermakna budaya.

**2. Fotografer Profesional & Berpengalaman** 👨‍🎨
Tim fotografer kami telah menangani ratusan sesi foto, dari pre-wedding hingga event corporate, dengan hasil yang memuaskan.

**3. Studio Batik Eksklusif** 🏆
Studio kami didesain dengan interior batik yang cantik, cocok untuk sesi foto dengan tema tradisional maupun modern.

**4. Hasil Foto Premium** 💎
Kami menggunakan peralatan fotografi terbaik (Canon, Sony, Nikon) dan editing berkualitas tinggi.

**5. Harga Terjangkau & Pelayanan Ramah** 🤝
Harga kompetitif dengan kualitas terbaik, serta pelayanan yang ramah dan profesional.

---

**🌿 Motto Kami:** "Mengabadikan Momen dengan Sentuhan Budaya Nusantara"

Tunggu apalagi? Booking sekarang dan rasakan pengalaman fotografi yang berbeda! 📸""",
            
            'en': """🎯 **5 Reasons to Choose Ciput Community**

**1. Batik & Photography Collaboration** ✨
We combine the aesthetics of Indonesian batik with modern photography techniques, creating works that are not only beautiful but also culturally meaningful.

**2. Professional & Experienced Photographers** 👨‍🎨
Our photography team has handled hundreds of photo sessions, from pre-wedding to corporate events, with satisfying results.

**3. Exclusive Batik Studio** 🏆
Our studio is designed with beautiful batik interiors, perfect for traditional or modern themed photo sessions.

**4. Premium Photo Results** 💎
We use the best photography equipment (Canon, Sony, Nikon) and high-quality editing.

**5. Affordable Prices & Friendly Service** 🤝
Competitive prices with best quality, plus friendly and professional service.

---

**🌿 Our Motto:** "Capturing Moments with a Touch of Indonesian Culture"

What are you waiting for? Book now and experience a different photography experience! 📸""",
            
            'jv': """🎯 **5 Alasan Milih Ciput Community**

**1. Kolaborasi Batik & Fotografi** ✨
Kita gabungake keindahan batik Nusantara karo teknik fotografi modern, gawe karya sing apik lan nduweni makna budaya.

**2. Fotografer Profesional & Berpengalaman** 👨‍🎨
Tim fotografer kita wis nangani atusan sesi foto, saka pre-wedding nganti event corporate, hasil sing memuaskan.

**3. Studio Batik Eksklusif** 🏆
Studio kita didesain karo interior batik sing apik, cocok kanggo sesi foto tema tradisional lan modern.

**4. Hasil Foto Premium** 💎
Kita gunakake peralatan fotografi terbaik (Canon, Sony, Nikon) lan editing kualitas tinggi.

**5. Rega Terjangkau & Pelayanan Ramah** 🤝
Rega kompetitif karo kualitas terbaik, serta pelayanan sing ramah lan profesional.

---

**🌿 Motto Kita:** "Ngabadikake Momen karo Sentuhan Budaya Nusantara"

Apa maneh sing ditunggu? Booking saiki lan rasakake pengalaman fotografi sing beda! 📸"""
        }
        return texts.get(self.language, texts['id'])
    
    # ==================== PRICELIST ====================
    def get_pricelist_text(self):
        texts = {
            'id': "💵 **Pricelist Jasa Fotografi Ciput Community**\n\n**Layanan Utama:**\n• 📸 Sewa Studio/Indoor: Rp 150.000/jam\n• 🌳 Sesi Foto Outdoor: Rp 250.000/jam\n• 🎉 Dokumentasi Event: Rp 500.000/jam\n• 🖥️ Editing Premium: Rp 50.000/foto\n\n**Add-ons (Tambahan):**\n• 💡 Pro Lighting Setup: +Rp 100.000\n• 👤 Talent/Model Tambahan: +Rp 200.000\n• 🖼️ Cetak Kanvas (ukuran A3): +Rp 150.000\n\n**Paket Spesial:**\n• 💍 Pre-wedding Batik: Rp 2.500.000\n• 👨‍👩‍👧‍👦 Family Gathering: Rp 1.500.000\n• 🎓 Graduation Batik: Rp 800.000\n\nKetik 'booking' untuk memesan!",
            'en': "💵 **Ciput Community Photography Service Pricelist**\n\n**Main Services:**\n• 📸 Studio/Indoor Rental: Rp 150.000/hour\n• 🌳 Outdoor Photo Session: Rp 250.000/hour\n• 🎉 Event Documentation: Rp 500.000/hour\n• 🖥️ Premium Editing: Rp 50.000/photo\n\n**Add-ons:**\n• 💡 Pro Lighting Setup: +Rp 100.000\n• 👤 Additional Talent/Model: +Rp 200.000\n\nType 'booking' to order!",
            'jv': "💵 **Pricelist Jasa Fotografi Ciput Community**\n\n**Layanan Utama:**\n• 📸 Sewa Studio/Indoor: Rp 150.000/jam\n• 🌳 Sesi Foto Outdoor: Rp 250.000/jam\n• 🎉 Dokumentasi Event: Rp 500.000/jam\n• 🖥️ Editing Premium: Rp 50.000/foto\n\nKetik 'booking' kangge pesen!"
        }
        return texts.get(self.language, texts['id'])
    
    # ==================== KONTAK ====================
    def get_contact_text(self):
        texts = {
            'id': "📞 **Kontak & Alamat Ciput Community**\n\n**Media Sosial:**\n• WhatsApp: +62 812-3456-7890 (Fast Response)\n• Instagram: @ciput.community\n• TikTok: @ciput.community\n• Email: info@ciputcommunity.com\n\n📍 **Alamat Studio:**\nJl. Batik Indah No. 45, Yogyakarta, Indonesia\n\n**Jam Operasional:**\n• Senin - Sabtu: 09.00 - 21.00 WIB\n• Minggu: 10.00 - 18.00 WIB\n\nKunjungi kami dan rasakan pengalaman fotografi yang berbeda! 📸",
            'en': "📞 **Ciput Community Contact & Address**\n\n**Social Media:**\n• WhatsApp: +62 812-3456-7890\n• Instagram: @ciput.community\n• Email: info@ciputcommunity.com\n\n📍 **Studio Address:**\nJl. Batik Indah No. 45, Yogyakarta, Indonesia\n\n**Operating Hours:**\n• Monday - Saturday: 09.00 - 21.00 WIB\n• Sunday: 10.00 - 18.00 WIB",
            'jv': "📞 **Kontak & Alamat Ciput Community**\n\n• WhatsApp: +62 812-3456-7890\n• Instagram: @ciput.community\n• Email: info@ciputcommunity.com\n\n📍 **Alamat Studio:**\nJl. Batik Indah No. 45, Yogyakarta\n\nJam Operasional: 09.00 - 21.00 WIB"
        }
        return texts.get(self.language, texts['id'])
    
    # ==================== REGISTRASI MEMBER ====================
    def get_registration_prompt(self, field):
        prompts = {
            'id': {
                'name': "✍️ **Pendaftaran Member Ciput Community**\n\nSilakan masukkan nama lengkap Anda:",
                'email': "Masukkan alamat email Anda:",
                'phone': "Masukkan nomor WhatsApp Anda (contoh: 08123456789):"
            },
            'en': {
                'name': "✍️ **Ciput Community Member Registration**\n\nPlease enter your full name:",
                'email': "Enter your email address:",
                'phone': "Enter your WhatsApp number:"
            },
            'jv': {
                'name': "✍️ **Pendaftaran Member Ciput Community**\n\nMangga lebetaken nama lengkap panjenengan:",
                'email': "Lebetaken alamat email panjenengan:",
                'phone': "Lebetaken nomor WhatsApp panjenengan:"
            }
        }
        return prompts.get(self.language, prompts['id']).get(field, "Silakan masukkan data Anda:")
    
    def get_registration_summary(self):
        texts = {
            'id': f"📋 **Konfirmasi Data Member**\n\nNama: {self.registration_data['name']}\nEmail: {self.registration_data['email']}\nWA: {self.registration_data['phone']}\n\nApakah data di atas sudah benar?\n\nKetik 'ya' untuk konfirmasi atau 'tidak' untuk batal:",
            'en': f"📋 **Member Data Confirmation**\n\nName: {self.registration_data['name']}\nEmail: {self.registration_data['email']}\nWhatsApp: {self.registration_data['phone']}\n\nIs the above data correct?\n\nType 'yes' to confirm or 'no' to cancel:",
            'jv': f"📋 **Konfirmasi Data Member**\n\nNama: {self.registration_data['name']}\nEmail: {self.registration_data['email']}\nWA: {self.registration_data['phone']}\n\nData nginggil puniko leres?\n\nKetik 'ya' kangge konfirmasi utawi 'tidak' kangge batal:"
        }
        return texts.get(self.language, texts['id'])
    
    # ==================== BOOKING ====================
    def get_booking_prompt(self):
        texts = {
            'id': "📅 **Booking Jasa Fotografi Ciput Community**\n\nSilakan ketik pesanan Anda dengan format:\n\n• 'studio 2 jam' - Sewa studio indoor\n• 'outdoor 3 jam' - Sesi foto outdoor  \n• 'event 4 jam' - Dokumentasi event\n• 'editing 5 foto' - Editing premium\n\n**Contoh:** 'studio 2 jam, 1 lighting'\n\nKetik 'selesai' jika sudah selesai booking.",
            'en': "📅 **Photography Service Booking**\n\nPlease enter your order with format:\n\n• 'studio 2 hours' - Studio rental\n• 'outdoor 3 hours' - Outdoor session\n• 'event 4 hours' - Event documentation\n• 'editing 5 photos' - Photo editing\n\nType 'done' when finished booking.",
            'jv': "📅 **Booking Jasa Fotografi**\n\nMangga ketik pesanan panjenengan kanthi format:\n\n• 'studio 2 jam' - Sewa studio\n• 'outdoor 3 jam' - Sesi outdoor\n• 'event 4 jam' - Dokumentasi event\n• 'editing 5 foto' - Editing foto\n\nKetik 'selesai' menawi sampun rampung booking."
        }
        return texts.get(self.language, texts['id'])
    
    def get_confirmation_prompt(self):
        total = self.calculate_total()
        texts = {
            'id': f"🛒 **Ringkasan Booking**\n\nTotal yang harus dibayar: Rp {total:,}\n\nApakah Anda ingin melanjutkan ke pembayaran?\n\nKetik 'ya' untuk lanjut atau 'tidak' para batal:",
            'en': f"🛒 **Booking Summary**\n\nTotal to pay: Rp {total:,}\n\nDo you want to proceed to payment?\n\nType 'yes' to continue or 'no' to cancel:",
            'jv': f"🛒 **Ringkesan Booking**\n\nTotal ingkang kedah dibayar: Rp {total:,}\n\nPunjenengan badhe nerusaken dhateng pambayaran?\n\nKetik 'ya' kangge nerusake utawi 'tidak' kangge batal:"
        }
        return texts.get(self.language, texts['id'])
    
    def get_payment_prompt(self):
        total = self.calculate_total()
        texts = {
            'id': f"💳 **Pembayaran**\n\nTotal yang harus dibayar: Rp {total:,}\n\n**Transfer ke rekening kami:**\n\n🏦 Bank BCA\n• Nomor: 829-1029-381\n• A/N: CIPUT COMMUNITY\n\n🏦 Bank Mandiri\n• Nomor: 137-00-112233-4\n• A/N: CIPUT COMMUNITY\n\n📸 **Setelah transfer, ketik 'selesai' untuk konfirmasi.**\n\nTerima kasih telah memilih Ciput Community! ✨",
            'en': f"💳 **Payment**\n\nTotal to pay: Rp {total:,}\n\n**Transfer to our bank account:**\n\n🏦 BCA Bank\n• Account: 829-1029-381\n• A/N: CIPUT COMMUNITY\n\n🏦 Mandiri Bank\n• Account: 137-00-112233-4\n• A/N: CIPUT COMMUNITY\n\n📸 **After transfer, type 'done' to confirm.**\n\nThank you for choosing Ciput Community! ✨",
            'jv': f"💳 **Pambayaran**\n\nTotal ingkang kedah dibayar: Rp {total:,}\n\nTransfer dhateng:\n• BCA: 829-1029-381 a/n CIPUT COMMUNITY\n• Mandiri: 137-00-112233-4 a/n CIPUT COMMUNITY\n\nSasampunipun transfer, ketik 'selesai' kangge konfirmasi."
        }
        return texts.get(self.language, texts['id'])
    
    # ==================== UTILITY FUNCTIONS ====================
    def calculate_total(self):
        total = 0
        for item in self.cart:
            total += item['price'] * item['qty']
        return total
    
    def parse_booking(self, text):
        """Parse booking dari input user"""
        text = text.lower()
        booking = None
        
        # Extract number
        numbers = re.findall(r'\d+', text)
        qty = int(numbers[0]) if numbers else 1
        
        # Deteksi jenis booking
        if 'studio' in text or 'indoor' in text:
            booking = {
                'item': 'Sewa Studio/Indoor',
                'qty': qty,
                'price': 150000,
                'emoji': '📸'
            }
        elif 'outdoor' in text or 'luar ruangan' in text:
            booking = {
                'item': 'Sesi Foto Outdoor',
                'qty': qty,
                'price': 250000,
                'emoji': '🌳'
            }
        elif 'event' in text or 'dokumentasi' in text or 'acara' in text:
            booking = {
                'item': 'Dokumentasi Event',
                'qty': qty,
                'price': 500000,
                'emoji': '🎉'
            }
        elif 'editing' in text or 'edit' in text or 'retouch' in text:
            booking = {
                'item': 'Editing Premium',
                'qty': qty,
                'price': 50000,
                'emoji': '🖥️'
            }
        elif 'lighting' in text or 'lampu' in text:
            booking = {
                'item': 'Lighting Setup Pro',
                'qty': qty,
                'price': 100000,
                'emoji': '💡'
            }
        elif 'model' in text or 'talent' in text:
            booking = {
                'item': 'Talent/Model Tambahan',
                'qty': qty,
                'price': 200000,
                'emoji': '👤'
            }
        
        return booking
    
    # ==================== MAIN STEP FUNCTION ====================
    def step(self, user_input=None):
        if user_input is None:
            # Initial greeting
            self.last_response = self.get_greeting()
            return
        
        # Deteksi intent menggunakan NLPEngine (PERBAIKAN: gunakan value yang benar)
        intent = self.nlp.detect_intent(user_input)
        
        # Handle berdasarkan state saat ini
        if self.state == State.IDLE:
            if intent == 'ASK_INFO':  # PERBAIKAN
                self.last_response = self.get_info_text()
            elif intent == 'ASK_PRICELIST':  # PERBAIKAN
                self.last_response = self.get_pricelist_text()
            elif intent == 'ASK_CONTACT':  # PERBAIKAN
                self.last_response = self.get_contact_text()
            elif intent == 'WHY_CIPUT':  # PERBAIKAN
                self.last_response = self.get_why_ciput_text()
            elif intent == 'REGISTER':  # PERBAIKAN
                self.state = State.REG_NAME
                self.last_response = self.get_registration_prompt('name')
            elif intent == 'BOOKING':  # PERBAIKAN
                self.state = State.ORDERING
                self.last_response = self.get_booking_prompt()
            else:
                self.last_response = self.get_greeting()
        
        elif self.state == State.ORDERING:
            # Check if user wants to finish booking
            if intent == 'CHECKOUT' or 'selesai' in user_input.lower():  # PERBAIKAN
                if len(self.cart) > 0:
                    self.state = State.CONFIRMATION
                    self.last_response = self.get_confirmation_prompt()
                else:
                    self.last_response = "Belum ada item yang dipesan. Silakan tambahkan item terlebih dahulu.\n\n" + self.get_booking_prompt()
                return
            
            # Cek jika user ingin lihat keranjang
            if any(w in user_input.lower() for w in ['lihat keranjang', 'keranjang', 'cart', 'my cart']):
                if self.cart:
                    cart_text = "🛒 **Isi Keranjang Anda:**\n\n"
                    for i, item in enumerate(self.cart, 1):
                        cart_text += f"{i}. {item['emoji']} {item['item']}: {item['qty']}x = Rp {item['price'] * item['qty']:,}\n"
                    cart_text += f"\n**Total: Rp {self.calculate_total():,}**"
                    self.last_response = cart_text
                else:
                    self.last_response = "Keranjang Anda masih kosong. Silakan booking dulu ya!"
                return
            
            # Gunakan NLPEngine untuk parsing booking (TAMBAHAN)
            booking_result = self.nlp.extract_booking_info(user_input)
            if booking_result["success"]:
                for order in booking_result["orders"]:
                    # Konversi ke format yang sesuai dengan cart
                    self.cart.append({
                        'item': order['desc'],
                        'qty': order['qty'],
                        'price': order['price'],
                        'emoji': order['emoji']
                    })
                self.last_response = f"✅ Ditambahkan {len(booking_result['orders'])} item ke keranjang!\n\nTotal sementara: Rp {self.calculate_total():,}\n\nKetik 'selesai' untuk checkout, atau lanjutkan booking lainnya."
            else:
                # Fallback ke parse_booking lama
                booking_info = self.parse_booking(user_input)
                if booking_info:
                    self.cart.append(booking_info)
                    self.last_response = f"✅ {booking_info['emoji']} {booking_info['item']} ({booking_info['qty']}x) ditambahkan ke keranjang!\n\nTotal sementara: Rp {self.calculate_total():,}\n\nKetik 'selesai' untuk checkout, atau lanjutkan booking lainnya."
                else:
                    self.last_response = self.get_booking_prompt()
        
        elif self.state == State.REG_NAME:
            if user_input.strip():
                self.registration_data['name'] = user_input
                self.state = State.REG_EMAIL
                self.last_response = self.get_registration_prompt('email')
            else:
                if self.language == 'id':
                    self.last_response = "❌ Nama tidak boleh kosong. Silakan masukkan nama lengkap Anda:"
                elif self.language == 'en':
                    self.last_response = "❌ Name cannot be empty. Please enter your full name:"
                elif self.language == 'jv':
                    self.last_response = "❌ Nama mboten boleh kosong. Mangga lebetaken nama lengkap panjenengan:"
                else:
                    self.last_response = "❌ Nama tidak boleh kosong. Silakan masukkan nama lengkap Anda:"
        
        elif self.state == State.REG_EMAIL:
            if '@' in user_input and '.' in user_input:
                self.registration_data['email'] = user_input
                self.state = State.REG_PHONE
                self.last_response = self.get_registration_prompt('phone')
            else:
                if self.language == 'id':
                    self.last_response = "❌ Email tidak valid. Masukkan email yang benar (contoh: nama@gmail.com):"
                elif self.language == 'en':
                    self.last_response = "❌ Invalid email. Please enter a valid email address (example: name@gmail.com):"
                elif self.language == 'jv':
                    self.last_response = "❌ Email ora valid. Lebetaken email ingkang leres (contoh: nama@gmail.com):"
                else:
                    self.last_response = "❌ Email tidak valid. Masukkan email yang benar (contoh: nama@gmail.com):"
        
        elif self.state == State.REG_PHONE:
            clean_phone = user_input.replace('+', '').replace(' ', '').replace('-', '')
            if clean_phone.isdigit() and len(clean_phone) >= 10:
                self.registration_data['phone'] = user_input
                self.state = State.REG_CONFIRM
                self.last_response = self.get_registration_summary()
            else:
                if self.language == 'id':
                    self.last_response = "❌ Nomor telepon tidak valid. Masukkan nomor yang benar (contoh: 08123456789):"
                elif self.language == 'en':
                    self.last_response = "❌ Invalid phone number. Please enter a valid phone number (example: 08123456789):"
                elif self.language == 'jv':
                    self.last_response = "❌ Nomer telepon ora valid. Lebetaken nomer ingkang leres (contoh: 08123456789):"
                else:
                    self.last_response = "❌ Nomor telepon tidak valid. Masukkan nomor yang benar (contoh: 08123456789):"
        
        elif self.state == State.REG_CONFIRM:
            if intent == 'YES':  # PERBAIKAN
                self.state = State.IDLE
                if self.language == 'id':
                    self.last_response = f"✅ Selamat! {self.registration_data['name']} telah terdaftar sebagai member Ciput Community!\n\nKartu member akan dikirim ke email: {self.registration_data['email']}\n\n✨ Anda akan mendapatkan:\n• Diskon 10% untuk booking pertama\n• Update event & workshop terbaru\n• Akses gallery member eksklusif\n\nSilakan ketik 'booking' untuk pesan jasa atau 'info' untuk informasi lainnya."
                elif self.language == 'en':
                    self.last_response = f"✅ Congratulations! {self.registration_data['name']} has been registered as a Ciput Community member!\n\nMember card will be sent to: {self.registration_data['email']}\n\n✨ You will get:\n• 10% discount for first booking\n• Latest event & workshop updates\n• Exclusive member gallery access\n\nType 'booking' to order or 'info' for more information."
                elif self.language == 'jv':
                    self.last_response = f"✅ Sugeng! {self.registration_data['name']} sampun kadaptar minangka member Ciput Community!\n\nKartu member badhe dipunkirim dhateng email: {self.registration_data['email']}\n\n✨ Panjenengan badhe pikantuk:\n• Diskon 10% kangge booking pertama\n• Update event & workshop paling anyar\n• Akses gallery member eksklusif\n\nKetik 'booking' kangge pesen jasa utawi 'info' kangge informasi sanesipun."
                else:
                    self.last_response = f"✅ Selamat! {self.registration_data['name']} telah terdaftar sebagai member Ciput Community!\n\nKartu member akan dikirim ke email: {self.registration_data['email']}\n\nSilakan ketik 'booking' untuk pesan jasa atau 'info' untuk informasi lainnya."
                self.registration_data = {'name': '', 'email': '', 'phone': ''}
            else:
                self.state = State.IDLE
                if self.language == 'id':
                    self.last_response = "❌ Pendaftaran dibatalkan. Silakan ketik 'daftar' jika ingin daftar ulang."
                elif self.language == 'en':
                    self.last_response = "❌ Registration cancelled. Type 'register' to try again."
                elif self.language == 'jv':
                    self.last_response = "❌ Pendaftaran dibatalake. Ketik 'daftar' menawi badhe ndaftar malih."
                else:
                    self.last_response = "❌ Pendaftaran dibatalkan. Silakan ketik 'daftar' jika ingin daftar ulang."
        
        elif self.state == State.CONFIRMATION:
            if intent == 'YES':  # PERBAIKAN
                self.state = State.PAYMENT
                self.last_response = self.get_payment_prompt()
            else:
                self.state = State.IDLE
                self.cart = []
                if self.language == 'id':
                    self.last_response = "❌ Booking dibatalkan. Silakan ketik 'booking' jika ingin memesan ulang."
                elif self.language == 'en':
                    self.last_response = "❌ Booking cancelled. Type 'booking' to order again."
                elif self.language == 'jv':
                    self.last_response = "❌ Booking dibatalake. Ketik 'booking' menawi badhe pesen malih."
                else:
                    self.last_response = "❌ Booking dibatalkan. Silakan ketik 'booking' jika ingin memesan ulang."
        
        elif self.state == State.PAYMENT:
            if intent == 'CHECKOUT' or 'selesai' in user_input.lower():  # PERBAIKAN
                self.state = State.IDLE
                if self.language == 'id':
                    self.last_response = f"✅ **Terima kasih! Booking Anda telah dikonfirmasi.**\n\n📸 Detail Booking:\n• Total pembayaran: Rp {self.calculate_total():,}\n• Booking ID: CIP{datetime.now().strftime('%Y%m%d%H%M%S')}\n\n📞 Tim kami akan menghubungi Anda dalam 1x24 jam untuk konfirmasi jadwal.\n\n✨ Terima kasih telah menggunakan jasa Ciput Community! ✨\n\nSilakan ketik 'info' untuk informasi lainnya."
                elif self.language == 'en':
                    self.last_response = f"✅ **Thank you! Your booking has been confirmed.**\n\n📸 Booking Details:\n• Total payment: Rp {self.calculate_total():,}\n• Booking ID: CIP{datetime.now().strftime('%Y%m%d%H%M%S')}\n\n📞 Our team will contact you within 24 hours to confirm the schedule.\n\n✨ Thank you for using Ciput Community services! ✨\n\nType 'info' for more information."
                elif self.language == 'jv':
                    self.last_response = f"✅ **Matur nuwun! Booking panjenengan sampun dikonfirmasi.**\n\n📸 Rincian Booking:\n• Total pambayaran: Rp {self.calculate_total():,}\n• Booking ID: CIP{datetime.now().strftime('%Y%m%d%H%M%S')}\n\n📞 Tim kita badhe ngubungi panjenengan ing 1x24 jam kangge konfirmasi jadwal.\n\n✨ Matur nuwun sampun ngginakaken jasa Ciput Community! ✨\n\nKetik 'info' kangge informasi sanesipun."
                else:
                    self.last_response = f"✅ **Terima kasih! Booking Anda telah dikonfirmasi.**\n\n📸 Detail Booking:\n• Total pembayaran: Rp {self.calculate_total():,}\n• Booking ID: CIP{datetime.now().strftime('%Y%m%d%H%M%S')}\n\n📞 Tim kami akan menghubungi Anda dalam 1x24 jam.\n\n✨ Terima kasih! ✨"
                self.cart = []
            else:
                self.last_response = self.get_payment_prompt()
    
    def get_response(self):
        return self.last_response
