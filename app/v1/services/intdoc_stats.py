import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, insert, desc, func, delete, text
from app.v1.models import Intdoc, IntdocHA, IntdocLPPIStatus, IntdocKantorPenerima, IntdocProdukAnalis, IntdocRef, RefDokumen
from app.v1.schemas import intdoc as sc_intdoc
from app.v1.schemas import intdoc_stats as sc_intdoc_stats
from typing import Union
import calendar
from collections import defaultdict

# Hitrate

def hitrate(start_date: str, end_date: str, db: Session = Depends):
    capaian = db.execute(select(func.count(Intdoc.id).label('jumlah')).filter(Intdoc.lppi_tgl.between(start_date, end_date))).scalar_one_or_none()
    print(select(func.count(Intdoc.id).label('jumlah')).filter(Intdoc.lppi_tgl.between(start_date, end_date)))
    return {"target": 120, "capaian": capaian}

# Hasil

def hasil(start_date: str, end_date: str, db: Session = Depends):
    r = db.execute(select(func.count(Intdoc.id), IntdocHA.ha)
        .join(IntdocHA)
        .group_by(IntdocHA.ha)
        .filter(Intdoc.lppi_tgl.between(start_date, end_date))).all()
    d = [({"ha": i[1], "jumlah": i[0]}) for i in r]
    return d

# Komposisi

def stats_komposisi(date: str, year: str, db: Session = Depends):
    r = db.execute(select(func.count(Intdoc.id), IntdocProdukAnalis.produk_analis)
        .join(IntdocProdukAnalis)
        .group_by(IntdocProdukAnalis.produk_analis)
        .filter(func.extract('year', Intdoc.lppi_tgl)==year)).all()
    d = [({"jumlah_produk_analis": i[1], "jenis_produk_analis": i[0]}) for i in r]
    return d

def lppi_status(start_date: str, end_date: str, db: Session = Depends):
    r = db.execute(select(func.count(Intdoc.id), IntdocLPPIStatus.lppi_status)
        .join(IntdocLPPIStatus)
        .group_by(IntdocLPPIStatus.lppi_status)
        .filter(Intdoc.lppi_tgl.between(start_date, end_date)).order_by(desc(func.count(Intdoc.id)))).all()
    d = [({"value": i[0], "name": i[1]}) for i in r]
    return d

def chart_komposisi(start_date: str, end_date: str, db: Session = Depends):
    r = db.execute(select(func.count(Intdoc.id), IntdocProdukAnalis.produk_analis)
        .join(IntdocProdukAnalis)
        .group_by(IntdocProdukAnalis.produk_analis)
        .filter(Intdoc.lppi_tgl.between(start_date, end_date))).all()
    d = [({"name": i[1], "value": i[0]}) for i in r]
    return d

# Tren

def chart_tren(start_date: str, end_date: str, db: Session = Depends):
    r = db.execute(select(func.count(Intdoc.id), func.extract('month', Intdoc.lppi_tgl), IntdocProdukAnalis.produk_analis)
        .join(IntdocProdukAnalis)
        .group_by(func.extract('month', Intdoc.lppi_tgl)).order_by(func.extract('month', Intdoc.lppi_tgl))
        .group_by(IntdocProdukAnalis.produk_analis)
        .filter(Intdoc.lppi_tgl.between(start_date, end_date))).all()
    data = [({"bulan": calendar.month_abbr[i[1]], "jenis_produk_analis": i[2], "jumlah_produk_analis": i[0]}) for i in r]

    # Extract unique 'jenis_produk_analis' values
    unique_jenis_produk_analis = set(d['jenis_produk_analis'] for d in data)

    # Organize data into a dictionary with 'bulan' as keys
    bulan_data = defaultdict(lambda: defaultdict(int))

    for d in data:
        bulan_data[d['bulan']][d['jenis_produk_analis']] += d['jumlah_produk_analis']

    # Create the desired structure dynamically
    result = {
        'bulan': [],
        'data': [{'jenis_produk_analis': jenis, 'jumlah_produk_analis': []} for jenis in unique_jenis_produk_analis]
    }

    for bulan, jenis_produk_analis_data in bulan_data.items():
        result['bulan'].append(bulan)
        for jenis_produk_analis in result['data']:
            jumlah = jenis_produk_analis_data.get(jenis_produk_analis['jenis_produk_analis'], 0)
            jenis_produk_analis['jumlah_produk_analis'].append(jumlah)

    return result

