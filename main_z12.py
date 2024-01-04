from collections import UserDict
from datetime import datetime
import time
import pickle

"""
Консольна програма записує телефонні номери у словник, реалізована з технологією класів.

Методи класу Record:
add_birthday(self, birthday_s) - додає день народження
days_to_birthday(self) -пише скільки днів залишилось до дня народження
add_phone(self,phone_s) - Додає телефон до списку запису
edit_phone(self, old_phone, new_phone) -Змінює телефон
remove_phone(self, phone) -видаляє телефон зі списку запису
find_phone(self, num_phone) - знаходить теелефон

Методи класу AddressBook:
add_record(self, record) -додає запис до книги(словник-імя:дані)
get_all_in_page(self,n) - видає книгу по порціям п-записів за раз, якщо не вказати товидасть всі записи за раз
get_all(self,count=-1) видає книгу по порціям count-записів за раз, якщо не вказати товидасть всі записи за раз
find(self, name) -Знаходить запис по імені
delete(self, name) Видаляє запис з книги по імені
get_find(self,found="") Виводить в консоль записи які включають в собі пошуковий рядок(частина номера або імені)

"""
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW="\033[93m"
RESET = "\033[0m"
BLUE = "\033[94m"

class Field:
    def __init__(self, value):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value=new_value



    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super.__init__(self,value)



class Phone(Field):
   def __init__(self, value):
        if int(value) and len(value)==10:
            self.value = value
        else:
            raise ValueError


class Birthday(Field):
    def __init__(self, value):
      try:
           self.value = value
           d=value.split("-")
           self.date=datetime(int(d[2]),int(d[1]),int(d[0]))
      except Exception as e:
          raise ValueError



class Name(Field):
    def __init__(self, value):
        self.value = value



class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday=birthday
        if birthday:
            try:
                self.date=Birthday(birthday)
            except  ValueError:
                print('день народження повинен бути в строковому типі "DD-MM-YYYY"')

    def add_birthday(self, birthday_s):
        try:
            self.value=birthday_s
            self.birthday = Birthday(birthday_s)
        except  ValueError:
            print(f'{birthday_s} день народження повинен бути в строковому типі "DD-MM-YYYY"')

    def days_to_birthday(self):
        if self.birthday:
            current_datetime = datetime.now()
            dbirt=datetime(current_datetime.year, self.birthday.date.month, self.birthday.date.day)
            if current_datetime>dbirt:
                dbirt=datetime(current_datetime.year+1, self.birthday.date.month, self.birthday.date.day)

            days= dbirt-current_datetime
            print(f"До дня народження {self.name}  залишилось {days.days} днів")
        else:
            print(f"birthday of {self.name} is unknown")

    def add_phone(self,phone_s):
      try:
          self.phones.append(Phone(phone_s))
      except ValueError as e:
          if len(str(e))>0:
             print(f'{RED}{e}{YELLOW} -у номері телефона мають бути тільки цифри {RESET}')
          else:
             print(f'{RED}{phone_s}{YELLOW}  номер телефона має складатись з 10 цифр{RESET}')

    def edit_phone(self, old_phone, new_phone):
        n=0
        f=True
        for phone in self.phones:
            if phone.value==old_phone:
                f=False
                self.phones.pop(n)
                self.phones.insert(n,Phone(new_phone))
            n+=1
        if f:
            raise ValueError

    def remove_phone(self, phone):
        n = 0
        f = True
        try:
            for phon in self.phones:
                if phon.value == phone:
                    f = False
                    self.phones.pop(n)
                n += 1
            if f:
                raise ValueError
        except ValueError:
            print(f'{RED}{phone} {YELLOW}- не знайдений{RESET}')

    def find_phone(self, num_phone):
        for phone in self.phones:
            if phone.value == num_phone:
                return phone

    def __str__(self):
        sp=f"{BLUE} phones:{YELLOW} {'; '.join(p.value for p in self.phones)}" if self.phones else ""
        sb=f",{BLUE} birthday: {YELLOW} {self.birthday}{RESET}" if self.birthday else ""
        return (f"{BLUE}Contact name:{YELLOW} {self.name.value} {sp} {sb}")


class AddressBook(UserDict):

    def add_record(self, record):
       self[record.name.value]=record


    def get_all_in_page(self,n=0):

        list_rec=[]
        for name, record in self.data.items():
            list_rec.append(record)
        if n<=0:
           n=len(list_rec)

        def list_generator(n, x=0):
            y = n + x
            for l in list_rec[x:y]:
                print(l)
            if y >= len(list_rec):
                return
            
            if input("нажміть  Enter для продовження") == "":
                if (x + n) <= len(list_rec):
                    x = x + n
                    list_generator(n, x)

        list_generator(n)

    def get_find(self,found=""):
        for name, record in self.data.items():
           find_tel=0
           for num in record.phones:
              if str(num).find(found)>=0:
                  find_tel=1
           if (name.find(found)>=0 or find_tel==1):
               print(record)


    def get_some(self,x,y):
        i=0
        for name, record in self.data.items():
           if (x <=i and i<=y):
               print(record)
           i += 1
    def get_all(self,count=-1):
        if count==-1 or count>len(self.data.items()):
            a = len(self.data.items())
        else:
            a=count-1

        y=a
        self.get_some(0,y)
        while y<len(self.data.items()):
            if input("нажміть  Enter для продовження")=="":
                print("%" * 50)
                x=y+1
                y+=a+1
                self.get_some(x, y)





    def find(self, name):
        for nam, rec in self.data.items():
            if rec.name.value==name:
               return rec

    def delete(self, name):
       for nam, rec in self.data.items():
            if nam == name:
                del self[nam]
                return nam
       return None

    def save_to_file(self,filename):
        with open(filename, 'wb') as fh:
            pickle.dump(self,fh)

