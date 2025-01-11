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

    if os.path.exists(directory_name):
        shutil.rmtree(directory_name)

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
        with open(file_name, 'r', encoding='utf-8') as file:
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
            print(f'The "crs:Cluster" attribute was not found in "{file_name}".')
    except FileNotFoundError:
        print(f'File not found: {file_name}')
    except PermissionError:
        print(f'Permission denied: Unable to read/write file "{file_name}" or "{output_path}".')
    except Exception as e:
        print(f'An error occurred while processing "{file_name}": {e}')

def remove_folder(folder_path: str):
    """_summary_

    Args:
        folder_path (str): _description_
    """

    # remove temp folder
    try:
        shutil.rmtree(folder_path)
        print(f'Directory "{folder_path}" removed successfully.')
    except FileNotFoundError:
        print(f'File not found: {folder_path}')

def remove_file(file_path: str):
    """_summary_

    Args:
        file_path (str): _description_
    """

    # remove temp folder
    try:
        os.remove(file_path)
        print(f'File "{file_path}" removed successfully.')
    except FileNotFoundError:
        print(f'File not found: {file_path}')

def process_folder(file_name: str, new_value: str):
    """
    Processes all XMP files in a folder, updating the 'crs:Cluster' attribute with a new value.

    Args:
        folder_path (str): The path to the folder containing the XMP files to be processed.
        new_value (str): The new value to replace the existing 'crs:Cluster' attribute.

    Note:
        - Calls the 'edit_xmp_cluster' function for each XMP file in the folder.
        - Creates a temporary directory for the output files.
        - Handles exceptions for directory traversal errors and other unexpected issues.
    """

    # create a temporary directory for output
    create_directory('./source')
    create_directory('./temp')

    # target directory 
    extract_dir = './source'
  
    # Format of archive file 
    archive_format = 'zip'
  
    # Unpack the archive file  
    shutil.unpack_archive(file_name, extract_dir, archive_format)  
    print("Archive file unpacked successfully.")

    # traverse the folder structure and process each .xmp file
    for root, dirs, files in os.walk(extract_dir):

        # create the directory structure in the temp directory
        directory_name = os.path.join('./temp/', root)
        create_directory(directory_name)

        for name in files:
            # construct paths for input and output files
            file_path = os.path.join(root, name)
            output_file_path = os.path.join('./temp/', root, name)

            # process only .xmp files
            if name.endswith('.xmp'):
                edit_xmp_cluster(file_path, new_value, output_file_path)

    # create a zip archive of the output directory
    output_folder_name = 'edited_presets'
    output_folder_path = './temp'

    shutil.make_archive(output_folder_name, 'zip', output_folder_path)

    # remove folders
    remove_folder('./source')
    remove_folder('./temp')

    return f'{output_folder_name}.zip'

# for debugging purposes
#if __name__ == '__main__':
#    
#    folder_path = str(input('Insert folder with presets to updating: ')).strip()
#    new_value = str(input('Insert required preset group: ')).strip()
#
#    process_folder(folder_path, new_value)