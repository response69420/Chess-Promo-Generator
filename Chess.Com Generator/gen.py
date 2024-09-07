import requests
import random
from faker import Faker

fake = Faker()
from colorama import Fore, Style, Back, init ; init()
import datetime
from datetime import datetime
def log(tag,content,color):
  ts= datetime.now().strftime('%H:%M:%S')
  print(f"{Style.BRIGHT}{Fore.BLACK}[{ts}] {color}[{tag}] {Fore.WHITE}{content}{Style.RESET_ALL}")


def getpromo(proxy):
    name = (fake.first_name()+fake.last_name()).lower()
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "referer": "https://www.chess.com/friends?name=joseph",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }
    response = requests.get("https://www.chess.com/member/"+name, headers=headers)
    try:
      uuid = response.text.split('data-user-uuid="')[1].split('"')[0]
      log("UUID",f"Scraped UUID -> {uuid} ({name})",Fore.BLUE)
    except:
      return None
    #print(uuid)
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://www.chess.com",
        "priority": "u=1, i",
        "referer": "https://www.chess.com/play/computer/discord-wumpus?utm_source=partnership&utm_medium=article&utm_campaign=discord2024_bot",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }
    json_data = {
        "userUuid": uuid,
        "campaignId": "4daf403e-66eb-11ef-96ab-ad0a069940ce",
    }
    response = requests.post(
        "https://www.chess.com/rpc/chesscom.partnership_offer_codes.v1.PartnershipOfferCodesService/RetrieveOfferCode",
        # cookies=cookies,
        headers=headers,
        json=json_data,
        proxies={
    "http": "http://"+proxy,
    "https": "http://"+proxy,
},
    )
    try:
      code = 'https://promos.discord.gg/'+response.json()["codeValue"]
      log("PROMO","Got promo -> {}".format(code),Fore.GREEN)
      with open('codes.txt','a') as f:
        f.write(code+'\n')
    except:
     log("ERR","Error occured -> {}".format(response.json(), Fore.RED))

with open('proxies.txt','r') as f:
  proxies = f.read().splitlines()
from concurrent.futures import ThreadPoolExecutor
import random
with ThreadPoolExecutor(max_workers=2) as exc:
  while True:
     p = random.choice(proxies)
     exc.submit(getpromo,p)
