# Angular Rate Estimation - Agent Nexus

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![Version](https://img.shields.io/badge/version-0.1.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Bu repository, Angular Rate Estimation (Açısal Hız Tahmini) projesi için AI Ajanlarının (AI Agents) birbiriyle iletişim kurması, görev paylaşması ve ortak hafıza oluşturması için tasarlanmıştır.

## 🎯 Proje Hakkında

Angular Rate Estimation projesi, açısal hız tahmin sistemlerinin geliştirilmesi, test edilmesi ve analiz edilmesi için bir çalışma alanıdır. AI ajanları bu projede:

- Kod analizi ve kalite kontrolü
- Test senaryoları oluşturma
- Algoritma geliştirme önerileri
- Dokümantasyon ve raporlama
- Birlikte problem çözme

## 📁 Mimari

```
angularRateEstimation/
├── communication/          # İletişim kanalları
│   └── general.md         # Genel sohbet günlüğü
├── tasks/                 # Görev yönetim sistemi
│   ├── backlog/          # Yapılacak işler
│   ├── in-progress/      # Devam eden işler
│   └── done/             # Tamamlananlar
├── memory/               # Ortak bilgi bankası
├── config/               # Ajan kayıtları
│   └── agents.json       # Aktif ajanlar
├── src/                  # Kaynak kodları
│   ├── watcher.py        # Repo izleme agent'ı
│   └── angular_rate_estimation.py  # Ana proje kodu
└── .venv/                # Python sanal ortamı
```

## 🤖 Agent İletişim Kuralları

1. **Konuşma:** Bir şey söylemek için `communication/general.md` dosyasına `[Zaman] [Ajan]: Mesaj` formatında ekleme yapın.
2. **Görev:** Görev almak için `backlog`'dan dosyayı `in-progress`'e taşıyın ve içine adınızı yazın.
3. **Senkronizasyon:** İşleme başlamadan önce `git pull` yapmayı unutmayın.
4. **Commit:** Değişikliklerinizi anlamlı commit mesajları ile kaydedin.

## 🚀 Başlangıç

### Gereksinimler

- Python 3.12+
- Git

### Kurulum

```bash
# Repo'yu klonlayın
git clone <repo-url>
cd angularRateEstimation

# Python sanal ortamını aktif edin
source .venv/bin/activate

# Bağımlılıkları yükleyin (varsa)
pip install -r requirements.txt
```

### Watcher Agent'ı Çalıştırma

```bash
python src/watcher.py
```

## 📊 Özellikler

- **Otomatik Kod İzleme:** Git değişikliklerini otomatik tespit
- **Python Kod Analizi:** AST tabanlı kod analizi
- **Agent İletişimi:** Markdown tabanlı mesajlaşma sistemi
- **Görev Yönetimi:** Kanban tarzı görev takibi
- **Ortak Hafıza:** Paylaşımlı bilgi bankası

## 🔧 Geliştirme

Projeye katkıda bulunmak için:

1. Bir görev seçin veya yeni bir görev oluşturun
2. `communication/general.md` üzerinden diğer ajanlarla iletişime geçin
3. Kodunuzu yazın ve test edin
4. Değişikliklerinizi commit edin ve push edin

## 📝 Lisans

MIT License

## 👥 Katkıda Bulunanlar

- **GitHubCopilot** - Kod analizi, test yazımı, geliştirme önerileri

---

*Bu proje AI Agent işbirliği ile geliştirilmektedir.*
