import wave
import numpy as np
import hashlib
import pytest

def create_mix(files, start_times, end_times, output_file="mix.wav"):
  """
  Args:
    files: Список путей к аудиофайлам.
    start_times: Список начальных времен для каждого файла в секундах.
    end_times: Список конечных времен для каждого файла в секундах.
    output_file: Имя файла для сохранения микса (по умолчанию "mix.wav").
  """
  if len(files) == 0 or len(start_times) == 0 or len(end_times) == 0:
    raise ValueError("invalid input, expected arrays with values")

  mix = []
  for i, file in enumerate(files):
    with wave.open(file, 'rb') as wf:
      # Получение параметров файла
      num_channels = wf.getnchannels()
      frame_rate = wf.getframerate()
      sample_width = wf.getsampwidth()
      num_frames = wf.getnframes()

      # Вычисление начала и конца в кадрах
      start_frame = int(start_times[i] * frame_rate)
      end_frame = int(end_times[i] * frame_rate)

      # Проверка на корректность входных данных
      if start_frame < 0 or end_frame > num_frames or start_frame > end_frame:
        raise ValueError(f"Неверные значения времени для файла '{file}'")

      # Чтение фрагмента из файла
      wf.setpos(start_frame)
      data = wf.readframes(end_frame - start_frame)

      # Преобразование в массив NumPy
      audio = np.frombuffer(data, dtype=np.int16)

      # Добавление фрагмента в микс
      mix.append(audio)

  # Объединение фрагментов в единый массив
  mix = np.concatenate(mix)

  # Сохранение микса в файл
  with wave.open(output_file, 'wb') as wf:
    wf.setnchannels(1)  # Количество каналов (может быть 1 или 2)
    wf.setframerate(44100)  # Частота дискретизации (например, 44100 Гц)
    wf.setsampwidth(2)  # Размер выборки (в байтах)
    wf.writeframes(mix.tobytes())

@pytest.mark.skip()
def test_create_mix_mb5(files, start_times, end_times, expected_file, want_file):
  """  Создает микс и сравнивает его с эталонным файлом по хэшу MB5.  """

  create_mix(files, start_times, end_times, expected_file)

  # Вычисление хэша MB5 для созданного микса
  with open(expected_file, 'rb') as f:
    mix_hash = hashlib.md5(f.read()).hexdigest()

  # Вычисление хэша MB5 для эталонного файла
  with open(want_file, 'rb') as f:
    expected_hash = hashlib.md5(f.read()).hexdigest()

  # Сравнение хэшей
  assert mix_hash == expected_hash

@pytest.mark.parametrize("files, start_times, end_times, expected_file, want_file", [
  (["audio.wav"], [0], [10], "single_file.wav", "expected_single_file.wav"),
  (["audio1.wav", "audio2.wav"], [0, 5], [10, 15], "multiple_files.wav", "expected_multiple_files.wav"),
])
def test_create_mix_mb5_parametrized(files, start_times, end_times, expected_file, want_file):
  test_create_mix_mb5(files, start_times, end_times, expected_file, want_file)

def test_create_mix_invalid_time():
  files = ["audio.wav"]
  start_times = [20]
  end_times = [0]
  with pytest.raises(ValueError):
    create_mix(files, start_times, end_times)


def test_create_mix_invalid_empty():
  files = []
  start_times = []
  end_times = []
  with pytest.raises(ValueError):
    create_mix(files, start_times, end_times)

# Запуск тестов
if __name__ == "__main__":
  ...