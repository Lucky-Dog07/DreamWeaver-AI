import wave
import io
import numpy as np
from typing import Tuple, Optional

class AudioProcessor:
    """音频处理工具"""

    @staticmethod
    def create_wav_header(
        num_channels: int = 1,
        sample_rate: int = 16000,
        num_samples: int = 0
    ) -> bytes:
        """
        创建WAV文件头

        Args:
            num_channels: 声道数
            sample_rate: 采样率
            num_samples: 样本数

        Returns:
            WAV文件头字节数据
        """
        byte_rate = sample_rate * num_channels * 2
        block_align = num_channels * 2
        bytes_per_sample = num_channels * 2
        data_size = num_samples * bytes_per_sample

        # WAV文件头
        header = b'RIFF'
        header += (36 + data_size).to_bytes(4, 'little')
        header += b'WAVE'
        header += b'fmt '
        header += (16).to_bytes(4, 'little')  # subchunk1size
        header += (1).to_bytes(2, 'little')   # AudioFormat (1 = PCM)
        header += num_channels.to_bytes(2, 'little')
        header += sample_rate.to_bytes(4, 'little')
        header += byte_rate.to_bytes(4, 'little')
        header += block_align.to_bytes(2, 'little')
        header += (16).to_bytes(2, 'little')  # BitsPerSample
        header += b'data'
        header += data_size.to_bytes(4, 'little')

        return header

    @staticmethod
    def merge_audio_chunks(audio_chunks: list) -> bytes:
        """
        合并多个音频块

        Args:
            audio_chunks: 音频块列表

        Returns:
            合并后的WAV文件字节数据
        """
        try:
            if not audio_chunks:
                return b''

            # 创建BytesIO对象
            output = io.BytesIO()

            # 使用wave模块创建WAV文件
            with wave.open(output, 'wb') as wav_file:
                # 假设是16bit单声道WAV, 采样率16000Hz
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(16000)

                # 合并所有音频数据
                for chunk in audio_chunks:
                    wav_file.writeframes(chunk)

            output.seek(0)
            return output.getvalue()

        except Exception as e:
            print(f"音频合并失败: {str(e)}")
            return b''

    @staticmethod
    def adjust_audio_volume(audio_data: bytes, volume_factor: float = 1.0) -> bytes:
        """
        调整音频音量

        Args:
            audio_data: WAV格式音频数据
            volume_factor: 音量调整系数 (0.5 = 50%, 2.0 = 200%)

        Returns:
            调整后的音频字节数据
        """
        try:
            # 读取WAV文件
            wav_file = io.BytesIO(audio_data)
            with wave.open(wav_file, 'rb') as wf:
                frames = wf.readframes(wf.getnframes())
                num_channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                framerate = wf.getframerate()

            # 转换为numpy数组
            audio_array = np.frombuffer(frames, dtype=np.int16)

            # 调整音量（确保不超过范围）
            adjusted_audio = np.clip(audio_array * volume_factor, -32768, 32767).astype(np.int16)

            # 转换回WAV格式
            output = io.BytesIO()
            with wave.open(output, 'wb') as wf:
                wf.setnchannels(num_channels)
                wf.setsampwidth(sample_width)
                wf.setframerate(framerate)
                wf.writeframes(adjusted_audio.tobytes())

            output.seek(0)
            return output.getvalue()

        except Exception as e:
            print(f"音量调整失败: {str(e)}")
            return audio_data

    @staticmethod
    def add_fade_in_out(audio_data: bytes, fade_duration: float = 0.5) -> bytes:
        """
        添加淡入淡出效果

        Args:
            audio_data: WAV格式音频数据
            fade_duration: 淡入/淡出时长（秒）

        Returns:
            处理后的音频字节数据
        """
        try:
            # 读取WAV文件
            wav_file = io.BytesIO(audio_data)
            with wave.open(wav_file, 'rb') as wf:
                frames = wf.readframes(wf.getnframes())
                num_channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                framerate = wf.getframerate()

            # 转换为numpy数组
            audio_array = np.frombuffer(frames, dtype=np.int16)

            # 计算淡入淡出样本数
            fade_samples = int(fade_duration * framerate)

            # 淡入
            fade_in = np.linspace(0, 1, fade_samples)
            audio_array[:fade_samples] = (audio_array[:fade_samples] * fade_in).astype(np.int16)

            # 淡出
            fade_out = np.linspace(1, 0, fade_samples)
            audio_array[-fade_samples:] = (audio_array[-fade_samples:] * fade_out).astype(np.int16)

            # 转换回WAV格式
            output = io.BytesIO()
            with wave.open(output, 'wb') as wf:
                wf.setnchannels(num_channels)
                wf.setsampwidth(sample_width)
                wf.setframerate(framerate)
                wf.writeframes(audio_array.tobytes())

            output.seek(0)
            return output.getvalue()

        except Exception as e:
            print(f"淡入淡出效果添加失败: {str(e)}")
            return audio_data

    @staticmethod
    def get_audio_duration(audio_data: bytes) -> float:
        """
        获取音频时长

        Args:
            audio_data: WAV格式音频数据

        Returns:
            音频时长（秒）
        """
        try:
            wav_file = io.BytesIO(audio_data)
            with wave.open(wav_file, 'rb') as wf:
                num_frames = wf.getnframes()
                framerate = wf.getframerate()
                duration = num_frames / framerate
                return duration

        except Exception as e:
            print(f"获取音频时长失败: {str(e)}")
            return 0.0

    @staticmethod
    def get_audio_info(audio_data: bytes) -> dict:
        """
        获取音频信息

        Args:
            audio_data: WAV格式音频数据

        Returns:
            包含音频信息的字典
        """
        try:
            wav_file = io.BytesIO(audio_data)
            with wave.open(wav_file, 'rb') as wf:
                num_channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                framerate = wf.getframerate()
                num_frames = wf.getnframes()
                duration = num_frames / framerate

                return {
                    "channels": num_channels,
                    "sample_width": sample_width,
                    "sample_rate": framerate,
                    "num_frames": num_frames,
                    "duration": duration,
                    "bitrate": framerate * num_channels * sample_width * 8
                }

        except Exception as e:
            print(f"获取音频信息失败: {str(e)}")
            return {}

    @staticmethod
    def validate_audio(audio_data: bytes) -> Tuple[bool, str]:
        """
        验证音频文件

        Args:
            audio_data: 音频字节数据

        Returns:
            (是否有效, 错误信息)
        """
        try:
            if not audio_data:
                return False, "音频数据为空"

            wav_file = io.BytesIO(audio_data)
            with wave.open(wav_file, 'rb') as wf:
                if wf.getnframes() == 0:
                    return False, "音频文件为空"

                if wf.getframerate() not in [8000, 16000, 22050, 44100, 48000]:
                    return False, "不支持的采样率"

            return True, ""

        except Exception as e:
            return False, f"无效的音频文件: {str(e)}"

    @staticmethod
    def normalize_audio(audio_data: bytes) -> bytes:
        """
        规范化音频（调整到最大音量但不失真）

        Args:
            audio_data: WAV格式音频数据

        Returns:
            规范化后的音频字节数据
        """
        try:
            wav_file = io.BytesIO(audio_data)
            with wave.open(wav_file, 'rb') as wf:
                frames = wf.readframes(wf.getnframes())
                num_channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                framerate = wf.getframerate()

            # 转换为numpy数组
            audio_array = np.frombuffer(frames, dtype=np.int16)

            # 计算最大绝对值
            max_val = np.max(np.abs(audio_array))

            if max_val > 0:
                # 规范化到最大值
                normalized = (audio_array / max_val * 32767).astype(np.int16)
            else:
                normalized = audio_array

            # 转换回WAV格式
            output = io.BytesIO()
            with wave.open(output, 'wb') as wf:
                wf.setnchannels(num_channels)
                wf.setsampwidth(sample_width)
                wf.setframerate(framerate)
                wf.writeframes(normalized.tobytes())

            output.seek(0)
            return output.getvalue()

        except Exception as e:
            print(f"音频规范化失败: {str(e)}")
            return audio_data

    @staticmethod
    def convert_audio_format(audio_data: bytes, target_sample_rate: int = 16000) -> bytes:
        """
        转换音频格式

        Args:
            audio_data: WAV格式音频数据
            target_sample_rate: 目标采样率

        Returns:
            转换后的音频字节数据
        """
        try:
            wav_file = io.BytesIO(audio_data)
            with wave.open(wav_file, 'rb') as wf:
                frames = wf.readframes(wf.getnframes())
                num_channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                original_sample_rate = wf.getframerate()

            # 转换为numpy数组
            audio_array = np.frombuffer(frames, dtype=np.int16)

            # 如果采样率不同，进行重采样
            if original_sample_rate != target_sample_rate:
                ratio = target_sample_rate / original_sample_rate
                new_length = int(len(audio_array) * ratio)
                # 使用线性插值
                indices = np.linspace(0, len(audio_array) - 1, new_length)
                audio_array = np.interp(indices, np.arange(len(audio_array)), audio_array).astype(np.int16)

            # 转换回WAV格式
            output = io.BytesIO()
            with wave.open(output, 'wb') as wf:
                wf.setnchannels(num_channels)
                wf.setsampwidth(sample_width)
                wf.setframerate(target_sample_rate)
                wf.writeframes(audio_array.tobytes())

            output.seek(0)
            return output.getvalue()

        except Exception as e:
            print(f"音频格式转换失败: {str(e)}")
            return audio_data
