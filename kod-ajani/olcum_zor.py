"""Zor gercek proje gorevleri (--set zor). Projeler ve alanlar olcum_gercek ile ayni.

Gercek set 0.14.2'de 32/33'e dayandi; bu set farki olcebilmek icin daha zor:
belirtinin baska dosyada gorundugu hatalar, yanlis yeri gosteren rapor, tek raporda iki hata,
bes yere dokunan ozellik ve 4.000-5.600 satirlik dosyalarda hatalar.
"""
from olcum_gercek import PROJELER  # noqa: F401  (olcum.py projeleri buradan da bulabilsin)
from olcum_gorevleri import _test

_YOL = "import sys\nsys.path.insert(0, 'src')\n"
CT = "src/cachetools/__init__.py"
CTI = "src/cachetools/__init__.pyi"
CK = "src/cachetools/keys.py"
MI = "more_itertools/more.py"
MR = "more_itertools/recipes.py"
MRI = "more_itertools/recipes.pyi"
KC = "src/click/core.py"
KT = "src/click/types.py"
KTU = "src/click/termui.py"

GOREVLER = [
    # ------------------------------------------------------------ cachetools
    {"ad": "zc_anahtar", "proje": "cachetools", "tur": "zor_uzak",
     "istek": "@cached ile süslediğim fonksiyon, anahtar kelimeyle verilen farklı argümanlara aynı sonucu döndürüyor: f(a=1) çağrıldıktan sonra f(b=1) de f(a=1)'in önbellekteki sonucunu alıyor. Hatayı bul ve düzelt.",
     "hata": [(CK, "    if kwargs:\n        return args + _kwmark + tuple(sorted(kwargs.items()))\n    else:\n        return args\n\n\ndef methodkey",
               "    if kwargs:\n        return args + tuple(sorted(kwargs.values()))\n    else:\n        return args\n\n\ndef methodkey")],
     "gizli_test": _test("calls = []\n@cached(LRUCache(10))\ndef f(**kw):\n    calls.append(kw)\n    return sorted(kw)\nself.assertEqual(f(a=1), ['a'])\nself.assertEqual(f(b=1), ['b'])\nself.assertEqual(len(calls), 2)\nself.assertNotEqual(hashkey(a=1), hashkey(b=1))\nself.assertNotEqual(hashkey(1), hashkey(x=1))\nself.assertEqual(hashkey(1, 2), (1, 2))",
                         _YOL + "from cachetools import cached, LRUCache\nfrom cachetools.keys import hashkey")},
    {"ad": "zc_peek", "proje": "cachetools", "tur": "zor_ozellik",
     "istek": "Cache sınıfına peek(key, default=None) metodu ekle: değeri döndürsün ama önbelleğin durumunu değiştirmesin. LRUCache'te okunan öğe yeni kullanılmış sayılmamalı, LFUCache'te kullanım sayısı artmamalı, süresi dolmuş TTLCache öğesi için default dönmeli. Bütün önbellek türlerinde çalışsın; tip dosyasını da güncelle.",
     "cozum": [(CT, "    def get(self, key, default=None):\n        if key in self:\n            return self[key]",
                "    def peek(self, key, default=None):\n        \"\"\"Return the value for *key* without changing the cache's state.\"\"\"\n        if key in self:\n            return self.__data[key]\n        else:\n            return default\n\n    def get(self, key, default=None):\n        if key in self:\n            return self[key]"),
               (CTI, "    def __len__(self) -> int: ...\n    @overload\n    def pop(self, key: _KT) -> _VT: ...",
                "    def __len__(self) -> int: ...\n    def peek(self, key: _KT, default: _VT | _T | None = None) -> _VT | _T | None: ...\n    @overload\n    def pop(self, key: _KT) -> _VT: ...")],
     "gizli_test": _test("c = LRUCache(2); c['a'] = 1; c['b'] = 2\nself.assertEqual(c.peek('a'), 1)\nc['c'] = 3\nself.assertNotIn('a', c)\nself.assertIn('b', c)\nself.assertEqual(c.peek('yok', 7), 7)\nl = LFUCache(2); l['a'] = 1; l['b'] = 2; l['b']\nfor _ in range(3):\n    l.peek('a')\nl['c'] = 3\nself.assertNotIn('a', l)\ns = [0]\nt = TTLCache(5, 10, timer=lambda: s[0]); t['x'] = 1\nself.assertEqual(t.peek('x'), 1)\ns[0] = 10\nself.assertIsNone(t.peek('x'))\nself.assertEqual(Cache(3).peek('z', 'd'), 'd')\nself.assertIn('def peek', open('src/cachetools/__init__.pyi', encoding='utf-8').read())",
                         _YOL + "from cachetools import Cache, LRUCache, LFUCache, TTLCache")},
    {"ad": "zc_istatistik", "proje": "cachetools", "tur": "zor_yaniltici",
     "istek": "@cached(LRUCache(10), info=True) ile aynı argümanla üç kez çağırınca cache_info() hits=1, misses=2 diyor; hits=2, misses=1 olmalı. Bence _decorator.py'deki sayaçlar yanlış artıyor. Düzelt.",
     "hata": [(CT, "            return cls(hits, misses, cache.maxsize, cache.currsize)",
               "            return cls(misses, hits, cache.maxsize, cache.currsize)")],
     "gizli_test": _test("@cached(LRUCache(10), info=True)\ndef f(x):\n    return x\nf(1); f(1); f(1)\ni = f.cache_info()\nself.assertEqual((i.hits, i.misses), (2, 1))\nself.assertEqual(i.maxsize, 10)\n@cached({}, info=True)\ndef g(x):\n    return x\ng(1); g(1); g(1)\nself.assertEqual(g.cache_info()[:2], (2, 1))",
                         _YOL + "from cachetools import cached, LRUCache")},
    # ------------------------------------------------------------ more-itertools
    {"ad": "zm_chunked_none", "proje": "more-itertools", "tur": "zor_uzak",
     "istek": "chunked(iterable, None) bütün elemanları tek bir liste olarak vermeli, belgesi de öyle diyor; ama list(chunked([1, 2, 3], None)) boş liste dönüyor. Sorun chunked'ın kendisinde olmayabilir: kök nedeni bul ve orada düzelt, chunked'a özel durum eklemek yetmez. Diğer davranışlar bozulmasın.",
     "hata": [(MR, "    return list(islice(iterable, n))\n", "    return list(islice(iterable, n or 0))\n")],
     "gizli_test": _test("self.assertEqual(list(chunked([1, 2, 3], None)), [[1, 2, 3]])\nself.assertEqual(list(chunked([1, 2, 3, 4, 5], 2)), [[1, 2], [3, 4], [5]])\nself.assertEqual(take(2, range(5)), [0, 1])\nself.assertEqual(take(10, range(3)), [0, 1, 2])\nself.assertEqual(take(None, range(3)), [0, 1, 2])",
                         "from more_itertools import chunked, take")},
    {"ad": "zm_running_sum", "proje": "more-itertools", "tur": "zor_ozellik",
     "istek": "Kütüphanedeki running_mean ve running_min gibi bir running_sum(iterable, *, maxlen=None) fonksiyonu ekle: şimdiye kadar görülen değerlerin toplamını, maxlen verilirse son maxlen değerin toplamını üretsin; maxlen 1'den küçükse ValueError versin. Projedeki benzer fonksiyonların eklendiği her yere ekle: kod, __all__, tip dosyası ve belgeler.",
     "cozum": [(MR, "    'running_statistics',\n    'sieve',\n", "    'running_statistics',\n    'running_sum',\n    'sieve',\n"),
               (MR, "", "\n\ndef running_sum(iterable, *, maxlen=None):\n    \"\"\"Cumulative sum of values seen so far or values in a sliding window.\"\"\"\n    iterator = iter(iterable)\n    if maxlen is None:\n        return accumulate(iterator)\n    maxlen = _index(maxlen)\n    if maxlen <= 0:\n        raise ValueError('Window size should be positive')\n    return _windowed_running_sum(iterator, maxlen)\n\n\ndef _windowed_running_sum(iterator, n):\n    window = deque()\n    total = 0\n    for value in iterator:\n        window.append(value)\n        total += value\n        if len(window) > n:\n            total -= window.popleft()\n        yield total\n"),
               (MRI, "    'running_statistics',\n    'sieve',\n", "    'running_statistics',\n    'running_sum',\n    'sieve',\n"),
               (MRI, "", "\ndef running_sum(\n    iterable: Iterable[_NumberT], *, maxlen: int | None = ...\n) -> Iterator[_NumberT]: ...\n"),
               ("docs/api.rst", ".. autofunction:: running_statistics", ".. autofunction:: running_statistics\n.. autofunction:: running_sum")],
     # README.rst'deki fonksiyon tablosu running_min/max/mean/median'i listeler; istek "belgeler" dedigi icin oraya
     # eklemek dogru, gereksiz dosya sayilmaz (32K olcumunde 5 kez yanlis alarm verdi).
     "izinli": ["README.rst"],
     "gizli_test": _test("self.assertEqual(list(running_sum([1, 2, 3, 4])), [1, 3, 6, 10])\nself.assertEqual(list(running_sum([1, 2, 3, 4], maxlen=2)), [1, 3, 5, 7])\nself.assertEqual(list(running_sum([])), [])\nwith self.assertRaises(ValueError):\n    list(running_sum([1], maxlen=0))\nimport more_itertools.more as m, more_itertools.recipes as r\nmod = 'more' if 'running_sum' in m.__all__ else 'recipes'\nself.assertIn('running_sum', (m if mod == 'more' else r).__all__)\nstub = open(f'more_itertools/{mod}.pyi', encoding='utf-8').read()\nself.assertIn('def running_sum', stub)\nself.assertIn(\"'running_sum'\", stub)\nself.assertIn('autofunction:: running_sum', open('docs/api.rst', encoding='utf-8').read())",
                         "from more_itertools import running_sum")},
    {"ad": "zm_windowed_adim", "proje": "more-itertools", "tur": "zor_buyuk",
     "istek": "windowed fonksiyonu step verilince pencereleri atlıyor: list(windowed(range(6), 3, step=2)) sonucu [(0, 1, 2), (2, 3, 4), (4, 5, None)] olmalı, ama arada pencereler kayboluyor. step=1 de etkileniyor olabilir. Hatayı bul ve düzelt.",
     "hata": [(MI, "    for _ in islice(filler, step - 1, None, step):\n        yield tuple(window)",
               "    for _ in islice(filler, step, None, step):\n        yield tuple(window)")],
     "gizli_test": _test("self.assertEqual(list(windowed(range(6), 3, step=2)), [(0, 1, 2), (2, 3, 4), (4, 5, None)])\nself.assertEqual(list(windowed([1, 2, 3, 4], 2)), [(1, 2), (2, 3), (3, 4)])\nself.assertEqual(list(windowed([1, 2, 3], 3, step=3)), [(1, 2, 3)])\nself.assertEqual(list(windowed([1, 2], 3)), [(1, 2, None)])",
                         "from more_itertools import windowed")},
    # ------------------------------------------------------------ click
    {"ad": "zk_envvar_oncelik", "proje": "click", "tur": "zor_buyuk",
     "istek": "Click'in belgesine göre bir seçeneğin değeri önce komut satırından, sonra ortam değişkeninden, sonra default_map'ten, en son varsayılandan gelir. Ama komut default_map ile çağrıldığında, o seçenek için default_map'te değer varsa ortam değişkeni yok sayılıyor. Kök nedeni bul ve düzelt.",
     "hata": [(KC, "        if value is UNSET:\n            envvar_value = self.value_from_envvar(ctx)",
               "        if value is UNSET and not ctx._default_map_has(self.name):\n            envvar_value = self.value_from_envvar(ctx)")],
     "gizli_test": _test("@click.command()\n@click.option('--name', envvar='K_NAME', default='def')\ndef k(name):\n    click.echo(name)\nr = CliRunner()\nself.assertEqual(r.invoke(k, [], env={'K_NAME': 'env'}, default_map={'name': 'map'}).output.strip(), 'env')\nself.assertEqual(r.invoke(k, [], default_map={'name': 'map'}).output.strip(), 'map')\nself.assertEqual(r.invoke(k, ['--name', 'cli'], env={'K_NAME': 'env'}, default_map={'name': 'map'}).output.strip(), 'cli')\nself.assertEqual(r.invoke(k, []).output.strip(), 'def')",
                         _YOL + "import click\nfrom click.testing import CliRunner")},
    {"ad": "zk_iki_hata", "proje": "click", "tur": "zor_iki",
     "istek": "İki ayrı sorun var, ikisini de düzelt: (1) IntRange(0, 10, max_open=True, clamp=True) ile 15 verilince 9 yerine 11 dönüyor. (2) click.style('x', bold=True) metni kalın yapmıyor, tersine kalınlığı kapatıyor.",
     "hata": [(KT, "        return bound + dir\n", "        return bound - dir\n"),
              (KTU, "1 if bold else 22", "22 if bold else 1")],
     "gizli_test": _test("t = click.IntRange(0, 10, max_open=True, clamp=True)\nself.assertEqual(t.convert('15', None, None), 9)\nself.assertEqual(click.IntRange(0, 10, min_open=True, clamp=True).convert('-5', None, None), 1)\nself.assertEqual(click.IntRange(0, 10, clamp=True).convert('15', None, None), 10)\nself.assertTrue(click.style('x', bold=True).startswith('\\x1b[1m'))\nself.assertTrue(click.style('x', bold=False).startswith('\\x1b[22m'))",
                         _YOL + "import click")},
    {"ad": "zk_yeni_tip", "proje": "click", "tur": "zor_ozellik",
     "istek": "Click'e yüzde değerleri için yeni bir parametre tipi ekle: click.PERCENT. '50%' ve '50' girdilerini 0.5 olarak döndürsün; sayı olmayan veya 0-100 aralığı dışındaki değerler Click'in kendi hata mekanizmasıyla (BadParameter) reddedilsin. Diğer hazır tipler gibi (click.INT, click.FLOAT) kullanılabilmeli.",
     "cozum": [(KT, "", "\n\nclass PercentParamType(ParamType):\n    name = \"percent\"\n\n    def convert(self, value, param, ctx):\n        text = str(value).strip()\n        if text.endswith(\"%\"):\n            text = text[:-1]\n        try:\n            number = float(text)\n        except ValueError:\n            self.fail(f\"{value!r} is not a valid percentage.\", param, ctx)\n        if not 0 <= number <= 100:\n            self.fail(f\"{value!r} is not between 0 and 100.\", param, ctx)\n        return number / 100\n\n    def __repr__(self) -> str:\n        return \"PERCENT\"\n\n\nPERCENT = PercentParamType()\n"),
               ("src/click/__init__.py", "from .types import File as File", "from .types import File as File\nfrom .types import PERCENT as PERCENT")],
     "gizli_test": _test("self.assertEqual(click.PERCENT.convert('50%', None, None), 0.5)\nself.assertEqual(click.PERCENT.convert('25', None, None), 0.25)\nfor bad in ('abc', '150', '-1%'):\n    with self.assertRaises(click.BadParameter):\n        click.PERCENT.convert(bad, None, None)\n@click.command()\n@click.option('--oran', type=click.PERCENT)\ndef k(oran):\n    click.echo(repr(oran))\nr = CliRunner()\nself.assertEqual(r.invoke(k, ['--oran', '20%']).output.strip(), '0.2')\nres = r.invoke(k, ['--oran', 'x'])\nself.assertNotEqual(res.exit_code, 0)\nself.assertIn('Invalid value', res.output)",
                         _YOL + "import click\nfrom click.testing import CliRunner")},
]
