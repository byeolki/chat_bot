from nextcord.ext import commands
import nextcord, datetime, sqlite3, pytz, random
from korcen import korcen

ko = korcen.korcen()
intents = nextcord.Intents.all()
client = commands.Bot(command_prefix='접두사 입력', intents=intents)
com = "접두사 입력"

@client.event
async def on_ready():
    i = datetime.datetime.now()
    print(f"{client.user.name}봇은 준비가 완료 되었습니다.")
    print(f"[!] 참가 중인 서버 : {len(client.guilds)}개의 서버에 참여 중")
    print(f"[!] 이용자 수 : {len(client.users)}와 함께하는 중")

@client.slash_command(name="배워",description="봇에게 단어를 학습 시킬수 있습니다")
async def hello(inter: nextcord.Interaction, 명령: str, 대답: str) -> None:
    conn = sqlite3.connect("learn.db", isolation_level=None)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS learn(id INTEGER, command TEXT, answer TEXT)")
    if ko.check(명령) is True or ko.check(대답) is True:
        return await inter.reply("이런! 욕설이 있어요!")
    elif len(명령.split(" ")) != 1:
        return await inter.reply("이런! 띄어쓰기가 있어요!")
    c.execute("INSERT INTO learn(id, command, answer) VALUES (?, ?, ?)", (inter.user.id, 명령, 대답,))
    embed = nextcord.Embed(title=f"봇이 성공적으로 학습했어요!",  color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
    embed.add_field(name="정보", value=f"**우주야 {명령}** 이라고 말하면 **{대답}** 라고 대답합니다!")
    embed.set_footer(text="Bot made by TEAM-JP", icon_url="https://cdn.nextcordapp.com/avatars/995207372853215282/a1f0223aa10e87618379286ce39f5dae.png?size=512")
    await inter.reply(embed=embed)

@client.event
async def on_message(message):
    conn = sqlite3.connect("learn.db", isolation_level=None)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS learn(id INTEGER, command TEXT, answer TEXT)")
    i = message.content.split(" ")[-1]
    if  message.content.split(" ")[0] == com:
        if c.execute(f"SELECT * FROM learn WHERE command=?",(i,)).fetchone() is None:
            return await message.reply("흠... 무슨 대답을 해야할지 모르겠어요!\n**/배워**를 통해 봇을 학습시켜보세요!")
        li = c.execute(f"SELECT * FROM learn WHERE command=?",(i,)).fetchall()
        if len(li) == 1:
            x = c.execute(f"SELECT * FROM learn WHERE command=?",(i,)).fetchone()
            return await message.reply(f"{x[2]}")
        x = random.choice(li)
        return await message.reply(f"{x[2]}")
