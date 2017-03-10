import os
import subprocess
import time
from __builtin__ import str


def write_submitted_code_to_file(base_path, submitted_code):

    java_file_name = str(long(time.time() * 1000)) + ".java"
    
    source_file = open(base_path + '/' + java_file_name, 'w')
    source_file.write(submitted_code)
    source_file.close()
    
    return base_path + '/' + java_file_name
     
    
def clean_up(java_file_path):
    if os.path.exists(java_file_path):
        os.remove(java_file_path)    


def build_string_message(stdout_or_stderr):
    message = ""
    for line in stdout_or_stderr.split(os.linesep):
        message += (line + "<br>")
    
    br_size = len("<br>")
    message_list = list(message)
    message_size = len(message_list)
    message_list[ (message_size - 1 - br_size):(message_size - 1) ] = ""; # remove the last "<br>"
    
    return "".join(message_list)


def grade(grader_id, submitted_code):
    """
    """
    
    # Step 0: write the submitted code to a temporary file in the user's home folder
    base_path = os.path.expanduser("~")
    java_file_path = write_submitted_code_to_file(base_path, submitted_code)
    

    # Step 1: ask GradersPreparer to do the preparation
    python_file_folder = os.path.dirname(os.path.realpath(__file__))
    # print 'python_file_folder = ' + python_file_folder
    preparer_classpath = python_file_folder + "/languages/java/:" + python_file_folder + "/languages/java/lib/cucumber-core-1.2.5.jar:" + python_file_folder + "/languages/java/lib/cucumber-html-0.2.3.jar:" + python_file_folder + "/languages/java/lib/cucumber-java-1.2.4.jar:" + python_file_folder + "/languages/java/lib/cucumber-junit-1.2.5.jar:" + python_file_folder + "/languages/java/lib/cucumber-jvm-deps-1.0.5.jar:" + python_file_folder + "/languages/java/lib/gherkin-2.12.2.jar:" + python_file_folder + "/languages/java/lib/hamcrest-core-1.4-atlassian-1.jar:" + python_file_folder + "/languages/java/lib/jchronic-0.2.6.jar:" + python_file_folder + "/languages/java/lib/jcommander-1.64.jar:" + python_file_folder + "/languages/java/lib/junit-4.12.jar"
    p = subprocess.Popen(["java", "-cp", preparer_classpath, "codeplayground.GradersPreparer", "-graderId", grader_id, "-submittedFilePath", java_file_path, "-cleanUp", "true"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    
    # Step 1.1: process errors
    if (len(err) > 0):
        clean_up(java_file_path)
        return {
            "error": build_string_message(err)
        }
    
    
    # Step 1.2: process GradersPreparer's returned value
    output_lines = [ '', '', '' ]
    lineNo = 0
    for line in out.split(os.linesep):
        if (len(line) > 0):
            print 'line[' + str(lineNo) + '] = ' + line
            output_lines[lineNo] = line
            lineNo += 1
            
    temporary_folder_path = output_lines[0]
    package_name = output_lines[1]
    package_folder_path = output_lines[2]
    
    
    # Step 2: ask the GraderRunner to perform the grading
    print 'temporary_folder_path = ' + temporary_folder_path
    runner_classpath = temporary_folder_path + "/:" + temporary_folder_path + "/lib/cucumber-core-1.2.5.jar:" + temporary_folder_path + "/lib/cucumber-html-0.2.3.jar:" + temporary_folder_path + "/lib/cucumber-java-1.2.4.jar:" + temporary_folder_path + "/lib/cucumber-junit-1.2.5.jar:" + temporary_folder_path + "/lib/cucumber-jvm-deps-1.0.5.jar:" + temporary_folder_path + "/lib/gherkin-2.12.2.jar:" + temporary_folder_path + "/lib/hamcrest-core-1.4-atlassian-1.jar:" + temporary_folder_path + "/lib/jchronic-0.2.6.jar:" + temporary_folder_path + "/lib/jcommander-1.64.jar:" + temporary_folder_path + "/lib/junit-4.12.jar"
    p = subprocess.Popen(["java", "-cp", runner_classpath, "codeplayground.GradersRunner", "-features", package_folder_path, "-steps", package_name, "-temp", temporary_folder_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    
    # Steps 3: process returned result
    if (len(err) > 0):
        clean_up(java_file_path)
        return {
            "error": build_string_message(err)
        }

    # Step 4: clean up
    clean_up(java_file_path)
    
    return {
        "ok": "ok"
    }


def test_grader_not_found():
    grading_result = grade("null_grader", code)
    if grading_result.has_key("ok"):
        print 'grading_result[ok]: ' + grading_result["ok"]
        
    if grading_result.has_key("error"):
        print 'grading_result[error]: ' + grading_result["error"]


if __name__ == "__main__":
    code_list = [
        "package codeplayground.multiply_a_number_by_two\n\npublic class MultiplyANumberByTwo { \n\n\tpublic static int Puzzle(final int x) { \n\t\treturn x*2; \n\t} \n}",
        "package codeplayground.multiply_a_number_by_two;\n\npublic class MultiplyANumberByTwo { \n\n\tpublic static int Puzzle(final int x) { \n\t\treturn x*2 + 1; \n\t} \n}",
        "package codeplayground.multiply_a_number_by_two;\n\npublic class MultiplyANumberByTwo { \n\n\tpublic static int Puzzle(final int x) { \n\t\treturn x*2; \n\t} \n}"
    ]
    
    for code in code_list:
        grading_result = grade("MultiplyANumberByTwoGrader", code)
        if grading_result.has_key("ok"):
            print 'grading_result[ok]: ' + grading_result["ok"]
            
        if grading_result.has_key("error"):
            print 'grading_result[error]: ' + grading_result["error"]
            
    test_grader_not_found()