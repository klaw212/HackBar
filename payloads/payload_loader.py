import os

def load_payloads(filename=None):
    """
    Belirli bir dosyayı yükler veya tüm txt dosyalarını sözlük olarak döner.
    """
    # Eğer bir dosya adı verilmişse (window.py'nin beklediği gibi)
    if filename:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    return [line.strip() for line in f.readlines() if line.strip()]
            except Exception as e:
                print(f"Hata: {filename} okunamadi. {e}")
                return []
        else:
            print(f"Uyari: {filename} bulunamadi.")
            return []

    # Eğer dosya adı verilmemişse, tüm klasörü tara (yedek senaryo)
    payloads = {}
    files = [f for f in os.listdir('.') if f.endswith('.txt')]
    for file in files:
        name = file.replace('.txt', '').upper()
        with open(file, 'r', encoding='utf-8') as f:
            payloads[name] = [line.strip() for line in f.readlines() if line.strip()]
    return payloads
