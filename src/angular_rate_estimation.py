"""
Angular Rate Estimation - Ana Modül
Açısal hız tahmin algoritmaları ve yardımcı fonksiyonlar
"""

import numpy as np


def estimate_angular_rate(measurements, time_delta):
    """
    Basit açısal hız tahmini
    
    Args:
        measurements: Açısal pozisyon ölçümleri (numpy array)
        time_delta: Zaman aralığı (saniye)
    
    Returns:
        Tahmini açısal hız (rad/s)
    """
    if len(measurements) < 2:
        return 0.0
    
    # Basit türev yaklaşımı
    angular_velocity = np.diff(measurements) / time_delta
    return np.mean(angular_velocity)


def kalman_filter_init(initial_state, initial_covariance):
    """
    Kalman filtre başlatma
    
    Args:
        initial_state: Başlangıç durumu
        initial_covariance: Başlangıç kovaryans matrisi
    
    Returns:
        Kalman filtre durumu (dict)
    """
    return {
        'state': initial_state,
        'covariance': initial_covariance,
        'initialized': True
    }


def moving_average_filter(data, window_size=5):
    """
    Hareketli ortalama filtresi
    
    Args:
        data: Giriş verisi (numpy array)
        window_size: Pencere boyutu
    
    Returns:
        Filtrelenmiş veri
    """
    if len(data) < window_size:
        return data
    
    weights = np.ones(window_size) / window_size
    return np.convolve(data, weights, mode='valid')


if __name__ == "__main__":
    # Test kodu
    print("Angular Rate Estimation Module")
    
    # Test verisi
    test_angles = np.array([0, 0.1, 0.2, 0.35, 0.5])
    test_dt = 0.1
    
    rate = estimate_angular_rate(test_angles, test_dt)
    print(f"Estimated angular rate: {rate:.2f} rad/s")
    
    # Filtreleme testi
    noisy_data = np.random.randn(100) * 0.1 + np.linspace(0, 10, 100)
    filtered = moving_average_filter(noisy_data, window_size=10)
    print(f"Original data points: {len(noisy_data)}")
    print(f"Filtered data points: {len(filtered)}")
