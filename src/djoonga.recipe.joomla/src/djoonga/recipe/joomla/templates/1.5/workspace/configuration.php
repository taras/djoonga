<?php
switch($_SERVER['SERVER_NAME']) {
        case('%(workspace)'): include('configuration.workspace.php'); break;
        default:
                include('configuration.live.php');
}
?>