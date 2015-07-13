# -*- cp1250 -*-

import requests
from bs4 import BeautifulSoup

class MultiDict(object):
    
    def __init__(self,url="http://pl.bab.la/slownik/angielski-polski/"):
        self.Dict = {}
        self.cyfra = input('Podaj jezyk: \n \
                          1) angielski \n \
                          2) niemiecki \n \
                          3) rosyjski \n \
                          ---> ')
        jezyk = {1:'angielski', 2:'niemiecki', 3:'rosyjski'}
        url = 'http://pl.bab.la/slownik/' + jezyk[self.cyfra] + '-polski/'
        self.url = url

    def wypCyfre(self):
        return self.cyfra

    def seturl(self,url):
        self.url = url
        
    def _get_html_page(self,url):
        """Just to fetch url source into a string"""
        req = requests.get(url)
        return req

    def _chckifWord(self,obj):
        """"""
        return type(obj) == str
    
    def _chckifList(self,obj):
        """"""
        return type(obj) == list
    
    def addWord(self,obj):
        """obj: string/list/tuple."""
        if self._chckifWord(obj) and obj not in self.Dict:
            self.Dict[obj] = []
            
        elif self._chckifList(obj):
            self.Dict.update({word:[] for word in obj})

    def _wrapper(self,word):
        """just to wrapp smthng"""
        url = self.url + word
        return self._get_html_page(url)
        
    def _info(self):
        """just to create a readable information abt words"""
        Info = ""
        for word in self.Dict:
            temp = word + ": \n"
            for translation in self.Dict[word]:
                temp += "- " + translation + "\n"
            Info += temp + "\n"
        print Info
                
    def translate(self,hits=5,info=True):
        """hits: int - how many translation of words we wanna get.
           info: bool - True/False, depends on if we wanna print a message (True) or return dict (False)"""
        for key in self.Dict:
            url = self._wrapper(key)
            soup = BeautifulSoup(url.content,"html.parser")
            g_data = soup.find_all("div",{"class":"row-fluid result-row"})
            for item in g_data:
                temp = item.contents[3].find_all("a",{"class":"result-link"})
                for inf in temp:
                    if len(self.Dict[key]) == hits:
                        break
                    self.Dict[key].append(inf.text)
        if info == True:
            return self._info()
                

if __name__ == "__main__":
    d = MultiDict()

    plik = d.wypCyfre()
    jezyk_pliku = {1:'slowka_EN.txt', 2:'slowka_DE.txt', 3:'slowka_RU.txt'}

    f = open(jezyk_pliku[plik], 'r')
    fd2 = f.readlines()
    f.close()
    fd=[]
    for i in fd2:
        if '\n' in i:
            fd.append(i[:-1])
        else:
            fd.append(i)
    print fd
    
    d.addWord(fd)
    d.translate()