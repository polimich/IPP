<?php
ini_set('display_errors', 'stderr');
$order = 1;
$xml = xmlwriter_open_memory();
$header = false;
xmlwriter_set_indent($xml, 1);
xmlwriter_set_indent_string($xml, ' ');
xmlwriter_start_document($xml, '1.0', 'UTF-8');

// checks variable 
function check_var($var) {
    if (preg_match('/^(GF|LF|TF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$/', $var) == 0) {
        echo "Wrong variable name";
        exit(23);
    }
}
function check_label($label) {
    if (preg_match('/^[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$/', $label) == 0) {
        echo "Wrong label name";
        exit(23);
    }
}
function check_exit_code($number) {
    // Check for int 0 to 49
    if (preg_match('/^int@([0-9]|[1-4][0-9])$/', $number) == 0) {
        echo "Wrong exit code";
        exit(23);
    }
    return "int";
}
function check_symb($symb) {
    if (preg_match('/^(GF|LF|TF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$/', $symb) == 0) {
        if (preg_match('/^(int|string|bool|nil)@([^\s#]|(\\\\[0-9]{3}))*$/', $symb) == 0) {
            echo "Wrong symbol";
            exit(23);
        }
        //return type 
        if (preg_match('/^int@[+-]?[0-9]+$/', $symb) == 1) {
            return "int";
        }
        if (preg_match('/^string@([^\s#]|(\\\\[0-9]{3}))*$/', $symb) == 1) {
            return "string";
        }
        if (preg_match('/^bool@(true|false)$/', $symb) == 1) {
            return "bool";
        }
        if (preg_match('/^nil@nil$/', $symb) == 1) {
            return "nil";
        } else {
            echo "Wrong symbol";
            exit(23);
        }

    }
    else {
        return "var";
    }
}
function check_type($type) {
    if (preg_match('/^(int|string|bool)$/', $type) == 0) {
        echo "Wrong type";
        exit(23);
    }
}
function symb_value($type, $symb) {
    if ($type == "int" || $type == "bool" || $type == "string" || $type == "nil") {
        $splitted = explode("@", $symb); 
        return $splitted[1];
    }
    return $symb;
}
// Check for 0 arguments
function check_0_args($fun_name, $fun_args ) {
    global $order;
    global $xml;
    if (count($fun_args) != 0) {
        echo "Wrong number of arguments";
        exit(23);
    }
    xmlwriter_start_element($xml, 'instruction');
    xmlwriter_start_attribute($xml, 'order');
    xmlwriter_text($xml, $order);
    xmlwriter_end_attribute($xml);
    xmlwriter_start_attribute($xml, 'opcode');
    xmlwriter_text($xml, $fun_name);
    xmlwriter_end_attribute($xml);
    xmlwriter_end_element($xml);
}
function check_1_args($fun_name, $fun_args, $type) {
    global $order;
    global $xml;

    if (count($fun_args) != 1) {
        echo "Wrong number of arguments";
        exit(23);
    }
    $value1 = symb_value($type, $fun_args[0]);
    xmlwriter_start_element($xml, 'instruction');
    xmlwriter_start_attribute($xml, 'order');
    xmlwriter_text($xml, $order);
    xmlwriter_end_attribute($xml);
    xmlwriter_start_attribute($xml, 'opcode');
    xmlwriter_text($xml, $fun_name);
    xmlwriter_end_attribute($xml);
    xmlwriter_start_element($xml, 'arg1');
    xmlwriter_start_attribute($xml, 'type');
    xmlwriter_text($xml, $type);
    xmlwriter_end_attribute($xml);
    xmlwriter_text($xml, $value1);
    xmlwriter_end_element($xml);
    xmlwriter_end_element($xml);
}
function check_2_args($fun_name, $fun_args, $type1, $type2) {
    global $order;
    global $xml;
    if (count($fun_args) != 2) {
        echo "Wrong number of arguments";
        exit(23);
    }
    $value1 = symb_value($type1, $fun_args[0]);
    $value2 = symb_value($type2, $fun_args[1]);

    xmlwriter_start_element($xml, 'instruction');
    xmlwriter_start_attribute($xml, 'order');
    xmlwriter_text($xml, $order);
    xmlwriter_end_attribute($xml);
    xmlwriter_start_attribute($xml, 'opcode');
    xmlwriter_text($xml, $fun_name);
    xmlwriter_end_attribute($xml);
    xmlwriter_start_element($xml, 'arg1');
    xmlwriter_start_attribute($xml, 'type');
    xmlwriter_text($xml, $type1);
    xmlwriter_end_attribute($xml);
    xmlwriter_text($xml, $value1);
    xmlwriter_end_element($xml);
    xmlwriter_start_element($xml, 'arg2');
    xmlwriter_start_attribute($xml, 'type');
    xmlwriter_text($xml, $type2);
    xmlwriter_end_attribute($xml);
    xmlwriter_text($xml, $value2);
    xmlwriter_end_element($xml);
    xmlwriter_end_element($xml);
}
function check_3_args($fun_name, $fun_args, $type1, $type2, $type3) {
    global $order;
    global $xml;
    if (count($fun_args) != 3) {
        echo "Wrong number of arguments";
        exit(23);
    }
    $value1 = symb_value($type1, $fun_args[0]);
    $value2 = symb_value($type2, $fun_args[1]);
    $value3 = symb_value($type3, $fun_args[2]);

    xmlwriter_start_element($xml, 'instruction');
    xmlwriter_start_attribute($xml, 'order');
    xmlwriter_text($xml, $order);
    xmlwriter_end_attribute($xml);
    xmlwriter_start_attribute($xml, 'opcode');
    xmlwriter_text($xml, $fun_name);
    xmlwriter_end_attribute($xml);
    xmlwriter_start_element($xml, 'arg1');
    xmlwriter_start_attribute($xml, 'type');
    xmlwriter_text($xml, $type1);
    xmlwriter_end_attribute($xml);
    xmlwriter_text($xml, $value1);
    xmlwriter_end_element($xml);
    xmlwriter_start_element($xml, 'arg2');
    xmlwriter_start_attribute($xml, 'type');
    xmlwriter_text($xml, $type2);
    xmlwriter_end_attribute($xml);
    xmlwriter_text($xml, $value2);
    xmlwriter_end_element($xml);
    xmlwriter_start_element($xml, 'arg3');
    xmlwriter_start_attribute($xml, 'type');
    xmlwriter_text($xml, $type3);
    xmlwriter_end_attribute($xml);
    xmlwriter_text($xml, $value3);
    xmlwriter_end_element($xml);
    xmlwriter_end_element($xml);
}

