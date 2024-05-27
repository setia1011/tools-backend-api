import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, insert, desc, func, delete, text
from app.v1.models import Intdoc, IntdocHA, IntdocLPPIStatus, IntdocKantorPenerima, IntdocProdukAnalis, RefEntitasJenis, RefEntitasIdJenis, RefDokumen
from app.v1.schemas import intdoc as sc_intdoc
from typing import Union


def lppi_status_post(lppi_status: str, lppi_status_keterangan: str = None, db: Session = Depends):
    return db.execute(insert(IntdocLPPIStatus).values(lppi_status=lppi_status, lppi_status_keterangan=lppi_status_keterangan))

def ha_post(ha: str, ha_keterangan: str = None, db: Session = Depends):
    return db.execute(insert(IntdocHA).values(ha=ha, ha_keterangan=ha_keterangan))

def produk_analis_post(produk_analis: str, produk_analis_keterangan: str = None, db: Session = Depends):
    return db.execute(insert(IntdocProdukAnalis).values(produk_analis=produk_analis, produk_analis_keterangan=produk_analis_keterangan))

def entitas_jenis_post(entitas_jenis: str, entitas_jenis_keterangan: str = None, db: Session = Depends):
    return db.execute(insert(RefEntitasJenis).values(entitas_jenis=entitas_jenis, entitas_jenis_keterangan=entitas_jenis_keterangan))

def entitas_id_jenis_post(entitas_id_jenis: str, entitas_id_jenis_keterangan: str = None, db: Session = Depends):
    return db.execute(insert(RefEntitasIdJenis).values(entitas_id_jenis=entitas_id_jenis, entitas_id_jenis_keterangan=entitas_id_jenis_keterangan))

def ref_dokumen(dokumen_kode: str, dokumen_nama_pendek: str, dokumen_keterangan: str = None, db: Session = Depends):
    return db.execute(insert(RefDokumen).values(dokumen_kode=dokumen_kode.lower(), dokumen_nama_pendek=dokumen_nama_pendek.lower(), dokumen_keterangan=dokumen_keterangan.lower()))

def create_rt_ambil_lppi_nomor(db: Session = Depends):
    rt_ambil_lppi_nomor = """
    CREATE PROCEDURE ambil_lppi_nomor(IN _tahun INT, OUT _nomor INT)
    BEGIN
    DECLARE current_sequence INT;

    -- Get the current sequence value for the given year
    SELECT nomor INTO current_sequence
    FROM set_lppi_nomor
    WHERE tahun = _tahun
    LIMIT 1;

    IF current_sequence IS NULL THEN
        -- If no sequence exists for the given year, insert a new record
        INSERT INTO set_lppi_nomor (tahun, nomor)
        VALUES (_tahun, 1);
        SET _nomor = 1;
    ELSE
        -- Update the sequence value for the given year
        SET _nomor = current_sequence + 1;
        UPDATE set_lppi_nomor
        SET nomor = _nomor
        WHERE tahun = _tahun;
    END IF;
    END;

    DELIMITER ;
    """
    db.execute(text(rt_ambil_lppi_nomor))
    db.commit()

def create_rt_ambil_lkai_nomor(db: Session = Depends):
    rt_ambil_lkai_nomor = """
    CREATE PROCEDURE ambil_lkai_nomor(IN _tahun INT, OUT _nomor INT)
    BEGIN
    DECLARE current_sequence INT;

    -- Get the current sequence value for the given year
    SELECT nomor INTO current_sequence
    FROM set_lkai_nomor
    WHERE tahun = _tahun
    LIMIT 1;

    IF current_sequence IS NULL THEN
        -- If no sequence exists for the given year, insert a new record
        INSERT INTO set_lkai_nomor (tahun, nomor)
        VALUES (_tahun, 1);
        SET _nomor = 1;
    ELSE
        -- Update the sequence value for the given year
        SET _nomor = current_sequence + 1;
        UPDATE set_lkai_nomor
        SET nomor = _nomor
        WHERE tahun = _tahun;
    END IF;
    END;

    DELIMITER ;
    """
    db.execute(text(rt_ambil_lkai_nomor))
    db.commit()
