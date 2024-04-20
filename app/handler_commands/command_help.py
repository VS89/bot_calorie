

class HandlerCommandHelp:

    @staticmethod
    def get_help_message() -> str:
        msg_by_row = [
            'Данный бот поможет тебе контролировать потребление и расход калорий.',
            'Каждый день тебе нужно вводить свой вес, а бот будет рассчитывать тебе норму кКал, '
            'для похудения необходимо потреблять норму кКал минус 500.',
            'Так же ты можешь вводить твои израсходованные кКал, которые потратил на активностях',
            'Ты можешь в любой момент обновить свой коэффициент активности используя команду /activity_coef',
            'Если хочешь посмотреть все команды бота, то используй команду /start',
        ]
        return '\n'.join(msg_by_row)