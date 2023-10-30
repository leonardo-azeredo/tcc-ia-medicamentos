<?php	
include "../../include/mysqlconecta.php";

if(isset($_POST['id'])){
    $id = $_POST['id'];
    $SQL = "DELETE FROM medicamento WHERE id_medicamento = $id";

    if(mysqli_query($conexao, $SQL)){
        $response = array('success' => true);
    } else {
        $response = array('success' => false);
    }

    echo json_encode($response);
} else {
    $response = array('success' => false);
    echo json_encode($response);
}
?>