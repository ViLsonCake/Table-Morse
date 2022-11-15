import re
import json
import requests
from bs4 import BeautifulSoup
import lxml


class Table_Morse:
    def __init__(self):
        self.url = 'https://calcsbox.com/post/perevodcik-azbuki-morze-onlajn.html'


    def main(self):
        self._txt_file(self.treatment(self.structure('latin')))


    def __request(self) -> str:
        self.responce = requests.get(self.url)

        return str(self.responce.text)


    def __save_html_file(self):
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(self.request())


    def __open_html_file(self) -> str:
        with open('index.html', encoding='utf-8') as file:
            self.src = file.read()

        return self.src


    def _json_file(self, data):
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


    def _txt_file(self, data: dict):
        self.output = ""
        for i in data.items():
            self.output += f'{i[0]}: {i[1]} \n'

        with open('table.txt', 'w', encoding='utf-8') as file:
            file.write(self.output)


    def scripe(self, text: str) -> list:
        self.soup = BeautifulSoup(text, 'lxml')

        self.table = self.soup.find('table', class_="table_morze")
        self.list_table = self.table.find_all('tr')

        for i in range(len(self.list_table)):
            self.list_table[i] = self.find_symbols(str(self.list_table[i]))

        return self.list_table[1:]


    def find_symbols(self, text: str) -> list:
        self.result = re.findall(r"\(.+?\)", text)

        for i in range(len(self.result)):
            self.result[i] = re.findall(r"'.+'", self.result[i])

        return self.result


    def structure(self, mode='latin') -> dict:
        self.table_dictionary = {}

        if mode.lower() == 'latin':
            for i in self.scripe(self.__request()):
                self.table_dictionary[i[1][0]] = i[2][0]

            return self.table_dictionary
        elif mode.lower() in ('cyrillic', 'cyrill', 'cyril'):
            for i in self.scripe(self.__request()):
                self.table_dictionary[i[0][0]] = i[2][0]

            return self.table_dictionary
        else:
            print(f'{mode} -> is incorrect mode.')
            return self.table_dictionary


    def treatment(self, objects: dict) -> dict:
        self.new_dictionary = {}

        for i in objects.items():
            self.new_dictionary[i[0][1:-1].strip()] = i[1][1:-1].strip()

        return self.new_dictionary


    def show(self, iterator) -> None:
        if type(iterator) is dict:
            for i in iterator.items():
                print(i)    
        else:
            for i in iterator:
                print(i)




if __name__ == '__main__':
    solution = Table_Morse()
    solution.main()
