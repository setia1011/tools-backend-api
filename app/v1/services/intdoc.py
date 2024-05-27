import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, insert, desc, func, delete, text, update
from app.v1.models import Intdoc, IntdocHA, IntdocLPPIStatus, IntdocKantorPenerima, IntdocProdukAnalis, IntdocRef, IntdocEntitas, RefEntitasJenis, RefDokumen, RefEntitasIdJenis, RefPerusahaan
from app.v1.schemas import intdoc as sc_intdoc
from typing import Union

# LPPI Status

def lppi_status_get_single(id: int, db: Session = Depends):
    return db.execute(select(IntdocLPPIStatus).filter(IntdocLPPIStatus.id==id)).scalar_one_or_none()

def lppi_status_get_all(lppi_status: str, db: Session = Depends):
    return db.execute(select(IntdocLPPIStatus).filter(IntdocLPPIStatus.lppi_status.like('%'+lppi_status+'%'))).scalars().all()

def lppi_status_post(t: sc_intdoc.LPPIStatusPost, db: Session = Depends):
    a = db.execute(insert(IntdocLPPIStatus).values(lppi_status=t.lppi_status, lppi_status_keterangan=t.lppi_status_keterangan))
    b = db.execute(select(IntdocLPPIStatus).filter(IntdocLPPIStatus.id==a.lastrowid)).scalar_one_or_none()
    return b

def lppi_status_patch(t: sc_intdoc.LPPIStatusPatch, db: Session = Depends):
    # md = model data, from database
    md = lppi_status_get_single(id=t.id, db=db)
    if md is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Data not found')
    for key, value in t.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(md, key, value)
    return md

def lppi_status_delete(id: int, db: Session = Depends):
    return db.execute(delete(IntdocLPPIStatus).filter(IntdocLPPIStatus.id==id))

# HA

def ha_get_single(id: int, db: Session = Depends):
    return db.execute(select(IntdocHA).filter(IntdocHA.id==id)).scalar_one_or_none()

def ha_get_all(ha: str, db: Session = Depends):
    return db.execute(select(IntdocHA).filter(IntdocHA.ha.like('%'+ha+'%'))).scalars().all()

def ha_post(t: sc_intdoc.HAPost, db: Session = Depends):
    a = db.execute(insert(IntdocHA).values(ha=t.ha, ha_keterangan=t.ha_keterangan))
    b = db.execute(select(IntdocHA).filter(IntdocHA.id==a.lastrowid)).scalar_one_or_none()
    return b

def ha_patch(t: sc_intdoc.HAPatch, db: Session = Depends):
    # md = model data, from database
    md = ha_get_single(id=t.id, db=db)
    if md is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Data not found')
    for key, value in t.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(md, key, value)
    return md

def ha_delete(id: int, db: Session = Depends):
    return db.execute(delete(IntdocHA).filter(IntdocHA.id==id))

# Produk Analis

def produk_analis_get_single(id: int, db: Session = Depends):
    return db.execute(select(IntdocProdukAnalis).filter(IntdocProdukAnalis.id==id)).scalar_one_or_none()

def produk_analis_get_all(produk_analis: str, db: Session = Depends):
    return db.execute(select(IntdocProdukAnalis).filter(IntdocProdukAnalis.produk_analis.like('%'+produk_analis+'%'))).scalars().all()

def produk_analis_post(t: sc_intdoc.ProdukAnalisPost, db: Session = Depends):
    a = db.execute(insert(IntdocProdukAnalis).values(produk_analis=t.produk_analis, produk_analis_keterangan=t.produk_analis_keterangan))
    b = db.execute(select(IntdocProdukAnalis).filter(IntdocProdukAnalis.id==a.lastrowid)).scalar_one_or_none()
    return b

def produk_analis_patch(t: sc_intdoc.ProdukAnalisPatch, db: Session = Depends):
    # md = model data, from database
    md = produk_analis_get_single(id=t.id, db=db)
    if md is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Data not found')
    for key, value in t.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(md, key, value)
    return md

def produk_analis_delete(id: int, db: Session = Depends):
    return db.execute(delete(IntdocProdukAnalis).filter(IntdocProdukAnalis.id==id))

# Penerima / kantor

def penerima_get_single(id: int, db: Session = Depends):
    return db.execute(select(IntdocKantorPenerima).filter(IntdocKantorPenerima.id==id)).scalar_one_or_none()

def penerima_get_all(kantor_penerima_nama: str, db: Session = Depends):
    return db.execute(select(IntdocKantorPenerima).filter(IntdocKantorPenerima.kantor_penerima_nama.like('%'+kantor_penerima_nama+'%'))).scalars().all()

