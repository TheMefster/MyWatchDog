from asyncio.tasks import gather, wait, Task, sleep, create_task
from asyncio.subprocess import create_subprocess_shell as cmd
from asyncio.events import get_event_loop as grl
from asyncio.runners import Runner
from asyncio.locks import Event
from json.decoder import JSONDecoder
from datetime import datetime

async def cmdout(txt):
    sub = await cmd(txt, stdout=-1, stderr=-1)
    ret = await sub.communicate()
    try: return ret[0].decode('latin1').strip().lower()
    except: return None

class Filter:
    process, aList, bList, dList, lock = lambda self, string: string.lower().split("`", 2) if "`" in string else [string.lower(), ""], [], [], [], None
    class Locker:
        def __init__(self, master):
            self.locked, self.task, self.master = False, None, master
            from random import Random
            from uuid import uuid1
            self.myid = str(Random(uuid1().node).randint(0,99999999999999999)*10+1)
            del uuid1, Random
        async def lock(self):
            if self.locked == True: return
            self.task = create_task(cmdout('pwsh -Command "try { $stream = [System.IO.File]::Open($HOME+\'/block.xxx\', [System.IO.FileMode]::Open, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None); while ($true) { Start-Sleep -Seconds 1; } } finally { if ($null -ne $stream) { $stream.Close(); $stream.Dispose(); } }"'))
            self.locked = True
        async def unlock(self):
            if self.locked == False: None
            else:
                self.task.cancel()
                try: await self.task
                except: None
                finally: self.locked, self.task = False, None
            await cmd('pwsh -Command "Get-Process pwsh | Where-Object Id -ne $PID | Stop-Process -Force"')
        async def updateList(self):
            def decoder(resp):
                try:
                    if resp[18:]==self.myid: return False
                    else: resp = str((int(resp[:18])*pow(int(resp[18:]),-1,10**18))%(10**18))
                    codde, codec = '', 0
                    for c in resp.zfill(18): codde, codec = f'{codde}{(int(c)-codec+10)%10}', (int(c)-codec+10)%10
                    coden, code, codec = codde[:10], [codde[10:12], codde[12:14], codde[14:16], codde[16:18]], 0
                    for c in ''.join([str(bin(int(f'{int(c)//8}{int(c)%8}')))[2:].zfill(8) for c in code]): codec = codec*2 + int(c)
                    return True if int(coden)==codec and str(code[:3]) == datetime.now().strftime("['%m', '%d', '%H']") else False
                except: return False
            while True:
                try:
                    await sleep(60)
                    fDir = await cmdout('pwsh -Command "echo $HOME/toblock.txt"')
                    try: file = open(fDir)
                    except: continue
                    if not decoder(file.readline()): continue
                    await self.unlock()
                    await sleep(1)
                    lines = await cmdout('pwsh -Command "echo $HOME/block.xxx"')
                    file.close()
                    with open(wDir, "w") as newFile, open(fDir, "w") as oldFile:
                        oldFile.write(f'{self.myid}{self.myid}')
                        for line in lines:
                            newFile.write(line)
                            oldFile.write(line)
                    await self.master.reset()
                except: None
    def current(self, words):
        t, ret = datetime.now(), {}
        for word in words:
            if (t.strftime("%H").lower() in word[1] or not any(c.isnumeric() for c in word[1])) and (t.strftime("%A").lower()[:2] in word[1] or not any(c.isalpha() for c in word[1])): ret[word[0]] = int(word[2].strip()) if len(word)>2 else 50
        return ret
    def b(self, val=None): return self.current(self.bList)[val] if val else self.current(self.bList).keys()
    def d(self, val=None): return self.current(self.dList)[val] if val else self.current(self.dList).keys()
    async def reset(self):
        await self.lock.unlock()
        self.aList, self.bList, self.dList = [], [], []
        mlist = ["#porn","# nude","#nude``30","#nudity","#sexy``40","#creampie","#erotic","#blowjob","#orgasm","youtube.com/shorts","#web proxy","#virtual private net",
                 "#private network","#proxy site","#proxy server","#proxy service","#tor browser","#tor onion","#tor project","#torproject","#onion router","#suicide``10",
                 "#suicidal``20","#bukkake","#cum shot","#cumming","#sexual rub","#sexual encounter","#jerk off","#jerking off","#sexual arousal","#anal sex``30",
                 "#virginity``10","#anilingus","#pompoir","#urethral sounding``40","#intercourse``20","#orgy``30","#gangbang","#gang bang``30","#lewd``20","#lascivious",
                 "@tor browser","#lingerie","#naked woman``30","#naked man``20","#vulnerable``10","#topless``20","#tempting man``20","#tempting woman``20","#tempting body``20",
                 "#tempting girl``20","#tempting body","#intima``5","#sensual``15","#sexy body","#having sex``20","# arouse``20","#twerk``20","#playboy``40","#bigo live",
                 "#bigolive","#periscope girl","#periscopegirl","#periscope live","#periscopelive"]
        fDir = await cmdout('pwsh -Command "echo $HOME/block.xxx"')
        try: file = open(fDir)
        except: file = type('File', (), {'readlines': (lambda self: []), 'close': (lambda self: None)})()
        for line in  mlist+file.readlines(): (self.bList.append(self.process(line.strip().lower()[1:])) if line.strip()[0]=="#" else self.aList.append(line.strip().lower()[1:]) if line.strip()[0]=="@" else self.dList.append(self.process(line.strip().lower()))) if line.strip()!="" else None
        file.close()
        await self.lock.lock()
    async def apply(self):
        self.lock = self.Locker(self)
        await self.reset()
        self.updater = create_task(self.lock.updateList())
    def request(self, flow): flow.request.url = "https://tools-httpstatus.pickup-services.com/418" if ("Referer" in getattr(flow.request,"headers",None) and any(dl in flow.request.headers["Referer"] for dl in self.d())) or any(dl in getattr(flow.request,"url",None) for dl in self.d()) else getattr(flow.request,"url",None)
    def response(self, flow): flow.response = flow.response if sum(self.b(bl)*(len(getattr(flow.response,"content","").split(bl.encode("utf-8")))-1) for bl in self.b())<100+(151 if "Content-Type" in flow.response.headers and "javascript" in flow.response.headers["Content-Type"] else 0) else flow.response.make(418, b"Blocked by MyWatchDog")

