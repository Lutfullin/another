import telebot
import re


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# comment here
# another comment here
#bot = telebot.TeleBot(config.token, parse_mode=None)
#подключаемся к ботику
bot = telebot.TeleBot("1691512641:AAE6IfALbbm8I4jkfBRQDvGNl4RsgVcqMxs", parse_mode=None)

#подключаем БД
cred = credentials.Certificate(r"D:\sqlbases\fatcalculator-ee746-firebase-adminsdk-2wjzv-a5ef5a5653.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fatcalculator-ee746-default-rtdb.firebaseio.com/'
})

ref = db.reference('Fat_Calculator')


import datetime
now = datetime.datetime.now()


def AddFood(id, name, protein, fat, carboh):
    data = {
        name:
        {
            "protein": protein,
            "fat": fat,
            "cabroh": carboh,
            "callories": ((4 * carboh) + (4 * protein) + (9 * fat))	
        }
    }
    ref.child(str(id)+"/My_products/").update(data)


def I_have_eatten(id, name, protein, fat, carboh, callories,mass):
    
    coeff = float(mass)/100
    data = {
        name:
        {
            "protein": protein*coeff,
            "fat": fat*coeff,
            "cabroh": carboh*coeff,
            "mass": mass,
            "callories": callories*coeff
        }
    }
    ref.child(str(id)+"/Eatten/"+str(now.day)+"_"+str(now.month)+"_"+str(now.year)).update(data)


#команда добавляющая новый продукт в реестр продуктов
@bot.message_handler(commands=['add'])
def send_welcome(message):

    bot.send_message(message.chat.id,
                     'Че хочешь добавить? Образец: "Яблоко 0.4 0.4 9.8" - это типа белки жиры углеводы в граммах')
    ref.child(str(message.chat.id)).update({"state":"adding"})#переключаем - чтобы чат ждал




@bot.message_handler(commands=['start'])
def send_welcome(message):

    '''
    #создаем новый рацион для нового чата
    data = {
        message.chat.id:
        {
            "state": "start"
        }
    }
    '''

    ref.child(str(message.chat.id)).update({"state":"start"})

    bot.send_message(message.chat.id,
                     "/eatten - узнай сколько всего сегодня съел\n"
                     "/add - добавить новый продутк в реестр\n"
                     "/have - сколько продуктов в реестре\n"
                     "/delete - удалить, что съел\n"
                     'Если съел напиши: "проудкт 234" 234 - это масса съеденного в граммах')



#обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def send_text(message):


    if (ref.child(str(message.chat.id)+"/state").get() == "adding"):#проверяем переключатель. ждет ли чат нового продукта в реестр
        try:
            product = message.text.lower() #делаем все маленькими буквами

            result = re.split(r' ', product)#разделяем по пробелам
            # "хлеб 34 23 75" → "хлеб", "34", "23", "75"
            #34 - белки, 23 - жиры, 75 - углеводы


            #добавляем в реестр продуктов новый объект - продукт
            AddFood(message.chat.id,result[0],float(result[1]),float(result[2]),float(result[3]))

            bot.send_message(message.chat.id, "Дело сделано!")


        #ну мало ли пойдет не так
        except Exception:
            bot.send_message(message.chat.id,"слышь, шутник иди в баню, напиши норм продукт, мы тута работаем вообще т")

        finally:
            #обратно переключим, чтобы чат больше не ждал продукт
            ref.child(str(message.chat.id)).update({"state":"start"})     

    elif(ref.child(str(message.chat.id)+"/state").get() == "start"):#если чат не ждет нового продукта, то пусть пока будет так. что пациент что-то съел

        text_of_message = message.text.lower()  # делаем все маленькими буквами
        result = re.split(r' ', text_of_message)#по пробелу разделяем название продукта и его массу
            #яблоко 250 → "яблоко" "250"
            #250 - это масса съеденного в граммах


        
        

        prod_info = ref.child("Comon_products/"+result[0]).get()

        


        if (prod_info is None):
            prod_info = ref.child(str(message.chat.id)+"/My_products/"+result[0]).get()
            
            if (prod_info is None):
                bot.send_message(message.chat.id, "Такой продукт не найден. Если хотите добавить, жмякните на /add ")
                
            else:
                I_have_eatten(message.chat.id, result[0], prod_info["protein"], prod_info["fat"], prod_info["cabroh"], prod_info["callories"], result[1])
                bot.send_message(message.chat.id, "добавлено!")                
        else:
            I_have_eatten(message.chat.id, result[0], prod_info["protein"], prod_info["fat"], prod_info["cabroh"], prod_info["callories"], result[1])
            bot.send_message(message.chat.id, "добавлено!")




bot.polling()
