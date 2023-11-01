<?php
include "../../include/mysqlconecta.php";

$SQL = "SELECT p.*, GROUP_CONCAT(DISTINCT ' ', e.nome_enfermidade) AS enfermidade, GROUP_CONCAT(DISTINCT ' ', m.nome_medicamento) AS medicamento
FROM Paciente p
LEFT JOIN paciente_enfermidade pe ON p.id_paciente = pe.id_paciente
LEFT JOIN enfermidade e ON pe.id_enfermidade = e.id_enfermidade
LEFT JOIN paciente_medicamento pm ON p.id_paciente = pm.id_paciente
LEFT JOIN medicamento m ON pm.id_medicamento = m.id_medicamento
GROUP BY p.id_paciente";

$result_id = @mysqli_query($conexao, $SQL) or die("Ocorreu um erro! 001");
$linhas_json = array();

while ($rows = mysqli_fetch_array($result_id)) {
    
    $id_paciente = $rows['id_paciente'];
    $anmpac_nome = $rows['nome'];
    $anmpac_cpf = $rows['cpf'];
    $anmpac_sexo = $rows['sexo'] == 'M' ? 'Masculino' : 'Feminino';
    $anmpac_idade = $rows['idade'];
    $anmpac_enfermidade = $rows['enfermidade'];
    $anmpac_medicamento = $rows['medicamento'];
    $buttonsadd = "<button type='button' class='btn btn-sm me-2 bg-warning text-light' onclick='addEnfermidade($id_paciente)'>Adicionar Enfermidade</button><button type='button' class='btn btn-sm md-2 bg-info text-light' onclick='addMedicamento($id_paciente)'>Adicionar Medicamentos</button>";
    $buttonMostrarInfo = "<button type='button' class='btn btn-sm btn-primary' onclick='mostrarInfo($id_paciente, \"$anmpac_enfermidade\", \"$anmpac_medicamento\")'>Analise da IA</button>";





    $linha_json = array(
        'id_paciente' => $id_paciente,
        'anmpac_nome' => $anmpac_nome,
        'anmpac_cpf' => $anmpac_cpf,
        'anmpac_sexo' => $anmpac_sexo,
        'anmpac_idade' => $anmpac_idade,
        'anmpac_enfermidade' => $anmpac_enfermidade,
        'anmpac_medicamento' => $anmpac_medicamento,
        'buttonsadd' => $buttonsadd,
        'buttonMostrarInfo' => $buttonMostrarInfo,
        
    );
    $linhas_json[] = $linha_json;
}
echo json_encode($linhas_json);
?>