// Test for correct arguments
if ($argc > 1) {
    if ($argv[1] == "--help" && $argc == 2) {
        echo "Usage: php parse.php [option] < [file]\n";
        echo "Script type filter (parse.php in PHP 8.1)\n";
        echo "Retrieve source code from standard input in IPP-code23,\n";
        echo "checks the code for lexical and syntactical correctness\n";
        echo "and prints the XML representation of the program to the standard output.\n";
        exit(0);
    }
    else {
        echo "Wrong number of paramters used";
        exit(10);
    }
}
// Start XML
xmlwriter_start_element($xml, 'program');
xmlwriter_start_attribute($xml, 'language');
xmlwriter_text($xml, 'IPPcode23');
xmlwriter_end_attribute($xml);

// Read lines from stdin
while ($line = fgets(STDIN)) {
    //remove blank lines
    if (preg_match('/^\s*$/', $line)) {
        continue;
    }
    // remove comment lines 
    if (preg_match('/^\s*#/', $line)) {
        continue;
    }
    // Remove inline comments
    if (strpos($line, "#")) {
        $line = substr($line, 0, strpos($line, "#"));
    }
    if ($header == false) { 
        if (preg_match('/^(.IPPcode23)$/', trim($line))) {
            $header = true;
            continue;
        }
        else {
            echo "Wrong header";
            exit(21);
        }
    }
    

    $splitted = preg_split('/\s+/', trim($line));
    $fun_name = strtoupper($splitted[0]);
    $fun_args = array_slice($splitted, 1);

    switch ($fun_name):
        // 0 arguments
        case "CREATEFRAME":
        case "PUSHFRAME":
        case "POPFRAME":
        case "RETURN":
        case "BREAK":
            check_0_args($fun_name, $fun_args);
            break;
        // 1 argument
        case "DEFVAR":  // <var>
        case "POPS":    // <var>
            check_var($fun_args[0]);
            check_1_args($fun_name, $fun_args, "var");
            break;

        case "CALL":    // <label>
        case "LABEL":   // <label>
        case "JUMP":    // <label>
            check_label($fun_args[0]);
            check_1_args($fun_name, $fun_args, "label");
            break;

        case "PUSHS":   // <symb>
        case "WRITE":   // <symb>
        case "DPRINT":  // <symb>
            check_1_args($fun_name, $fun_args, check_symb($fun_args[0]));
            break;
        case "EXIT":    // <symb>
            check_1_args($fun_name, $fun_args, check_symb($fun_args[0]));
            break;
        // 2 arguments
        case "MOVE":        // <var> <symb>
        case "INT2CHAR":    // <var> <symb>
        case "STRLEN":      // <var> <symb>
        case "TYPE":        // <var> <symb>
        case "NOT":
            check_var($fun_args[0]);
            check_2_args($fun_name, $fun_args, "var", check_symb($fun_args[1]));
            break;
        case "READ":        // <var> <type>
            check_var($fun_args[0]);
            check_type($fun_args[1]);
            check_2_args($fun_name, $fun_args, "var", "type");
            break;
        // 3 arguments
        case "ADD":     // <var> <symb> <symb>    
        case "SUB":     // <var> <symb> <symb>
        case "MUL":     // <var> <symb> <symb>
        case "IDIV":    // <var> <symb> <symb>
        case "LT":      // <var> <symb> <symb>
        case "GT":      // <var> <symb> <symb>
        case "EQ":      // <var> <symb> <symb>
        case "AND":     // <var> <symb> <symb>
        case "OR":      // <var> <symb> <symb>
        case "STRI2INT":    // <var> <symb> <symb>
        case "CONCAT":      // <var> <symb> <symb>
        case "GETCHAR":     // <var> <symb> <symb>
        case "SETCHAR":     // <var> <symb> <symb>
            check_var($fun_args[0]);
            check_3_args($fun_name, $fun_args, "var", check_symb($fun_args[1]), check_symb($fun_args[2]));
            break;
        case "JUMPIFEQ":
        case "JUMPIFNEQ":
            check_label($fun_args[0]);
            check_3_args($fun_name, $fun_args, "label", check_symb($fun_args[1]), check_symb($fun_args[2]));
            break;
        default:
            echo "Wrong instruction";
            exit(22);
    endswitch;
    $order++;
}
xmlwriter_end_element($xml);
echo xmlwriter_output_memory($xml);
?>
