<?php
session_start();
include "../../include/mysqlconecta.php";

$nome = $_POST['nome'];
$sexo = $_POST['sexo'];
$cpf = $_POST['cpf'];
$idade = $_POST['idade'];

// Verifica se o CPF já existe
$checkSQL = "SELECT * FROM paciente WHERE cpf='$cpf';";
$checkResult = @mysqli_query($conexao, $checkSQL);
if(mysqli_num_rows($checkResult) > 0){
    $linhas_json = array(
        'success'=>false,
        'msg'=>'Erro: CPF já cadastrado.'
    );
    echo json_encode($linhas_json);
    exit;
}

$SQL = "INSERT INTO paciente
(nome, cpf, sexo, idade)
VALUES( '$nome', '$cpf', '$sexo', $idade);";
$result = @mysqli_query($conexao,$SQL) or die("Erro, código:001");

if($result){
    $linhas_json = array(
        'success'=>true,
        'msg'=>'Cadastro bem-sucedido.'
    );
    echo json_encode($linhas_json);
    exit;
} else {
    $linhas_json = array(
        'success'=>false,
        'msg'=>'Cadastro mal-sucedido.'
    ); 
    echo json_encode($linhas_json);
    exit; 
}

?>
