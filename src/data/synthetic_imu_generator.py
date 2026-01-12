"""
Synthetic IMU Data Generator
6-DOF (3-axis gyroscope + 3-axis accelerometer) simülatörü
Abuzer tarafından geliştirildi
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class IMUConfig:
    """IMU sensör konfigürasyonu"""
    sampling_rate: float = 100.0  # Hz
    gyro_noise_std: float = 0.01  # rad/s
    gyro_bias_drift: float = 0.001  # rad/s per second
    accel_noise_std: float = 0.1  # m/s^2
    accel_bias: np.ndarray = None  # 3x1 vector

    def __post_init__(self):
        if self.accel_bias is None:
            self.accel_bias = np.zeros(3)


class SyntheticIMUGenerator:
    """Synthetic IMU data generator"""

    def __init__(self, config: IMUConfig = None):
        """
        Args:
            config: IMU konfigürasyonu (default: IMUConfig())
        """
        self.config = config if config else IMUConfig()
        self.dt = 1.0 / self.config.sampling_rate

    def generate_rotation_sequence(
        self,
        duration: float,
        angular_velocity: np.ndarray,
        initial_orientation: np.ndarray = None
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Sabit açısal hız ile rotasyon sekansı üretir

        Args:
            duration: Süre (saniye)
            angular_velocity: 3x1 açısal hız vektörü [wx, wy, wz] (rad/s)
            initial_orientation: Başlangıç orientation (Euler angles [roll, pitch, yaw])

        Returns:
            timestamps: Zaman damgaları (N,)
            gyro_data: Gyroscope ölçümleri (N, 3) - [wx, wy, wz] (rad/s)
            accel_data: Accelerometer ölçümleri (N, 3) - [ax, ay, az] (m/s^2)
        """
        num_samples = int(duration * self.config.sampling_rate)
        timestamps = np.arange(num_samples) * self.dt

        if initial_orientation is None:
            initial_orientation = np.zeros(3)

        # Gyroscope data: gerçek açısal hız + noise + drift
        gyro_bias_drift = np.cumsum(
            np.random.randn(num_samples, 3) * self.config.gyro_bias_drift * self.dt,
            axis=0
        )
        gyro_noise = np.random.randn(num_samples, 3) * self.config.gyro_noise_std
        gyro_data = angular_velocity + gyro_bias_drift + gyro_noise

        # Accelerometer data: gravity vektörü + noise
        # Basitleştirilmiş model: statik durum (sadece gravity)
        gravity = 9.81  # m/s^2
        accel_data = np.zeros((num_samples, 3))
        accel_data[:, 2] = gravity  # Z-axis: yukarı yönlü gravity

        # Orientation değişimine göre gravity projection (basitleştirilmiş)
        # TODO: Daha gelişmiş rotation matrix hesaplaması
        accel_noise = np.random.randn(num_samples, 3) * self.config.accel_noise_std
        accel_data += accel_noise + self.config.accel_bias

        return timestamps, gyro_data, accel_data

    def generate_sinusoidal_motion(
        self,
        duration: float,
        frequency: float = 1.0,
        amplitude: float = 0.5
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Sinüzoidal hareket (salınım) üretir

        Args:
            duration: Süre (saniye)
            frequency: Frekans (Hz)
            amplitude: Genlik (rad/s)

        Returns:
            timestamps, gyro_data, accel_data
        """
        num_samples = int(duration * self.config.sampling_rate)
        timestamps = np.arange(num_samples) * self.dt

        # Sinusoidal açısal hız (sadece Z-axis etrafında)
        omega = 2 * np.pi * frequency
        angular_velocity = np.zeros((num_samples, 3))
        angular_velocity[:, 2] = amplitude * np.sin(omega * timestamps)

        # Noise ve drift ekle
        gyro_bias_drift = np.cumsum(
            np.random.randn(num_samples, 3) * self.config.gyro_bias_drift * self.dt,
            axis=0
        )
        gyro_noise = np.random.randn(num_samples, 3) * self.config.gyro_noise_std
        gyro_data = angular_velocity + gyro_bias_drift + gyro_noise

        # Accelerometer: basit gravity + noise
        accel_data = np.zeros((num_samples, 3))
        accel_data[:, 2] = 9.81
        accel_noise = np.random.randn(num_samples, 3) * self.config.accel_noise_std
        accel_data += accel_noise + self.config.accel_bias

        return timestamps, gyro_data, accel_data

    def generate_step_response(
        self,
        duration: float,
        step_time: float = 1.0,
        step_magnitude: float = 1.0
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Step response (ani hareket değişimi) üretir

        Args:
            duration: Toplam süre (saniye)
            step_time: Step zamanı (saniye)
            step_magnitude: Step büyüklüğü (rad/s)

        Returns:
            timestamps, gyro_data, accel_data
        """
        num_samples = int(duration * self.config.sampling_rate)
        timestamps = np.arange(num_samples) * self.dt

        # Step function
        angular_velocity = np.zeros((num_samples, 3))
        step_idx = int(step_time * self.config.sampling_rate)
        angular_velocity[step_idx:, 2] = step_magnitude

        # Noise ve drift
        gyro_bias_drift = np.cumsum(
            np.random.randn(num_samples, 3) * self.config.gyro_bias_drift * self.dt,
            axis=0
        )
        gyro_noise = np.random.randn(num_samples, 3) * self.config.gyro_noise_std
        gyro_data = angular_velocity + gyro_bias_drift + gyro_noise

        # Accelerometer
        accel_data = np.zeros((num_samples, 3))
        accel_data[:, 2] = 9.81
        accel_noise = np.random.randn(num_samples, 3) * self.config.accel_noise_std
        accel_data += accel_noise + self.config.accel_bias

        return timestamps, gyro_data, accel_data

    @staticmethod
    def save_to_csv(
        timestamps: np.ndarray,
        gyro_data: np.ndarray,
        accel_data: np.ndarray,
        filename: str
    ):
        """
        IMU verisini CSV formatında kaydeder

        Args:
            timestamps: Zaman damgaları
            gyro_data: Gyroscope verisi (N, 3)
            accel_data: Accelerometer verisi (N, 3)
            filename: Çıktı dosyası adı
        """
        df = pd.DataFrame({
            'timestamp': timestamps,
            'gyro_x': gyro_data[:, 0],
            'gyro_y': gyro_data[:, 1],
            'gyro_z': gyro_data[:, 2],
            'accel_x': accel_data[:, 0],
            'accel_y': accel_data[:, 1],
            'accel_z': accel_data[:, 2]
        })
        df.to_csv(filename, index=False)
        print(f"✅ IMU data saved to {filename}")


# Test ve örnek kullanım
if __name__ == "__main__":
    print("🚀 Synthetic IMU Data Generator - Test Suite")
    print("=" * 60)

    # Config oluştur
    config = IMUConfig(
        sampling_rate=100.0,
        gyro_noise_std=0.01,
        gyro_bias_drift=0.001,
        accel_noise_std=0.1
    )

    generator = SyntheticIMUGenerator(config)

    # Test 1: Sabit rotasyon
    print("\n1️⃣  Generating constant rotation data...")
    t, gyro, accel = generator.generate_rotation_sequence(
        duration=5.0,
        angular_velocity=np.array([0.0, 0.0, 0.5])  # 0.5 rad/s Z-axis
    )
    generator.save_to_csv(t, gyro, accel, "test_constant_rotation.csv")
    print(f"   Samples: {len(t)}, Duration: {t[-1]:.2f}s")

    # Test 2: Sinusoidal hareket
    print("\n2️⃣  Generating sinusoidal motion...")
    t, gyro, accel = generator.generate_sinusoidal_motion(
        duration=10.0,
        frequency=0.5,
        amplitude=1.0
    )
    generator.save_to_csv(t, gyro, accel, "test_sinusoidal_motion.csv")
    print(f"   Samples: {len(t)}, Frequency: 0.5 Hz")

    # Test 3: Step response
    print("\n3️⃣  Generating step response...")
    t, gyro, accel = generator.generate_step_response(
        duration=5.0,
        step_time=2.0,
        step_magnitude=1.5
    )
    generator.save_to_csv(t, gyro, accel, "test_step_response.csv")
    print(f"   Samples: {len(t)}, Step at: 2.0s")

    print("\n" + "=" * 60)
    print("✨ Test suite completed! 3 CSV files generated.")
    print("📊 Statistics:")
    print(f"   - Gyro mean: [{np.mean(gyro[:, 0]):.4f}, {np.mean(gyro[:, 1]):.4f}, {np.mean(gyro[:, 2]):.4f}] rad/s")
    print(f"   - Gyro std:  [{np.std(gyro[:, 0]):.4f}, {np.std(gyro[:, 1]):.4f}, {np.std(gyro[:, 2]):.4f}] rad/s")
    print(f"   - Accel mean: [{np.mean(accel[:, 0]):.4f}, {np.mean(accel[:, 1]):.4f}, {np.mean(accel[:, 2]):.4f}] m/s^2")
