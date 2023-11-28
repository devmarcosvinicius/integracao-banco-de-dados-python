from sqlalchemy.orm import *
from sqlalchemy import *

Base = declarative_base()


class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String(9))
    endereco = Column(String)

    conta = relationship("Conta", back_populates="cliente")

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"


class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(String)
    saldo = Column(DECIMAL)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return (f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, numero={self.num}, "
                f"saldo={self.saldo}, cliente={self.id_cliente})")


print(Cliente.__tablename__)
print(Conta.__tablename__)

engine = create_engine("sqlite://")
Base.metadata.create_all(engine)
inspector_engine = inspect(engine)

print(inspector_engine.get_table_names())
print(inspector_engine.default_schema_name)

with Session(engine) as session:
    julia = Cliente(
        nome="Julia Lellis",
        cpf="123456789-00",
        endereco="Qr. 55, Rua 593, Apt. 55 Bloco J, Aguas Claras, Distrito Federal.",
        conta=[Conta(tipo="CP", agencia="0001", num="5574-0", saldo=7000.00)]
    )

    cinthia = Cliente(
        nome="Cinthia Bello",
        cpf="123456789-01",
        endereco="Qr. 55, Rua 593, Numero. 55 Condominio Jardins, Jardim Botânico, Distrito Federal.",
        conta=[Conta(tipo="CC", agencia="0001", num="5575-0", saldo=9000.00)]
    )

    marcos = Cliente(
        nome="Marcos Vinicius",
        cpf="123456789-02",
        endereco="Qr. 444, Rua 555, Numero. 55, Jardim Inga, Luziânia, Goias.",
        conta=[Conta(tipo="CC", agencia="0001", num="5575-0", saldo=856000.00)]
    )

    session.add_all([julia, cinthia, marcos])
    session.commit()

print("\n=-=-=-= recuperando clientes por nome =-=-=-=")
stmt_name = select(Cliente).where(Cliente.nome.in_(['Julia Lellis', 'Cinthia Bello', 'Marcos Vinicius']))

for cliente in session.scalars(stmt_name):
    print(cliente)

print("\n=-=-=-= recuperando contas por id =-=-=-=")
stmt_conta = select(Conta).where(Conta.id_cliente.in_([2, 3]))

for conta in session.scalars(stmt_conta):
    print(conta)

print("\n=-=-=-= recuperando cliente em ordem ascendente =-=-=-=")
stmt_order = select(Cliente).order_by(Cliente.nome.asc())

for cliente in session.scalars(stmt_order):
    print(cliente)

print("\n=-=-=-= recuperando cliente e conta =-=-=-=")
stmt_join = select(Cliente.nome, Conta.tipo).join_from(Conta, Cliente)
connection = engine.connect()
results = connection.execute(stmt_join).fetchall()

for result in results:
    print(result)

print("\n=-=-=-= recuperando a quantidade de clientes =-=-=-=")
stmt_count = select(func.count("*")).select_from(Cliente)

for result in session.scalars(stmt_count):
    print(result)

session.close()
