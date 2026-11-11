"""Korumali ortam. Kacis denemeleri gercek Docker ve yerel debian imajiyla calisir; Docker yoksa atlanir."""
import getpass
import os
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import ajan as a

IMAJ = os.environ.get("KOD_AJANI_TEST_IMAJ", "debian:latest")
PYTHON_IMAJ = "python:3.13-slim"


def docker_var():
    try:
        return (subprocess.run(["docker", "image", "inspect", IMAJ], capture_output=True, stdin=subprocess.DEVNULL,
                               timeout=20).returncode == 0)
    except (OSError, subprocess.TimeoutExpired):
        return False


class KuruTest(unittest.TestCase):
    """Docker gerektirmez."""

    def setUp(self):
        self.g = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.g, ignore_errors=True)
        (self.g / ".git").mkdir()
        (self.g / ".env").write_text("x", encoding="utf-8")
        (self.g / "node_modules").mkdir()
        (self.g / "node_modules" / ".env").write_text("x", encoding="utf-8")
        self.k = a.KorumaliOrtam(IMAJ)
        self.k.hazir = True

    def test_guvenlik_bayraklari(self):
        c = self.k.komut("echo hi", self.g)
        for b in ["--network=none", "--cap-drop=ALL", "--security-opt=no-new-privileges", "--read-only", "--pull=never",
                  "--rm", "--user=1000:1000"]:
            self.assertIn(b, c)
        self.assertEqual(c[-4:], [IMAJ, "sh", "-c", "echo hi"])
        self.assertFalse([x for x in c if "docker.sock" in x or "--privileged" in x])

    def test_git_salt_okunur_gizli_dosya_maskeli(self):
        bag = " ".join(self.k.komut("x", self.g))
        self.assertRegex(bag, r"dst=/work/\.git,readonly")
        self.assertIn("src=/dev/null,dst=/work/.env,readonly", bag)
        self.assertNotIn("node_modules/.env", bag)

    def test_virgullu_yol_reddedilir(self):
        (self.g / "a,b.env").write_text("x", encoding="utf-8")
        with self.assertRaises(a.AracHatasi):
            self.k.komut("x", self.g)

    def test_docker_yoksa_bilgisayarda_calismaz(self):
        arac = a.Araclar(self.g)
        arac.kum = a.KorumaliOrtam(IMAJ)
        isaret = self.g / "calisti.txt"
        with patch.object(arac.kum, "_docker", side_effect=OSError("docker yok")):
            sonuc = arac.calistir("run_command", {"command": f"python -c \"open(r'{isaret}','w')\""})
        self.assertTrue(sonuc.startswith("HATA"), sonuc)
        self.assertFalse(isaret.exists())

    def test_imaj_yoksa_indirmez_reddeder(self):
        k = a.KorumaliOrtam("yok/boyle-bir-imaj:1")
        yanit = subprocess.CompletedProcess([], 1)
        with patch.object(k, "_docker", side_effect=[subprocess.CompletedProcess([], 0), yanit]) as d:
            with self.assertRaises(a.AracHatasi):
                k.denetle()
        self.assertFalse([c for c in d.call_args_list if "pull" in c.args])

    def test_seccomp_denemesi_sonucuna_gore_karar(self):
        tamam = subprocess.CompletedProcess([], 0)
        for cikti, gecer in [(b"KORUMA_ACIK\n", True), (b"KORUMA_KAPALI\n", False), (b"KORUMA_BILINMIYOR\n", False), (b"", False)]:
            with self.subTest(cikti=cikti):
                k = a.KorumaliOrtam(IMAJ)
                deneme = subprocess.CompletedProcess([], 0, stdout=cikti, stderr=b"hata")
                with patch.object(k, "_docker", side_effect=[tamam, tamam, deneme]) as d:
                    if gecer:
                        k.denetle()
                        self.assertTrue(k.hazir)
                        calistirilan = d.call_args_list[2].args
                        for b in a._KAPSAYICI_GUVENLIK:
                            self.assertIn(b, calistirilan)
                    else:
                        with self.assertRaises(a.AracHatasi):
                            k.denetle()
                        self.assertFalse(k.hazir)

    def test_sistem_istemi_ortami_soyler(self):
        with patch.dict(os.environ, {"KOD_AJANI_VERI": str(self.g / "v")}):
            icerik = a.Ajan(self.g, "s", korumali=IMAJ).mesajlar[0]["content"]
        self.assertIn("isolated container", icerik)
        self.assertNotIn("PowerShell", icerik)


