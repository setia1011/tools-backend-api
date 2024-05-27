import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Union


class MyBaseModel(BaseModel):
    class Config:
        model_config = ConfigDict(from_attributes=True)

# LPPI Status
        
class LPPIStatus(MyBaseModel):
    id: Union[int, None] = None
    lppi_status: Union[str, None] = None
    lppi_status_keterangan: Union[str, None] = None

class LPPIStatusPost(MyBaseModel):
    lppi_status: str
    lppi_status_keterangan: Union[str, None] = None

class LPPIStatusPatch(MyBaseModel):
    id: int
    lppi_status: Union[str, None] = None
    lppi_status_keterangan: Union[str, None] = None

# HA
    
class HA(MyBaseModel):
    id: Union[int, None] = None
    ha: Union[str, None] = None
    ha_keterangan: Union[str, None] = None

class HAPost(MyBaseModel):
    ha: str
    ha_keterangan: Union[str, None] = None

class HAPatch(MyBaseModel):
    id: int
    ha: Union[str, None] = None
    ha_keterangan: Union[str, None] = None

# Produk Analis
    
class ProdukAnalis(MyBaseModel):
    id: Union[int, None] = None
    produk_analis: Union[str, None] = None
    produk_analis_keterangan: Union[str, None] = None

class ProdukAnalisPost(MyBaseModel):
    produk_analis: str
    produk_analis_keterangan: Union[str, None] = None

class ProdukAnalisPatch(MyBaseModel):
    id: int
    produk_analis: Union[str, None] = None
    produk_analis_keterangan: Union[str, None] = None

# 

class RefEntitasJenis(MyBaseModel):
    id: Union[int, None] = None
    entitas_jenis: Union[str, None] = None
    entitas_jenis_keterangan: Union[str, None] = None

class RefEntitasIDJenis(MyBaseModel):
    id: Union[int, None] = None
    entitas_id_jenis: Union[str, None] = None
    entitas_id_jenis_keterangan: Union[str, None] = None

# Entitas

class Entitas(MyBaseModel):
    id: Union[int, None] = None
    entitas_jenis_id: Union[int, None] = None
    entitas_id_jenis_id: Union[int, None] = None
    entitas_id_nomor: Union[str, None] = None
    entitas_nama: Union[str, None] = None
    entitas_keterangan: Union[str, None] = None

    ref_entitas_jenis: Optional[RefEntitasJenis]
    ref_entitas_id_jenis: Optional[RefEntitasIDJenis]

class EntitasPost(MyBaseModel):
    entitas_jenis_id: int
    entitas_id_jenis_id: int
    entitas_id_nomor: str
    entitas_nama: str
    entitas_keterangan : Union[str, None] = None

class EntitasPatch(MyBaseModel):
    id: int
    entitas_jenis_id: Union[int, None] = None
    entitas_id_jenis_id: Union[int, None] = None
    entitas_id_nomor: Union[str, None] = None
    entitas_nama: Union[str, None] = None
    entitas_keterangan: Union[str, None] = None

# Penerima
    
class Penerima(MyBaseModel):
    id: Union[int, None] = None
    intdoc_id: Union[int, None] = None
    kantor_penerima_kode: Union[str, None] = None
    kantor_penerima_nama: Union[str, None] = None
    keterangan: Union[str, None] = None
    creator: Union[str, None] = None
    created_at: Union[datetime.datetime, None] = None
    editor: Union[str, None] = None
    updated_at: Union[datetime.datetime, None] = None

class PenerimaPost(MyBaseModel):
    intdoc_id: Union[int, None] = None
    kantor_penerima_kode: str
    kantor_penerima_nama: str
    keterangan: Union[str, None] = None

class PenerimaPatch(MyBaseModel):
    id: int
    intdoc_id: Union[int, None] = None
    kantor_penerima_kode: Union[str, None] = None
    kantor_penerima_nama: Union[str, None] = None
    keterangan: Union[str, None] = None

# Kantor
    
class RefKantorEx(MyBaseModel):
    kd_kantor: Union[str, None] = None
    nama_kantor: Union[str, None] = None

# Intdoc Ref
    
class IntdocRef(MyBaseModel):
    id: Union[int, None] = None
    intdoc_id: Union[int, None] = None
    ref: Union[str, None] = None
    ref_kode: Union[str, None] = None
    ref_keterangan: Union[str, None] = None

# Ref Dokumen