def penerima_post(t: sc_intdoc.PenerimaPost, creator: int, db: Session = Depends):
    a = db.execute(insert(IntdocKantorPenerima).values(intdoc_id=t.intdoc_id, kantor_penerima_kode=t.kantor_penerima_kode, kantor_penerima_nama=t.kantor_penerima_nama, keterangan=t.keterangan, creator=creator))
    b = db.execute(select(IntdocKantorPenerima).filter(IntdocKantorPenerima.id==a.lastrowid)).scalar_one_or_none()
    return b

def penerima_postImport(t: sc_intdoc.PenerimaPost, lppi_no: int, lppi_tgl: str, creator: int, db: Session = Depends):
    x = db.execute(select(Intdoc).filter(Intdoc.lppi_no==lppi_no).filter(Intdoc.lppi_tgl==lppi_tgl)).scalar_one_or_none()
    a = db.execute(insert(IntdocKantorPenerima).values(intdoc_id=t.intdoc_id, kantor_penerima_kode=t.kantor_penerima_kode, kantor_penerima_nama=t.kantor_penerima_nama, keterangan=t.keterangan, creator=creator))
    b = db.execute(select(IntdocKantorPenerima).filter(IntdocKantorPenerima.id==a.lastrowid)).scalar_one_or_none()
    return b

def penerima_patch(t: sc_intdoc.PenerimaPatch, editor, db: Session = Depends):
    # md = model data, from database
    md = penerima_get_single(id=t.id, db=db)
    if md is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Data not found')
    md.editor = editor
    for key, value in t.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(md, key, value)
    return md

def penerima_delete(id: int, db: Session = Depends):
    return db.execute(delete(IntdocKantorPenerima).filter(IntdocKantorPenerima.id==id))

# Intdoc

def doc_get_single(id: int, db: Session = Depends):
    return db.execute(select(Intdoc).filter(Intdoc.id==id)).scalar_one_or_none()

def doc_get_all(q: str, order: str, page: int, per_page: int, db: Session = Depends):
    k = select(Intdoc)
    if q:
        k = k.filter(Intdoc.lppi_no.like('%'+q+'%'))
    if order == 'desc':
        k = k.order_by(desc(Intdoc.lppi_no))
    k = k.limit(per_page).offset(page)
    return db.execute(k).scalars().all()
    # return db.execute(select(Intdoc).filter(Intdoc.lppi_no.like('%'+q+'%'))).scalars().all()

def doc_count(q: str, db: Session = Depends):
    k = select(func.count(Intdoc.id))
    if q:
        k = k.filter(Intdoc.lppi_no.like('%'+q+'%'))
    return db.execute(k).scalar_one_or_none()

def doc_post(t: sc_intdoc.IntdocPost, creator: str, db: Session = Depends):
    from datetime import datetime
    _tahun = datetime.now().year
    db.execute(text(f"CALL ambil_lppi_nomor({_tahun}, @_nomor)"))
    lppi_no = db.execute(text('SELECT @_nomor')).scalar_one_or_none()
    a = db.execute(insert(Intdoc).values(
        lppi_no=lppi_no,
        lppi_tgl=t.lppi_tgl,
        lppi_kantor_penerbit_kode=t.lppi_kantor_penerbit_kode,
        lppi_kantor_penerbit_nama=t.lppi_kantor_penerbit_nama,
        lppi_penerima_nip=t.lppi_penerima_nip,
        lppi_penerima_nama=t.lppi_penerima_nama,
        lppi_penilai_nip=t.lppi_penilai_nip,
        lppi_penilai_nama=t.lppi_penilai_nama,
        lppi_status_id=t.lppi_status_id,
        lppi_konseptor_nip=t.lppi_konseptor_nip,
        lppi_konseptor_nama=t.lppi_konseptor_nama,
        lkai_no=t.lkai_no,
        lkai_tgl=t.lkai_tgl,
        lkai_analis_nip=t.lkai_analis_nip,
        lkai_analis_nama=t.lkai_analis_nama,
        lkai_kasi_nip=t.lkai_kasi_nip,
        lkai_kasi_nama=t.lkai_kasi_nama,
        lkai_kasubdit_nip=t.lkai_kasubdit_nip,
        lkai_kasubdit_nama=t.lkai_kasubdit_nama,
        produk_analis_id=t.produk_analis_id,
        produk_analis_no=t.produk_analis_no,
        produk_analis_tgl=t.produk_analis_tgl,
        materi=t.materi,
        keterangan=t.keterangan,
        ha_id=t.ha_id,
        tindak_lanjut=t.tindak_lanjut,
        tambah_bayar=t.tambah_bayar,
        entitas_npwp=t.entitas_npwp,
        entitas_nama=t.entitas_nama,
        komoditi=t.komoditi,
        nilai_barang=t.nilai_barang,
        dokumen=t.dokumen,
        lartas=t.lartas,
        lartas_123=t.lartas_123,
        creator=creator
    ))
    b = db.execute(select(Intdoc).filter(Intdoc.id==a.lastrowid)).scalar_one_or_none()
    if t.kantor_penerima is not None:
        for i in t.kantor_penerima:
            db.execute(insert(IntdocKantorPenerima).values(intdoc_id=b.id, kantor_penerima_kode=i.kd_kantor, kantor_penerima_nama=i.nama_kantor, creator=creator))
    if t.asal is not None:
        for i in t.asal:
            db.execute(insert(IntdocRef).values(intdoc_id=b.id, ref=i.dokumen_kode, ref_kode=i.dokumen_nama_pendek, ref_keterangan=i.dokumen_nama_panjang, creator=creator))
    return b

