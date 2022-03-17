
create table receita(
	id int not null auto_increment,
    nome varchar(255),
    
    primary key(id)
);

create table secao(
	id int not null auto_increment,
    nome varchar(255),
    
    primary key(id)
);

create table conteudo(
	id int not null auto_increment,
    item text,
    
    primary key(id)
);

create table receita_secao(
	id int not null auto_increment,
    id_receita int,
    id_secao int,
    foreign key (id_receita) references receita (id),
    foreign key (id_secao) references secao (id),
    primary key(id)
);

create table secao_conteudo(
	id int not null auto_increment,
    id_conteudo int,
    id_secao int,
    id_receita int,
    foreign key (id_conteudo) references conteudo (id),
    foreign key (id_secao) references secao (id),
    foreign key (id_receita) references receita (id),
    primary key(id)
);
