import requests
from colorama import Fore
import json
import os

banner = f"""{Fore.LIGHTCYAN_EX}
     _______                       _______       __   __    
    |   _   .---.-.-----.-----.   |   _   .--.--|  |_|  |--.
    |.  1___|  _  |__ --|  -__|   |.  1   |  |  |   _|     | 
    |.  __)_|___._|_____|_____|   |.  _   |_____|____|__|__|
    |:  1   |                     |:  |   |             
    |::.. . |                     |::.|:. |              
    `-------'                     `--- ---'         {Fore.RESET}
    Developed by gui ;) | {Fore.LIGHTCYAN_EX}https://mdsmax.dev{Fore.RESET}
"""

def obterDatabase():
    with open("auth.json") as f:
        return json.load(f)

def VerificarWebSite(url):
    url = requests.get(url=url)
    if url.json()["message"] == "EaseAPI_Website":
        return True
    else: return False

def VerificarKey(url, key): # coloquei rate limit na API
    headers = {
        "authorization": key
    }
    response2 = requests.get(url=f"{url}/verifyKey", headers=headers)
    if not response2.status_code == 200:
        return False
    
    return True

def menu():
    os.system("cls" if os.name == "nt" else "clear")
    print(banner)
    print(f"""
    {Fore.LIGHTCYAN_EX}[ 1 ] API Informations{Fore.RESET}
    {Fore.LIGHTCYAN_EX}[ 2 ] Pull Members{Fore.RESET}
    {Fore.LIGHTCYAN_EX}[ 3 ] Configure API{Fore.RESET}
    {Fore.LIGHTCYAN_EX}[ 0 ] Exit{Fore.RESET}
""")
    choice = input(f"    Choice: ")
    redirect(choice)
    
def redirect(choice: int):
    os.system("cls" if os.name == "nt" else "clear")
    def VerificarDB():
        db = obterDatabase()
        if db["authorization"] == "" or db["url"] == "":
            return False
        return True 

    if choice == "1":
        status = VerificarDB()
        if not status: 
            input(f"    {Fore.RED}informações incorretas:{Fore.RESET} ")
            return menu()
        Choices.APIinfo()

    elif choice == "2":
        status = VerificarDB()
        if not status: 
            input(f"    {Fore.RED}informações incorretas:{Fore.RESET} ")
            return menu()
        Choices.PullMembers()

    elif choice == "3":
        return Choices.Config.Configuration()
    elif choice == "0":
        exit()
    else:
        input(f"    {Fore.RED}informações incorretas:{Fore.RESET} ")
        return menu()
    
class Choices():
    def APIinfo():
        db = obterDatabase()
        url = db["url"]
        auth = db["authorization"]
        members = requests.get(f"{url}members", headers={
            "authorization": auth
        })

        if not members.status_code == 200:
            input(f"    {Fore.RED}informações incorretas:{Fore.RESET} ")
            return menu()
        
        print(banner)
        print(f"    {Fore.LIGHTCYAN_EX}URL:{Fore.RESET} {url}")
        print(f"    {Fore.LIGHTCYAN_EX}Auth:{Fore.RESET} {auth}")
        print(f"    {Fore.LIGHTCYAN_EX}Members:{Fore.RESET} {members.json()["message"]}")
        input(f"    {Fore.LIGHTCYAN_EX}>{Fore.RESET} ")
        menu()
    
    def PullMembers():
        print(banner)
        print(f"    verificando")
        db = obterDatabase()

        status = VerificarKey(db["url"], db["authorization"])
        if not status:
            input(f"    {Fore.RED}informações incorretas:{Fore.RESET} ")
            return menu()

        os.system("cls" if os.name == "nt" else "clear")
        print(banner)
        id = input(f"    {Fore.LIGHTCYAN_EX}ID:{Fore.RESET} ")
        response = requests.get(f"{db["url"]}/pullmembers/guild", headers={"authorization": db["authorization"]}, json={"guildID": id})
        if not response.status_code == 200:
            input(f"    {Fore.RED}informações incorretas:{Fore.RESET} ")
            return menu()

        response = requests.get(f"{db["url"]}/pullmembers/2", headers={"authorization": db["authorization"]}, json={"guildID": id}, stream=True)
        if response.status_code != 200:
            print("erro ao conectar com o endpoint:", response.status_code)
            return

        for line in response.iter_lines(decode_unicode=True):
            if line.startswith("data: "):
                data_json = line[6:]
                try:
                    data = json.loads(data_json)
                    if data.get("user"):
                        print(f"    {Fore.LIGHTCYAN_EX}membro:{Fore.RESET} {data['status']} | {Fore.LIGHTCYAN_EX}user:{Fore.RESET} {data['user']['id']} - {Fore.LIGHTCYAN_EX}email:{Fore.RESET} {data['user']['email']}")
                    if data.get("error"):
                        print(f"    erro: {data['error']}")
                except Exception as e:
                    print("erro ao processar evento:", e)
        
            input(f"    {Fore.GREEN}processo finalizado:{Fore.RESET} ")
            return menu()
    
    class Config():
        def Configuration():
            print(banner)
            url = input(f"    {Fore.LIGHTCYAN_EX}URL:{Fore.RESET} ")

            if not url.endswith("/"):
                url = url+"/"

            auth = input(f"    {Fore.LIGHTCYAN_EX}Authorization:{Fore.RESET} ")
            status1 = VerificarWebSite(url)
            if not status1:
                input(f"    {Fore.RED}informações incorretas:{Fore.RESET} ")
                return menu()
            status2 = VerificarKey(url, auth)
            if not status2:
                input(f"    {Fore.RED}informações incorretas:{Fore.RESET} ")
                return menu()
            
            db = obterDatabase()
            db["url"] = url
            db["authorization"] = auth
            with open("auth.json", "w") as f:
                json.dump(db, f, indent=4)
            
            input(f"    {Fore.GREEN}informações salvas com sucesso:{Fore.RESET} ")
            menu()

try:
    menu()
except KeyboardInterrupt:
    exit()