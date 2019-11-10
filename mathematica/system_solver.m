(* Seta o Diretório do Notebook (deste arquivo) como Principal *)
(* SetDirectory[NotebookDirectory[]]; *)

(* Abre o arquivo "entrada" em modo Leitura *)
OpenRead["entrada.txt"];
(* Lê a quantidade de Letras *)

qtdeLetras = Read["entrada.txt", Number];
(* Lê a quantidade de Estados *)

qtdeEstados = Read["entrada.txt", Number];
(* Lê se há ou não probabilidade *)
prob = Read["entrada.txt", Number];
(* Lê o Sistema e calcula o mesmo *)
system = << "entrada.txt";
(* Fecha o arquivo "entrada" *)
Close["entrada.txt"];
(* Abre o arquivo "saida" em modo Escrita *)
OpenWrite["saida.txt"];
(* Escreve o Sistema no arquvio "saida" *)

Write["saida.txt", system];
(* Verifica se calculará com probabilidade ou não, já realizando o \
mesmo *)
If[prob == 0, 
  derivateFunction = system[[1, qtdeEstados]] /. z -> (z/qtdeLetras), 
  derivateFunction = system[[1, qtdeEstados]]];
(* Calcula a média da sequência *)

media = D[derivateFunction, z] /. z -> 1;
(* Escreve a Média da Sequência no arquvio "saida" *)

Write["saida.txt", media];
(* Fecha o arquivo "saida" *)
Close["saida.txt"];

(* Fecha o Notebook (este arquivo) *)
(* NotebookClose[] *)
