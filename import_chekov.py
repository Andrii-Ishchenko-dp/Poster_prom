import requests
import xlwt

token = input('Введите токен аккаунта: ')

cheks=[]
count_cheks=0

data_start = input('Введите дату начала выгрузки: ')
data_end = input('Введите дату конца выгрузки: ')

url_dash = 'https://joinposter.com/api/dash.getTransactions?token={}' \
           '&dateFrom={}' \
           '&dateTo={}'

res_chek = requests.get(url_dash.format(token,data_start,data_end)).json()

for l in res_chek['response']:
      countofstor ={
            'id':res_chek['response'][count_cheks]['transaction_id'],
            'date_close_date':res_chek['response'][count_cheks]['date_close_date']
      }
      count_cheks+=1
      cheks.append(countofstor) # Получил список чеков в указанный период времени

dish = []
activ_prom = []

for i in range(len(cheks)):
    count_dish = 0
    url_tovari = 'https://joinposter.com/api/dash.getTransactionsProducts?token={}' \
               '&transactions_id={}'
    res_dish=requests.get(url_tovari.format(token,cheks[i]['id'])).json()
    # dish.append(cheks[i]['date_close_date'])# добавляю дату перед позициями по акции
    for o in res_dish['response']:
        dic_dish={
            'prod_name':res_dish['response'][count_dish]['product_name'],
            'num':res_dish['response'][count_dish]['num'],
            'payed_sum':res_dish['response'][count_dish]['payed_sum'],
            'product_sum':res_dish['response'][count_dish]['product_sum'],
            'promotion_id':res_dish['response'][count_dish]['promotion_id']
        }
        if dic_dish['promotion_id']!=0:
            dish.append(dic_dish)# Получил список блюд с указанных чеков, на которые распространялась акция
            if activ_prom.count(dic_dish['promotion_id'])==0:
                activ_prom.append(dic_dish['promotion_id'])
        count_dish+=1

prom=[]
count_prom=0
url_prom = 'https://joinposter.com/api/clients.getPromotions?token={}'
res_prom = requests.get(url_prom.format(token)).json()
for p in res_prom['response']:
    dic_prom={
        'promotion_id':res_prom['response'][count_prom]['promotion_id'],
        'name':res_prom['response'][count_prom]['name']
    }
    prom.append(dic_prom)
    count_prom+=1

# создать отдельный список акций, которые были задействованы в этом периоде времени
wb = xlwt.Workbook()
activ_prom_with_name= []

for t in range(len(prom)):
    if int(prom[t]['promotion_id']) in activ_prom:
        activ_prom_with_name.append(prom[t])

# unic_name_dish=[]

# for q in range(len(dish)):
#     if dish[q]['prod_name'] not in unic_name_dish:
#         unic_name_dish.append(dish[q]['prod_name']['pro'])


for r in range(len(activ_prom_with_name)):
    ws = wb.add_sheet(activ_prom_with_name[r]['name'])
    ws.write(0, 0, 'Название')
    ws.write(0, 1, 'Количество')
    ws.write(0, 2, 'Цена без акции')
    ws.write(0, 3, 'Цена с акцией')
    ws.write(0, 4, 'Скидка')
    y = 1
    for b in dish:
        x = 0
        if b['promotion_id'] == int(activ_prom_with_name[r]['promotion_id']):
            ws.write(y,x, b['prod_name'])
            x += 1
            ws.write(y,x,float(b['num']))
            x += 1
            ws.write(y,x, float(b['product_sum']))
            x += 1
            ws.write(y,x, float(b['payed_sum']))
            x+=1
            ws.write(y,x,xlwt.Formula("C{}-D{}".format(y+1,y+1)))
            y += 1

wb.save('{}-{}.xls'.format(data_start, data_end))
print(dish)
print(activ_prom_with_name)



# задача - сделать список позиций, которые были проданы в период времени по акции, скидке
# Товары могут быть со скидкой, добавленные в чек по условиям акции и скидка может распространяться на весь чек
