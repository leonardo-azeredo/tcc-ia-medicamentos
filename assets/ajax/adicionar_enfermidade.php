<?php
include "../../include/valida_session_usuario.php";
include "../../include/mysqlconecta.php";

$id_paciente = $_POST['id_paciente'];
$id_enfermidade = $_POST['enfermidade'];

if(isset($id_paciente) && isset($id_enfermidade)){

    $SQL = "INSERT INTO paciente_enfermidade (id_paciente, id_enfermidade) VALUES ($id_paciente, $id_enfermidade)";
    
    $result = @mysqli_query($conexao, $SQL) or die("Erro, código:001");

    if ($result) {
        $linhas_json = array(
            'success' => true,
            'msg' => 'Cadastro bem-sucedido.'
        );
        echo json_encode($linhas_json);
        exit;
    } else {
        $linhas_json = array(
            'success' => false,
            'msg' => 'Cadastro mal-sucedido.'
        );
        echo json_encode($linhas_json);
        exit;
    }

}
?>