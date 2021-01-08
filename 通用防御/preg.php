<?php
/*
    初步推测上次waf失效原因为 变量作用域被隔离导致未引用到关键字正则
*/

    error_reporting(0);
    $isattack = false;
    /*
    $get = $_GET;
    $post = $_POST;
    $cookie = $_COOKIE;
    */
    $request = $_REQUEST;
    $file = $_FILES;
    $header = getallheaders();

    function eachArray($arr) {
        foreach($arr as $k => $v) {
            if (is_array($v)) {
                eachArray($v);
            }
            else {
                // 循环URL解码
                eachURLdecode($k);
                eachURLdecode($v);
            }
        }
    }

    function eachURLdecode($code) {
        if (stripos($code, "%25") !== false) {
            $code = str_replace("%25", "%", $code);
            eachURLdecode($code);
        } else {
            attackDetect($code);
        }
    }

    function attackDetect($code) {
        $attackpreg = 'eval|assert';
        $attackpreg .= '|file_put_contents|fwrite|curl|\.\.|stream_socket_server|scandir';
        $attackpreg .= '|passthru|exec|system|putenv|chroot|chgrp|chown|shell_exec|popen|proc_open|pcntl_exec|ini_alter|ini_restore|dl|openlog|syslog|readlink|symlink|popepassthru|pcntl_alarm|pcntl_fork|pcntl_waitpid|pcntl_wait|pcntl_wifexited|pcntl_wifstopped|pcntl_wifsignaled|pcntl_wifcontinued|pcntl_wexitstatus|pcntl_wtermsig|pcntl_wstopsig|pcntl_signal|pcntl_signal_dispatch|pcntl_get_last_error|pcntl_strerror|pcntl_sigprocmask|pcntl_sigwaitinfo|pcntl_sigtimedwait|pcntl_exec|pcntl_getpriority|pcntl_setpriority|imap_open|apache_setenv';
        $attackpreg .= '|select|insert|update|drop|delete|dumpfile|outfile|load_file|floor|extractvalue|updatexml|geometrycollection|multipoint|polygon|multipolygon|linestring|multilinestring|exp';
        $attackpreg .= '|base64_decode|str_rot13|hexdec|chr|serialize';
        if (preg_match("/$attackpreg/i", $code)) {
            $isattack = true;
        }
    }

    