<h1>Hi everyone!</h1>
<h1>It is just a warmup task</h1>
<h1>Enjoy it!</h1>

<?php
include 'flag.php';
$a = $_GET["cmp"];
if (strcmp($a, $string_to_compare) == 0) {
	echo $flag;
} else {
	echo "Incorrect";
}
?>