class RefDokumen(MyBaseModel):
    id: Union[int, None] = None
    dokumen_kode: Union[str, None] = None
    dokumen_nama_pendek: Union[str, None] = None
    dokumen_nama_panjang: Union[str, None] = None

# Book

class BookLPPINumberPost(MyBaseModel):
    lppi_tgl: datetime.datetime
    lppi_kantor_penerbit_kode: str
    lppi_kantor_penerbit_nama: str
    # token: str

class BookLKAINumberPost(MyBaseModel):
    id: int
    lkai_tgl: datetime.datetime
    # token: str

# Intdoc

class Intdoc(MyBaseModel):
    id: Union[int, None] = None
    lppi_no: Union[int, None] = None
    lppi_tgl: Union[datetime.datetime, None] = None

    lppi_kantor_penerbit_kode: Union[str, None] = None
    lppi_kantor_penerbit_nama: Union[str, None] = None

    lppi_penerima_nip: Union[str, None] = None
    lppi_penerima_nama: Union[str, None] = None
    lppi_penilai_nip: Union[str, None] = None
    lppi_penilai_nama: Union[str, None] = None
    lppi_status_id: Union[int, None] = None
    lppi_konseptor_nip: Union[str, None] = None
    lppi_konseptor_nama: Union[str, None] = None

    lkai_no: Union[int, None] = None
    lkai_tgl: Union[datetime.datetime, None] = None
    lkai_analis_nip: Union[str, None] = None
    lkai_analis_nama: Union[str, None] = None
    lkai_kasi_nip: Union[str, None] = None
    lkai_kasi_nama: Union[str, None] = None
    lkai_kasubdit_nip: Union[str, None] = None
    lkai_kasubdit_nama: Union[str, None] = None

    produk_analis_id: Union[int, None] = None
    produk_analis_no: Union[str, None] = None
    produk_analis_tgl: Union[datetime.datetime, None] = None

    materi: Union[str, None] = None
    keterangan: Union[str, None] = None
    ha_id: Union[int, None] = None
    tindak_lanjut: Union[str, None] = None
    tambah_bayar: Union[float, None] = None
    entitas_npwp: Union[str, None] = None
    entitas_nama: Union[str, None] = None
    komoditi: Union[str, None] = None
    nilai_barang: Union[float, None] = None
    dokumen_jenis: Union[str, None] = None
    dokumen: Union[str, None] = None
    lartas: Union[int, None] = None
    lartas_123: Union[str, None] = None

    creator: Union[str, None] = None
    created_at: Union[datetime.datetime, None] = None
    editor: Union[str, None] = None
    updated_at: Union[datetime.datetime, None] = None

    produk_analis: Optional[ProdukAnalis]
    ha: Optional[HA]
    lppi_status: Optional[LPPIStatus]
    asal: Optional[list[IntdocRef]]
    kantor_penerima: Optional[list[Penerima]]


class IntdocPost(MyBaseModel):
    lppi_no: Union[int, None] = None
    lppi_tgl: Union[datetime.datetime, None] = None

    lppi_kantor_penerbit_kode: str
    lppi_kantor_penerbit_nama: str

    lppi_penerima_nip: Union[str, None] = None
    lppi_penerima_nama: Union[str, None] = None
    lppi_penilai_nip: Union[str, None] = None
    lppi_penilai_nama: Union[str, None] = None
    lppi_status_id: Union[int, None] = None
    lppi_konseptor_nip: Union[str, None] = None
    lppi_konseptor_nama: Union[str, None] = None

    lkai_no: Union[int, None] = None
    lkai_tgl: Union[datetime.datetime, None] = None
    lkai_analis_nip: Union[str, None] = None
    lkai_analis_nama: Union[str, None] = None
    lkai_kasi_nip: Union[str, None] = None
    lkai_kasi_nama: Union[str, None] = None
    lkai_kasubdit_nip: Union[str, None] = None
    lkai_kasubdit_nama: Union[str, None] = None

    produk_analis_id: Union[int, None] = None
    produk_analis_no: Union[str, None] = None
    produk_analis_tgl: Union[datetime.datetime, None] = None

    materi: Union[str, None] = None
    keterangan: Union[str, None] = None
    ha_id: Union[int, None] = None
    tindak_lanjut: Union[str, None] = None
    tambah_bayar: Union[float, None] = None
    entitas_npwp: Union[str, None] = None
    entitas_nama: Union[str, None] = None
    komoditi: Union[str, None] = None
    nilai_barang: Union[float, None] = None
    # dokumen_jenis: Union[str, None] = None
    dokumen: Union[str, None] = None
    lartas: Union[int, None] = None
    lartas_123: Union[str, None] = None

    kantor_penerima: Union[list[RefKantorEx], None] = None
    asal: Union[list[RefDokumen], None] = None

