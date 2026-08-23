import json
import hashlib
import os
from datetime import datetime

def generate_anon_id(username):
    if not username:
        username = "deleted"
    hash_object = hashlib.md5(str(username).encode())
    return 'usr_' + hash_object.hexdigest()[:8]

def extract_comments(comments_list, temp_dataset, topic):
    for comment in comments_list:
        if comment.get('kind') == 't1':  
            c_data = comment['data']
            body = c_data.get('body')
            author = c_data.get('author')
            created_utc = c_data.get('created_utc')
            score = c_data.get('score', 0)
            
            if body and body not in ['[deleted]', '[removed]']:
                
                # FİLTRE: Resim/GIF linki olanları veya çok kısa yorumları atla
                if "preview.redd.it" in body or "giphy.com" in body or "imgur.com" in body:
                    pass 
                elif len(body.split()) < 4:
                    pass 
                else:
                    dt_object = datetime.fromtimestamp(created_utc)
                    formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                    is_relevant = True if score >= 0 else False
                    
                    temp_dataset.append({
                        "topic": topic,
                        "post": body.strip(),
                        "created_at": formatted_date,
                        "anon_user_id": generate_anon_id(author),
                        "is_relevant": is_relevant
                    })
                
            replies = c_data.get('replies')
            if replies and isinstance(replies, dict):
                extract_comments(replies['data']['children'], temp_dataset, topic)

def ana_islem():
    print("Ham JSON dosyası okunuyor...")
    try:
        with open('reddit_ham.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        temp_dataset = []
        
        if isinstance(data, list) and len(data) > 1:
            topic = data[0]['data']['children'][0]['data'].get('title', 'Bilinmeyen Başlık')
            comments_data = data[1]['data']['children']
            
            extract_comments(comments_data, temp_dataset, topic)
            
            # --- VERİ BİRİKTİRME (KUMBARA) MANTIĞI ---
            ana_veri_seti = []
            dosya_adi = 'net_gundem_temiz.json'
            
            # Eğer ana dosyamız zaten varsa, içindeki eski verileri oku
            if os.path.exists(dosya_adi):
                with open(dosya_adi, 'r', encoding='utf-8') as f:
                    try:
                        ana_veri_seti = json.load(f)
                    except json.JSONDecodeError:
                        ana_veri_seti = []
            
            # Yeni başlıktan çıkan verileri, eski verilerin sonuna ekle
            ana_veri_seti.extend(temp_dataset)
            
            # Tüm verileri ana dosyaya tekrar kaydet
            with open(dosya_adi, 'w', encoding='utf-8') as f:
                json.dump(ana_veri_seti, f, ensure_ascii=False, indent=2)
                
            print(f"Harika! Bu başlıktan {len(temp_dataset)} adet yorum dönüştürüldü.")
            print(f"--> NET GÜNDEM Toplam Veri Sayınız: {len(ana_veri_seti)} / 2000")
            
        else:
            print("Hata: Dosya formatı uygun değil. Linkin sonuna .json eklediğinizden emin olun.")
            
    except FileNotFoundError:
        print("Hata: 'reddit_ham.json' dosyası bulunamadı. Lütfen kopyaladığınız metni bu isimle aynı klasöre kaydedin.")
    except json.JSONDecodeError:
        print("Hata: Kopyaladığınız metin geçerli bir JSON değil. Kopyalarken eksik bir parça kalmadığından emin olun (Ctrl+A kullanın).")

if __name__ == "__main__":
    ana_islem()