@unittest.skipUnless(docker_var(), "Docker veya debian imaji yok")
class KacisTesti(unittest.TestCase):
    """Her biri kapsayicidan disari cikmaya calisir."""

    def setUp(self):
        self.g = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.g, ignore_errors=True)
        (self.g / ".git" / "hooks").mkdir(parents=True)
        (self.g / ".git" / "HEAD").write_text("ref\n", encoding="utf-8")
        (self.g / ".env").write_text("PAROLA=cokgizli\n", encoding="utf-8")
        (self.g / "a.txt").write_text("x\n", encoding="utf-8")
        self.arac = a.Araclar(self.g)
        self.arac.kum = a.KorumaliOrtam(IMAJ)

    def kos(self, komut):
        return self.arac.calistir("run_command", {"command": komut})

    def test_proje_gorunur_ve_yazilabilir(self):
        s = self.kos("cat a.txt && echo yeni > b.txt")
        self.assertIn("cikis kodu: 0", s)
        self.assertEqual((self.g / "b.txt").read_text().strip(), "yeni")

    def test_cikis_kodu_iletilir(self):
        self.assertIn("cikis kodu: 3", self.kos("exit 3"))

    def test_root_degil_yetki_yok(self):
        s = self.kos("id -u; grep CapEff /proc/self/status; grep NoNewPrivs /proc/self/status")
        self.assertIn("1000", s)
        self.assertRegex(s, r"CapEff:\s+0+\b")
        self.assertRegex(s, r"NoNewPrivs:\s+1")

    def test_ag_yok(self):
        s = self.kos("ls /sys/class/net; cat /proc/net/route | wc -l; (exec 3<>/dev/tcp/1.1.1.1/53) 2>&1; echo son")
        self.assertIn("lo", s)
        self.assertNotIn("eth0", s)
        self.assertIn("1\n", s.replace("\r", ""))  # yonlendirme tablosu yalniz baslik

    def test_seccomp_denetimi_gecer(self):
        self.arac.kum.denetle()  # debian: unshare yolu
        self.assertTrue(self.arac.kum.hazir)

    def test_seccomp_kapaliysa_deneme_fark_eder(self):
        # Urun seccomp'u hic kapatmaz; burada kapatip denemenin bunu yakaladigi gosterilir.
        for imaj in [IMAJ, PYTHON_IMAJ]:
            if subprocess.run(["docker", "image", "inspect", imaj], capture_output=True, stdin=subprocess.DEVNULL).returncode:
                continue
            for ek, beklenen in [([], "KORUMA_ACIK"), (["--security-opt", "seccomp=unconfined"], "KORUMA_KAPALI")]:
                with self.subTest(imaj=imaj, ek=ek):
                    s = subprocess.run(["docker", "run", "--rm", "--pull=never", *a._KAPSAYICI_GUVENLIK, *ek, imaj,
                                        "sh", "-c", a._SECCOMP_DENEMESI], capture_output=True, stdin=subprocess.DEVNULL, timeout=60)
                    self.assertIn(beklenen, s.stdout.decode())

    def test_seccomp_yasak_cagrilari_reddeder(self):
        s = self.kos("unshare -U true && echo UNSHARE_CALISTI; unshare -m true && echo MOUNT_ALANI_CALISTI; echo son")
        self.assertIn("son", s)
        self.assertNotIn("UNSHARE_CALISTI", s)
        self.assertNotIn("MOUNT_ALANI_CALISTI", s)

    def test_sistem_salt_okunur(self):
        s = self.kos("touch /etc/kacis; touch /usr/kacis; touch /kacis; ls /etc/kacis /kacis 2>&1; true")
        self.assertIn("Read-only file system", s)
        self.assertNotIn("/etc/kacis\n", s.replace("No such", ""))

    def test_bilgisayar_diski_gorunmez(self):
        s = self.kos("ls /mnt /host /c /host_mnt /Users 2>&1; df -a 2>/dev/null | grep -ciE 'users|c:' ; true")
        self.assertNotIn(getpass.getuser().lower(), s.lower())  # the host user's name must not be visible
        self.assertNotIn("Windows", s)

    def test_docker_soketi_yok(self):
        self.assertIn("yok", self.kos("test -e /var/run/docker.sock && echo var || echo yok"))

    def test_ortam_degiskenleri_sizmaz(self):
        with patch.dict(os.environ, {"BENIM_TOKEN": "cokgizli", "NORMAL_DEGER": "gorunmez"}):
            s = self.kos("env")
        self.assertNotIn("cokgizli", s)
        self.assertNotIn("gorunmez", s)

    def test_gizli_dosya_bos_ve_degistirilemez(self):
        s = self.kos("cat .env; echo x > .env; echo bitti")
        self.assertNotIn("cokgizli", s)
        self.assertEqual((self.g / ".env").read_text(encoding="utf-8"), "PAROLA=cokgizli\n")

    def test_git_kancasi_yazilamaz(self):
        s = self.kos("echo kotu > .git/hooks/pre-commit; echo x >> .git/HEAD; true")
        self.assertIn("Read-only", s)
        self.assertFalse((self.g / ".git" / "hooks" / "pre-commit").exists())
        self.assertEqual((self.g / ".git" / "HEAD").read_text(encoding="utf-8"), "ref\n")

    def test_tmp_var_ama_sinirli(self):
        s = self.kos("echo x > /tmp/a && cat /tmp/a; head -c 300000000 /dev/zero > /tmp/b; echo durum=$?")
        self.assertIn("x", s)
        self.assertIn("durum=1", s)

    def test_catal_bombasi_sinirlanir(self):
        s = self.kos("n=0; while [ $n -lt 400 ]; do sleep 30 & n=$((n+1)); done 2>&1 | head -1; echo bitti; pkill sleep 2>/dev/null; true")
        self.assertRegex(s, r"(?i)fork|resource|cannot|bitti")

    def test_zaman_asiminda_kapsayici_olur(self):
        with patch.object(a, "KOMUT_ZAMAN_ASIMI", 3):
            bas = time.time()
            s = self.kos("sleep 100")
        self.assertIn("durduruldu", s)
        self.assertLess(time.time() - bas, 30)
        self.assertFalse(self.kalan(self.arac.kum.ad))

    def test_durdur_kapsayiciyi_oldurur(self):
        import threading
        t = threading.Thread(target=self.kos, args=("sleep 100",))
        t.start()
        time.sleep(3)
        self.assertTrue(self.kalan(self.arac.kum.ad))
        self.arac.durdur()
        t.join(30)
        self.assertFalse(t.is_alive())
        self.assertFalse(self.kalan(self.arac.kum.ad))

    def test_python_ile_gercek_soket_baglanamaz(self):
        if subprocess.run(["docker", "image", "inspect", PYTHON_IMAJ], capture_output=True,
                          stdin=subprocess.DEVNULL).returncode != 0:
            self.skipTest("python imaji yok")
        self.arac.kum = a.KorumaliOrtam(PYTHON_IMAJ)
        (self.g / "ag.py").write_text(
            "import socket\n"
            "for h in [('1.1.1.1', 53), ('host.docker.internal', 80), ('172.17.0.1', 80), ('192.168.65.2', 80)]:\n"
            "    try:\n"
            "        socket.create_connection(h, 3); print('BAGLANDI', h)\n"
            "    except OSError as e:\n"
            "        print('engellendi', h[0])\n", encoding="utf-8")
        s = self.kos("python ag.py")
        self.assertNotIn("BAGLANDI", s)
        self.assertEqual(s.count("engellendi"), 4, s)

    @staticmethod
    def kalan(ad):
        return subprocess.run(["docker", "ps", "-q", "--filter", f"name={ad}"], capture_output=True, text=True,
                              stdin=subprocess.DEVNULL).stdout.strip()


if __name__ == "__main__":
    unittest.main()
