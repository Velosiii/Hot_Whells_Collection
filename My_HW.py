import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
import json
import os

JSON_DOSYA = "My_Hw_Collection.json"

# JSON'dan veri oku
def urunleri_yukle():
    if not os.path.exists(JSON_DOSYA):
        return []
    with open(JSON_DOSYA, "r", encoding="utf-8") as f:
        return json.load(f)

# JSON'a veri kaydet
def urunleri_kaydet():
    with open(JSON_DOSYA, "w", encoding="utf-8") as f:
        json.dump(urunler, f, ensure_ascii=False, indent=4)

# Listeyi güncelle
def listeyi_guncelle(veri_listesi):
    listebox.delete(0, tk.END)
    for urun in veri_listesi:
        listebox.insert(tk.END, urun["isim"])

# Seçilen ürünü göster
def urun_sec(event):
    secim = listebox.curselection()
    if not secim:
        return
    index = secim[0]
    urun_adi = listebox.get(index)
    urun = next((u for u in urunler if u["isim"] == urun_adi), None)
    if not urun:
        return
    resim_yolu = urun.get("resim", "")
    if not os.path.exists(resim_yolu):
        messagebox.showwarning("Uyarı", f"Resim bulunamadı: {resim_yolu}")
        return
    img = Image.open(resim_yolu)
    img = img.resize((300, 400))
    img_tk = ImageTk.PhotoImage(img)
    resim_label.config(image=img_tk)
    resim_label.image = img_tk
    baslik_label.config(text=urun['isim'])

# Yeni resim seç
def resim_sec(entry):
    yol = filedialog.askopenfilename(
        title="Resim Seç",
        filetypes=[("Resim dosyaları", "*.jpg *.png *.jpeg *.bmp")]
    )
    if yol:
        entry.delete(0, tk.END)
        entry.insert(0, yol)

# Yeni ürün ekle
def urun_ekle():
    isim = entry_isim.get().strip()
    kategori_raw = entry_kategori.get().strip()
    resim_yolu = entry_resim.get().strip()
    if not isim or not kategori_raw or not resim_yolu:
        messagebox.showwarning("Uyarı", "Tüm alanları doldurmalısın!")
        return
    if not os.path.exists(resim_yolu):
        messagebox.showerror("Hata", "Seçilen resim bulunamadı!")
        return
    kategori_listesi = [k.strip() for k in kategori_raw.split(",") if k.strip()]
    yeni_urun = {
        "isim": isim,
        "kategori": kategori_listesi,
        "resim": resim_yolu
    }
    urunler.append(yeni_urun)
    urunleri_kaydet()
    filtre_guncelle()
    entry_isim.delete(0, tk.END)
    entry_kategori.delete(0, tk.END)
    entry_resim.delete(0, tk.END)
    messagebox.showinfo("Başarılı", f"'{isim}' ürünü eklendi!")

# Ürün düzenleme
def urun_duzenle():
    secim = listebox.curselection()
    if not secim:
        messagebox.showwarning("Uyarı", "Düzenlemek için bir ürün seçin!")
        return
    index = secim[0]
    urun_adi = listebox.get(index)
    urun = next((u for u in urunler if u["isim"] == urun_adi), None)
    if not urun:
        return

    duzenle_pencere = Toplevel(pencere)
    duzenle_pencere.title("Ürünü Düzenle")
    duzenle_pencere.geometry("400x300")
    duzenle_pencere.config(bg="#dfe6e9")

    tk.Label(duzenle_pencere, text="İsim:", bg="#dfe6e9").grid(row=0, column=0, sticky="e", pady=5, padx=5)
    entry_duzen_isim = tk.Entry(duzenle_pencere, width=30)
    entry_duzen_isim.grid(row=0, column=1, pady=5)
    entry_duzen_isim.insert(0, urun["isim"])

    tk.Label(duzenle_pencere, text="Kategori:", bg="#dfe6e9").grid(row=1, column=0, sticky="e", pady=5, padx=5)
    entry_duzen_kategori = tk.Entry(duzenle_pencere, width=30)
    entry_duzen_kategori.grid(row=1, column=1, pady=5)
    kategori_yaz = urun["kategori"]
    if isinstance(kategori_yaz, list):
        kategori_yaz = ", ".join(kategori_yaz)
    entry_duzen_kategori.insert(0, kategori_yaz)

    tk.Label(duzenle_pencere, text="Resim Yolu:", bg="#dfe6e9").grid(row=2, column=0, sticky="e", pady=5, padx=5)
    entry_duzen_resim = tk.Entry(duzenle_pencere, width=30)
    entry_duzen_resim.grid(row=2, column=1, pady=5)
    entry_duzen_resim.insert(0, urun["resim"])

    btn_resim_sec = tk.Button(duzenle_pencere, text="Resim Seç", command=lambda: resim_sec(entry_duzen_resim))
    btn_resim_sec.grid(row=2, column=2, padx=5)

    def kaydet_duzenleme():
        yeni_isim = entry_duzen_isim.get().strip()
        yeni_kategori_raw = entry_duzen_kategori.get().strip()
        yeni_resim = entry_duzen_resim.get().strip()
        if not yeni_isim or not yeni_kategori_raw or not yeni_resim:
            messagebox.showwarning("Uyarı", "Tüm alanları doldurmalısın!")
            return
        yeni_kategori_listesi = [k.strip() for k in yeni_kategori_raw.split(",") if k.strip()]
        urun["isim"] = yeni_isim
        urun["kategori"] = yeni_kategori_listesi
        urun["resim"] = yeni_resim
        urunleri_kaydet()
        filtre_guncelle()
        duzenle_pencere.destroy()
        messagebox.showinfo("Başarılı", f"'{yeni_isim}' başarıyla güncellendi!")

    btn_kaydet_duzen = tk.Button(duzenle_pencere, text="Kaydet", bg="#0984e3", fg="white", command=kaydet_duzenleme)
    btn_kaydet_duzen.grid(row=3, column=1, pady=15)

