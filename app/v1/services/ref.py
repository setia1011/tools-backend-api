import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, insert, desc, func, delete
from app.v1.models import IntdocRef, RefDokumen, RefPerusahaan, IntdocEntitas, RefEntitasJenis, RefEntitasIdJenis
from typing import Union
from app.v1.schemas import ref as sc_ref

def get_ref_dokumen(q: str, db: Session = Depends):
   return db.execute(select(RefDokumen).filter(RefDokumen.dokumen_nama_pendek.like('%'+q+'%'))).scalars().all()

def get_ref_perusahaan(q: str, db: Session = Depends):
   return db.execute(select(RefPerusahaan).filter(RefPerusahaan.perusahaan_nama.like('%'+q+'%'))).scalars().all()

def get_entitas(q: str, db: Session = Depends):
   return db.execute(select(IntdocEntitas).filter(IntdocEntitas.entitas_nama.like('%'+q+'%'))).scalars().all()

def get_entitas_jenis(q: str, db: Session = Depends):
   return db.execute(select(RefEntitasJenis).filter(RefEntitasJenis.entitas_jenis.like('%'+q+'%'))).scalars().all()

def get_entitas_id_jenis(q: str, db: Session = Depends):
   return db.execute(select(RefEntitasIdJenis).filter(RefEntitasIdJenis.entitas_id_jenis.like('%'+q+'%'))).scalars().all()

# Ref dokumen

def ref_dokumen_get_one(id: int, db: Session = Depends):
   return db.execute(select(RefDokumen).filter(RefDokumen.id==id)).scalar_one_or_none()

def ref_dokumen_get_all(q: str, order: str, page: int, per_page: int, db: Session = Depends):
   k = select(RefDokumen)
   if q:
      k = k.filter(RefDokumen.dokumen_kode.like('%'+q+'%'))
   if order == 'desc':
      k = k.order_by(desc(RefDokumen.dokumen_kode))
   k = k.limit(per_page).offset(page)
   return db.execute(k).scalars().all()

def ref_dokumen_count(q: str, db: Session = Depends):
   k = select(func.count(RefDokumen.id))
   if q:
      k = k.filter(RefDokumen.dokumen_kode.like('%'+q+'%'))
   return db.execute(k).scalar_one_or_none()

def ref_dokumen_post(t: sc_ref.RefDokumenPost, db: Session = Depends):
    a = db.execute(insert(RefDokumen).values(dokumen_kode=t.dokumen_kode, dokumen_nama_pendek=t.dokumen_nama_pendek, dokumen_nama_panjang=t.dokumen_nama_panjang, dokumen_keterangan=t.dokumen_keterangan))
    b = db.execute(select(RefDokumen).filter(RefDokumen.id==a.lastrowid)).scalar_one_or_none()
    return b

def ref_dokumen_patch(t: sc_ref.RefDokumenPatch, db: Session = Depends):
    # md = model data, from database
    md = ref_dokumen_get_one(id=t.id, db=db)
    if md is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Data not found')
    for key, value in t.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(md, key, value)
    return md

def ref_dokumen_delete(id: int, db: Session = Depends):
    r = db.execute(select(RefDokumen).filter(RefDokumen.id==id)).scalar_one_or_none()
    c = db.execute(select(func.count(IntdocRef.id)).filter(IntdocRef.ref_kode==r.dokumen_kode)).scalar_one_or_none()
    if c is None or c == 0:
        return db.execute(delete(RefDokumen).filter(RefDokumen.id==id))
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error")