class IntdocPostImport(MyBaseModel):
    lppi_no: int
    lppi_tgl: datetime.datetime

    lppi_kantor_penerbit_kode: str
    lppi_kantor_penerbit_nama: str

    lppi_penerima_nip: Union[str, None] = None
    lppi_penerima_nama: Union[str, None] = None
    lppi_penilai_nip: Union[str, None] = None
    lppi_penilai_nama: Union[str, None] = None
    lppi_status_id: Union[int, None] = None
    lppi_konseptor_nip: Union[str, None] = None
    lppi_konseptor_nama: Union[str, None] = None

    lkai_no: Union[int, None] = None
    lkai_tgl: Union[datetime.datetime, None] = None
    lkai_analis_nip: Union[str, None] = None
    lkai_analis_nama: Union[str, None] = None
    lkai_kasi_nip: Union[str, None] = None
    lkai_kasi_nama: Union[str, None] = None
    lkai_kasubdit_nip: Union[str, None] = None
    lkai_kasubdit_nama: Union[str, None] = None

    produk_analis_id: Union[int, None] = None
    produk_analis_no: Union[str, None] = None
    produk_analis_tgl: Union[datetime.datetime, None] = None

    materi: Union[str, None] = None
    keterangan: Union[str, None] = None
    ha_id: Union[int, None] = None
    tindak_lanjut: Union[str, None] = None
    tambah_bayar: Union[float, None] = None
    entitas_npwp: Union[str, None] = None
    entitas_nama: Union[str, None] = None
    komoditi: Union[str, None] = None
    nilai_barang: Union[float, None] = None
    dokumen_jenis: Union[str, None] = None
    dokumen: Union[str, None] = None
    lartas: Union[int, None] = None
    lartas_123: Union[str, None] = None

    kantor_penerima: Union[list[RefKantorEx], None] = None
    asal: Union[list[RefDokumen], None] = None
    
class IntdocPatch(MyBaseModel):
    id: int
    lppi_no: Union[int, None] = None
    lppi_tgl: Union[datetime.datetime, None] = None

    lppi_kantor_penerbit_kode: Union[str, None] = None
    lppi_kantor_penerbit_nama: Union[str, None] = None

    lppi_penerima_nip: Union[str, None] = None
    lppi_penerima_nama: Union[str, None] = None
    lppi_penilai_nip: Union[str, None] = None
    lppi_penilai_nama: Union[str, None] = None
    lppi_status_id: Union[int, None] = None
    lppi_konseptor_nip: Union[str, None] = None
    lppi_konseptor_nama: Union[str, None] = None

    lkai_no: Union[int, None] = None
    lkai_tgl: Union[datetime.datetime, None] = None
    lkai_analis_nip: Union[str, None] = None
    lkai_analis_nama: Union[str, None] = None
    lkai_kasi_nip: Union[str, None] = None
    lkai_kasi_nama: Union[str, None] = None
    lkai_kasubdit_nip: Union[str, None] = None
    lkai_kasubdit_nama: Union[str, None] = None

    produk_analis_id: Union[int, None] = None
    produk_analis_no: Union[str, None] = None
    produk_analis_tgl: Union[datetime.datetime, None] = None

    materi: Union[str, None] = None
    keterangan: Union[str, None] = None
    ha_id: Union[int, None] = None
    tindak_lanjut: Union[str, None] = None
    tambah_bayar: Union[float, None] = None
    entitas_npwp: Union[str, None] = None
    entitas_nama: Union[str, None] = None
    komoditi: Union[str, None] = None
    nilai_barang: Union[float, None] = None
    dokumen_jenis: Union[str, None] = None
    dokumen: Union[str, None] = None
    lartas: Union[int, None] = None
    lartas_123: Union[str, None] = None

    kantor_penerima: Union[list[RefKantorEx], None] = None
    asal: Union[list[RefDokumen], None] = None

class IntdocPaginate(MyBaseModel):
    items: list[Intdoc]
    total_pages: Optional[int]
    total_items: Optional[int]

class EntitasPaginate(MyBaseModel):
    items: list[Entitas]
    total_pages: Optional[int]
    total_items: Optional[int]
    