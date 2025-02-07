import subprocess
import sys

def unoconvert(infile, outfile, convert_to=None, input_filter=None, output_filter=None, filter_options=None, host='127.0.0.1', port=2002):
    # Construct the base command
    command = ['unoconvert']

    # Add optional arguments
    if convert_to:
        command.extend(['--convert-to', convert_to])
    if input_filter:
        command.extend(['--input-filter', input_filter])
    if output_filter:
        command.extend(['--output-filter', output_filter])
    if filter_options:
        command.extend(['--filter-options', filter_options])
    
    # Set host and port
    # command.extend(['--host', host, '--port', str(port)])

    # Add input and output files
    command.append(infile)
    command.append(outfile)

    # Execute the command
    try:
        subprocess.run(command, check=True)
        print(f"Successfully converted '{infile}' to '{outfile}'")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Example usage
    infile = 'content/Docker-Freshers.pptx'  # Replace with your input file
    outfile = 'output_file.pdf'  # Replace with your desired output file

    # Call the unoconvert function
    unoconvert(infile, outfile, convert_to='pdf')  # Change 'pdf' to desired format if needed
