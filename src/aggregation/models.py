from datetime import datetime
from decimal import Decimal
from sqlalchemy import Date
from sqlalchemy import Date
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped,mapped_column

class Base(DeclarativeBase):
    pass

class AnpData(Base):
    __tablename__ = 'anp_data'

    id: Mapped[int] = mapped_column(primary_key=True)
    regiao_sigla:   Mapped[str]         = mapped_column(String(2))
    estado_sigla:   Mapped[str]         = mapped_column(String(2))
    municipio:      Mapped[str]         = mapped_column(String(255))
    revenda:        Mapped[str]         = mapped_column(String(255))
    cnpj_revenda:   Mapped[str]         = mapped_column(String(18))
    nome_rua:       Mapped[str | None]  = mapped_column(String(255))
    numero_rua:     Mapped[str | None]  = mapped_column(String(50))
    complemento:    Mapped[str | None]  = mapped_column(String(255))
    bairro:         Mapped[str | None]  = mapped_column(String(255), nullable=True)
    cep:            Mapped[str]         = mapped_column(String(8))
    produto:        Mapped[str]         = mapped_column(String(50))
    data_coleta:    Mapped[datetime]    = mapped_column(Date)
    valor_venda:    Mapped[Decimal]     = mapped_column(Numeric(precision=10,scale=2))
    valor_compra:   Mapped[Decimal]     = mapped_column(Numeric(precision=10,scale=2))
    unidade_medida: Mapped[str]         = mapped_column(String(50))
    bandeira:       Mapped[str]         = mapped_column(String(50))









