from json import loads, dump, load
from urllib.request import urlretrieve
from sys import stdout
from os.path import split, exists
from threading import Thread


def makedir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def beautifyjson(json_path: str):
    with open(json_path, encoding="utf-8") as f:
        json_to_dict = load(f)
    with open(json_path, "w", encoding='utf-8') as f:
        dump(json_to_dict,
             f,
             indent=2,
             sort_keys=True,
             ensure_ascii=False)


def download(url: str, path: str):
    try:
        (file_path, file_name) = split(path)
        makedir(file_path)

        def hook(blocknum, bs, size):
            a = int(float(blocknum * bs) / size * 100)
            if a >= 100:
                a = 100
            stdout.write("\r >>正在下载" + file_name + str(a) + "%")
        urlretrieve(url, path, reporthook=hook)
        print("\n")
    except:
        print("\n 网络异常，正在尝试重新下载\n")
        download(url=url, path=path)


def Install(version: str, mcdir: str, source: str):
    Threads = []
    if source == "BMCLAPI":
        download(f"https://bmclapi2.bangbang93.com/version/{version}/client",
                 f"{mcdir}\\versions\\{version}\\{version}.jar")
        download(f"https://bmclapi2.bangbang93.com/version/{version}/json",
                 f"{mcdir}\\versions\\{version}\\{version}.json")
        beautifyjson(f"{mcdir}\\versions\\{version}\\{version}.json")
        version_json = open(
            f"{mcdir}\\versions\\{version}\\{version}.json", "r")
        dic = loads(version_json.read())
        version_json.close()
        for lib in dic["libraries"]:
            if 'artifact' in lib["downloads"] and not "classifiers" in lib["downloads"]:
                url = lib["downloads"]["artifact"]["url"].replace("https://libraries.minecraft.net",
                                                                  "https://bmclapi2.bangbang93.com/maven")
                path = f'{mcdir}\\libraries\\{lib["downloads"]["artifact"]["path"]}'
                t = Thread(target=download, args=(url, path))
            if "classifiers" in lib["downloads"]:
                for cl in lib["downloads"]["classifiers"].values():
                    url = cl["url"].replace("https://libraries.minecraft.net",
                                            "https://bmclapi2.bangbang93.com/maven")
                    path = f'{mcdir}\\libraries\\{cl["path"]}'
                    t = Thread(target=download, args=(url, path))
                    t.start()
        url = dic["assetIndex"]["url"].replace("https://launchermeta.mojang.com",
                                               "https://bmclapi2.bangbang93.com")
        path = f"{mcdir}\\assets\\indexes\\{dic['assetIndex']['id']}.json"
        download(url, path)
        beautifyjson(path)
        for object in loads(open(path, "r").read())["objects"].values():
            url = f"https://bmclapi2.bangbang93.com/assets/{object['hash'][:2]}/{object['hash']}"
            path = f"{mcdir}\\assets\\objects\\{object['hash'][:2]}\\{object['hash']}"
            if not exists(path):
                def runnable():
                    print(object['hash'])
                    urlretrieve(url=url, filename=path)
                thread = Thread(target = runnable)
                thread.start()
                Threads.append(thread)
                i = 7
                while i >0:
                    i -= 1
        
        for th in Thread:
            th.join()


class GameCoreInstaller():
    async def InstallAsync():
        pass


if __name__ == "__main__":
    Install("1.7.10", ".minecraft", "BMCLAPI")
