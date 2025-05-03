import os, glob, fnmatch
import mimetypes
from pathspec.patterns import GitWildMatchPattern
from pathspec import PathSpec

class ProjectCompiler:
    def __init__(self, directory):
        self.root_dir = directory
        self.gitignores_spec = self.compile_gitignores()

    def compile_gitignores(self):
        # Recursively find all .gitignore files in the directory and subdirectories
        gitignore_files = glob.glob(os.path.join(self.root_dir, '**', '.gitignore'), recursive=True)
        # Read each .gitignore file and compile the patterns
        all_patterns = []
        for gitignore_file in gitignore_files:
            with open(gitignore_file, 'r') as f:
                lines = f.readlines()
            spec = PathSpec.from_lines(GitWildMatchPattern, lines)
            all_patterns.extend(spec.patterns)
        return PathSpec(all_patterns)

    # Given a list of files, compile them into a single text file
    def compile_files(self, files, output_file):
        with open(output_file, 'w') as outfile:
            for file in files:
                try:
                    with open(file, 'r') as infile:
                        # Read the content and write it to the output file
                        outfile.write(f'{file}\n{infile.read()}')
                        outfile.write("\n")  # Add a newline between files
                except UnicodeDecodeError:
                    continue # Skip files that can't be decoded as text

    def is_not_gitignored(self, filename):
        # Check if the file matches any patterns in any .gitignore file
        return not self.gitignores_spec.match_file(filename)

    def is_text_file(self, filename):
        # Check if the file is a text file based on its MIME type
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type and mime_type.startswith('text/')

    def is_valid_file(self, filename):
        # Use all checks
        checks = [self.is_not_gitignored]
        return all(check(filename) for check in checks)

    # Compile all files into a single text file
    def project_to_txt(self, output_file, verbose=False):
        # Get all files in directory and subdirectories
        # Use glob to find all files in the directory
        directory = self.root_dir
        # files = glob.glob(os.path.join(directory, '**'), recursive=True) # TODO: requires optimization

        valid_files = []
        for dirpath, dirnames, filenames in os.walk(directory):
            rel_dir = os.path.relpath(dirpath, directory)
            if rel_dir == '.':
                rel_dir = ''  # so that os.path.join works cleanly
                pruned = []
            for d in dirnames:
                # Build the relative path spec expects (directory paths end with slash)
                candidate = os.path.join(rel_dir, d) + '/'
                if self.gitignores_spec.match_file(candidate) or candidate.__contains__('.git'):
                    # this subdirectory is ignored → skip descending into it
                    continue
                pruned.append(d)
            dirnames[:] = pruned
        
            for filename in filenames:
                candidate = os.path.join(dirpath, filename)
                valid = self.is_valid_file(candidate)
                if valid:
                    valid_files.append(candidate)
                    print(f"Processing text file: {candidate}") if verbose else None
                else:
                    print(f"Skipping non-text file: {candidate}") if verbose else None
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