def doc_post_import(t: sc_intdoc.IntdocPostImport, creator: str, db: Session = Depends):
    a = db.execute(insert(Intdoc).values(
        lppi_no=t.lppi_no,
        lppi_tgl=t.lppi_tgl,
        lppi_kantor_penerbit_kode=t.lppi_kantor_penerbit_kode,
        lppi_kantor_penerbit_nama=t.lppi_kantor_penerbit_nama,
        lppi_penerima_nip=t.lppi_penerima_nip,
        lppi_penerima_nama=t.lppi_penerima_nama,
        lppi_penilai_nip=t.lppi_penilai_nip,
        lppi_penilai_nama=t.lppi_penilai_nama,
        lppi_status_id=t.lppi_status_id,
        lppi_konseptor_nip=t.lppi_konseptor_nip,
        lppi_konseptor_nama=t.lppi_konseptor_nama,
        lkai_no=t.lkai_no,
        lkai_tgl=t.lkai_tgl,
        lkai_analis_nip=t.lkai_analis_nip,
        lkai_analis_nama=t.lkai_analis_nama,
        lkai_kasi_nip=t.lkai_kasi_nip,
        lkai_kasi_nama=t.lkai_kasi_nama,
        lkai_kasubdit_nip=t.lkai_kasubdit_nip,
        lkai_kasubdit_nama=t.lkai_kasubdit_nama,
        produk_analis_id=t.produk_analis_id,
        produk_analis_no=t.produk_analis_no,
        produk_analis_tgl=t.produk_analis_tgl,
        materi=t.materi,
        keterangan=t.keterangan,
        ha_id=t.ha_id,
        tindak_lanjut=t.tindak_lanjut,
        tambah_bayar=t.tambah_bayar,
        entitas_npwp=t.entitas_npwp,
        entitas_nama=t.entitas_nama,
        komoditi=t.komoditi,
        nilai_barang=t.nilai_barang,
        dokumen=t.dokumen,
        lartas=t.lartas,
        lartas_123=t.lartas_123,
        creator=creator
    ))
    b = db.execute(select(Intdoc).filter(Intdoc.id==a.lastrowid)).scalar_one_or_none()
    db.execute(insert(IntdocRef).values(intdoc_id=b.id, ref=t.dokumen_jenis, creator=creator))
    return b

def doc_patch(t: sc_intdoc.IntdocPatch, editor, db: Session = Depends):
    # md = model data, from database
    md = doc_get_single(id=t.id, db=db)
    if md is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Data not found')
    md.editor = editor
    
    # Kantor penrima
    _kantor_penerima_kode = []
    if t.kantor_penerima is not None:
        for i in t.kantor_penerima:
            c = db.execute(select(IntdocKantorPenerima).filter(IntdocKantorPenerima.kantor_penerima_kode==i.kd_kantor).filter(IntdocKantorPenerima.intdoc_id==t.id)).scalar_one_or_none()
            if c is None:
                db.execute(insert(IntdocKantorPenerima).values(intdoc_id=t.id, kantor_penerima_kode=i.kd_kantor, kantor_penerima_nama=i.nama_kantor, editor=editor))
            _kantor_penerima_kode.append(i.kd_kantor)

    _kantor_penerima_todelete = db.execute(select(IntdocKantorPenerima).
                            filter(IntdocKantorPenerima.intdoc_id==t.id).
                            filter(IntdocKantorPenerima.kantor_penerima_kode.notin_(_kantor_penerima_kode))).scalars().all()
    for i in _kantor_penerima_todelete:
        db.execute(delete(IntdocKantorPenerima).filter(IntdocKantorPenerima.intdoc_id==t.id).filter(IntdocKantorPenerima.kantor_penerima_kode==i.kantor_penerima_kode))

    # asal
    _asal = []
    if t.asal is not None:
        for i in t.asal:
            c = db.execute(select(IntdocRef).filter(IntdocRef.ref==i.dokumen_kode).filter(IntdocRef.intdoc_id==t.id)).scalar_one_or_none()
            if c is None:
                db.execute(insert(IntdocRef).values(intdoc_id=t.id, ref=i.dokumen_kode, ref_kode=i.dokumen_nama_pendek, ref_keterangan=i.dokumen_nama_panjang, editor=editor))
            _asal.append(i.dokumen_kode)
    
    _asal_todelete = db.execute(select(IntdocRef).
                            filter(IntdocRef.intdoc_id==t.id).
                            filter(IntdocRef.ref.notin_(_asal))).scalars().all()
    for i in _asal_todelete:
        db.execute(delete(IntdocRef).filter(IntdocRef.intdoc_id==t.id).filter(IntdocRef.ref==i.ref))

    t.kantor_penerima = None
    t.asal = None
    
    for key, value in t.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(md, key, value)
    
    return md

