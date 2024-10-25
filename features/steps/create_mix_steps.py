from behave import *
from main import create_mix
import hashlib

@given('Существует аудиофайл "{file_name}"')
def step_impl(context, file_name):
  context.files = [file_name]

@given('Начальное время для файла - {start_time} секунд')
def step_impl(context, start_time):
  context.start_times = [int(start_time)]

@given('Конечное время для файла - {end_time} секунд')
def step_impl(context, end_time):
  context.end_times = [int(end_time)]

@given('Существуют аудиофайлы "{file_name1}" и "{file_name2}"')
def step_impl(context, file_name1, file_name2):
  context.files = [file_name1, file_name2]

@given('Начальные времена для файлов - {start_time1} и {start_time2} секунд соответственно')
def step_impl(context, start_time1, start_time2):
  context.start_times = [int(start_time1), int(start_time2)]

@given('Конечные времена для файлов - {end_time1} и {end_time2} секунд соответственно')
def step_impl(context, end_time1, end_time2):
  context.end_times = [int(end_time1), int(end_time2)]

@when('Вызывается функция create_mix с данными')
def step_impl(context):
  try:
    create_mix(context.files, context.start_times, context.end_times)
    context.success = True
  except ValueError:
    context.success = False

@then('Создается микс "mix.wav"')
def step_impl(context):
  assert context.success == True

@then('Хэш MB5 созданного микса совпадает с хэшем эталонного файла "{want_file}"')
def step_impl(context, want_file):
  with open("mix.wav", 'rb') as f:
    mix_hash = hashlib.md5(f.read()).hexdigest()
  with open(want_file, 'rb') as f:
    expected_hash = hashlib.md5(f.read()).hexdigest()
  assert mix_hash == expected_hash

@then('Возникает исключение ValueError')
def step_impl(context):
  assert context.success == False
