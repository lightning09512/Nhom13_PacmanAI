"""
Sound Manager Module
Quản lý tất cả âm thanh trong game
"""

import pygame
try:
    import numpy as np
except Exception as e:
    np = None
    print(f"⚠️ numpy chưa sẵn sàng cho sound synth: {e}. Sẽ chạy không âm thanh tổng hợp.")


class SoundManager:
    """Quản lý âm thanh cho game"""
    
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self.sound_enabled = True
        
        # Tạo âm thanh đơn giản bằng code
        self.create_sounds()
    
    def create_sounds(self):
        """Tạo âm thanh đơn giản"""
        try:
            # Âm thanh ăn dot
            self.sounds['eat_dot'] = self.create_beep_sound(800, 0.1)
            # Âm thanh ăn power pellet
            self.sounds['eat_power'] = self.create_beep_sound(1200, 0.2)
            # Âm thanh ăn fruit
            self.sounds['eat_fruit'] = self.create_beep_sound(600, 0.15)
            # Âm thanh ăn ghost
            self.sounds['eat_ghost'] = self.create_beep_sound(400, 0.3)
            # Âm thanh mất mạng
            self.sounds['lose_life'] = self.create_beep_sound(200, 0.5)
            # Âm thanh chuyển level
            self.sounds['level_up'] = self.create_chord_sound([400, 500, 600], 0.5)
            # Âm thanh pause
            self.sounds['pause'] = self.create_beep_sound(300, 0.1)
            print("Sound system initialized successfully")
        except Exception as e:
            print(f"Warning: Could not create sounds - {e}")
            print("Tip: Install numpy with: pip install numpy")
    
    def create_beep_sound(self, frequency, duration):
        """Tạo âm thanh beep đơn giản"""
        try:
            if np is None:
                raise RuntimeError("numpy not available")
            sample_rate = 22050
            frames = int(duration * sample_rate)
            
            # Tạo mảng time
            t = np.linspace(0, duration, frames, False)
            
            # Tạo sine wave
            wave = np.sin(frequency * 2 * np.pi * t)
            
            # Apply envelope để tránh click sounds
            envelope = np.ones_like(wave)
            fade_samples = int(0.01 * sample_rate)  # 10ms fade
            envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
            envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
            wave = wave * envelope
            
            # Scale to 16-bit range
            wave = (wave * 32767).astype(np.int16)
            
            # Stereo (2 channels)
            stereo_wave = np.column_stack((wave, wave))
            
            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound
        except Exception as e:
            # Fallback: return a dummy Sound-like object to avoid crashes
            print(f"Error creating beep sound: {e}")
            return None
    
    def create_chord_sound(self, frequencies, duration):
        """Tạo âm thanh chord"""
        try:
            if np is None:
                raise RuntimeError("numpy not available")
            sample_rate = 22050
            frames = int(duration * sample_rate)
            
            # Tạo mảng time
            t = np.linspace(0, duration, frames, False)
            
            # Mix multiple frequencies
            wave = np.zeros(frames)
            for freq in frequencies:
                wave += np.sin(freq * 2 * np.pi * t) / len(frequencies)
            
            # Apply envelope
            envelope = np.ones_like(wave)
            fade_samples = int(0.01 * sample_rate)
            envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
            envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
            wave = wave * envelope
            
            # Scale to 16-bit range
            wave = (wave * 32767).astype(np.int16)
            
            # Stereo
            stereo_wave = np.column_stack((wave, wave))
            
            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound
        except Exception as e:
            print(f"Error creating chord sound: {e}")
            return None
    
    def play_sound(self, sound_name):
        """Phát âm thanh"""
        if self.sound_enabled and sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def toggle_sound(self):
        """Bật/tắt âm thanh"""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled
