<?php	
include "../../include/mysqlconecta.php";

$SQL = "select * from enfermidade";

$result_id = @mysqli_query($conexao,$SQL) or die("Ocorreu um erro! 001");
$linhas_json = array();

while($rows = mysqli_fetch_array($result_id)){
    
    $linha_json = array(
        'id_enfermidade'=>$rows['id_enfermidade'],
        'nome_enfermidade'=>$rows['nome_enfermidade'],
    ); 
    $linhas_json[] = $linha_json; 
}
echo json_encode($linhas_json);
?>