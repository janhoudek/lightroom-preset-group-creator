import os
import re
import shutil

def create_directory(directory_name: str):
    """
    Creates a directory with the specified name if it does not already exist.

    Args:
        directory_name (str): The name of the directory to create. This can be a relative
                              or absolute path (e.g., 'example_directory' or 'path/to/example_directory').

    Note:
        - Prints messages indicating the success or failure of the operation.
        - Handles exceptions for permission errors or other unexpected issues.
    """

    if not os.path.exists(directory_name):
        try:
            os.makedirs(os.path.join(directory_name))
            print(f'Directory "{directory_name}" created successfully.')
        except PermissionError:
            print(f'Permission denied: Unable to create "{directory_name}".')
        except Exception as e:
            print(f'An error occurred while creating "{directory_name}": {e}')

def edit_xmp_cluster(file_name: str, new_value: str, output_path: str):
    """
    Edits the value of the 'crs:Cluster' attribute in an XMP file and saves the modified content to a specified output file.

    Args:
        file_name (str): The path to the input XMP file to be modified.
        new_value (str): The new value to replace the existing 'crs:Cluster' attribute.
        output_path (str): The path where the updated file will be saved.

    Note:
        - Assumes the input file is encoded in UTF-8.
        - Skips files that do not contain the 'crs:Cluster' attribute.
        - Handles exceptions for file I/O errors and other unexpected issues.
    """

    try:
        # open the input file and read its content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # look for the "crs:Cluster" attribute and replace its value
        if 'crs:Cluster="' in content:
            updated_content = re.sub(
                r'crs:Cluster=".*?"',  # regex to find the crs:Cluster attribute
                f'crs:Cluster="{new_value}"',  # replacement with the new value
                content
            )

            # save the updated content to the output file
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(updated_content)
            
            print(f'Updated "crs:Cluster" to "{new_value}" and saved to {output_path}')
        else:
            print(f'The "crs:Cluster" attribute was not found in "{file_path}".')
    except FileNotFoundError:
        print(f'File not found: {file_path}')
    except PermissionError:
        print(f'Permission denied: Unable to read/write file "{file_path}" or "{output_path}".')
    except Exception as e:
        print(f'An error occurred while processing "{file_path}": {e}')
    

if __name__ == '__main__':
    # input folder containing presets and the new cluster value.
    folder_path = str(input('Insert folder with presets to updating: ')).strip()
    new_value = str(input('Insert required preset group: ')).strip()

    # create a temporary directory for output.
    create_directory('./temp')

    # traverse the folder structure and process each .xmp file.
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            # construct paths for input and output files.
            file_path = os.path.join(root, name)
            output_file_path = os.path.join('./temp/', root, name)

            # create the directory structure in the temp directory.
            create_directory(os.path.dirname(output_file_path))

            # process only .xmp files.
            if name.endswith('.xmp'):
                edit_xmp_cluster(file_path, new_value, output_file_path)

    # create a zip archive of the output directory.
    output_folder_name = os.listdir('./temp')[0]
    output_folder_path = os.path.join('./temp/', output_folder_name)

    shutil.make_archive(output_folder_name, 'zip', output_folder_path)

    # remove temp folder
    try:
        shutil.rmtree('./temp')
    except FileNotFoundError:
        print(f'File not found: "./temp"')