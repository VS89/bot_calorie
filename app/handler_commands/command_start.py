

class HandlerCommandStart:

    @staticmethod
    def get_start_message() -> str:
        msg_by_row = [
            'Привет!',
            '\nМы рады видеть тебя в нашем "Похудизируй".',
            'Он создан, чтобы помочь тебе в твоем похудении.',
            'Чтобы добавить свой ввес нужно отправить сообщение, например, "85.1 кг"',
            'Чтобы добавить потребленные кКал - "+100 ккал"',
            'Чтобы добавить потраченные кКал - "-100 ккал"',
            'Если ты хочешь узнать подробности взаимодействия с нами, то используй команду /help',
            '\nКоманды бота:',
            '\n/help - показывает справку',
            '/start - показывает приветственное сообщение',
            '/activity_coef - добавление/обновления коэффициента активности от 1 до 5',
            '/statistics - получить динамику веса, потребляемых и израсходованных калорий за 10/30 дней',
            '/export - получить динамику веса, потребляемых и израсходованных калорий за все время в файле *.csv'
        ]
        return '\n'.join(msg_by_row)
