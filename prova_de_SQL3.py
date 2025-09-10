# CREATE TABLE Estoque (
#     EstoqueID INTEGER PRIMARY KEY,
#     ProdutoID INTEGER,
#     FornecedorID INTEGER,
#     Quantidade INTEGER,
#     DataEntrada DATE,
#     FOREIGN KEY (ProdutoID) REFERENCES Produtos(ProdutoID),
#     FOREIGN KEY (FornecedorID) REFERENCES Fornecedores(FornecedorID)
# );

# Não tenho o SQL baixado no Pc, mas esse seria o codigo pra Rodar no programa