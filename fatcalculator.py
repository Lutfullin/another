import telebot
import re
#import config

#bot = telebot.TeleBot(config.token, parse_mode=None)

bot = telebot.TeleBot("1691512641:AAE6IfALbbm8I4jkfBRQDvGNl4RsgVcqMxs", parse_mode=None)


#класс для хранения базы разных продуктов и информаци о них
class Product:

    def __init__(self, name, protein, fat, carboh):
        #сколько там белков жиров и углеводов
        self.protein = protein
        self.fat = fat
        self.carboh = carboh
        #название продукта
        self.name = name
        #сразу считаем калории в 100 граммах! так как carboh protein fat - это количетсво граммов в 100 граммах
        self.calories = ((4 * carboh) + (4 * protein) + (9 * fat))



#класс для хранения всего съеденного за день
class Todays_ration:
    #на вход принимает ID чата
    def __init__(self, users_id):
        self.users_id = users_id

    state = "start"  # это переменная для переключения состояния ждет чат добавления нового продукта в реестр или нет
    #"start" - нулевое состояние
    #"addind" - пополняем реестр
    #"delete" - удаляем съеденное


    #изначально калорий ноль
    calories = 0


    #этот лист хранит список съеденных продуктов в их массой за сегодня
    ratio = [

        #название продукта
        ["start",
        #масса съеденого
        0,
        #сколько это калорий
        0
        ]

    ]


    #метод добавляющий продукты в рацион
    def add_product_to_ration(self, name, mass, calories):

        self.ratio.append([name,mass,calories])

        #сразу плюсанем калории
        self.calories += calories

    #метод, удаляющий продукт из рациона на вход он принимает индекс удаляемого компонента
    def delete_product_to_ration(self, index):
        self.ratio.pop(index-1)

    #метод, возвращающий в виде листа все, что съел персонаж
    def get_ratio(self):

        #это лист, который будет возвращать
        list_of_eatten = []


        if (len(self.ratio)>1):#первый элемент в рационе - это [start, 0, 0] - его считать не надо
            i = 1#счетчик для нумерации продуктов
            for item in self.ratio:
                if (item[0] != "start"):
                    list_of_eatten.append( str (i)+". "+item[0] + ", "+ str(item[1])+"г , "+str(item[2])+"ккал\n")
                    i+=1
            list_of_eatten.append("Всего: "+ str(self.calories)+"ккал")
        else:
            list_of_eatten = ["Ничего ты сегодня еще не поел!"]


        return list_of_eatten


#создадим лист из продуктов - туда сразу два дефотлных продукта
Products = [Product("яблоко", 0.4, 0.4, 9.8),Product("груша", 0.4, 0.4, 9.8)]

#в этом словаре хранятся рационы участников чата. ключ - это ID чата
Persons = {0:Todays_ration(0)}

@bot.message_handler(commands=['start'])
def send_welcome(message):

    #создаем новый рацион для нового чата
    Persons[message.chat.id]=Todays_ration(message.chat.id)

    bot.send_message(message.chat.id,
                     "/eatten - узнай сколько всего сегодня съел\n"
                     "/add - добавить новый продутк в реестр\n"
                     "/have - сколько продуктов в реестре\n"
                     "/delete - удалить, что съел\n"
                     'Если съел напиши: "проудкт 234" 234 - это масса съеденного в граммах')



#эта команда будет вовзращать сегодняшний рацион
@bot.message_handler(commands=['eatten'])
def send_welcome(message):

    #запрашивает функцию которая выдаст в виде листа все что съел персонаж
    for item in Persons[message.chat.id].get_ratio():
        bot.send_message(message.chat.id, item)


    #bot.send_message(message.chat.id, Persons[message.chat.id].get_ratio())


    '''
    #пишет в чат число калорий
    bot.send_message(message.chat.id, Persons[message.chat.id].calories)


    #пока в чат не умеет писать рацион так что принт
    print(Persons[message.chat.id].ratio)
    '''