async def main():
    class Master:
        class Options:
            def __init__(self):
                self._options = {}
                self.add_option("server", bool, True)
                self.add_option("add_upstream_certs_to_client_chain", bool, False)
                self.add_option("confdir", str, "~/.mitmproxy")
                self.add_option("cert_passphrase", str | None)
                self.add_option("client_certs", str | None)
                self.add_option("listen_host", str, "localhost")
                self.add_option("listen_port", int | None, 6692)
                self.add_option("mode", list | dict, ["regular"])
                self.add_option("upstream_cert", bool, True)
                self.add_option("http2", bool, True)
                self.add_option("http2_ping_keepalive", int, 58)
                self.add_option("http3", bool, True)
                self.add_option("websocket", bool, True)
                self.add_option("ssl_insecure", bool, False)
                self.add_option("ssl_verify_upstream_trusted_confdir", str | None)
                self.add_option("ssl_verify_upstream_trusted_ca", str | None)
                self.add_option("key_size", int, 2048)
                self.add_option("tcp_timeout", int, 600)
            def add_option(self, name, typespec, default=None):
                cpy = lambda x: [cpy(y) for y in x] if type(x)==list else tuple([cpy(y) for y in x]) if type(x)==tuple else dict([(cpy(y),cpy(z)) for y,z in x.items()]) if type(x)==dict else x
                option = type("Option", (), {"name": name, "typespec": typespec, "_default": default})
                option.current = lambda opt: cpy(opt._default)
                self._options[name] = option()
            __getattr__ = lambda self, attr: (self._options[attr].current() if attr in self._options else None)
            def __setattr__(self, attr, value):
                if self.__dict__.get("_options"): self.update(**{attr: value})
                else: super().__setattr__(attr, value)
            def update(self, **kwargs):
                known, unknown = {}, {}
                for k, v in kwargs.items():
                    if k in self._options: known[k] = v
                    else: unknown[k] = v
                updated = set(known.keys())
                if updated or unknown: print(f"Update Error Occured: {updated | unknown}")
        class AddonManager:
            def __init__(self, master):
                self.lookup = {}
                self.master = master
                self.filter = Filter()
                from mitmproxy.addons import next_layer, tlsconfig, proxyserver
                for addon in [proxyserver.Proxyserver(), next_layer.NextLayer(), tlsconfig.TlsConfig(), self.filter]: self.lookup[addon.__class__.__name__.lower()] = addon
                del next_layer, tlsconfig, proxyserver
                self.trigger(master.lHook)
            def _iter_hooks(self, addon, event):
                func = getattr(addon, event.name, None)
                if func and callable(func): yield addon, func
            def invoke_addon_sync(self, addon, event):
                for addon, func in self._iter_hooks(addon, event):
                    try: func(*event.args())
                    except: None
            async def handle_lifecycle(self, event):
                for i in self.lookup.values():
                    for addon, func in self._iter_hooks(i, event):
                        try: await func(*event.args())
                        except: None
            def trigger(self, event):
                for i in self.lookup.values():
                    try: self.invoke_addon_sync(i, event)
                    except: return
        def __init__(self):
            self.options = self.Options()
            self.lHook,self.dHook,self.rHook = self.getHooks()
            self.addons = self.AddonManager(self)
            self.event_loop = grl()
            self.should_exit = Event()
        def etf(self,l,c,*,n=None,x=None): return Task(c,loop=l,name=n,context=x,eager_start=True)
        def getHooks(self):
            from dataclasses import dataclass
            class Loader:
                def __init__(self, master): self.master = master
                def add_option(self, name, typespec, default=None, *args, **kwargs): self.master.options.add_option(name, typespec, default)
            hargs = lambda self: [getattr(self, f.name) for f in getattr(self, '__dataclass_fields__').values() if type(f._field_type).__name__ == '_FIELD_BASE']
            Hook = type("", (), {"args": hargs, "__hash__": object.__hash__, "__eq__": object.__eq__})
            @dataclass
            class LH(Hook):
                loader: Loader
                name="load"
            @dataclass
            class DH(Hook): name="done"
            @dataclass
            class RH(Hook): name="running"
            del dataclass
            return LH(Loader(self)),DH(),RH()
        async def run(self):
            _loop = grl()
            _ehandler = _loop.get_exception_handler()
            _loop.set_exception_handler(lambda *args: print(f"Unhandled asyncio error: {args}"))
            _efact = _loop.get_task_factory()
            _loop.set_task_factory(self.etf)
            try:
                self.should_exit.clear()
                await wait([_loop.create_task(self.addons.lookup["proxyserver"].setup_servers()), _loop.create_task(self.should_exit.wait())], return_when='FIRST_COMPLETED')
                if self.should_exit.is_set(): return
                try:
                    await self.addons.handle_lifecycle(self.rHook)
                    await self.should_exit.wait()
                finally: await self.addons.handle_lifecycle(self.dHook)
            finally:
                _loop.set_exception_handler(_ehandler)
                _loop.set_task_factory(_efact)
    async def runProx():
        while True:
            from mitmproxy import ctx
            ctx.master = proxy = Master()
            ctx.options = proxy.options
            del ctx
            await proxy.addons.filter.apply()
            try: await proxy.run()
            except: proxy.event_loop.call_soon_threadsafe(proxy.should_exit.set)
    async def runTimer():
        async def appMgr():
            alist, resp = Filter().aList, await cmdout('pwsh -Command "gps | where { $_.MainWindowTitle } | select Id, Name, MainWindowTitle | ConvertTo-Json"')
            try: windows = JSONDecoder().decode(resp) if resp else []
            except: return
            for window in windows:
                if type(window)==dict and (window['name'] in alist or any(a.lower() in window['mainwindowtitle'].lower() for a in alist)): await cmd(f'pwsh -Command "spps -id {window["id"]}"')
        async def configMgr(win):
            if win:
                h = 'pwsh -Command "sp -Path \'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\' -Name {0} -Value {1}"'.format
                await gather(cmd(h('ProxyEnable','1 -Type DWord')), cmd(h('ProxyServer','localhost:6692')))
            else:
                h = 'pwsh -Command \'[System.Environment]::SetEnvironmentVariable("http{0}_proxy", "http{0}://localhost:6692", "User"\''.format
                await gather(cmd(h('')), cmd(h('s')))
        await sleep(5)
        os = await cmdout('pwsh -Command "5*$IsWindows+3*$IsMacOS+2*$IsLinux"')
        match os:
            case "5":
                await cmd('certutil -addstore -f -User Root $HOME/.mitmproxy/mitmproxy-ca-cert.cer')
                await cmd('pwsh -Command "New-ItemProperty -Path \'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\' -Name \'MyWatchDog\' -Value $PWD\\MyWatchDog.exe -PropertyType String -Force"')
            case "3": await cmd('security add-trusted-cert -d -r trustRoot -k ~/Library/Keychains/login.keychain-db $HOME/.mitmproxy/mitmproxy-ca-cert.cer')
            case "2": None
            case _: return
        while True: await gather(appMgr(), configMgr(os=="5"), sleep(1))
    async def getPWSH():
        system = await cmdout('echo $OSTYPE')
        if '$ostype' in system: await cmd('winget install Microsoft.PowerShell')
        elif 'darwin' in system: await cmd('brew install --cask powershell')
        else: await cmd('curl -sL https://github.com/PowerShell/PowerShell/releases/download/v7.6.5/powershell-7.6.5-linux-x64.tar.gz | tar -xzC ~/.local/bin/ && chmod +x ~/.local/bin/pwsh')
    check = await cmdout('pwsh -Command "$true"')
    if check!="true": await getPWSH()
    del getPWSH, check
    await cmd('pwsh -Command "Get-Process -Name \'MyWatchDog\' | Sort-Object StartTime -Descending | Select-Object -Skip 1 | Stop-Process -Force"')
    restarter = create_task(cmd('pwsh -Command "while ($true) { if ((Get-Process -Name \'MyWatchDog\' -ErrorAction SilentlyContinue).Count -eq 0) {Start-Process \'MyWatchDog\'} else {Start-Sleep -Seconds 1}"'))
    await sleep(3)
    await gather(runTimer(), runProx())
    return restarter
Runner().run(main())
