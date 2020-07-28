import datetime

import Data

def responder(message, username):

    def numMonthToString(num):
        if num == 1:
            return 'Января'
        elif num == 2:
            return 'Февраля'
        elif num == 3:
            return 'Марта'
        elif num == 4:
            return 'Апреля'
        elif num == 5:
            return 'Мая'
        elif num == 6:
            return 'Июня'
        elif num == 7:
            return 'Июля'
        elif num == 8:
            return 'Августа'
        elif num == 9:
            return 'Сентября'
        elif num == 10:
            return 'Октября'
        elif num == 11:
            return 'Ноября'
        elif num == 12:
            return 'Декабря'

    message = message.lower()
    splitedMsg = message.strip().split(" ")
    if (splitedMsg[0] == "!follow" or splitedMsg[0] == "!watchtime" or splitedMsg[0] == "!followed" or splitedMsg[0] == "!followage"):
        user_id = Data.Chat.userlist[username.lower()]["_id"]
        user_follows = Data.TwitchAPI.request(f'https://api.twitch.tv/kraken/users/{user_id}/follows/channels')
        for follow in user_follows['follows']:
            if follow['channel']['_id'] == Data.Stream.channel_ID:
                startTime = datetime.datetime.strptime(follow['created_at'],"%Y-%m-%dT%H:%M:%SZ")
                nowTimeNoForm = datetime.datetime.now(datetime.timezone.utc)
                daltaYear = nowTimeNoForm.year - startTime.year
                deltaMonth = nowTimeNoForm.month - startTime.month
                deltaDay = nowTimeNoForm.day - startTime.day

                if daltaYear > 0:
                    writeInMessage = f'{daltaYear} {Data.declensionNumsRus(daltaYear, "год", "года", "лет")}'
                elif deltaMonth > 0:
                    writeInMessage = f'{deltaMonth} {Data.declensionNumsRus(deltaMonth, "месяц", "месяца", "месяцев")}'
                elif deltaDay > 0:
                    writeInMessage = f'{deltaDay} {Data.declensionNumsRus(deltaDay, "день", "дня", "дней")}'
                else:
                    writeInMessage = "с сегодняшнего дня"

                return f'{username}, следит за каналом {writeInMessage}. С {startTime.day} {numMonthToString(startTime.month)} {startTime.year}'