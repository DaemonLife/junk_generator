import os
import shutil
import time

def get_unique_filename(directory, base_filename):
    """
    Generates a unique file name by adding a numeric suffix
    if a file with the base name already exists.
    """
    name, ext = os.path.splitext(base_filename)
    counter = 0
    new_filename = base_filename
    while os.path.exists(os.path.join(directory, new_filename)):
        counter += 1
        new_filename = f"{name}_{counter}{ext}"
    return new_filename

def generate_junk_file(base_filename="junk_file.bin", block_size=1*1024*1024): # 1 Mb
    """
    Generates a garbage file in the same directory as the script until disk space is full.
    If a file with the base name exists, creates a new one with a numeric suffix.

    Arguments:
      base_filename (str): The base name of the garbage file.
      block_size (int): The size of each block to write (in bytes).
                        Defaults to 1 MB.
    """
    script_dir = os.path.dirname(__file__)
    
    # Getting a unique file name
    filename = get_unique_filename(script_dir, base_filename)
    filepath = os.path.join(script_dir, filename)

    print(f"Trying to fill the disk: {script_dir}")
    print(f"The trash file will be created at: {filepath}")

    try:
        with open(filepath, 'wb') as f:
            # Pre-generate a large block of random data for reuse
            data_block = os.urandom(block_size)
            bytes_written = 0 # Add a counter of written bytes

            # Determine how often to output information (for example, every 64 MB)
            print_interval_bytes = block_size * 64 

            while True:
                try:
                    # Getting information about disk space
                    total, used, free = shutil.disk_usage(script_dir)
                  
                    # Output progress information only if we have written enough data
                    # or this is the very first output
                    if (bytes_written % print_interval_bytes == 0) or (bytes_written == 0):
                        written_gb = bytes_written / (1024**3)
                        free_gb = free / (1024**3)
                        print(f"Writed: {written_gb:.2f} Gb | Available space: {free_gb:.2f} Gb")

                    # Check if there is space left for the next block
                    if free < block_size:
                        print("Недостаточно места для следующего блока. Диск почти заполнен.")
                        break

                    f.write(data_block) # Write the pre-generated block
                    f.flush() # Force writing to disk so that the data actually takes up space
                    bytes_written += block_size # Increase the counter of written bytes

                except OSError as e:
                    print(f"Error writing file or checking disk space: {e}")
                    print("The disk is probably full or an I/O error has occurred. Stopping.")
                    break
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    break
    except IOError as e:
        print(f"Failed to open file for writing: {e}")
        print("Please check if you have write permission in the script directory.")
    except Exception as e:
        print(f"An error occurred before recording: {e}")
    finally:
        # Make sure we output the final file size
        if os.path.exists(filepath):
            final_size = os.path.getsize(filepath)
            print(f"Garbage file generation stopped. Total file size: {final_size / (1024**3):.2f} Gb")
        else:
            print("The junk file was not created or was deleted.")
        print(f"You can delete the generated file '{filename}' to free up space.")

if __name__ == "__main__":
    confirmation = input(f"This script will fill the disk where it is located. Are you sure you want to continue? (y/n): ")
    if confirmation.lower() == 'y':
        generate_junk_file()
    else:
        print("Canceled.")
