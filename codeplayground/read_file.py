

def read_file(file_path):
    
    file = open(file_path)
    lines = file.readlines()
    
    print "".join(l for l in lines)
    
    
if __name__ == "__main__":
    print 'Code skeleton:'
    read_file("graders/codeplayground/multiply_a_number_by_two/code_skeleton.txt")
    print '\n'
    
    print 'Question:'
    read_file("graders/codeplayground/multiply_a_number_by_two/question.txt")
    print '\n'
    
    print 'Answer:'
    read_file("graders/codeplayground/multiply_a_number_by_two/answer.txt")
    print '\n'