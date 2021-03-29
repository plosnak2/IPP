#!/usr/bin/php
<?php
class Arguments {
    # trieda ktora sa stara o parametre a drzi nejake zakladne atributy
    public $directory;
    public $recursive;
    public $parse_script;
    public $int_script;
    public $parse_only;
    public $int_only;
    public $jexamxml;
    public $jexamcfg;
    public $int_script_bool;
    public $parse_script_bool;

    public function parse_arguments($argc, $argv){
        # metoda pre spracovanie parametrov
        if(in_array("--help", $argv)){
            if($argc != 2){
                fwrite(STDERR, "Help sa nemoze kombinovat s inymi parametrami.\n");
                exit(10);
            } else {
                fwrite(STDOUT, "Skript sluzi pre kontrolu suborov interpret.py a suboru parse.php\nSkript bezi s nasledujucimi parametrami:\n--help: vypise tuto napovedu\n--directory=path: testy bude hladat v zadamom adresari\n--recursive: testy bude hladat rekurzivne aj v podadresaroch\n--parse-script=file: subor s parser skriptom\n--int-script=file: subor s interpretom\n--parse-only: skript testuje iba parser\n--int-only: skript testuje iba interpret\n--jexamxml=file: subor s JAR balickom s nastrojom JExamll XML\n --jexamcfg=file: subor s konfiguraciou nastroja JExam XML\n");
            }
            exit(0);
        }

        $longopts = array(
            "directory:",
            "recursive",
            "parse-script:",
            "int-script:",
            "parse-only",
            "int-only",
            "jexamxml:",
            "jexamcfg:"
        );
        $options = getopt("", $longopts);
        
        $args = 0;
        if($argc < 1 or $argc > 9){
            fwrite(STDERR, "Zly počet argumentov.\n");
            exit(10);
        } else {
            if(array_key_exists('directory', $options)){
                $this->directory = $options['directory'];
                $args += 1;
            } else {
                $this->directory = getcwd().'/';
            }

            if(array_key_exists('recursive', $options)){
                $this->recursive = true;
                $args += 1;
            } else {
                $this->recursive = false;
            }

            if(array_key_exists('parse-script', $options)){
                $this->parse_script = $options['parse-script'];
                $this->parse_script_bool = true;
                $args += 1;
            } else {
                $this->parse_script = './parse.php';
                $this->parse_script_bool = false;
            }

            if(array_key_exists('int-script', $options)){
                $this->int_script = $options['int-script'];
                $this->int_script_bool = true;
                $args += 1;
            } else {
                $this->int_script = './interpret.py';
                $this->int_script_bool = false;
            }

            if(array_key_exists('parse-only', $options)){
                $this->parse_only = true;
                $args += 1;
            } else {
                $this->parse_only = false;
            }

            if(array_key_exists('int-only', $options)){
                $this->int_only = true;
                $args += 1;
            } else {
                $this->int_only = false;
            }

            if(array_key_exists('jexamxml', $options)){
                $this->jexamxml = $options['jexamxml'];
                $args += 1;
            } else {
                $this->jexamxml = '/pub/courses/ipp/jexamxml/jexamxml.jar';
            }

            if(array_key_exists('jexamcfg', $options)){
                $this->jexamcfg = $options['jexamcfg'];
                $args += 1;
            } else {
                $this->jexamcfg = '/pub/courses/ipp/jexamxml/options';
            }
        }

        if($args != $argc - 1){
            fwrite(STDERR, "Nespravne argumenty.\n");
            exit(10);
        }

        if($this->int_only == true and ($this->parse_only == true or $this->parse_script_bool == true)){
            fwrite(STDERR, "Zla kombinacia argumentov.\n");
            exit(10);
        }

        if($this->parse_only == true and ($this->int_only == true or $this->parse_int_bool == true)){
            fwrite(STDERR, "Zla kombinacia argumentov.\n");
            exit(10);
        }

        $this->check_paths();
    }

    private function check_paths(){
        # metoda ktora kontroluje existenciu suborov/priecinkov
        if(!file_exists($this->directory)){
            fwrite(STDERR, "$this->directory neexistuje\n");
            exit(41);
        }

        if(!file_exists($this->parse_script)){
            if($this->int_only == false){
                fwrite(STDERR, "$this->parse_script neexistuje\n");
                exit(41);
            }
        }

        if(!file_exists($this->int_script)){
            if($this->parse_only == false){
                fwrite(STDERR, "$this->int_script neexistuje\n");
                exit(41);
            }
        }

        if(!file_exists($this->jexamxml)){
            fwrite(STDERR, "$this->jexamxml neexistuje\n");
            exit(41);
        }

        if(!file_exists($this->jexamcfg)){
            fwrite(STDERR, "$this->jexamcfg neexistuje\n");
            exit(41);
        }
    }
}

class HTML_generator{
    public function generate_head(){
        echo "<!DOCTYPE html>\n";
        echo "<html>\n";
        echo "<head>\n";
        echo "<title>IPP 20121 tests</title>\n";
        echo "<style>\n";
        echo "body{\n";
        echo "width:80%;\n";
        echo "margin:auto;\n";
        echo "}\n";
        echo "header{\n";
        echo "text-align:center;\n";
        echo "font-size:50px;\n";
        echo "color:blue;\n";
        echo "}\n";
        echo "footer{\n";
        echo "text-align:center;\n";
        echo "}\n";
        echo "hr{\n";
        echo "border-color:red;\n";
        echo "}\n";
        echo "table{\n";
        echo "width:80%;\n";
        echo "margin:auto;\n";
        echo "}\n";
        echo "table td{\n";
        echo "text-align:center;\n";
        echo "height:50px;\n";
        echo "}\n";
        echo "</style>\n";
        echo "</head>\n";
        echo "<body>\n";
        echo "<header>\n";
        echo "IPP 2021 Projekt -> test.php\n";
        echo "</header>\n";
        echo "<hr></hr>\n";
        echo "<table>\n";
        echo "<tr>\n";
        echo "<th>Číslo testu</th>\n";
        echo "<th>Cesta k testu</th>\n";
        echo "<th>Meno testu</th>\n";
        echo "<th>Výsledok</th>\n";
        echo "</tr>\n";
    }

    public function generate_tail($type, $passed, $failed){
        echo "</table>";
        echo "<hr></hr>\n";
        echo "<footer>\n";
        if($type == "int"){
            echo "<h2>Typ testov: Interpret only</h2>\n";
        } elseif ($type == "parse"){
            echo "<h1>Typ testov: Parse only</h1>\n";
        } else {
            echo "<h1>Typ testov: Both</h1>\n";
        }
        if($passed + $failed == 0){
            $rate = 0;
            $passed = 0;
            $failed = 0;
        } else {
            $rate = ($passed / ($passed + $failed)) * 100;
        }
        echo "<h2 style='color:green'>Tests Passed: $passed</h2>\n";
        echo "<h2 style='color:red'>Tests Failed: $failed</h2>\n";
        echo "<h2 style='color:grey'>Success rate: $rate%</h2>\n";
        echo "</footer>\n";
        echo "</body>\n";
        echo "</html>\n";
    }

    public function generate_test($order, $path, $name, $result){
        echo "<tr>\n";
        echo "<td>$order</td>\n";
        echo "<td>$path</td>\n";
        echo "<td>$name</td>\n";
        if($result == "pass"){
            echo "<td style='color:green'>PASSED</td>\n";
        } else {
            echo "<td style='color:red'>FAILED</td>\n";
        }
        echo "</tr>\n";
    }
}

class Tests extends Arguments{
    public $file_name;
    public $test_count;
    public $success_count;
    public $failed_count;
    public $path;
    public $html;

    function __construct(){
        $this->html = new HTML_generator();
        $this->$test_count = 0;
        $this->success_count = 0;
        $this->failed_count = 0;
        
    }

    public function start_tests(){
        $stack = array(realpath($this->directory));
        $actual_dir = array_pop($stack);
        
        while($actual_dir != NULL){
            $openned = opendir($actual_dir);

            while($file = readdir($openned)){
                if($file == '.' or $file == '..'){
                    continue;
                }
                if(is_dir("$actual_dir" . "/" . "$file") and $this->recursive == true){
                    //echo "TOTO JE DIR" . "$actual_dir" . "/" . "$file" . "\n";
                    $path = "$actual_dir" . "/" . "$file";
                    array_push($stack, $path);
                }
                if(is_file("$actual_dir" . "/" . "$file")){
                    //echo "TOTO JE FILE" . "$actual_dir" . "/" . "$file" . "\n";
                    $path_file = "$actual_dir" . "/" . "$file";
                    $ext = pathinfo($path_file, PATHINFO_EXTENSION);
                    if($ext == 'src'){
                        $this->file_name = pathinfo($path_file, PATHINFO_FILENAME);
                        
                        if(!file_exists("$actual_dir" . "/" . "$this->file_name" . ".rc")){
                            touch("$actual_dir" . "/" . "$this->file_name" . ".rc");
                            exec("echo '0' >" . "$actual_dir" . "/" . "$this->file_name" . ".rc");
                        }

                        if(!file_exists("$actual_dir" . "/" . "$this->file_name" . ".out")){
                            touch("$actual_dir" . "/" . "$this->file_name" . ".out");
                        }

                        if(!file_exists("$actual_dir" . "/" . "$this->file_name" . ".in")){
                            touch("$actual_dir" . "/" . "$this->file_name" . ".in");
                        }
                        
                        $this->path = "$actual_dir" . "/" . "$this->file_name";
                        
                        $this->exec_test();
                    }
                }
               
            }

            $actual_dir = array_pop($stack);
        }
    }

    public function exec_test(){
        $this->test_count++;
        $rc_file = fopen("$this->path" . ".rc", 'r');
        $rc = fgets($rc_file);
        fclose($rc_file);

        if($this->int_only == true){
            exec("python3.8 " . "$this->int_script" . " --input=" . "$this->path" . ".in --source=" . "$this->path" . ".src > temp_output", $nothing, $exit_status);
            if($exit_status != $rc){
                $this->failed_count++;
                $this->html->generate_test($this->test_count, $this->path, $this->file_name, "fail");
            } else {
                if($exit_status != 0){
                    $this->success_count++;
                    $this->html->generate_test($this->test_count, $this->path, $this->file_name, "pass");
                } else {
                    exec("diff temp_output " . "$this->path" . ".out > temp_diff");
                    if('' == file_get_contents("temp_diff")){
                        $this->success_count++;
                        $this->html->generate_test($this->test_count, $this->path, $this->file_name, "pass");
                    } else {
                        $this->failed_count++;
                        $this->html->generate_test($this->test_count, $this->path, $this->file_name, "fail");
                    }
                    exec('rm -f temp_diff');
                }
            }
            exec('rm -f temp_output');
        } elseif($this->parse_only == true){
            exec("php7.4 " . "$this->parse_script" . " < " . "$this->path" . ".src > temp_output", $nothing, $exit_status);
            if($exit_status != $rc){
                $this->failed_count++;
                $this->html->generate_test($this->test_count, $this->path, $this->file_name, "fail");
            } else {
                if($exit_status != 0){
                    $this->success_count++;
                    $this->html->generate_test($this->test_count, $this->path, $this->file_name, "pass");
                } else {
                    exec("java -jar " . "$this->jexamxml" . " " . "temp_output " . "$this->path" . ".out temp_xml " . "$this->jexamcfg", $nothing, $exit_jexam);
                    if($exit_jexam == 0){
                        $this->success_count++;
                        $this->html->generate_test($this->test_count, $this->path, $this->file_name, "pass");
                    } else {
                        $this->failed_count++;
                        $this->html->generate_test($this->test_count, $this->path, $this->file_name, "fail");
                    }
                    exec('rm -f temp_xml');
                }
            }
            exec('rm -f temp_output');
        } else{
            exec("php7.4 " . "$this->parse_script" . " < " . "$this->path" . ".src > temp_output", $nothing, $exit_status);
            exec("python3.8 " . "$this->int_script" . " --input=" . "$this->path" . ".in --source=temp_output > final_output", $nothing, $exit_final);
            if($exit_final != $rc){
                $this->failed_count++;
                $this->html->generate_test($this->test_count, $this->path, $this->file_name, "fail");
            } else {
                if($exit_final != 0){
                    $this->success_count++;
                    $this->html->generate_test($this->test_count, $this->path, $this->file_name, "pass");
                } else {
                    exec("diff final_output " . "$this->path" . ".out > temp_diff");
                    if('' == file_get_contents("temp_diff")){
                        $this->success_count++;
                        $this->html->generate_test($this->test_count, $this->path, $this->file_name, "pass");
                    } else {
                        $this->failed_count++;
                        $this->html->generate_test($this->test_count, $this->path, $this->file_name, "fail");
                    }
                    exec('rm -f temp_diff');
                }
            }
            exec("rm -f temp_output");
            exec("rm -f final_output");
        }
    }
}

$arguments = new Tests();
$arguments->parse_arguments($argc, $argv);

$html = new HTML_generator();
$html->generate_head();

$arguments->start_tests();

if($arguments->int_only == true){
    $html->generate_tail("int", $arguments->success_count, $arguments->failed_count);
} elseif($arguments->parse_only == true){
    $html->generate_tail("parse", $arguments->success_count, $arguments->failed_count);
} else {
    $html->generate_tail("both", $arguments->success_count, $arguments->failed_count);
}