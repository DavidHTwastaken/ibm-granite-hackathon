import os, glob, fnmatch
import mimetypes

class ProjectCompiler:
    def __init__(self, directory):
        self.root_dir = directory
        self.gitignore = self.read_gitignore()

    def read_gitignore(self, gitignore_file='.gitignore'):
        gitignore_file = os.path.join(self.root_dir, gitignore_file)
        # Check if the .gitignore file exists
        if not os.path.isfile(gitignore_file):
            print(f"Warning: {gitignore_file} not found. No files will be ignored.")
            return []
        # Read the .gitignore file and return a list of patterns to ignore
        with open(gitignore_file, 'r') as f:
            patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return patterns

    # Given a list of files, compile them into a single text file
    def compile_files(self, files, output_file):
        with open(output_file, 'w') as outfile:
            for file in files:
                with open(file, 'r') as infile:
                    # Read the content and write it to the output file
                    outfile.write(f'{file}\n{infile.read()}')
                    outfile.write("\n")  # Add a newline between files

    def is_not_gitignored(self, filename):
        # Check if the file matches any patterns in the .gitignore file
        for pattern in self.gitignore:
            if fnmatch.fnmatch(filename, pattern):
                return False
        return True

    def is_text_file(self, filename):
        # Check if the file is a text file based on its MIME type
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type and mime_type.startswith('text/')

    def is_valid_file(self, filename):
        # Use all checks
        checks = [os.path.isfile, self.is_text_file, self.is_not_gitignored]
        return all(check(filename) for check in checks)

    # Compile all files into a single text file
    def project_to_txt(self, output_file):
        # Get all files in directory and subdirectories
        # Use glob to find all files in the directory
        directory = self.root_dir
        files = glob.glob(os.path.join(directory, '**'), recursive=True) # TODO: requires optimization

        valid_files = []
        # Iterate through each file
        for filename in files:
            # Check type
            valid = self.is_valid_file(filename)
            if valid:
                valid_files.append(filename)
                print(f"Processing text file: {filename}")
            else:
                print(f"Skipping non-text file: {filename}")
                continue
        # Compile the valid files into a single text file
        self.compile_files(valid_files, output_file)        

def main():
    # Testing on project_dir
    project_dir = 'project_dir'
    output_file = 'tmp.txt'
    pc = ProjectCompiler(project_dir)
    pc.project_to_txt(output_file)
    print(f"Compiled files into {output_file}, output: \n")
    with open(output_file, 'r') as f:
        print(f.read())


if __name__ == '__main__':
    main()