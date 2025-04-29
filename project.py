import os, glob
import mimetypes

# Given a list of files, compile them into a single text file
def compile_files(files, output_file):
    with open(output_file, 'w') as outfile:
        for file in files:
            with open(file, 'r') as infile:
                # Read the content and write it to the output file
                outfile.write(f'{file}\n{infile.read()}')
                outfile.write("\n")  # Add a newline between files

def is_text_file(filename):
    # Check if the file is a text file based on its MIME type
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type and mime_type.startswith('text/')

# Given a directory, compile all files into a single text file
def project_to_txt(directory, output_file):
    # Get all files in the directory
    files = glob.glob(os.path.join(directory, '*'))
    valid_files = []
    # Iterate through each file
    for filename in files:
        # Check type
        valid = is_text_file(filename)
        if valid:
            valid_files.append(filename)
            print(f"Processing text file: {filename}")
        else:
            print(f"Skipping non-text file: {filename}")
            continue
    # Compile the valid files into a single text file
    compile_files(valid_files, output_file)        

def main():
    # Testing on project_dir
    project_dir = 'project_dir'
    output_file = 'tmp.txt'
    project_to_txt(project_dir, output_file)
    print(f"Compiled files into {output_file}, output: \n")
    with open(output_file, 'r') as f:
        print(f.read())


if __name__ == '__main__':
    main()