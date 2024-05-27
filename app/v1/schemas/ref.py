import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Union


class MyBaseModel(BaseModel):
   class Config:
      model_config = ConfigDict(from_attributes=True)

# Ref Dokumen
      
class RefDokumen(MyBaseModel):
   id: Union[int, None] = None
   dokumen_kode: Union[str, None] = None
   dokumen_nama_pendek: Union[str, None] = None
   dokumen_nama_panjang: Union[str, None] = None
   dokumen_keterangan: Union[str, None] = None

class RefDokumenPost(MyBaseModel):
   dokumen_kode: str
   dokumen_nama_pendek: Union[str, None] = None
   dokumen_nama_panjang: Union[str, None] = None
   dokumen_keterangan: Union[str, None] = None

class RefDokumenPatch(MyBaseModel):
   id: int
   dokumen_kode: Union[str, None] = None
   dokumen_nama_pendek: Union[str, None] = None
   dokumen_nama_panjang: Union[str, None] = None
   dokumen_keterangan: Union[str, None] = None

# Entitas

class RefEntitasJenis(MyBaseModel):
   id: Union[int, None] = None
   entitas_jenis: Union[str, None] = None
   entitas_jenis_keterangan: Union[str, None] = None

class RefEntitasIdJenis(MyBaseModel):
   id: Union[int, None] = None
   entitas_id_jenis: Union[str, None] = None
   entitas_id_jenis_keterangan: Union[str, None] = None

class Entitas(MyBaseModel):
   id: Union[int, None] = None
   entitas_jenis_id: Union[int, None] = None
   entitas_id_jenis_id: Union[int, None] = None
   entitas_id_nomor: Union[str, None] = None
   entitas_nama: Union[str, None] = None
   entitas_keterangan: Union[str, None] = None

   ref_entitas_jenis: Optional[RefEntitasJenis]
   ref_entitas_id_jenis: Optional[RefEntitasIdJenis]