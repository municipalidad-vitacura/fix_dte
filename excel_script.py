from __future__ import annotations

from io import BytesIO


def modificar_archivo(contenido: bytes, extension: str) -> BytesIO:
    extension = extension.lower()
    if extension == ".xml":
        return modificar_archivo_xml(contenido)

    raise ValueError("Formato no soportado para procesamiento.")


def modificar_archivo_xml(contenido_xml: bytes) -> BytesIO:
    """
    Mantiene la primera linea del XML y recorta el contenido al primer bloque DTE.
    """
    if not contenido_xml:
        return BytesIO(contenido_xml)

    salto_linea = contenido_xml.find(b"\n")
    if salto_linea == -1:
        primera_linea = contenido_xml
    else:
        primera_linea = contenido_xml[: salto_linea + 1]

    inicio_dte = contenido_xml.find(b"<DTE")
    if inicio_dte == -1:
        return BytesIO(contenido_xml)

    fin_dte = contenido_xml.find(b"</DTE>", inicio_dte)
    if fin_dte == -1:
        return BytesIO(contenido_xml)
    fin_dte += len(b"</DTE>")

    inicio_bloque = max(inicio_dte, len(primera_linea))
    nuevo_contenido = primera_linea + contenido_xml[inicio_bloque:fin_dte]

    salida = BytesIO(nuevo_contenido)
    salida.seek(0)
    return salida
