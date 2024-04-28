from typing import Any

from app.keyboards import InlineKeyboardsModel, InlineKeyboardButtonModel
from app.models.telegram.tg_request_models import SendMessageModel


class CommandName:
    START = '/start'
    HELP = '/help'
    ACTIVITY_COEF = '/activity_coef'
    STATISTICS = '/statistics'
    EXPORT = '/export'


class LimitValues:
    MIN_VALUE_KG = 40
    MAX_VALUE_KG = 250


class PrefixCallbackData:
    """
    Префиксы для callback data в inline кнопках
    """

    ACTIVITY_COEF = 'acoef'


class TextBotMessage:
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


class MessageConstant:

    def __init__(self, user_id: int, callback_data: Any = None, text: str | None = None):
        self._user_id = user_id
        self._callback_data = callback_data
        self._text = text

    @property
    def confirm_activity_coef_msg(self) -> SendMessageModel:
        return SendMessageModel(
            chat_id=self._user_id,
            text=TextBotMessage.CONFIRM_CHANGE_ACTIVITY_COEF_MSG.format(self._callback_data),
            reply_markup=InlineKeyboardsModel(rows=1).create_keyboard(buttons=[
                InlineKeyboardButtonModel(
                    text=TextBotMessage.YES,
                    callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_{TextBotMessage.YES}_{self._callback_data}'),
                InlineKeyboardButtonModel(
                    text=TextBotMessage.NO,
                    callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_{TextBotMessage.NO}')
            ])
        )

    @property
    def select_activity_coef_msg(self) -> SendMessageModel:
        return SendMessageModel(
            chat_id=self._user_id,
            text=self._text,
            reply_markup=InlineKeyboardsModel(rows=1).create_keyboard(buttons=[
                InlineKeyboardButtonModel(text='1', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_1'),
                InlineKeyboardButtonModel(text='2', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_2'),
                InlineKeyboardButtonModel(text='3', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_3'),
                InlineKeyboardButtonModel(text='4', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_4'),
                InlineKeyboardButtonModel(text='5', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_5'),
            ])
        )

    @property
    def success_registration_msg(self) -> SendMessageModel:
        return SendMessageModel(chat_id=self._user_id, text=TextBotMessage.SUCCESS_REGISTRATION_MSG)