#команда добавляющая новый продукт в реестр продуктов
@bot.message_handler(commands=['add'])
def send_welcome(message):

    bot.send_message(message.chat.id,
                     'Че хочешь добавить? Образец: "Яблоко 0.4 0.4 9.8" - это типа белки жиры углеводы в граммах')


    Persons[message.chat.id].state = "adding"#переключаем - чтобы чат ждал


#сколько есть всего в реестре
@bot.message_handler(commands=['have'])
def send_welcome(message):
    for i in Products:
        bot.send_message(message.chat.id, (i.name))





#команда, удаляющая еду из списка съеденного
@bot.message_handler(commands=['delete'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Че хочешь удалить? напиши норер строки")
    for item in Persons[message.chat.id].get_ratio():
        bot.send_message(message.chat.id, item)
    Persons[message.chat.id].state  = "delete"

#обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def send_text(message):


        if (Persons[message.chat.id].state == "adding"):#проверяем переключатель. ждет ли чат нового продукта в реестр

            try:
                product = message.text.lower() #делаем все маленькими буквами

                result = re.split(r' ', product)#разделяем по пробелам
                # "хлеб 34 23 75" → "хлеб", "34", "23", "75"
                #34 - белки, 23 - жиры, 75 - углеводы


                #добавляем в реестр продуктов новый объект - продукт
                Products.append(Product(result[0],float(result[1]),float(result[2]),float(result[3])))

                bot.send_message(message.chat.id, "Дело сделано!")


            #ну мало ли пойдет не так
            except Exception:
                bot.send_message(message.chat.id,"слышь, шутник иди в баню, напиши норм продукт, мы тута работаем вообще т")

            finally:
                #обратно переключим, чтобы чат больше не ждал продукт
                Persons[message.chat.id].state = "start"
        elif(Persons[message.chat.id].state == "start"):#если чат не ждет нового продукта, то пусть пока будет так. что пациент что-то съел

            is_it_found = False#нашли ли мы продукт в реестре

            try:
                product = message.text.lower()  # делаем все маленькими буквами
                result = re.split(r' ', product)#по пробелу разделяем название продукта и его массу
                    #яблоко 250 → "яблоко" "250"
                #250 - это масса съеденного в граммах




                #ищем продукт в реестре
                for i in Products:

                    if (i.name == result[0]):

                        is_it_found = True
                        #добавляем съеденный продукт в рацион и сразу по ходу дела считаем сколько это в калориях
                        Persons[message.chat.id].add_product_to_ration(i.name, float(result[1]), float(result[1])*(i.calories/100))
                                                                                #float(result[1]) - это масса
                                                                                    #i.calories - это калории в 100г! поэтому надо делить на 100
                        bot.send_message(message.chat.id, "добавлено!")
                        break
            except Exception:
                is_it_found = False

            finally:
                if (not is_it_found):
                    bot.send_message(message.chat.id, "Такой продукт не найден. Если хотите добавить, жмякните на /add ")
        elif(Persons[message.chat.id].state == "delete"):#если программка ждет удаления продукта

            try:
                print("here")

                intermediate_object = re.search(r'(\d)+',message.text)#ищем в тексте сообщения целове число
                number_of_deliting_point = int (intermediate_object.group(0))#преобразуем в интеджер
                Persons[message.chat.id].delete_product_to_ration(number_of_deliting_point)



            except Exception:
                bot.send_message(message.chat.id, "Ты че наделал, мудило? Все из-за тебя весь бот упал и люди остались без бота, пока разрабы не придут и не перезапустят, а это может случиться ой как не скоро. Надеюсь ты доволен собой? Да шучу я, тут все продумано на случай таких мудаков как ты. Так что иди в жопу!")
                print("сработало исключение при выполнении команды delete"+Exception)
            finally:
                Persons[message.chat.id].state == "start"


bot.polling()
