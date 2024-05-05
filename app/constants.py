from typing import Any

from app.keyboards import InlineKeyboardsModel, InlineKeyboardButtonModel
from app.models.telegram.tg_request_models import SendMessageModel


class FormatFile:
    """
    Форматы файлов
    """

    PNG = 'png'
    CSV = 'csv'


class CommandName:
    """
    Команды бота
    """

    START = '/start'
    HELP = '/help'
    ACTIVITY_COEF = '/activity_coef'
    STATISTICS = '/statistics'
    EXPORT = '/export'


class LimitValues:
    """
    Лимиты
    """

    MIN_VALUE_KG = 40
    MAX_VALUE_KG = 250
    CALORIE_DEFICIT = 500
    CALORIE_BALANCE_LIMIT_A = 550
    CALORIE_BALANCE_LIMIT_B = 490
    CALORIE_BALANCE_LIMIT_C = 100
    CALORIE_BALANCE_LIMIT_D = -50
    STATISTIC_10_DAY = 10
    STATISTIC_30_DAY = 30


class PrefixCallbackData:
    """
    Префиксы для callback data в inline кнопках
    """

    ACTIVITY_COEF = 'acoef'
    WEIGHT = 'kg'
    STATISTICS = 'statistics'


class TextBotMessage:
    """
    Сообщения бота
    """

    ACTIVITY_COEF_FIRST_MSG_FOR_NEW_USER = '\n'.join([
        'И последний шаг перед стартом нашего пути это ввод коэффициента активности. '
        'Выбери его на клавиатуре под сообщением где:',
        '\n1 - сидячая работа, минимум спортивной активности',
        '2 - раз в неделю посещаешь тренажорный зал или бассейн',
        '3 - две/три тренировки в неделю',
        '4 - больше трех тренировок в неделю, но тебе чуть-чуть не хватает до профи',
        '5 - тяжелый физический труд, 5-6 тренировок в неделю или ты проффесиональный спортсмен',
        '\nЧтобы изменить значение данного коэффициента можно воспользоваться командой /activity_coef'
    ])

    ACTIVITY_COEF_MSG = '\n'.join([
        'Выбери свой коэффицицент активности:',
        '\n1 - сидячая работа, минимум спортивной активности',
        '2 - раз в недельку посещаешь тренажорный зал или бассейн',
        '3 - две/три тренировки в неделю',
        '4 - больше трех тренировок в неделю, но тебе чуть-чуть не хватает до профи',
        '5 - тяжелый физический труд, 5-6 тренировок в неделю или ты проффесиональный спортсмен'
    ])

    HELP_MSG = '\n'.join([
        'Данный бот поможет тебе контролировать потребление и расход калорий.',
        'Каждый день тебе нужно вводить свой вес, а бот будет рассчитывать тебе норму кКал, '
        'для похудения необходимо потреблять норму кКал минус 500.',
        'Так же ты можешь вводить твои израсходованные кКал, которые потратил на активностях',
        'Ты можешь в любой момент обновить свой коэффициент активности используя команду /activity_coef',
        'Если хочешь посмотреть все команды бота, то используй команду /start',
    ])

    START_MSG = '\n'.join([
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
    ])

    SECOND_START_MSG_FOR_NEW_USER = ('Перед тем как начать вести подсчет калорий, нам нужно узнать твой текущий вес в '
                                     'килограммах. Для этого введи текст - "N кг", где N - твой текущий вес')

    SUCCESS_REGISTRATION_MSG = ('Отлично! Теперь ты готов контролировать свою физическую активность и килокалории. '
                                'Не забудь каждый день добавлять свой текущий вес(лучше всего это делать '
                                'в одно и тоже время, например, утром перед завтраком). И помни, '
                                'достижение большой цели начинается с маленького шага вперед, и ты его уже сделал!')

    CONFIRM_CHANGE_ACTIVITY_COEF_MSG = 'Ты точно хочешь изменить свой коэффициент активности на {}?'

    SUCCESS_CONFIRM_CHANGE_ACTIVITY_COEF_MSG = ('Твой новый коэффициент активности успешно сохранен.\n'
                                                'И теперь твоя норма кКал составляет {}, '
                                                'но не забудь про дефицит -500 кКал')

    FAILED_CONFIRM_CHANGE_ACTIVITY_COEF_MSG = 'Хорошо, оставим все как было'

    YES = 'Да'

    NO = 'Нет'

    CAN_HANDLER_ONLY_TEXT = 'К сожалению я могу обрабатывать только текстовые сообщения'

    KCAL_BALANCE_LESS_MINUS_50 = 'Кажется, сегодня ты облопался!'
    KCAL_BALANCE_MORE_MINUS_50_LESS_100 = 'Сегодня ты не поправился!'
    KCAL_BALANCE_MORE_100_LESS_490 = 'Сегодня ты немножко молодец!'
    KCAL_BALANCE_MORE_490_LESS_550 = 'Отлично, ты молодец!'
    KCAL_BALANCE_MORE_550 = 'Ооо, тебе сегодня можно ещё покушать на {} kcal'

    SAVE_NEW_WEIGHT = ("Спасибо! Это мы запомнили ;)\n\n"
                       "Твоя норма кКал изменилась и теперь она составляет {}, но не забудь, что для похудения "
                       "нужно соблюдать дефицит -500 кКал.")

    CONFIRM_RESAVE_NEW_WEIGHT = "Сегодня был добавлен вес {} кг. Заменить?"

    SAVE_OLD_WEIGHT = "Оставили вес равный {} кг"

    SELECT_PERIOD_STATISTICS = "Выбери за какой период, в днях, ты хочешь получить статистику?"

    STATISTICS_NOT_FOUND = "К сожалению мы не смогли найти для вас статистику"

    STATISTICS_MSG = '\n'.join(['1) Дата',
                                '2) Вес',
                                '3) Потреблено(кКал)',
                                '4) Израсходовано(кКал)',
                                '5) Баланс(кКал)\n\n'])

    CAPTION_CHART_STATISTIC_WEIGHT = 'Твоя динамика веса за {} дней'
