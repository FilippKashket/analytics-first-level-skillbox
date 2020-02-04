# -*- coding: utf-8 -*-

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.


class NotNameError(Exception):
    pass


class NotEmailError(Exception):
    pass


class LogFilter:

    def run(self, file_name):
        with open('registrations_good.log', 'w') as self.good_log:
            with open('registrations_bad.log', 'w') as self.bad_log:
                self._proceed_file(file_name)

    def _proceed_file(self, file_name):
        with open(file_name, 'r') as ff:
            for line in ff:
                self._proceed_line(line)

    def _proceed_line(self, line):
        try:
            self._check_line(line)
        except ValueError as exc:
            message = exc.args[0]
            if 'not enough values to unpack' in message:
                message = 'Неполные данные'
            elif 'invalid literal for int' in message:
                message = 'Возраст не является числом'
            self.bad_log.write(f'{line[:-1]} - {message}\n')
        except NotNameError:
            self.bad_log.write(line[:-1] + ' - Это не имя' + '\n')
        except NotEmailError:
            self.bad_log.write(line[:-1] + ' - Это не email' + '\n')
        else:
            self.good_log.write(line)

    def _check_line(self, line):
        name, email, age = line.split(' ')
        if not name.isalpha():
            raise NotNameError()
        if '@' not in email or '.' not in email:
            raise NotEmailError()
        if not 10 <= int(age) <= 99:
            raise ValueError('Age not in 10..99 range')


flt = LogFilter()
flt.run(file_name='registrations.txt')