# Source Reference

def referensi(start_date: str, end_date: str, db: Session = Depends):
    r = db.execute(select(func.count(Intdoc.id), IntdocRef.ref)
        .join(IntdocRef)
        .group_by(IntdocRef.ref)
        .filter(Intdoc.lppi_tgl.between(start_date, end_date))).all()
    d = [({"jumlah": i[0], "referensi": i[1]}) for i in r]
    return d

# Datatables

def top10_analis(start_date: str, end_date: str, db: Session = Depends):
    r = db.execute(select(func.count(Intdoc.id), Intdoc.lkai_analis_nama)
        .group_by(Intdoc.lkai_analis_nama)
        .filter(Intdoc.lppi_tgl.between(start_date, end_date)).order_by(desc(func.count(Intdoc.id))).limit(10)).all()
    d = [({"jumlah": i[0], "lkai_analis_nama": i[1]}) for i in r]
    return d

def top10_perusahaan(start_date: str, end_date: str, db: Session = Depends):
    r = db.execute(select(func.count(Intdoc.id), Intdoc.entitas_nama)
        .group_by(Intdoc.entitas_nama)
        .filter(Intdoc.lppi_tgl.between(start_date, end_date)).order_by(desc(func.count(Intdoc.id))).limit(10)).all()
    d = [({"jumlah": i[0], "entitas_nama": i[1]}) for i in r]
    return d

def top10_komoditi(start_date: str, end_date: str, db: Session = Depends):
    r = db.execute(select(func.count(Intdoc.id), Intdoc.komoditi)
        .group_by(Intdoc.komoditi)
        .filter(Intdoc.lppi_tgl.between(start_date, end_date)).order_by(desc(func.count(Intdoc.id))).limit(10)).all()
    d = [({"jumlah": i[0], "komoditi": i[1]}) for i in r]
    return d

def top10_tujuan(start_date: str, end_date: str, db: Session = Depends):
    r = db.execute(select(func.count(Intdoc.id), IntdocKantorPenerima.kantor_penerima_nama)
        .join(IntdocKantorPenerima)
        .group_by(IntdocKantorPenerima.kantor_penerima_nama)
        .filter(Intdoc.lppi_tgl.between(start_date, end_date)).order_by(desc(func.count(Intdoc.id))).limit(10)).all()
    d = [({"jumlah": i[0], "kantor_penerima_nama": i[1]}) for i in r]
    return d

def top10_asal(start_date: str, end_date: str, db: Session = Depends):
    r = db.execute(select(func.count(Intdoc.id), IntdocRef.ref)
        .join(IntdocRef)
        .group_by(IntdocRef.ref)
        .filter(Intdoc.lppi_tgl.between(start_date, end_date)).order_by(desc(func.count(Intdoc.id))).limit(10)).all()
    d = [({"jumlah": i[0], "dokumen_jenis": i[1]}) for i in r]
    return d

def top10_penindakan(start_date: str, end_date: str, db: Session = Depends):
    r = db.execute(select(func.count(Intdoc.id), Intdoc.tindak_lanjut)
        .group_by(Intdoc.tindak_lanjut)
        .filter(Intdoc.lppi_tgl.between(start_date, end_date)).order_by(desc(func.count(Intdoc.id))).limit(10)).all()
    d = [({"jumlah": i[0], "tindak_lanjut": i[1]}) for i in r]
    return d


































    # res = {}
    # for item in d:
    #     res.setdefault(item['bulan'], []).append({
    #         "jenis_produk_analis": 2,
    #         "jumlah_produk_analis": item['jumlah_produk_analis']
    #     })

    # return res
    
    # f = {}
    # _a = []
    # for i, o in res.items():
    #     for j in o:
    #         print(j)
    # return f

    # _x = []
    # _z = []
    # for x in d:

    #     m = x['bulan']
    #     if m not in y['bulan']:
    #         y['bulan'].append(m)

    #     a = x['jenis_produk_analis']
    #     if a not in _x:
    #         _x.append(a)
        
    #         _z.append()
    # y
    # return _z
    