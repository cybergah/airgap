"""Gercek acik kaynak projelerde gorevler. Kaynak kod sabit commit'te, gorev basina gecici kopyada kullanilir.

Alanlar: proje, ad, tur, istek, gizli_test
  hata: [(dosya, dogru_metin, hatali_metin)] kopyaya yerlestirilen hata; referans cozum bunun tersidir
  cozum: yeni ozellik gorevlerinin referans cozumu; eski "" ise metin dosya sonuna eklenir
"""
from olcum_gorevleri import _test

PROJELER = {
    "click": ("https://github.com/pallets/click.git", "8abb77a8432e03ed14a95f972b44f905279415a7"),
    "more-itertools": ("https://github.com/more-itertools/more-itertools.git", "f42daddf205f335fea6e200dad46049f33e71221"),
    "cachetools": ("https://github.com/tkem/cachetools.git", "1ce79efa552d1bdda70d144d401ef9105d999184"),
}
_YOL = "import sys\nsys.path.insert(0, 'src')\n"
CT = "src/cachetools/__init__.py"
MI = "more_itertools/more.py"
MR = "more_itertools/recipes.py"
KT = "src/click/types.py"
KU = "src/click/utils.py"
KF = "src/click/formatting.py"

GOREVLER = [
    # ------------------------------------------------------------ cachetools
    {"ad": "ct_lru_okuma", "proje": "cachetools", "tur": "gercek_hata",
     "istek": "LRUCache okunan öğeyi yeni kullanılmış saymıyor. maxsize=2 iken a ve b ekleyip a'yı okuyunca, c eklendiğinde b atılmalı ama a atılıyor. Hatayı bul ve düzelt.",
     "hata": [(CT, "            self.__order.move_to_end(key)\n        except KeyError:  # __missing__ may not store item",
               "            self.__order[key]\n        except KeyError:  # __missing__ may not store item")],
     "gizli_test": _test("c = LRUCache(2); c['a'] = 1; c['b'] = 2; c['a']; c['c'] = 3\nself.assertIn('a', c)\nself.assertNotIn('b', c)\nc2 = LRUCache(2); c2['a'] = 1; c2['b'] = 2; c2['c'] = 3\nself.assertNotIn('a', c2)", _YOL + "from cachetools import LRUCache")},
    {"ad": "ct_ttl_sinir", "proje": "cachetools", "tur": "gercek_hata",
     "istek": "TTLCache'te süresi tam dolan bir anahtar `in` ile hâlâ varmış gibi görünüyor, ama okununca KeyError veriyor. İkisi tutarlı olmalı: süre dolduysa `in` False dönmeli. Düzelt.",
     "hata": [(CT, "            return False\n        else:\n            return self.timer() < link.expires\n\n    def __getitem__(self, key, cache_getitem=Cache.__getitem__):\n        links = self.__links\n        try:\n            link = links[key]\n        except KeyError:\n            return cache_getitem(self, key)\n        links.move_to_end(key)\n        if self.timer() < link.expires:",
               "            return False\n        else:\n            return self.timer() <= link.expires\n\n    def __getitem__(self, key, cache_getitem=Cache.__getitem__):\n        links = self.__links\n        try:\n            link = links[key]\n        except KeyError:\n            return cache_getitem(self, key)\n        links.move_to_end(key)\n        if self.timer() < link.expires:")],
     "gizli_test": _test("s = [0]\nc = TTLCache(5, 10, timer=lambda: s[0]); c['a'] = 1\nself.assertIn('a', c)\ns[0] = 10\nself.assertNotIn('a', c)\nwith self.assertRaises(KeyError):\n    c['a']", _YOL + "from cachetools import TTLCache")},
    {"ad": "ct_kapasite", "proje": "cachetools", "tur": "gercek_hata",
     "istek": "Cache kapasitesinden bir eksik öğe tutuyor: maxsize=2 olan önbellekte ikinci öğeyi ekleyince ilki siliniyor. Hatayı bul ve düzelt.",
     "hata": [(CT, "while self.__currsize + 1 > maxsize:", "while self.__currsize + 1 >= maxsize:")],
     "gizli_test": _test("c = LRUCache(2); c['a'] = 1; c['b'] = 2\nself.assertEqual(len(c), 2)\nc['c'] = 3\nself.assertEqual(len(c), 2)\nf = FIFOCache(1); f['a'] = 1\nself.assertEqual(len(f), 1)", _YOL + "from cachetools import LRUCache, FIFOCache")},
    {"ad": "ct_yeni_ozellik", "proje": "cachetools", "tur": "gercek_ozellik",
     "istek": "Cache sınıfına doluluk oranını veren bir `fill_ratio` özelliği (property) ekle: currsize / maxsize döndürsün, maxsize 0 ise 0.0 döndürsün. Bütün önbellek türlerinde çalışsın. Tip dosyası varsa onu da güncelle.",
     "cozum": [(CT, "    @property\n    def maxsize(self):", "    @property\n    def fill_ratio(self):\n        \"\"\"The ratio of the current size to the maximum size.\"\"\"\n        return self.currsize / self.maxsize if self.maxsize else 0.0\n\n    @property\n    def maxsize(self):")],
     "gizli_test": _test("c = LRUCache(4); c['a'] = 1\nself.assertEqual(c.fill_ratio, 0.25)\nself.assertEqual(Cache(0).fill_ratio, 0.0)\nt = TTLCache(2, 10); t['x'] = 1\nself.assertEqual(t.fill_ratio, 0.5)\nwith self.assertRaises(AttributeError):\n    c.fill_ratio = 1", _YOL + "from cachetools import Cache, LRUCache, TTLCache")},
    # ------------------------------------------------------------ more-itertools
    {"ad": "mi_maxsplit", "proje": "more-itertools", "tur": "gercek_hata",
     "istek": "split_at, maxsplit=1 verilince bir yerine iki kez bölüyor. list(split_at('abcdcba', lambda x: x == 'b', maxsplit=1)) sonucu [['a'], ['c','d','c','b','a']] olmalı. Hatayı bul ve düzelt.",
     "hata": [(MI, "            if maxsplit == 1:\n                yield list(it)\n                return\n            buf = []\n            maxsplit -= 1\n        else:\n            buf.append(item)\n    yield buf\n\n\ndef split_before",
               "            if maxsplit == 0:\n                yield list(it)\n                return\n            buf = []\n            maxsplit -= 1\n        else:\n            buf.append(item)\n    yield buf\n\n\ndef split_before")],
     "gizli_test": _test("f = lambda x: x == 'b'\nself.assertEqual(list(split_at('abcdcba', f, maxsplit=1)), [['a'], ['c', 'd', 'c', 'b', 'a']])\nself.assertEqual(list(split_at('abcdcba', f)), [['a'], ['c', 'd', 'c'], ['a']])\nself.assertEqual(list(split_at('abcdcba', f, maxsplit=2)), [['a'], ['c', 'd', 'c'], ['a']])", "from more_itertools import split_at")},
    {"ad": "mi_partition", "proje": "more-itertools", "tur": "gercek_hata",
     "istek": "partition fonksiyonu koşul None verilince grupları ters veriyor: partition(None, [0, 1]) sonucunda ilk grup [0] olmalı. Hatayı bul ve düzelt.",
     "hata": [(MR, "    if pred is None:\n        pred = bool\n    iterator = iter(iterable)\n\n    false_queue = deque()", "    if pred is None:\n        pred = lambda x: not x\n    iterator = iter(iterable)\n\n    false_queue = deque()")],
     "gizli_test": _test("a, b = partition(None, [0, 1, '', 'x'])\nself.assertEqual((list(a), list(b)), ([0, ''], [1, 'x']))\na, b = partition(lambda x: x % 2, range(4))\nself.assertEqual((list(a), list(b)), ([0, 2], [1, 3]))", "from more_itertools import partition")},
    {"ad": "mi_yeni_fonksiyon", "proje": "more-itertools", "tur": "gercek_ozellik",
     "istek": "Kütüphaneye every_nth(iterable, n) adında yeni bir fonksiyon ekle: 0. elemandan başlayarak her n. elemanı üretsin, n 1'den küçükse ValueError versin. `from more_itertools import every_nth` çalışmalı ve projenin kuralına uygun olarak tip dosyasına da eklenmeli.",
     "cozum": [(MI, "__all__ = [\n", "__all__ = [\n    'every_nth',\n"), (MI, "def first(iterable, default=_marker):", "def every_nth(iterable, n):\n    \"\"\"Yield every *n*-th item of *iterable*, starting at the first.\"\"\"\n    if n < 1:\n        raise ValueError('n must be at least 1')\n    return islice(iterable, 0, None, n)\n\n\ndef first(iterable, default=_marker):"),
               ("more_itertools/more.pyi", "", "\ndef every_nth(iterable: Iterable[_T], n: int) -> Iterator[_T]: ...\n")],
     "gizli_test": _test("self.assertEqual(list(every_nth('abcdef', 2)), ['a', 'c', 'e'])\nself.assertEqual(list(every_nth([1], 1)), [1])\nwith self.assertRaises(ValueError):\n    list(every_nth([], 0))\nself.assertIn('every_nth', open('more_itertools/more.pyi', encoding='utf-8').read())\nimport more_itertools.more as m\nself.assertIn('every_nth', m.__all__)", "from more_itertools import every_nth")},
    # ------------------------------------------------------------ click
    {"ad": "ck_aralik", "proje": "click", "tur": "gercek_hata",
     "istek": "IntRange sınır değerlerini yanlış yorumluyor: IntRange(min=1, max=5) ile 1 değeri reddediliyor, min_open=True iken 1 ise kabul ediliyor. Hatayı bul ve düzelt.",
     "hata": [(KT, "operator.le if self.min_open else operator.lt", "operator.lt if self.min_open else operator.le")],
     "gizli_test": _test("t = click.IntRange(min=1, max=5)\nself.assertEqual(t.convert('1', None, None), 1)\nself.assertEqual(t.convert('5', None, None), 5)\nwith self.assertRaises(click.BadParameter):\n    t.convert('0', None, None)\nwith self.assertRaises(click.BadParameter):\n    click.IntRange(min=1, min_open=True).convert('1', None, None)", _YOL + "import click")},
    {"ad": "ck_secim", "proje": "click", "tur": "gercek_hata",
     "istek": "click.Choice için case_sensitive=False verildiğinde büyük-küçük harf ayrımı kalkmıyor: Choice(['Elma'], case_sensitive=False) ile 'elma' reddediliyor. Hatayı bul ve düzelt.",
     "hata": [(KT, "normed_value = normed_value.casefold()", "normed_value = normed_value.strip()")],
     "gizli_test": _test("c = click.Choice(['Elma', 'Armut'], case_sensitive=False)\nself.assertEqual(c.convert('elma', None, None), 'Elma')\nself.assertEqual(c.convert('ARMUT', None, None), 'Armut')\nwith self.assertRaises(click.BadParameter):\n    click.Choice(['Elma']).convert('elma', None, None)", _YOL + "import click")},
    {"ad": "ck_secenek_sirasi", "proje": "click", "tur": "gercek_hata",
     "istek": "Yardım çıktısında seçenekler ters sırada çıkıyor: --help ekranında '--verbose, -v' yazıyor, '-v, --verbose' olmalı (kısa seçenek önce). Kök nedeni bul ve düzelt.",
     "hata": [(KF, "rv.sort(key=lambda x: x[0])\n    return \", \".join(x[1] for x in rv), any_prefix_is_slash", "rv.sort(key=lambda x: -x[0])\n    return \", \".join(x[1] for x in rv), any_prefix_is_slash")],
     "gizli_test": _test("@click.command()\n@click.option('--verbose', '-v', is_flag=True)\ndef k(verbose):\n    pass\nr = CliRunner().invoke(k, ['--help'])\nself.assertIn('-v, --verbose', r.output)\nfrom click.formatting import join_options\nself.assertEqual(join_options(['--a', '-a'])[0], '-a, --a')", _YOL + "import click\nfrom click.testing import CliRunner")},
    {"ad": "ck_yeni_ozellik", "proje": "click", "tur": "gercek_ozellik",
     "istek": "Click'e truncate(text, width, suffix='...') adında genel bir yardımcı fonksiyon ekle: metin width karakterden uzunsa, sonuç suffix dahil width karakter olacak şekilde kessin; değilse metni olduğu gibi döndürsün. `click.truncate` olarak dışarıdan kullanılabilmeli.",
     "cozum": [(KU, "def make_str(value: t.Any) -> str:", "def truncate(text: str, width: int, suffix: str = \"...\") -> str:\n    \"\"\"Shorten *text* to *width* characters, suffix included.\"\"\"\n    if len(text) <= width:\n        return text\n    return text[: max(width - len(suffix), 0)] + suffix\n\n\ndef make_str(value: t.Any) -> str:"),
               ("src/click/__init__.py", "from .utils import echo as echo", "from .utils import echo as echo\nfrom .utils import truncate as truncate")],
     "gizli_test": _test("self.assertEqual(click.truncate('merhaba dunya', 8), 'merha...')\nself.assertEqual(click.truncate('kisa', 10), 'kisa')\nself.assertEqual(click.truncate('abcdef', 4, suffix='-'), 'abc-')\nself.assertEqual(click.truncate('abcd', 4), 'abcd')", _YOL + "import click")},
]
