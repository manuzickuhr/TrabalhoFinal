create database if not exists trabalhoFinal;
USE trabalhoFinal;

CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    primeiroNome VARCHAR(50) NOT NULL,
    sobrenome VARCHAR(50) NOT NULL,
    tipo ENUM('Funcionario', 'Cliente') NOT NULL
);

CREATE TABLE Funcionario (
    id INT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    funcao ENUM('Gerente', 'Atendente', 'Outro') NOT NULL,
    FOREIGN KEY (id) REFERENCES Usuario(id) ON DELETE CASCADE
);

CREATE TABLE Cliente (
    id INT PRIMARY KEY,
    emprestimos INT DEFAULT 0,
    FOREIGN KEY (id) REFERENCES Usuario(id) ON DELETE CASCADE
);

CREATE TABLE Livro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    nome VARCHAR(100) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    edicao VARCHAR(20),
    quantidade INT NOT NULL,
    emprestado BOOLEAN DEFAULT FALSE
);

CREATE TABLE Emprestimo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_emprestimo DATE NOT NULL,
    data_devolucao DATE NOT NULL,
    id_livro INT NOT NULL,
    id_cliente INT NOT NULL,
    id_funcionario INT NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_livro) REFERENCES Livro(id) ON DELETE CASCADE,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id) ON DELETE CASCADE,
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id) ON DELETE CASCADE
);

CREATE TABLE multa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dias_atraso INT NOT NULL,        
    valor DECIMAL(10, 2) NOT NULL,    
    data_multa DATETIME DEFAULT CURRENT_TIMESTAMP,  
    emprestimo_id INT NOT NULL,       
    cliente_id INT NOT NULL,          
    status ENUM('pendente', 'paga') DEFAULT 'pendente', 
    FOREIGN KEY (emprestimo_id) REFERENCES emprestimo(id),
    FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);


alter table livro
modify emprestado int ;

select * from usuario ;
select * from cliente; 
select * from funcionario;
select * from livro ;
select * from emprestimo ;
select * from multa ;