# --- Ana pencere ---
pencere = tk.Tk()
pencere.title("Ürün Görüntüleyici")
pencere.geometry("1000x620")
pencere.config(bg="#e0e0e0")

urunler = urunleri_yukle()

# Sol taraf
liste_frame = tk.Frame(pencere, bg="#d0d0d0", padx=10, pady=10)
liste_frame.pack(side="left", fill="y")

tk.Label(liste_frame, text="Ürün Listesi", bg="#d0d0d0", font=("Arial", 12, "bold")).pack()

KATEGORILER = ["Toyota", "Porsche", "Subaru", "Ford", "Honda","Lamborghini", "Ferrari", "Bmw", "Kia"]
kategori_vars = []
sutun_siniri = 3

# Filtre frame
filtre_frame = tk.LabelFrame(pencere, text="Kategori Filtrele", bg="#d0d0d0", padx=10, pady=10)
filtre_frame.place(x=220, y=20, width=400, height=150)

for i, kat in enumerate(KATEGORILER):
    var = tk.IntVar()
    satir = i // sutun_siniri
    sutun = i % sutun_siniri
    cb = tk.Checkbutton(filtre_frame, text=kat, variable=var, bg="#d0d0d0",
                        font=("Arial", 10, "bold"), command=filtre_frame)
    cb.grid(row=satir, column=sutun, padx=10, pady=5, sticky="w")
    kategori_vars.append(var)

# Arama kutusu
arama_frame = tk.Frame(liste_frame, bg="#d0d0d0")
arama_frame.pack(pady=5)
entry_arama = tk.Entry(arama_frame, width=18)
entry_arama.pack(side="left", padx=3)
entry_arama.bind("<Return>", lambda event: filtre_guncelle())

btn_arama = tk.Button(arama_frame, text="Ara", command=filtre_frame)
btn_arama.pack(side="left")

# Liste kutusu
listebox = tk.Listbox(liste_frame, width=30, height=18)
listebox.pack(pady=5, fill="y")

btn_duzenle = tk.Button(liste_frame, text="Düzenle", bg="#74b9ff", command=urun_duzenle)
btn_duzenle.pack(pady=5, fill="x")

# Sağ taraf - Görsel
gorsel_frame = tk.Frame(pencere, bg="#e0e0e0", padx=10, pady=10)
gorsel_frame.pack(side="right", fill="both", expand=True)

baslik_label = tk.Label(gorsel_frame, text="", font=("Arial", 14, "bold"), bg="#e0e0e0")
baslik_label.pack(pady=10)
resim_label = tk.Label(gorsel_frame, bg="#e0e0e0")
resim_label.pack()

# Alt kısım - Yeni ürün ekleme
ekleme_frame = tk.Frame(pencere, bg="#cfcfcf", padx=10, pady=10)
ekleme_frame.pack(side="bottom", fill="x")

tk.Label(ekleme_frame, text="İsim:", bg="#cfcfcf").grid(row=0, column=0, sticky="e")
entry_isim = tk.Entry(ekleme_frame, width=25)
entry_isim.grid(row=0, column=1, padx=5)

tk.Label(ekleme_frame, text="Kategori:", bg="#cfcfcf").grid(row=1, column=0, sticky="e")
entry_kategori = tk.Entry(ekleme_frame, width=25)
entry_kategori.grid(row=1, column=1, padx=5)

tk.Label(ekleme_frame, text="Resim Yolu:", bg="#cfcfcf").grid(row=2, column=0, sticky="e")
entry_resim = tk.Entry(ekleme_frame, width=40)
entry_resim.grid(row=2, column=1, padx=5)

btn_resim = tk.Button(ekleme_frame, text="Resim Seç", command=lambda: resim_sec(entry_resim))
btn_resim.grid(row=2, column=2, padx=5)

btn_kaydet = tk.Button(ekleme_frame, text="Kaydet", bg="#4caf50", fg="white", command=urun_ekle)
btn_kaydet.grid(row=3, column=1, pady=10)

# --- Filtreleme fonksiyonu ---
def filtre_guncelle(event=None):
    secilen_kategoriler = [k for k, var in zip(KATEGORILER, kategori_vars) if var.get() == 1]
    aranan = entry_arama.get().strip().lower()
    filtreli = []
    for u in urunler:
        urun_kategorileri = u["kategori"]
        if isinstance(urun_kategorileri, str):
            urun_kategorileri = [urun_kategorileri]
        checkbox_uyum = not secilen_kategoriler or any(k in urun_kategorileri for k in secilen_kategoriler)
        isim_var = aranan in u["isim"].lower() if aranan else True
        kategori_var = any(aranan in k.lower() for k in urun_kategorileri) if aranan else True
        if checkbox_uyum and (isim_var or kategori_var):
            filtreli.append(u)
    listeyi_guncelle(filtreli)

# Başlangıçta tüm ürünleri listele
filtre_guncelle()
listebox.bind("<<ListboxSelect>>", urun_sec)

pencere.mainloop()
