<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>

<?php

//$dir = scandir('../FOOD');
//var_dump($dir);
//
//foreach ( $dir as $item) {
//    var_dump(scandir($item));
//}

$iterator = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator('../FOOD',
        FilesystemIterator::SKIP_DOTS),
    RecursiveIteratorIterator::SELF_FIRST);

foreach($iterator as $file) {

    if($file->isDir()) {
        $indent = str_repeat('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', $iterator->getDepth());
        echo $indent . '<a href="' . $file . '">' . ucwords(strtolower($file->getFilename())) . '</a><br>';
    }
}

?>

</body>
</html>