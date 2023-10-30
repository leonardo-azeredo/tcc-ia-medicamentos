<?php	
include "../../include/mysqlconecta.php";

$SQL = "select * from medicamento";

$result_id = @mysqli_query($conexao,$SQL) or die("Ocorreu um erro! 001");
$linhas_json = array();

while($rows = mysqli_fetch_array($result_id)){
    
    $linha_json = array(
        'id_medicamento'=>$rows['id_medicamento'],
        'nome_medicamento'=>$rows['nome_medicamento'],
    ); 
    $linhas_json[] = $linha_json; 
}
echo json_encode($linhas_json);
?>