def main():

    def read_from_file(file):
        with open(file, 'rb') as fh:
            return pickle.load(fh)
    try:
        book=read_from_file(filename)
        #book.get_all()
    except Exception:
        book = AddressBook()


    print(f'{YELLOW}Вітаю! Ви зайшли в книгу контаків, для виходу введіть "exit" , Довідка по командам -"Help"{RESET}')

    def help():
        print(f' List of comand:\n'
              f'{YELLOW} add {BLUE}-add contact to phone book\n'
              f'{YELLOW} all{BLUE}- показати всі записи\n'
              f'{YELLOW} add tel {BLUE}- add phone to record with Name\n'
              f'{YELLOW} delete{BLUE} - delete  record from list\n'
              f'{YELLOW} find {BLUE}- search for records by part of a name or phone number\n'
              f'{YELLOW} help {BLUE}- help\n'
              f'{YELLOW} exit  {BLUE}- exit from program\n{RESET}')

    while True:
        data=input(">").lower()
        if data=="exit":
            book.save_to_file(filename)
            break
        elif data=="help":
            help()
        elif data=="add":
            name=input("веедіть імя :")
            if (name):
              record = Record(name)
              phone=input("веедіть номер тел (або Enter для пропуску):")
              if phone:
                  record.add_phone(phone)
              birthday = input("веедіть lane дату народження [DD-MM-YYYY](або Enter для пропуску):")
              if birthday:
                  record.add_birthday(birthday)
              book.add_record(record)
        elif data == "add tel":
            name = input("веедіть імя :")
            if (name):
                rec=book.find(name)
                if rec:
                   phone = input("веедіть номер тел:")
                   rec.add_phone(phone)
                else:
                  print(f"ім'я {name} не знайдено у книзі")

        elif data=="delete":
            name = input("веедіть імя :")
            if (name ):
              nam=book.delete(name)
              if nam:
                 print(f"{nam} видалено з книги")
              else:
                 print(f"{name} не знайдено в книзі")
        elif data=="find":
             f=input("введіть пошуковий рядок (частину імені або телефона):")
             book.get_find(f)

        elif data=="all":
            n=-1
            if len(book.data.items())>10:
                n=10
            book.get_all(n)
        else:
            print(f'команда "{data}" не визначена')






if __name__ == "__main__":
    filename = "save_contacts.bin"
    main()
#
#
#
# record1=Record("Pepo")
# record1.add_phone("7889ewrwe")
# record1.add_phone("7889667733")
# record1.add_phone("7889662233")
# record1.add_phone("788933")
# record1.find_phone("7889667733")
#
# record1.edit_phone("7889667733","7889667722")
#
#
#
#
#
# record2=Record("Pipo")
# record2.add_phone("7889940")
# record2.add_phone("9044992020")
# record2.add_phone("30349920202")
# record2.add_phone("9044999990")
# record2.days_to_birthday()
# record2.add_birthday("22-09-1978")
#
#
# record3=Record("Papo",)
# record3.add_birthday("31-01-2003")
# print("+"*25)
# record3.days_to_birthday()
#
# record4=Record("Pupo","30-03-1969")
# record4.add_phone("7889940222")
# record4.add_phone("9044999999")
#
#

# book.add_record(record1)
# book.add_record(record2)
# book.add_record(record3)
# book.add_record(record4)
#
#
#
#
#
# for name, record in book.data.items():
#         print(f'---{record}')
#
# print("*1"*20)
# book.get_all()
# print("*2"*20)
# book.delete("Pipo")
# book.get_all()
# print("*3"*20)
#
#
#
#
#
#
# print(f'знайшли {book.find("Pepo")}')
#
# book.find("Pepo").add_phone("7889662244")
# print(f'знайшли {book.find("Pepo")}')
# book.find("Pepo").edit_phone("7889662244", "7889662266")
#
# print(f'знайшли {book.find("Pepo")}')
#
#
#
#
#
# print('_______________________________')
#
# book.get_all()
#
# db=Birthday("17-03-2002")
# print(db)
# print(db.date.date())
#
#
# d="2012-04-19"
# ds=d.split("-")
# print(ds)
# dat=datetime(int(ds[0]),int(ds[1]),int(ds[2]))
# print(dat.date())
#
#
# seventh_day_2020 = datetime(year=2020, month=1, day=7, hour=14)
# print(seventh_day_2020.strftime(' %d %B %Y %A')) # Tuesday 07 January 2020
#
# book.find("Papo").add_phone("7889662245")
# print('&'*25)
# start_time = datetime.now().time()
# book.get_all(7)
# print (f"{datetime.now().time()} - {start_time}")
# print('&'*25)
# book.get_some(1,2)
#
# elist=[4,6,3,9,2,6,8,77,3]
#
# print('#'*25)
#
#
#
#
#
# start_time = datetime.now().time()
# book.get_all_in_page(2)
# print (f"{datetime.now().time()} - {start_time}")