def doc_delete(id: int, db: Session = Depends):
    return db.execute(delete(Intdoc).filter(Intdoc.id==id))

def doc_ambil_lppi_nomor(t: sc_intdoc.BookLPPINumberPost, creator: str, db: Session = Depends):
    from datetime import datetime
    _tahun = datetime.now().year
    db.execute(text(f"CALL ambil_lppi_nomor({_tahun}, @_nomor)"))
    lppi_no = db.execute(text('SELECT @_nomor')).scalar_one_or_none()
    a = db.execute(insert(Intdoc).values(
        lppi_no=lppi_no,
        lppi_tgl=t.lppi_tgl,
        lppi_kantor_penerbit_kode=t.lppi_kantor_penerbit_kode,
        lppi_kantor_penerbit_nama=t.lppi_kantor_penerbit_nama,
        creator=creator
    ))
    b = db.execute(select(Intdoc).filter(Intdoc.id==a.lastrowid)).scalars().all()
    return b

def doc_ambil_lkai_nomor(t: sc_intdoc.BookLKAINumberPost, editor: str, db: Session = Depends):
    from datetime import datetime
    _tahun = datetime.now().year
    db.execute(text(f"CALL ambil_lkai_nomor({_tahun}, @_nomor)"))
    lkai_no = db.execute(text('SELECT @_nomor')).scalar_one_or_none()
    print(lkai_no)
    a = db.execute(update(Intdoc).values(
        lkai_no=lkai_no,
        lkai_tgl=t.lkai_tgl,
        editor=editor
    ).filter(Intdoc.id==t.id))
    b = db.execute(select(Intdoc).filter(Intdoc.id==a.lastrowid)).scalars().all()
    return b

# Entitas

def entitas_get_one(id: int, db: Session = Depends):
    return db.execute(select(IntdocEntitas).filter(IntdocEntitas.id==id)).scalar_one_or_none()

def entitas_get_all(q: str, order: str, page: int, per_page: int, db: Session = Depends):
    k = select(IntdocEntitas)
    if q:
        k = k.filter(IntdocEntitas.entitas_nama.like('%'+q+'%'))
    if order == 'desc':
        k = k.order_by(desc(IntdocEntitas.entitas_nama))
    k = k.limit(per_page).offset(page)
    return db.execute(k).scalars().all()

def entitas_count(q: str, db: Session = Depends):
    k = select(func.count(IntdocEntitas.id))
    if q:
        k = k.filter(IntdocEntitas.entitas_nama.like('%'+q+'%'))
    return db.execute(k).scalar_one_or_none()

def entitas_post(t: sc_intdoc.EntitasPost, db: Session = Depends):
    a = db.execute(insert(IntdocEntitas).values(entitas_jenis_id=t.entitas_jenis_id, entitas_id_jenis_id=t.entitas_id_jenis_id, entitas_id_nomor=t.entitas_id_nomor, entitas_nama=t.entitas_nama, entitas_keterangan=t.entitas_keterangan))
    b = db.execute(select(IntdocEntitas).filter(IntdocEntitas.id==a.lastrowid)).scalar_one_or_none()
    return b

def entitas_patch(t: sc_intdoc.EntitasPatch, db: Session = Depends):
    # md = model data, from database
    md = entitas_get_one(id=t.id, db=db)
    if md is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Data not found')
    for key, value in t.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(md, key, value)
    return md

def entitas_delete(id: int, db: Session = Depends):
    r = db.execute(select(IntdocEntitas).filter(IntdocEntitas.id==id)).scalar_one_or_none()
    c = db.execute(select(func.count(Intdoc.id)).filter(Intdoc.entitas_npwp==r.entitas_id_nomor)).scalar_one_or_none()
    if c is None or c == 0:
        return db.execute(delete(IntdocEntitas).filter(IntdocEntitas.id==id))
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error")