import os, glob
import mimetypes

# Given a directory, compile all files into a single text file
def compile_files(directory, output_file):
    # Get all files in the directory
    files = glob.glob(os.path.join(directory, '*'))
    
    # Open the output file for writing
    with open(output_file, 'w') as outfile:
        # Iterate through each file
        for filename in files:
            # Check type
            mime_type, _ = mimetypes.guess_type(filename)
            if mime_type and mime_type.startswith('text/'):
                print(f"Processing text file: {filename}")
            else:
                print(f"Skipping non-text file: {filename}")
                continue
            # Open the current file for reading
            with open(filename, 'r') as infile:

                # Read the content and write it to the output file
                outfile.write(f'{filename}\n{infile.read()}')
                outfile.write("\n")  # Add a newline between files

def main():
    # Testing on project_dir
    project_dir = 'project_dir'
    output_file = 'tmp.txt'
    compile_files(project_dir, output_file)
    print(f"Compiled files into {output_file}, output: \n")
    with open(output_file, 'r') as f:
        print(f.read())


if __name__ == '__main__':
    main()