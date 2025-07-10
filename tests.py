from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


def test():
    
    ## get file content tests
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))

    ## get files info tests
    # print(get_files_info("calculator", "."))
    # print(get_files_info("calculator", "pkg"))
    # print(get_files_info("calculator", "/bin"))
    # print(get_files_info("calculator", "../main.py"))

if __name__ == "__main__":
    test()
