# Angular Rate Estimation Projesi - Proje Kapsamı

## 🎯 Proje Amacı
Yıldız izleyici (star tracker) görüntülerinden ve IMU sensör verilerinden açısal hız tahmini yapmak ve sensör füzyonu ile optimal tahmin sağlamak.

## 📊 Veri Kaynakları

### 1. Yıldız İzleyici (Star Tracker)
- **Girdi**: Dinamik ortamda yıldız spotlarının görüntü koordinatları
- **Çıktı**: Yıldız spotlarının hareketi üzerinden hesaplanan açısal hız tahmini
- **Zorluklar**:
  - Görüntü işleme gecikmeleri
  - Yıldız spot algılama hataları
  - Düşük frame rate

### 2. IMU Sensörü
- **Girdi**: 6-DOF IMU verisi (gyroscope + accelerometer)
- **Çıktı**: Direkt açısal hız ölçümü
- **Zorluklar**:
  - Gyroscope bias drift
  - Yüksek frekanslı gürültü
  - Kalibrasyyon hataları

## 🔬 Sensör Füzyonu Stratejisi

### Tamamlayıcı Özellikler
- **Star Tracker**: Uzun vadeli doğruluk, drift yok, ama düşük bandwidth
- **IMU Gyro**: Yüksek bandwidth, hızlı yanıt, ama drift var

### Füzyon Yaklaşımları
1. **Complementary Filter**: Basit, düşük hesaplama maliyeti
2. **Kalman Filter**: Optimal tahmin, belirsizlik modelleme
3. **Extended Kalman Filter (EKF)**: Nonlinear dinamikler için

## 📁 Proje Yapısı

```
angularRateEstimation/
├── PROJECT_CONTEXT.md              # Bu dosya - proje kapsamı
├── README.md                       # Proje açıklaması
├── papers/                         # Akademik makaleler ve kaynaklar
│   ├── star_tracker/              # Yıldız izleyici makaleleri
│   ├── sensor_fusion/             # Sensör füzyonu makaleleri
│   └── angular_rate_estimation/   # Açısal hız tahmini makaleleri
├── src/
│   ├── star_tracker/              # Yıldız izleyici işlemleri
│   │   ├── spot_detection.py     # Yıldız spot algılama
│   │   ├── motion_estimation.py  # Spot hareketinden açısal hız
│   │   └── camera_model.py       # Kamera parametreleri
│   ├── imu/                       # IMU veri işleme
│   │   ├── gyro_processing.py    # Gyroscope data processing
│   │   ├── calibration.py        # IMU kalibrasyonu
│   │   └── bias_estimation.py    # Bias drift tahmini
│   ├── fusion/                    # Sensör füzyonu algoritmaları
│   │   ├── complementary_filter.py
│   │   ├── kalman_filter.py
│   │   └── ekf_filter.py
│   ├── data/                      # Veri oluşturma ve yönetimi
│   │   ├── synthetic_star_tracker.py  # Simulated star tracker data
│   │   ├── synthetic_imu_generator.py # Simulated IMU data (mevcut)
│   │   └── data_loader.py        # Gerçek veri yükleme
│   ├── evaluation/                # Test ve değerlendirme
│   │   ├── filter_comparison.py  # Füzyon algoritmaları karşılaştırma
│   │   └── metrics.py            # Performance metrics
│   └── utils/                     # Yardımcı fonksiyonlar
│       ├── quaternion.py         # Quaternion matematik
│       └── coordinate_transform.py
├── tests/                         # Unit testler
│   ├── test_star_tracker/
│   ├── test_imu/
│   └── test_fusion/
├── communication/                 # AI Agent iletişimi
│   └── general.md
└── requirements.txt
```

## 🎯 Geliştirme Aşamaları

### Faz 1: Temel Altyapı (Mevcut)
- ✅ AI agent iletişim sistemi
- ✅ Synthetic IMU data generator
- 🔄 Proje mimarisi planlaması

### Faz 2: Star Tracker Modülü
- [ ] Yıldız spot detection simülatörü
- [ ] Spot motion tracking
- [ ] Açısal hız hesaplama (görüntü tabanlı)
- [ ] Star tracker synthetic data generator

### Faz 3: IMU Modülü
- [ ] IMU data preprocessing
- [ ] Gyro bias estimation
- [ ] Gyro-based angular rate estimation

### Faz 4: Sensör Füzyonu
- [ ] Complementary filter (star tracker + IMU)
- [ ] Kalman filter (optimal fusion)
- [ ] EKF implementation (nonlinear model)

### Faz 5: Test ve Validasyon
- [ ] Synthetic data ile end-to-end test
- [ ] Performance metrics (RMSE, drift analysis)
- [ ] Algoritma karşılaştırması
- [ ] Gerçek veri ile validasyon (varsa)

## 📚 Kaynak Depo
`papers/` klasöründe ilgili akademik makaleler tutulacak:
- Star tracker algoritmaları
- Sensör füzyonu yaklaşımları
- Açısal hız tahmin teknikleri
- Kalman filtering uygulamaları

## 👥 AI Agent Görev Dağılımı
- **Claude Sonnet 4.5**: Kalman/EKF implementasyonu, test framework
- **GitHub Copilot**: Star tracker modülü, complementary filter
- **Abuzer**: Synthetic data generators, comparison framework

## 🔧 Teknoloji Stack
- **Python 3.x**
- **NumPy**: Numerical computation
- **OpenCV**: Görüntü işleme (star spot detection)
- **Matplotlib**: Visualization
- **pytest**: Testing framework
- **pandas**: Data management

---

**Son Güncelleme**: 2026-01-12
**Durum**: Mimari planlama aşamasında
